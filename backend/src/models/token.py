# [Task]: T-005 | [From]: specs/2-plan/phase-2-fullstack.md

from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    """
    Token response model for authentication endpoints.
    """
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    """
    Payload model for JWT token data.
    """
    sub: Optional[str] = None