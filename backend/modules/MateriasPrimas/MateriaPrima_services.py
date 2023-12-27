import logging
import uuid
from modules.MateriasPrimas.MateriaPrima_exceptions import MateriaPrimaExceptions
from modules.MateriasPrimas.MateriaPrima_repositories import MateriaPrimaRepository
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima, MateriaPrimaInDB
from shared.utils.service_result import ServiceResult
from databases import Database
from uuid import UUID

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

    async def get_materia_prima_by_id(self, id: str) -> ServiceResult:
        try:
            uuid_obj = uuid.UUID(id)
            materia_prima = await MateriaPrimaRepository(self.db).get_materia_prima_by_id(uuid_obj)
            return ServiceResult(materia_prima)
        except ValueError:
            return ServiceResult(MateriaPrimaExceptions.MateriaPrimaInvalidUUIDException())
        except Exception  as e:
            return ServiceResult(e)

    # Aquí puedes implementar métodos adicionales para actualizar, eliminar y listar materias primas
