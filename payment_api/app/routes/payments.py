from sanic import Blueprint, json
from hashlib import sha256
from app.models import Account, Payment
from app.schemas import PaymentCreate, PaymentResponse
from app.config import SECRET_KEY


payment_bp = Blueprint("payment", url_prefix="/payment")


@payment_bp.post("/webhook")
async def payment_webhook(request):
    data = PaymentCreate(**request.json)

    signature_str = (f"{data.account_id}{data.amount}"
                     f"{data.transaction_id}{data.user_id}{SECRET_KEY}")
    calculated_signature = sha256(signature_str.encode()).hexdigest()

    if calculated_signature != data.signature:
        return json({"error": "Invalid signature"}, status=400)

    account = await Account.get_or_create(
        id=data.account_id,
        defaults={"user_id": data.user_id, "balance": 0}
    )

    if await Payment.filter(transaction_id=data.transaction_id).exists():
        return json({"error": "Duplicate transaction"}, status=400)

    payment = await Payment.create(
        transaction_id=data.transaction_id,
        account_id=data.account_id,
        user_id=data.user_id,
        amount=data.amount
    )

    account.balance += data.amount
    await account.save()

    return json(PaymentResponse(**payment.__dict__).dict())
