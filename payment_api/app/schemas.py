from pydantic import BaseModel


class UserCreate(BaseModel):
    email: str
    password: str
    full_name: str
    is_admin: bool = False

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str

class AccountResponse(BaseModel):
    id: int
    user_id: int
    balance: float

class PaymentCreate(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str

class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    amount: float
