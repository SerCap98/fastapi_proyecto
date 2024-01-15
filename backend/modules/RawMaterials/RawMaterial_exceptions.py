from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class RawMaterialExceptions:
    class RawMaterialCreationException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error actualizando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)
    class RawMaterialDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error eliminando materia prima"
            AppExceptionCase.__init__(self, status_code, msg)


    class RawMaterialNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Materia prima no encontrada"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class RawMaterialInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "No se pudo recuperar la lista de materias primas"
            AppExceptionCase.__init__(self, status_code, msg)

