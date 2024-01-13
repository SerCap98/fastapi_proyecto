
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB
from modules.ManufacturedProduct.ManufacturedProduct_exceptions import ManufacturedProductExceptions
from modules.ManufacturedProduct.ManufacturedProduct_repositories import ManufacturedProductRepository
from modules.ManufacturedProduct.ManufacturedProduct_schemas import ManufacturedProduct
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID


class ManufacturedProductService:

    def __init__(self, db: Database):
        self.db = db

    async def create_manufactured_product(self, manufactured_product: ManufacturedProduct, id_product: UUID, current_user: UserInDB) -> ServiceResult:
        manufactured_product_repo = ManufacturedProductRepository(self.db)

        product_query = "SELECT id FROM Product WHERE id = :id_product"
        product_exists = await self.db.fetch_one(query=product_query, values={"id_product": id_product})

        if not product_exists:
            return ServiceResult(error="El producto ingresado no ha sido fabricado")

        try:
            new_manufactured_product = await manufactured_product_repo.create_manufactured_product(manufactured_product,current_user)
            return ServiceResult(new_manufactured_product,)

        except Exception as e:
            return ServiceResult(e)

    async def get_manufactured_product_by_lot_number(self, lot_number: str) -> ServiceResult:
        try:
            manufactured_product = await ManufacturedProductRepository(self.db).get_manufactured_product_by_lot_number(lot_number)
            return ServiceResult(manufactured_product)
        except Exception  as e:

            return ServiceResult(e)


    async def update_manufactured_product_by_lot_number(self, lot_number: str, manufactured_product_update: ManufacturedProduct, id_product: UUID, current_user: UserInDB) -> ServiceResult:
        try:
            exist_manufactured_product=await self.get_manufactured_product_by_lot_number(lot_number)
            if not exist_manufactured_product.success:return exist_manufactured_product

            product_query = "SELECT id FROM Product WHERE id = :id_product"
            product_exists = await self.db.fetch_one(query=product_query, values={"id_product": id_product})

            if not product_exists:
                return ServiceResult(error="El producto ingresado no ha sido fabricado")

            updated_manufactured_product = await ManufacturedProductRepository(self.db).update_manufactured_product_by_lot_number(exist_manufactured_product, manufactured_product_update,current_user)
            return ServiceResult(updated_manufactured_product)
        except Exception as e:
            return ServiceResult(e)


    async def delete_manufactured_product_by_lot_number(self, lot_number: str) -> ServiceResult:
        try:

            exist=await self.get_manufactured_product_by_lot_number(lot_number)
            if not exist.success:return exist

            await ManufacturedProductRepository(self.db).delete_manufactured_product_by_lot_number(lot_number)
            return ServiceResult({"message": "Producto Manufacturado eliminado exitosamente"})
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
                route=f"{API_PREFIX}/manufactured product",
            )
            return ServiceResult(response)
        except Exception as e:

            return ServiceResult(e)