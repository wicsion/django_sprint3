from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User, Account, Payment


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalar_one_or_none()


async def get_user_accounts(db: AsyncSession, user_id: int):
    result = await db.execute(select(Account).filter(Account.user_id == user_id))
    return result.scalars().all()


async def process_payment(db: AsyncSession, payment_data: dict):
    account = await db.execute(select(Account)
                               .filter(Account.id == payment_data["account_id"]))
    account = account.scalar_one_or_none()

    if not account:
        account = Account(id=payment_data["account_id"], user_id=payment_data["user_id"])
        db.add(account)

    # Проверка дубликата транзакции
    existing = await db.execute(select(Payment)
                                .filter(Payment.transaction_id == payment_data["transaction_id"]))
    if existing.scalar_one_or_none():
        return None

    # Создание платежа
    payment = Payment(**payment_data)
    db.add(payment)

    # Обновление баланса
    account.balance += payment_data["amount"]

    await db.commit()
    return payment