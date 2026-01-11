"""Custom exceptions for amrkt library."""


class MarketError(Exception):
    """Base exception for all market errors."""
    pass


class AuthenticationError(MarketError):
    """Raised when authentication fails or token is invalid."""
    pass


class APIError(MarketError):
    """Raised when API returns an error response."""
    
    def __init__(self, message: str, status_code: int = None, response_text: str = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_text = response_text


class NotFoundError(MarketError):
    """Raised when a resource (gift, user, etc.) is not found."""
    pass


class NotForSaleError(MarketError):
    """Raised when trying to buy a gift that is not for sale."""
    pass


class InsufficientBalanceError(MarketError):
    """Raised when balance is not enough for the operation."""
    pass
