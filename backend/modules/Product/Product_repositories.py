
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid
from shared.utils.service_result import ServiceResult
from modules.users.users.user_schemas import UserInDB

from modules.Product.Product_exceptions import ProductExceptions
from modules.Product.Product_schemas import Product,ProductInDB, ProductList
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository




class ProductRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[Product]:
        return Product

    @property
    def _schema_out(self) -> Type[ProductInDB]:
        return ProductInDB

    async def create_product(self, product: Product,current_user: UserInDB) -> ProductInDB:
        from modules.Product.Product_sqlstaments import CREATE_PRODUCT
       
        product_id = str(uuid.uuid4())
        current_time = datetime.now()
        print(product_id)
        
        values = {
            "id": product_id ,
            "name": product.name.upper() if product.name else None,
            "cost_per_bag": product.cost_per_bag if product.cost_per_bag else None,
            "created_by": current_user.id,
            "created_at": current_time
            }
        print(values)
        try:
            print(values)
            record = await self.db.fetch_one(query=CREATE_PRODUCT, values=values)
        except Exception as e:
            raise ProductExceptions.ProductInvalidCreateParamsException(e=e)

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_product_by_name(self, name: str) -> ProductInDB:
        from modules.Product.Product_sqlstaments import GET_PRODUCT_BY_NAME
        values = {"name": name.upper()}
        record = await self.db.fetch_one(query=GET_PRODUCT_BY_NAME, values=values)
        if not record:
            raise ProductExceptions.ProductNotFoundException()
        return self._schema_out(**dict(record))

    async def update_product_by_name(self, exist_product: ServiceResult, product_update: Product,current_user: UserInDB) -> ProductInDB:
        from modules.Product.Product_sqlstaments import UPDATE_PRODUCT_BY_NAME

        updated_values = {
            "name": product_update.name.upper() if product_update.name else exist_product.value.name,
            "cost_per_bag": product_update.cost_per_bag if product_update.cost_per_bag else exist_product.value.cost_per_bag,
            "updated_by": current_user.id,
            "updated_at": datetime.now()
        }
        try:
            record = await self.db.fetch_one(query=UPDATE_PRODUCT_BY_NAME, values={**updated_values, "original_name": exist_product.value.name.upper()})

            return self._schema_out(**dict(record))
        except Exception as e:
            raise ProductExceptions.ProductInvalidUpdateParamsException(e=e)

    async def delete_product_by_name(self, name: str):
        from modules.Product.Product_sqlstaments import DELETE_PRODUCT_BY_NAME
        try:
            await self.db.execute(query=DELETE_PRODUCT_BY_NAME, values={"name": name.upper()})
        except Exception as e:
            raise ProductExceptions.ProductDeletionException()
        return True

    async def get_all_product(self,
        search: str | None,
        order: str | None,
        direction: str | None
        ) -> List:

        from modules.Product.Product_sqlstaments import LIST_PRODUCT,PRODUCT_COMPLEMENTS,PRODUCT_SEARCH

        order = order.lower() if order != None else None
        direction = direction.upper() if order != None else None
        values = {}
        sql_sentence = PRODUCT_COMPLEMENTS(order, direction)
        sql_search = PRODUCT_SEARCH()
        if not search:
            sql_sentence = LIST_PRODUCT + sql_sentence
        else:
            sql_sentence = LIST_PRODUCT + sql_search + sql_sentence
            values["search"] = "%" + search + "%"
        try:
           
            records = await self.db.fetch_all(query=sql_sentence,values=values)
            if len(records) == 0 or not records:
                return []

            return [ProductList(**dict(record)) for record in records]
        

        except Exception as e:
            raise ProductExceptions.ProductListException