
from shared.core.config import API_PREFIX
from shared.utils.short_pagination import short_pagination
from modules.users.users.user_schemas import UserInDB


from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID
import uuid

from modules.RawMaterials.RawMaterial_services import RawMaterialService
from modules.Product.Product_services import ProductService
from modules.Formula.Formula_exceptions import FormulaExceptions
from modules.Formula.Formula_schemas import Formula,FormulaInDB,FormulaList
from modules.Formula.Formula_repositories import FormulaRepository

class FormulaService:

    def __init__(self, db: Database):
        self.db = db

    async def create_formula(self, Form: Formula,current_user: UserInDB) -> ServiceResult:
        Formula_repo = FormulaRepository(self.db)

        try:

            exist_product_and_raw_material=await self.exist_Product_RawMaterial(Form.product_name,Form.raw_material_code)
            if not exist_product_and_raw_material.success:
                return exist_product_and_raw_material

            raw_material_id=uuid.UUID(str(exist_product_and_raw_material.value["raw_material_id"]))
            product_id=uuid.UUID(str(exist_product_and_raw_material.value["product_id"]))

            new_Form = await Formula_repo.create_formula(Form,current_user,raw_material_id,product_id)
            return ServiceResult(new_Form)

        except Exception as e:
            return ServiceResult(e)

    async def get_formula_by_product_and_material(self, product_name: str, raw_material_code: str) -> ServiceResult:
        try:

            exist_product_and_raw_material=await self.exist_Product_RawMaterial(product_name,raw_material_code)
            if not exist_product_and_raw_material.success:
                return exist_product_and_raw_material

            raw_material_id=uuid.UUID(str(exist_product_and_raw_material.value["raw_material_id"]))
            product_id=uuid.UUID(str(exist_product_and_raw_material.value["product_id"]))

            formula = await FormulaRepository(self.db).get_formula_by_product_and_material(raw_material_id,product_id)
            return ServiceResult(formula)
        except Exception  as e:

            return ServiceResult(e)





    async def exist_Product_RawMaterial(self, product_name: str, raw_material_code: str) -> ServiceResult:
        Raw_Material_services=RawMaterialService(self.db)
        Product_services=ProductService(self.db)

        try:
            exist_raw_material=await Raw_Material_services.get_raw_material_by_code(raw_material_code.upper())
            if not exist_raw_material.success:return exist_raw_material

            exist_product=await Product_services.get_product_by_name(product_name.upper())
            if not exist_product.success:return exist_product

            result = {
                    "raw_material_id": exist_raw_material.value.id,
                    "product_id": exist_product.value.id
                }

            return ServiceResult(result)

        except Exception as e:
            return ServiceResult(e)

    async def get_all_formula(self, search: str | None, page_num: int = 1, page_size: int = 10, order: str = None, direction: str = None, ) -> ServiceResult:
            try:

                formula = await FormulaRepository(self.db).get_all_formula(search,order,direction)
                formula_list = [FormulaList(**item.dict()) for item in formula]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=formula_list,
                    route=f"{API_PREFIX}/formula",
                )
                return ServiceResult(response)
            except Exception as e:

                return ServiceResult(e)



    async def get_formula_by_mat_code(self,
            code: str,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                manufactured_product = await FormulaRepository(self.db).get_inventory_by_mat_code(code, order, direction)
                manufactured_product_list = [FormulaList(**item.dict()) for item in manufactured_product]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=manufactured_product_list,
                    route=f"{API_PREFIX}/manufactured-products/by-identifier/{code}",
                )
                return ServiceResult(response)
            except Exception as e:
                return ServiceResult(e)
            
    async def get_inventory_by_fact_identifier(self,
            identifier: str,
            page_num: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: str = None,
        ) -> ServiceResult:
            try:
                manufactured_product = await FormulaRepository(self.db).get_inventory_by_fact_identifier(identifier, order, direction)
                manufactured_product_list = [FormulaList(**item.dict()) for item in manufactured_product]
                response = short_pagination(
                    page_num=page_num,
                    page_size=page_size,
                    data_list=manufactured_product_list,
                    route=f"{API_PREFIX}/manufactured-products/by-identifier/{identifier}",
                )
                return ServiceResult(response)
            except Exception as e:
                return ServiceResult(e)