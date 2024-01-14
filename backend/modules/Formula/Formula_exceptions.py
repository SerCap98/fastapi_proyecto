from typing import Any

from shared.utils.app_exceptions import AppExceptionCase

class FormulaExceptions:

    class FormulaException(AppExceptionCase):
        def __init__(self, msg: str = "",e: Any = None):
            status_code = 500
            msg = str(e)
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaNotFoundException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 404
            msg = "Entry not found"
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaDeleteException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Error deleting record"
            AppExceptionCase.__init__(self, status_code, msg)

    class FormulaListException(AppExceptionCase):
        def __init__(self, msg: str = ""):
            status_code = 500
            msg = "Could not retrieve list"
            AppExceptionCase.__init__(self, status_code, msg)
