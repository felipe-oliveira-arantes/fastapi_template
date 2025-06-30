import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter
import os
from pydantic import BaseModel
from uuid import UUID
from typing import Type
import json
import logging
from google.cloud import secretmanager
from mockfirestore import MockFirestore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FirestoreAdapter:
    def __init__(
        self,
        credentials_path: str = None,
    ):
        self.credentials_path = credentials_path
    
    def connect_to_in_memory_db(self):
        # This method was made to create unit tests for functions that use Firestore
        # withou needing JWT connection
        self.db = MockFirestore()
        
    def connect_to_firestore(self, credentials_path: str = None):
        if credentials_path is None:
            credentials_path = self.credentials_path
        credentials_path = './credentials.json' 
        
        try:
            # Try local credentials file first
            if os.path.exists(credentials_path):
                logger.info(f"Found local credentials file at {credentials_path}. Initializing...")
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
                logger.info("Successfully initialized Firebase using local credentials file.")
            else:
                # If no local file, try Secret Manager
                logger.info("Local credentials file not found. Attempting to use Secret Manager...")
                creds_dict = self._get_credentials_from_secret_manager()
                if creds_dict:
                    logger.info("Successfully loaded Firebase credentials from Secret Manager")
                    cred = credentials.Certificate(creds_dict)
                    firebase_admin.initialize_app(cred)
                else:
                    # If Secret Manager also fails or isn't configured
                    logger.error("Failed to load credentials from Secret Manager.")
                    raise ValueError("No Firebase credentials found locally or in Secret Manager")
            
            self.db = firestore.client()
            logger.info("Successfully initialized Firestore client")
            
        except ValueError as ve:
            logger.error(f"Credential configuration error: {str(ve)}")
            raise
        except Exception as e:
            logger.error(f"Error initializing FirestoreAdapter: {str(e)}")
            raise

    def _get_credentials_from_secret_manager(self):
        try:
            project_id = os.getenv('GOOGLE_CLOUD_PROJECT')
            if not project_id:
                logger.warning("GOOGLE_CLOUD_PROJECT environment variable not set for Secret Manager access.")
                # Don't raise error here, allow fallback if possible, or let the main logic handle it
                return None

            client = secretmanager.SecretManagerServiceClient()
            secret_name = f"projects/{project_id}/secrets/firebase-credentials/versions/latest"
            
            try:
                logger.info(f"Accessing secret: {secret_name}")
                response = client.access_secret_version(request={"name": secret_name})
                creds = json.loads(response.payload.data.decode("UTF-8"))
                logger.info("Successfully retrieved credentials from Secret Manager")
                return creds
            except Exception as e:
                logger.error(f"Error accessing Secret Manager ({secret_name}): {str(e)}")
                return None
                
        except ImportError:
            logger.error("google-cloud-secret-manager package not installed. Cannot use Secret Manager.")
            return None
        except Exception as e:
            logger.error(f"Error initializing Secret Manager client: {str(e)}")
            return None

    def uuidToString(self, payload_dict: dict, model_class: Type[BaseModel]) -> dict:
        # Convert UUID fields to string
        for field in model_class.model_fields.items():
            field_name = field[0]
            field_type = field[1].annotation
            if field_type == UUID:
                payload_dict[field_name] = str(payload_dict[field_name])
        return payload_dict

    async def insertOne(
            self, 
            database:str,
            collection: str, 
            payload: dict,
            convert_uuid: bool = False,
            database_model = None
        ) -> dict:
        
        if convert_uuid == True:
            payload = self.uuidToString(payload_dict=payload, model_class=database_model)
        collection_ref = self.db.collection(collection)
        result = collection_ref.add(payload)
        
        return {"payload": payload, "result": result}

    async def findOneStr(
            self, 
            database: str,
            collection: str, 
            key: str, 
            search_str: str
        ):
        collection_ref = self.db.collection(collection)
        query = collection_ref.where(key, '==', search_str).get()
        results = [{"id": doc.id, **doc.to_dict()} for doc in query]
        
        if len(results) == 1:
            message = {
                "message": results[0],
                "status": "success"
            }
            
        elif len(results) > 1:
            message = {
                "message": f"The query returned {len(results)} instead of just one",
                "status": "multiple results"
            }
            
        elif len(results) == 0:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
            
        return message
    
    async def findOneMultiStr(
        self, 
        database: str,
        collection: str, 
        filters: dict  
    ):
        collection_ref = self.db.collection(collection)
        
        query = collection_ref
        for key, value in filters.items():
            query = query.where(key, "==", value)
        
        results = [{"id": doc.id, **doc.to_dict()} for doc in query.get()]
        
        if len(results) == 1:
            message = {
                "message": results[0],
                "status": "success"
            }
            
        elif len(results) > 1:
            message = {
                "message": f"The query returned {len(results)} instead of just one",
                "status": "multiple results"
            }
            
        elif len(results) == 0:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
            
        return message

    async def findMany(
            self, 
            database: str,
            collection: str, 
            key: str, 
            search_str: str,
            order_by: list[str, str] = []
        ):
        collection_ref = self.db.collection(collection)
        
        if order_by == []:
            query = collection_ref.where(key, "==", search_str).get()
        else:
            query = collection_ref.where(key, "==", search_str).order_by(order_by[0], direction=order_by[1]).get()
        
        results = [{"id": doc.id, **doc.to_dict()} for doc in query]
        
        if len(results) >= 1:
            message = {
                "message": results,
                "status": "success"
            }
            
            
        elif len(results) == 0:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
            
        return message

    async def findManyInList(
            self, 
            database: str,
            collection: str, 
            key: str, 
            search_list: list,
            order_by: list[str, str] = []
        ):
        collection_ref = self.db.collection(collection)
        
        if order_by == []:
            query = collection_ref.where(key, "in", search_list).get()
        else:
            query = collection_ref.where(key, "in", search_list).order_by(order_by[0], direction=order_by[1]).get()
        
        results = [{"id": doc.id, **doc.to_dict()} for doc in query]
        
        if len(results) >= 1:
            message = {
                "message": results,
                "status": "success"
            }
            
            
        elif len(results) == 0:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
            
        return message
    
    async def updateOneStrKey(
            self, 
            database: str,
            collection: str, 
            key: str, 
            search_str: str, 
            update_field: str, 
        update_value):
        collection_ref = self.db.collection(collection)
        results = collection_ref.where(key, "==", search_str).get()
        
        if len(results) == 1:
            doc_ref = results[0].reference
            doc_ref.update({update_field: update_value})
            
            message =  {
                "status": "success",
                "result": "Updated",
                "key": key,
                "search_str": search_str,
                "update_field": update_field,
                "update_value": update_value
            }
        elif len(results) > 1:
            message = {
                "message": f"The query returned {len(results)} instead of just one",
                "status": "multiple results"
            }
        else:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
        
        return message
        
    async def updateOneMultiStrKey(
            self, 
            database: str,
            collection: str, 
            filters: dict, 
            update_field: str, 
            update_value
        ):
        collection_ref = self.db.collection(collection)
        
        query = collection_ref
        for key, value in filters.items():
            query = query.where(key, "==", value)
        
        query_results = query.get()

        results = [doc for doc in query_results]
        
        if len(results) == 1:
            doc_ref = results[0].reference
            doc_ref.update({update_field: update_value})
            
            message =  {
                "status": "success",
                "result": "Updated",
                "key": key,
                "search_str": filters,
                "update_field": update_field,
                "update_value": update_value
            }
        elif len(results) > 1:
            message = {
                "message": f"The query returned {len(results)} instead of just one",
                "status": "multiple results"
            }
        else:
            message = {
                "message": "The query returned no results",
                "status": "not found"
            }
        
        return message
    
    async def get_all(
        self,
        database: str,
        collection: str,
    ):
        collection_ref = self.db.collection(collection)
        docs = collection_ref.stream()
                
        dict_results = {
            "results": []
        }
        
        for doc in docs:
            dict_results["results"].append({"id": doc.id, **doc.to_dict()})
            
        return dict_results

# Initialize based on the new logic (local file or Secret Manager)
# firestoreDB = FirestoreAdapter()