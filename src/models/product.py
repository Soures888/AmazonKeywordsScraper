from peewee import (Model, DateTimeField, TextField,
                    IntegerField, BooleanField)
from pydantic import BaseModel
import datetime
from db import db


class BaseORMModel(Model):
    class Meta:
        database = db


class ProductData(BaseModel):
    dt: datetime.datetime
    product_id: str
    keyword: str
    rank_type: str
    rank: int
    page_number: int
    bestseller_badge: bool = False
    amazonchoice_badge: bool = False


class ProductORM(BaseORMModel):
    dt = DateTimeField()
    product_id = TextField()
    keyword = TextField()
    rank_type = TextField()
    rank = IntegerField()
    page_number = IntegerField()
    bestseller_badge = BooleanField(default=False)
    amazonchoice_badge = BooleanField(default=False)

