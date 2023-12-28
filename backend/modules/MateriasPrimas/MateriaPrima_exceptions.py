from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class MateriaPrimaExceptions:
    class MateriaPrimaCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)
    class MateriaPrimaDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaSearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Materia prima no encontrada"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = f"Parámetros de actualización inválidos para materia prima: {str(e)}"
            AppExceptionCase.__init__(self, status_code, msg)
    class MateriaPrimaInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = f"Parámetros de creacion inválidos para materia prima: {str(e)}"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de materias primas"
            AppExceptionCase.__init__(self, status_code, msg)

    class MateriaPrimaInvalidUUIDException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "UUID Invalido"
            AppExceptionCase.__init__(self, status_code, msg)
