from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class WarehouseExceptions:
    class WarehouseCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando almacén"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando almacén"
            AppExceptionCase.__init__(self, status_code, msg)
    class WarehouseDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando almacén"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseSearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando almacén"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Almacén no encontrado"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class WarehouseInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de almacenes"
            AppExceptionCase.__init__(self, status_code, msg)

