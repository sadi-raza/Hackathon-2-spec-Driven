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
        import logging
        logging.error(f"Token expired: {token[:20]}..." if len(token) > 20 else token)
        raise HTTPException(status_code=401, detail="Token expired")
    except InvalidTokenError as e:
        import logging
        logging.error(f"Invalid token: {str(e)}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        import logging
        logging.error(f"Unexpected error during token verification: {str(e)}")
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

    token_parts = authorization.split(" ")
    if len(token_parts) != 2:
        import logging
        logging.error("Malformed authorization header")
        raise HTTPException(status_code=401, detail="Malformed authorization header")

    token = token_parts[1]
    payload = verify_token(token)

    user_id_str = payload.get("sub") or payload.get("userId")
    if not user_id_str:
        import logging
        logging.error("Missing user ID in token payload")
        raise HTTPException(status_code=401, detail="Invalid token payload - missing user ID")

    # Convert to int (user IDs are now integers)
    try:
        user_id = int(user_id_str)
        import logging
        logging.info(f"Successfully extracted user ID: {user_id} from token")
    except (ValueError, TypeError):
        import logging
        logging.error(f"Failed to convert user ID to integer: {user_id_str}")
        raise HTTPException(status_code=401, detail="Invalid user ID in token")

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    result = await db.execute(statement)
    user = result.scalar_one_or_none()

    if not user:
        import logging
        logging.error(f"User not found in database: {user_id}")
        raise HTTPException(status_code=401, detail="User not found")

    return user


from fastapi import Depends
from typing import Annotated

CurrentUser = Annotated[User, Depends(get_current_user)]