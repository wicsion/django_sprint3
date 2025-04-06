from sanic import Blueprint, json
from app.auth import protected, is_admin
from app.models import User, Account
from app.schemas import UserResponse, AccountResponse

user_bp = Blueprint("user", url_prefix="/user")

@user_bp.get("/me")
@protected()  # Обратите внимание на скобки - теперь это вызов функции
async def get_me(request):
    return json(UserResponse(**request.ctx.user.__dict__).dict())

@user_bp.get("/accounts")
@protected()
async def list_accounts(request):
    accounts = await Account.filter(user_id=request.ctx.user.id)
    return json([AccountResponse(**acc.__dict__).dict() for acc in accounts])
