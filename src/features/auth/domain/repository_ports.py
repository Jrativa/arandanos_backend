# src/features/auth/domain/ports.py
import datetime
from typing import Protocol, Optional
from uuid import UUID
from src.features.auth.domain import schemas

class RoleRepository(Protocol):
    """Puerto para manejar operaciones de Roles"""
    def get_by_name(self, name: str) -> Optional[schemas.RoleResponse]:
        ...
        
    def create(self, role: schemas.RoleCreate) -> schemas.RoleResponse:
        ...

class UserRepository(Protocol):
    """Puerto para manejar operaciones de Usuarios"""
    def get_by_email(self, email: str) -> Optional[schemas.UserResponse]:
        ...

    """Puerto para manejar operaciones de Usuarios"""
    def get_current_user(self, token: str) -> Optional[schemas.UserResponse]:
        ...

    def get_by_username(self, username: str) -> Optional[schemas.UserResponse]:
        ...
        
    def get_by_login_id(self, user_identifier: str) -> Optional[schemas.UserResponse]:
        """Busca por email o username (para el login)"""
        ...
        
    # Fíjate que pedimos 'hashed_password' y no el schema puro, 
    # porque la capa de aplicación lo hasheará antes de enviarlo.
    def create(self, user: schemas.UserCreate, hashed_password: str) -> schemas.UserResponse:
        ...

class SessionRepository(Protocol):
    """Puerto para manejar operaciones de Sesiones (Refresh Tokens)"""
    def create_session(self, user_id: UUID, refresh_token: str, expires_at: datetime):
        ...
        
    def get_valid_session(self, refresh_token: str):
        ...