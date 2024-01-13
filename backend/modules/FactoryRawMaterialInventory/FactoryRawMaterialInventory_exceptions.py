from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class FactoryRawMaterialInventoryExceptions:

    class FactoryRawMaterialException(AppExceptionCase):
        def __init__(self, msg: str = "",e: Any = None):
            status_code = 500
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryRawMaterialNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Entry not found"
            AppExceptionCase.__init__(self, status_code, msg)

    class FactoryRawMaterialDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error deleting record"
            AppExceptionCase.__init__(self, status_code, msg)

