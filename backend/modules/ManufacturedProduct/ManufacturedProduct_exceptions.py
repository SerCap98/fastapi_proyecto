from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class ManufacturedProductExceptions:
    class ManufacturedProductCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando producto manufacturado"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando producto manufacturado"
            AppExceptionCase.__init__(self, status_code, msg)
    class ManufacturedProductDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando producto manufacturado"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductSearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando producto manufacturado"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Producto manufacturado no encontrado"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class ManufacturedProductInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de productos manufacturados"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductInvalidUUIDException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "UUID Invalido"
            AppExceptionCase.__init__(self, status_code, msg)
