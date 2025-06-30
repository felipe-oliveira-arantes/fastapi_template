from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from fastapi import FastAPI
from app.dependencies.container import engine
from app.routers import appointmentRouter, patientsRouter

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🔧 Criando tabelas no startup...")
    SQLModel.metadata.create_all(engine)
    yield
    print("🛑 Encerrando app...")
    
app = FastAPI(
    title="Medical Clinic Secretary System",
    description="API for managing patients and appointments in a medical clinic.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(appointmentRouter.router)
app.include_router(patientsRouter.router)


@app.get("/")
async def get_home():
    return {"message": "User app"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat()
    }
