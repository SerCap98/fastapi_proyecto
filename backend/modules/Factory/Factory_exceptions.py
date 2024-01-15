from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class FactoryExceptions:
    class FactoryCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando fábrica"
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando fábrica"
            AppExceptionCase.__init__(self, status_code, msg)
    class FactoryDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando fábrica"
            AppExceptionCase.__init__(self, status_code, msg)

    class FactorySearchException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error buscando fábrica"
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Fábrica no encontrada"
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class FactoryInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de fábricas"
            AppExceptionCase.__init__(self, status_code, msg)
