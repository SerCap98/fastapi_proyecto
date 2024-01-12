
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.Product.Product_exceptions import ProductExceptions
from modules.Product.Product_repositories import ProductRepository
from modules.Product.Product_schemas import Product
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class ProductService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_product(self, product: Product,current_user: UserInDB) -> ServiceResult:
        product_repo = ProductRepository(self.db)
        try:
            new_product = await product_repo.create_product(product,current_user)
            return ServiceResult(new_product)
        
        except Exception as e:
            return ServiceResult(e)

    async def get_product_by_name(self, name: str) -> ServiceResult:
        try:
            product = await ProductRepository(self.db).get_product_by_name(name)
            return ServiceResult(product)
        except Exception  as e:

            return ServiceResult(e)


    async def update_product_by_name(self, name: str, product_update: Product,current_user: UserInDB) -> ServiceResult:
        try:
            exist_product=await self.get_product_by_name(name)
            if not exist_product.success:return exist_product
            updated_product = await ProductRepository(self.db).update_product_by_name(exist_product, product_update,current_user)
            return ServiceResult(updated_product)
        except Exception as e:
            return ServiceResult(e)


    async def delete_product_by_name(self, name: str) -> ServiceResult:
        try:
     
            exist=await self.get_product_by_name(name)
            if not exist.success:return exist

            await ProductRepository(self.db).delete_product_by_name(name)
            return ServiceResult({"message": "Producto eliminado exitosamente"})
        except Exception as e:
            return ServiceResult(e)
 
    async def get_all_product(self, 
        search: str | None,
        page_num: int = 1,
        page_size: int = 10,
        order: str = None,
        direction: str = None,
    ) -> ServiceResult:
        try:
     
            product = await ProductRepository(self.db).get_all_product(search,order,direction)
            product_list = [Product(**item.dict()) for item in product]
            response = short_pagination(
                page_num=page_num,
                page_size=page_size,
                data_list=product_list,
                route=f"{API_PREFIX}/product",
            )
            return ServiceResult(response)
        except Exception as e:
            
            return ServiceResult(e)