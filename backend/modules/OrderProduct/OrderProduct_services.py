from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB

from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID
import uuid

from modules.Product.Product_services import ProductService
from modules.OrderProduct.OrderProduct_exceptions import OrderProductExceptions
from modules.OrderProduct.OrderProduct_schemas import OrderProduct,OrderProductInDB,OrderProductList
from modules.OrderProduct.OrderProduct_repositories import OrderProductRepository

class OrderProductService:

    def __init__(self, db: Database):
        self.db = db

    async def create_order_product(self, OrderProduct: OrderProduct,current_user: UserInDB) -> ServiceResult:
        OrderProduct_repo = OrderProductRepository(self.db)

        try:
            if OrderProduct.product_name:
                exist_product=await self.exist_Product(OrderProduct.product_name)
                if not exist_product.success:
                    return exist_product
            else: return ServiceResult(OrderProductExceptions.OrderProductInvalidCreateParamsException())

           
          
            new_OrderProduct = await OrderProduct_repo.create_order_product(OrderProduct,current_user,exist_product.value.id,exist_product.value.cost_per_bag)
            return ServiceResult(new_OrderProduct)

        except Exception as e:
            return ServiceResult(e)



    async def exist_Product(self, product_name: str) -> ServiceResult:
        Product_services=ProductService(self.db)

        try:
            exist_product=await Product_services.get_product_by_name(product_name.upper())
            if not exist_product.success:return exist_product

            result = exist_product.value 

            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)

