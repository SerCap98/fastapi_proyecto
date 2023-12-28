
from datetime import datetime
from typing import List, Type
from uuid import UUID
import uuid

from modules.MateriasPrimas.MateriaPrima_exceptions import MateriaPrimaExceptions
from modules.MateriasPrimas.MateriaPrima_schemas import MateriaPrima,MateriaPrimaInDB
from shared.utils.record_to_dict import record_to_dict
from shared.utils.repositories_base import BaseRepository


class MateriaPrimaRepository(BaseRepository):
    @property
    def _schema_in(self) -> Type[MateriaPrima]:
        return MateriaPrima

    @property
    def _schema_out(self) -> Type[MateriaPrimaInDB]:
        return MateriaPrimaInDB

    async def create_materia_prima(self, materia_prima: MateriaPrima) -> MateriaPrimaInDB:
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import CREATE_MATERIA_PRIMA

        materia_prima_id = str(uuid.uuid4())
        current_time = datetime.now()
        materia_prima.nombre = materia_prima.nombre.upper()
        materia_prima.codigo = materia_prima.codigo.upper()

        values = {
            "id": materia_prima_id,
            "nombre": materia_prima.nombre,
            "codigo": materia_prima.codigo,
            "created_at": current_time,
            "updated_at": current_time
        }

        try:
            record = await self.db.fetch_one(query=CREATE_MATERIA_PRIMA, values=values)
        except Exception as e:
            raise MateriaPrimaExceptions.MateriaPrimaCreationException()

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_materia_prima_by_code(self, codigo: str) -> MateriaPrimaInDB:
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import GET_MATERIA_PRIMA_BY_CODE
        values = {"codigo": codigo}
        record = await self.db.fetch_one(query=GET_MATERIA_PRIMA_BY_CODE, values=values)
        if not record:
            raise MateriaPrimaExceptions.MateriaPrimaNotFoundException()
        return self._schema_out(**dict(record))

    async def update_materia_prima_by_code(self, codigo: str, materia_prima_update: MateriaPrima) -> MateriaPrimaInDB:
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import UPDATE_MATERIA_PRIMA_BY_CODE

        updated_values = {
            "nombre": materia_prima_update.nombre.upper() if materia_prima_update.nombre else None,
            "codigo": codigo.upper(),
            "updated_at": datetime.now()
        }

        try:
            record = await self.db.fetch_one(query=UPDATE_MATERIA_PRIMA_BY_CODE, values=updated_values)
            return self._schema_out(**dict(record))
        except Exception as e:
            raise MateriaPrimaExceptions.MateriaPrimaUpdateException()

    async def delete_materia_prima_by_code(self, codigo: str):
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import DELETE_MATERIA_PRIMA_BY_CODE
        try:
            await self.db.execute(query=DELETE_MATERIA_PRIMA_BY_CODE, values={"codigo": codigo.upper()})
        except Exception as e:
            raise MateriaPrimaExceptions.MateriaPrimaDeletionException()
        return True

    async def get_all_materias_primas(self) -> List[MateriaPrimaInDB]:
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import LIST_MATERIAS_PRIMAS

        try:
            records = await self.db.fetch_all(query=LIST_MATERIAS_PRIMAS)
            return [self._schema_out(**dict(record)) for record in records]
        except Exception as e:
            raise MateriaPrimaExceptions.MateriaPrimaListException        