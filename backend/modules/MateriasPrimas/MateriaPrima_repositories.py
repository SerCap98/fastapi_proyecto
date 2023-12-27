
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

        values = {
            "id": materia_prima_id,
            "nombre": materia_prima.nombre,
            "cantidad": materia_prima.cantidad,
            "unidad_medida": materia_prima.unidad_medida,
            "created_at": current_time,
            "updated_at": current_time
        }

        try:
            record = await self.db.fetch_one(query=CREATE_MATERIA_PRIMA, values=values)
        except Exception as e:
            # Manejo del error
            raise MateriaPrimaExceptions.MateriaPrimaCreationException()

        result = record_to_dict(record)
        return self._schema_out(**result)

    async def get_materia_prima_by_id(self, id: UUID) -> MateriaPrimaInDB:
        from modules.MateriasPrimas.MateriaPrima_sqlstaments import GET_MATERIA_PRIMA_BY_ID
        values = {"id": id}
        record = await self.db.fetch_one(query=GET_MATERIA_PRIMA_BY_ID, values=values)
        if not record:
            raise MateriaPrimaExceptions.MateriaPrimaNotFoundException()
        return self._schema_out(**dict(record))

