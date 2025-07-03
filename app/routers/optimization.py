"""API routers for the Diet Optimizer."""

from fastapi import APIRouter, HTTPException, Depends
import logging

from app.models.request import OptimizationRequest
from app.models.response import OptimizationResult, HealthCheckResponse
from app.services.optimizer import DietOptimizer
from app.core.exceptions import (
    OptimizationError,
    InfeasibleProblemError,
    UnboundedProblemError,
    SolverTimeoutError
)
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


def get_optimizer() -> DietOptimizer:
    """Dependency injection for the optimizer service."""
    return DietOptimizer()


@router.post("/optimize", response_model=OptimizationResult)
async def optimize_diet(
    request: OptimizationRequest,
    optimizer: DietOptimizer = Depends(get_optimizer)
) -> OptimizationResult:
    """
    Optimize diet based on food options and nutritional constraints.
    
    This endpoint solves the classic Diet Problem using linear programming
    to find the minimum-cost combination of foods that meets all specified
    nutritional requirements.
    
    Args:
        request: OptimizationRequest containing foods and constraints
        optimizer: DietOptimizer service (injected)
    
    Returns:
        OptimizationResult: The optimal solution with costs and quantities
        
    Raises:
        HTTPException: If optimization fails or inputs are invalid
    """
    try:
        logger.info(f"Received optimization request with {len(request.foods)} foods")
        
        # Perform optimization
        result = optimizer.optimize(request.foods, request.constraints)
        
        logger.info(f"Optimization completed successfully. Status: {result.status}")
        return result
        
    except InfeasibleProblemError as e:
        logger.warning(f"Infeasible problem: {e.message}")
        return OptimizationResult(
            status="infeasible",
            total_cost=0.0,
            optimal_quantities=[],
            nutritional_summary={
                "total_calories": 0.0,
                "total_protein": 0.0,
                "total_carbs": 0.0,
                "total_fat": 0.0,
                "total_vitamin_a": 0.0,
                "total_vitamin_c": 0.0,
                "total_calcium": 0.0,
                "total_iron": 0.0,
                "total_potassium": 0.0,
                "total_sodium": 0.0,
                "total_cholesterol": 0.0
            },
            constraint_satisfaction={
                "calories_within_bounds": False,
                "protein_within_bounds": False,
                "carbs_within_bounds": False,
                "fat_within_bounds": False,
                "vitamin_a_within_bounds": False,
                "vitamin_c_within_bounds": False,
                "calcium_within_bounds": False,
                "iron_within_bounds": False,
                "potassium_within_bounds": False,
                "sodium_within_bounds": False,
                "cholesterol_within_bounds": False
            }
        )
    
    except UnboundedProblemError as e:
        logger.warning(f"Unbounded problem: {e.message}")
        return OptimizationResult(
            status="unbounded",
            total_cost=0.0,
            optimal_quantities=[],
            nutritional_summary={
                "total_calories": 0.0,
                "total_protein": 0.0,
                "total_carbs": 0.0,
                "total_fat": 0.0,
                "total_vitamin_a": 0.0,
                "total_vitamin_c": 0.0,
                "total_calcium": 0.0,
                "total_iron": 0.0,
                "total_potassium": 0.0,
                "total_sodium": 0.0,
                "total_cholesterol": 0.0
            },
            constraint_satisfaction={
                "calories_within_bounds": False,
                "protein_within_bounds": False,
                "carbs_within_bounds": False,
                "fat_within_bounds": False,
                "vitamin_a_within_bounds": False,
                "vitamin_c_within_bounds": False,
                "calcium_within_bounds": False,
                "iron_within_bounds": False,
                "potassium_within_bounds": False,
                "sodium_within_bounds": False,
                "cholesterol_within_bounds": False
            }
        )
    
    except SolverTimeoutError as e:
        logger.error(f"Solver timeout: {e.message}")
        raise HTTPException(
            status_code=408,
            detail={
                "error": "solver_timeout",
                "message": e.message,
                "timeout": settings.solver_timeout
            }
        )
    
    except OptimizationError as e:
        logger.error(f"Optimization error: {e.message}")
        raise HTTPException(
            status_code=400,
            detail={
                "error": "optimization_error",
                "message": e.message,
                "details": e.details
            }
        )
    
    except Exception as e:
        logger.exception(f"Unexpected error during optimization: {e}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "internal_server_error",
                "message": "An unexpected error occurred during optimization"
            }
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check() -> HealthCheckResponse:
    """
    Health check endpoint to verify API status.
    
    Returns:
        HealthCheckResponse: API status information
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        message="Diet Optimizer API is running successfully"
    )


@router.get("/")
async def root():
    """Root endpoint with basic API information."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "docs_url": "/docs",
        "health_url": "/health",
        "optimize_url": "/optimize"
    }