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

            exist_product=await self.exist_Product(OrderProduct.product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            new_OrderProduct = await OrderProduct_repo.create_order_product(OrderProduct,current_user,product_id)
            return ServiceResult(new_OrderProduct)

        except Exception as e:
            return ServiceResult(e)

    async def get_order_by_product(self, product_name: str) -> ServiceResult:
        try:

            exist_product=await self.exist_Product(product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            OrderProduct = await OrderProductRepository(self.db).get_order_by_product(product_id)
            return ServiceResult(OrderProduct)
        except Exception  as e:

            return ServiceResult(e)

    async def exist_Product(self, product_name: str) -> ServiceResult:
        Product_services=ProductService(self.db)

        try:
            exist_product=await Product_services.get_product_by_name(product_name.upper())
            if not exist_product.success:return exist_product

            result = { "product_id": exist_product.value.id }

            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)


    async def get_all_order_product(self,
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:

                OrderProduct = await OrderProductRepository(self.db).get_all_order_product(search,order,direction)
                OrderProduct_list = [OrderProductList(**item.dict()) for item in OrderProduct]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=OrderProduct_list,
                    route=f"{API_PREFIX}/OrderProduct",
                )
                return ServiceResult(response)
            except Exception as e:

                return ServiceResult(e)