import datetime
from typing import Optional
from enum import Enum#, IntEnum

from pydantic import BaseModel, BaseConfig
from bson import ObjectId

class PaymentType(str, Enum):
    credit_card = 'CREDIT_CARD'
    mobile_payment = 'MOBILE_PAYMENT'
    merchant = 'MERCHANT'

class OID(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        try:
            return ObjectId(str(v))
        except InvalidId:
            raise ValueError("Not a valid ObjectId")

class MongoModel(BaseModel):
    class Config(BaseConfig):
        json_encoders = {
            datetime: lambda dt: dt.isoformat(),
            ObjectId: lambda oid: str(oid),
        }
