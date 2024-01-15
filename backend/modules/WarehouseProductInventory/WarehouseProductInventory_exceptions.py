from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class WarehouseProductInventoryExceptions:
    class WarehouseProductInventoryCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando registro"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseProductInventoryUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando registro"
            AppExceptionCase.__init__(self, status_code, msg)
    class WarehouseProductInventoryDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando registro"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseProductInventorySearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando registro"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseProductInventoryNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "registro no encontrado"
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseProductInventoryInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class WarehouseProductInventoryInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class WarehouseProductInventoryListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de registros"
            AppExceptionCase.__init__(self, status_code, msg)

