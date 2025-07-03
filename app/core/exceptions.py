"""Custom exception handlers for the Diet Optimizer API."""

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import logging


logger = logging.getLogger(__name__)


class OptimizationError(Exception):
    """Custom exception for optimization-related errors."""
    
    def __init__(self, message: str, details: str | None = None):
        self.message = message
        self.details = details
        super().__init__(self.message)


class InfeasibleProblemError(OptimizationError):
    """Exception raised when the optimization problem is infeasible."""
    
    def __init__(self, message: str = "No solution exists that satisfies all constraints"):
        super().__init__(message)


class UnboundedProblemError(OptimizationError):
    """Exception raised when the optimization problem is unbounded."""
    
    def __init__(self, message: str = "The optimization problem is unbounded"):
        super().__init__(message)


class SolverTimeoutError(OptimizationError):
    """Exception raised when the solver times out."""
    
    def __init__(self, timeout: int):
        message = f"Solver timed out after {timeout} seconds"
        super().__init__(message)


async def optimization_exception_handler(request: Request, exc: OptimizationError) -> JSONResponse:
    """Handle optimization-related exceptions."""
    logger.error(f"Optimization error: {exc.message}")
    return JSONResponse(
        status_code=400,
        content={
            "error": "optimization_error",
            "message": exc.message,
            "details": exc.details
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """Handle Pydantic validation errors."""
    logger.error(f"Validation error: {exc}")
    return JSONResponse(
        status_code=422,
        content={
            "error": "validation_error",
            "message": "Invalid input data",
            "details": exc.errors()
        }
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """Handle HTTP exceptions."""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle general exceptions."""
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred",
            "details": str(exc) if logger.level <= logging.DEBUG else None
        }
    )