# [Task]: T-005 | [From]: specs/2-plan/phase-2-fullstack.md

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from slowapi import Limiter
from slowapi.util import get_remote_address
from src.models.user import UserCreate, UserPublic, UserUpdate, User
from src.models.token import Token
from src.services.auth_service import AuthService
from src.db.session import get_session
from src.api.deps import get_current_user

# Initialize rate limiter for auth endpoints
limiter = Limiter(key_func=get_remote_address)


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/signup", response_model=UserPublic)
@limiter.limit("5/minute")
async def signup(
    request: Request,
    user_create: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Register a new user.

    Args:
        request: HTTP request object for rate limiting
        user_create: User creation data (email, name, password)
        session: Async database session

    Returns:
        UserPublic: Public user data (without password)

    Raises:
        HTTPException: 400 if email already exists or validation fails
    """
    auth_service = AuthService()

    try:
        # Register the user using the service
        created_user = await auth_service.register_user(session, user_create)

        if not created_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    # Return public user data (without password)
    return UserPublic.from_orm(created_user) if hasattr(UserPublic, 'from_orm') else UserPublic(
        id=created_user.id,
        email=created_user.email,
        name=created_user.name,
        created_at=created_user.created_at,
        updated_at=created_user.updated_at
    )


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    """
    Authenticate user and return access token.

    Args:
        request: HTTP request object for rate limiting
        form_data: OAuth2 form data (username/email and password)
        session: Async database session

    Returns:
        Token: Access token for authentication

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    auth_service = AuthService()

    # Authenticate the user using the service
    user = await auth_service.authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token using the service
    access_token = await auth_service.generate_access_token(user.id)

    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserPublic)
async def get_current_user_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get the profile of the currently authenticated user.

    Args:
        current_user: The authenticated user (from get_current_user dependency)

    Returns:
        UserPublic: Public user data (email, name, id, timestamps)
    """
    # Return the current user's public data
    # The user is already fetched and validated by the get_current_user dependency
    return UserPublic.from_orm(current_user) if hasattr(UserPublic, 'from_orm') else UserPublic(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )


@router.post("/signout")
async def signout():
    """
    Sign out the current user (session invalidation).

    Note: Since we're using stateless JWT tokens, this endpoint serves as a
    placeholder for client-side token cleanup. The actual token remains valid
    until expiration, but the client should remove it from storage.

    Returns:
        Success message confirming signout
    """
    # In a real implementation with server-side session management,
    # we would invalidate the token here.
    # With JWT, the token remains valid until expiration, so this is
    # primarily for client-side cleanup.
    return {"message": "Successfully signed out"}


@router.put("/profile", response_model=UserPublic)
async def update_user_profile(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """
    Update the profile of the currently authenticated user.

    Args:
        user_update: User update data (email, name, password)
        current_user: The authenticated user (from get_current_user dependency)
        session: Async database session

    Returns:
        UserPublic: Updated public user data (email, name, id, timestamps)

    Raises:
        HTTPException: 400 if email already exists for another user or validation fails
    """
    auth_service = AuthService()

    try:
        # Update the user profile using the service
        updated_user = await auth_service.update_user_profile(session, current_user.id, user_update)

        if not updated_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    return UserPublic.from_orm(updated_user) if hasattr(UserPublic, 'from_orm') else UserPublic(
        id=updated_user.id,
        email=updated_user.email,
        name=updated_user.name,
        created_at=updated_user.created_at,
        updated_at=updated_user.updated_at
    )