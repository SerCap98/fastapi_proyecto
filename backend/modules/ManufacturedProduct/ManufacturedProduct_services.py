from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB

from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID
import uuid

from modules.Product.Product_services import ProductService
from modules.ManufacturedProduct.ManufacturedProduct_exceptions import ManufacturedProductExceptions
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct,ManufacturedProductInDB
from modules.ManufacturedProduct.ManufacturedProduct_repositories import ManufacturedProductRepository

class ManufacturedProductService:

    def __init__(self, db: Database):
        self.db = db

    async def create_manufactured_product(self, ManufacturedProduct: ManufacturedProduct,current_user: UserInDB) -> ServiceResult:
        Manufactured_Product_repo = ManufacturedProductRepository(self.db)

        try:

            exist_product=await self.exist_Product(ManufacturedProduct.product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            new_ManufacturedProduct = await Manufactured_Product_repo.create_manufactured_product(ManufacturedProduct, current_user, product_id)
            return ServiceResult(new_ManufacturedProduct)

        except Exception as e:
            return ServiceResult(e)


    #GET BY ID PRODUCT
    async def get_manufactured_product_by_id_product(self, product_name: str) -> ServiceResult:
        try:

            exist_product=await self.exist_Product(product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            manufactured_product = await ManufacturedProductRepository(self.db).get_manufactured_product_by_id_product(product_id)
            return ServiceResult(manufactured_product)
        except Exception  as e:

            return ServiceResult(e)

    #GET BY LOT NUMBER
    async def get_manufactured_product_by_lot_number(self, lot_number: str) -> ServiceResult:
        try:
            manufactured_product = await ManufacturedProductRepository(self.db).get_manufactured_product_by_lot_number(lot_number)
            return ServiceResult(manufactured_product)
        except Exception  as e:

            return ServiceResult(e)


    #UPDATE BY ID PRODUCT
    async def update_quantity_by_id_product(self,current_user: UserInDB,product_name: str, update_quantity:float) -> ServiceResult:
        try:

            exist_product=await self.exist_Product(product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            manufactured_product = await ManufacturedProductRepository(self.db).update_quantity_by_id_product(current_user,product_id,update_quantity)
            return ServiceResult(manufactured_product)
        except Exception  as e:
            return ServiceResult(e)

    #UPDATE BY LOT NUMBER
    async def update_quantity_by_lot_number(self,current_user: UserInDB,lot_number: str, update_quantity:float) -> ServiceResult:
        try:

            manufactured_product=await self.get_manufactured_product_by_lot_number(lot_number)
            if not manufactured_product.success:return manufactured_product
            updated_quantity = await ManufacturedProductRepository(self.db).update_quantity_by_lot_number(manufactured_product, update_quantity,current_user)
            return ServiceResult(updated_quantity)
        except Exception as e:
            return ServiceResult(e)


    #DELETE BY ID PRODUCT
    async def delete_manufactured_product_by_id_product(self, product_name: str) -> ServiceResult:
        try:

            exist_product=await self.exist_Product(product_name)
            if not exist_product.success:
                return exist_product

            product_id=uuid.UUID(str(exist_product.value["product_id"]))

            await ManufacturedProductRepository(self.db).delete_manufactured_product_by_id_product(product_id)
            return ServiceResult({"message": "Record deleted successfully"})
        except Exception  as e:
            return ServiceResult(e)

    #DELETE BY LOT NUMBER
    async def delete_manufactured_product_by_lot_number(self, lot_number: str) -> ServiceResult:
        try:

            exist=await self.get_manufactured_product_by_lot_number(lot_number)
            if not exist.success:return exist

            await ManufacturedProductRepository(self.db).delete_manufactured_product_by_lot_number(lot_number)
            return ServiceResult({"message": "Producto manufacturado eliminado exitosamente"})
        except Exception as e:
            return ServiceResult(e)


    async def exist_Product(self, product_name: str) -> ServiceResult:
        Product_services=ProductService(self.db)

        try:
            exist_product=await Product_services.get_product_by_name(product_name.upper())
            if not exist_product.success:return exist_product

            result = {
                    "product_id": exist_product.value.id
                }

            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)


    async def get_all_manufactured_product(self,
            search: str | None,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:

                manufactured_product = await ManufacturedProductRepository(self.db).get_all_manufactured_product(search,order,direction)
                manufactured_product_list = [ManufacturedProduct(**item.dict()) for item in manufactured_product]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=manufactured_product_list,
                    route=f"{API_PREFIX}/manufactured-products",
                )
                return ServiceResult(response)
            except Exception as e:

                return ServiceResult(e)