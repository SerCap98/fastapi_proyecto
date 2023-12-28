
from modules.MateriasPrimas.MateriaPrima_exceptions import MateriaPrimaExceptions
from modules.MateriasPrimas.MateriaPrima_repositories import MateriaPrimaRepository
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID

#import logging
#logger = logging.getLogger(__name__)
#logging.basicConfig(level=logging.DEBUG)
#logger.debug(f"Error: {e}")

class MateriaPrimaService:
    
    def __init__(self, db: Database):
        self.db = db

    async def create_materia_prima(self, materia_prima: MateriaPrima) -> ServiceResult:
        materia_prima_repo = MateriaPrimaRepository(self.db)
        try:
            new_materia_prima = await materia_prima_repo.create_materia_prima(materia_prima)
            return ServiceResult(new_materia_prima)
        except Exception as e:
            return ServiceResult(e)

    async def get_materia_prima_by_code(self, code: str) -> ServiceResult:
        try:
            materia_prima = await MateriaPrimaRepository(self.db).get_materia_prima_by_code(code)
            return ServiceResult(materia_prima)
        except Exception  as e:
            return ServiceResult(e)


    async def update_materia_prima_by_code(self, code: str, materia_prima_update: MateriaPrima) -> ServiceResult:
        try:
            exist=await self.get_materia_prima_by_code(code)
            if not exist.success:return exist
            updated_materia_prima = await MateriaPrimaRepository(self.db).update_materia_prima_by_code(code, materia_prima_update)
            return ServiceResult(updated_materia_prima)
        except Exception as e:
            return ServiceResult(e)


    async def delete_materia_prima_by_code(self, code: str) -> ServiceResult:
        try:
     
            exist=await self.get_materia_prima_by_code(code)
            if not exist.success:return exist

            await MateriaPrimaRepository(self.db).delete_materia_prima_by_code(code)
            return ServiceResult({"message": "Materia prima eliminada exitosamente"})
        except Exception as e:
            return ServiceResult(e)
 
    async def get_all_materias_primas(self) -> ServiceResult:
        try:
            materias_primas = await MateriaPrimaRepository(self.db).get_all_materias_primas()
            return ServiceResult(materias_primas)
        except Exception as e:
            return ServiceResult(e)            
        