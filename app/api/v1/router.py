from fastapi import APIRouter
from app.api.v1.chat import router as chat_router
from app.api.v1.projects import router as projects_router
from app.api.v1.knowledge import router as knowledge_router
from app.api.v1.leads import router as leads_router
from app.api.v1.health import router as health_router
from app.api.v1.store import router as store_router
from app.api.v1.appstore import router as appstore_router

api_router = APIRouter(prefix="/v1")
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(projects_router)
api_router.include_router(knowledge_router)
api_router.include_router(leads_router)
api_router.include_router(store_router)
api_router.include_router(appstore_router)
