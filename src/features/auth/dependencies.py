# src/features/auth/dependencies.py
import importlib
from fastapi import Depends
from src.core.config import settings
from src.core.databases import get_db

from src.features.auth.application.services import AuthService

# 1. Construimos la ruta del módulo dinámicamente según el motor del .env
# Si es "postgres" -> src.features.auth.infrastructure.postgres.repositories
# Si es "mongo"    -> src.features.auth.infrastructure.mongo.repositories
repo_module_path = f"src.features.auth.infrastructure.{settings.DB_ENGINE}.repositories"

# 2. Importamos el módulo UNA SOLA VEZ cuando arranca FastAPI
try:
    repos = importlib.import_module(repo_module_path)
except ImportError:
    raise NotImplementedError(f"Repositorios no implementados para el motor: {settings.DB_ENGINE}")

# 3. La fábrica ahora es 100% agnóstica y súper corta
def get_auth_service(db = Depends(get_db)) -> AuthService:
    """Fábrica dinámica que inyecta las dependencias correctas"""
    return AuthService(
        user_repo=repos.UserRepository(db),
        role_repo=repos.RoleRepository(db),
        session_repo=repos.SessionRepository(db)
    )