from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class ProductExceptions:
    class ProductCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando producto"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando producto"
            AppExceptionCase.__init__(self, status_code, msg)
    class ProductDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando producto"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductSearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando producto"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Producto no encontrado"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class ProductInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de productos"
            AppExceptionCase.__init__(self, status_code, msg)

    class ProductInvalidUUIDException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 422
            msg = "UUID Invalido"
            AppExceptionCase.__init__(self, status_code, msg)
