class AppException(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)


class UnauthorizedException(AppException):
    def __init__(self, detail: str = "Invalid credentials"):
        super().__init__(detail=detail, status_code=401)


class ForbiddenException(AppException):
    def __init__(self, detail: str = "Access denied"):
        super().__init__(detail=detail, status_code=403)


class NotFoundException(AppException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail=detail, status_code=404)


class ConflictException(AppException):
    def __init__(self, detail: str = "Data conflict"):
        super().__init__(detail=detail, status_code=409)


class BudgetExceededException(AppException):
    def __init__(self, category: str, limit: float, spent: float):
        self.category = category
        self.limit = limit
        self.spent = spent
        detail = (
            f"Attention! The limit for category '{category}' has been exceeded: "
            f"limit {limit:.2f}, spent {spent:.2f}"
        )
        super().__init__(detail=detail, status_code=200)
