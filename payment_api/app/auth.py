from functools import wraps
from sanic.exceptions import Unauthorized, Forbidden
from app.models import User
from jose import jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def protected():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                raise Unauthorized("Missing token")

            try:
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user = await User.get(id=payload.get("sub"))
                if not user:
                    raise Unauthorized("Invalid user")
                request.ctx.user = user
            except Exception as e:
                raise Unauthorized(f"Invalid token: {str(e)}")

            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator

def is_admin():
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            if not hasattr(request.ctx, 'user') or not request.ctx.user.is_admin:
                raise Forbidden("Admin access required")
            return await f(request, *args, **kwargs)
        return decorated_function
    return decorator

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
