# src/features/auth/presentation/routes.py
from fastapi import APIRouter, Depends, HTTPException
from src.features.auth.domain import schemas
from src.features.auth.application.services import AuthService
from src.features.auth.dependencies import get_auth_service

router = APIRouter()

@router.post("/roles/", response_model=schemas.RoleResponse)
def create_role(
    role: schemas.RoleCreate, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.create_role(role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/users/", response_model=schemas.UserResponse)
def create_user(
    user: schemas.UserCreate, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.register_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/users/{username}", response_model=schemas.UserResponse)
def get_user(
    username: str, 
    auth_service: AuthService = Depends(get_auth_service)
):
    user = auth_service.user_repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user

@router.post("/login", response_model=schemas.LoginResponse) # Actualizamos el response_model
def login(
    login_data: schemas.LoginRequest, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.login(login_data)
    except ValueError as e:
        if str(e) == "Usuario inactivo":
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh", response_model=schemas.LoginResponse)
def refresh_token(
    request: schemas.RefreshTokenRequest, 
    auth_service: AuthService = Depends(get_auth_service)
):
    try:
        return auth_service.refresh_token(request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))