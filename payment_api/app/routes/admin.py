from sanic import Blueprint, json
from app.auth import protected, is_admin
from app.models import User
from app.schemas import UserResponse

admin_bp = Blueprint("admin", url_prefix="/admin")

@admin_bp.post("/users")
@protected()
@is_admin()  # Теперь оба декоратора вызываются как функции
async def create_user(request):
    user_data = request.json
    user = await User.create(**user_data)
    return json(UserResponse(**user.__dict__).dict())
