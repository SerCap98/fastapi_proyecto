from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class RawMaterialOrderExceptions:

    class RawMaterialOrderException(AppExceptionCase):
        def __init__(self, msg: str = "",e: Any = None):
            status_code = 500
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialOrderNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Entry not found"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialOrderDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error deleting record"
            AppExceptionCase.__init__(self, status_code, msg)
    class RawMaterialOrderUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error updating record"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialOrderCreateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creating record"
            AppExceptionCase.__init__(self, status_code, msg)
    class RawMaterialOrderListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Could not retrieve list"
            AppExceptionCase.__init__(self, status_code, msg)

    class RawMaterialOrderInvalidUpdateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)
    class RawMaterialOrderInvalidCreateParamsException(AppExceptionCase):
        def __init__(self, msg: str = "", e: Any = None):
            status_code = 422
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

