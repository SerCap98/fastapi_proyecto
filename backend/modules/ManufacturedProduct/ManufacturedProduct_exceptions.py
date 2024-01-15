from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class ManufacturedProductExceptions:

    class ManufacturedProductException(AppExceptionCase):
        def __init__(self, msg: str = "",e: Any = None):
            status_code = 500
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductCreateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error creating record"
            AppExceptionCase.__init__(self, status_code, msg)
    class ManufacturedProductNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Entry not found"
            AppExceptionCase.__init__(self, status_code, msg)

    class ManufacturedProductDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error deleting record"
            AppExceptionCase.__init__(self, status_code, msg)


    class ManufacturedProductUpdateException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error updating record"
            AppExceptionCase.__init__(self, status_code, msg)  
    class ManufacturedProductListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Could not retrieve list"
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
