from fastapi import Depends, HTTPException, Header
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from typing import Annotated

from ..config import settings
from ..database import get_db
from ..models.user import User


security = HTTPBearer()


def verify_token(token: str) -> dict:
    """
    Verify JWT and return payload.
    """
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=["HS256"],
        )
        return payload
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_user(
    authorization: str = Header(None),
    db: AsyncSession = Depends(get_db),
) -> User:
    """
    Extract and validate user from JWT token.
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing authorization")

    token = authorization.split(" ")[1]
    payload = verify_token(token)

    user_id = payload.get("sub") or payload.get("userId")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


from fastapi import Depends
from typing import Annotated

CurrentUser = Annotated[User, Depends(get_current_user)]