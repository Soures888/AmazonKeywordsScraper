from typing import List
from src.models.product import ProductORM, ProductData

class ProductCrud:

    def create(self, obj_in: ProductData) -> ProductORM:
        return ProductORM.create(**obj_in.dict(skip_defaults=True))

    def create_many(self, obj_in_list: List[ProductData]):
        for obj_in in obj_in_list:
            self.create(obj_in)

