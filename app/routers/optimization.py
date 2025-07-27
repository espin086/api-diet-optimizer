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


@router.post(
    "/optimize", 
    response_model=OptimizationResult,
    summary="Optimize Diet with Linear Programming",
    description="""
    ## 🎯 Diet Optimization Endpoint
    
    Solves the classic **Diet Problem** using linear programming to find the minimum-cost 
    combination of foods that meets all specified nutritional requirements.
    
    ### 📊 Supported Nutrients (12 total)
    
    **Macronutrients (grams):**
    - Calories, Protein, Carbohydrates, Fat
    
    **Vitamins & Minerals:**
    - **Vitamin A** (⚠️ **mcg RAE** - micrograms!)
    - **Vitamin C, Calcium, Iron, Magnesium, Potassium, Sodium, Cholesterol** (all in **mg**)
    
    ### ⚠️ Critical Unit Requirements
    
    **ATTENTION**: Vitamin A is measured in **micrograms (mcg RAE)**, all other nutrients in **milligrams (mg)**.
    
    | Nutrient | Correct Unit | Example Value | Common Mistake |
    |----------|--------------|---------------|----------------|
    | Vitamin A | **mcg RAE** | `469` (spinach) | Using mg: `0.469` ❌ |
    | Vitamin C | **mg** | `28.1` (spinach) | Using mcg: `28100` ❌ |
    | Calcium | **mg** | `99` (spinach) | Using g: `0.099` ❌ |
    
    ### 🍎 Example Request Body
    
    ```json
    {
      "foods": [
        {
          "name": "Spinach",
          "cost_per_100g": 2.40,
          "calories_per_100g": 23,
          "carbs_per_100g": 3.6,
          "protein_per_100g": 2.9,
          "fat_per_100g": 0.4,
          "vitamin_a_per_100g": 469,      // mcg RAE ⚠️
          "vitamin_c_per_100g": 28.1,     // mg
          "calcium_per_100g": 99,         // mg
          "iron_per_100g": 2.7,           // mg
          "magnesium_per_100g": 83,       // mg
          "potassium_per_100g": 558,      // mg
          "sodium_per_100g": 79,          // mg
          "cholesterol_per_100g": 0       // mg
        }
      ],
      "constraints": {
        "min_calories": 1800, "max_calories": 2200,
        "min_protein": 120, "max_protein": 180,
        "min_carbs": 150, "max_carbs": 250,
        "min_fat": 50, "max_fat": 80,
        "min_vitamin_a": 700,      // mcg RAE ⚠️
        "max_vitamin_a": 3000,     // mcg RAE ⚠️
        "min_vitamin_c": 75,       // mg
        "max_vitamin_c": 2000,     // mg
        "min_calcium": 1000,       // mg
        "max_calcium": 2500,       // mg
        "min_iron": 8,             // mg
        "max_iron": 45,            // mg
        "min_magnesium": 310,      // mg
        "max_magnesium": 800,      // mg
        "min_potassium": 3500,     // mg
        "max_potassium": 10000,    // mg
        "min_sodium": 1500,        // mg
        "max_sodium": 2300,        // mg
        "min_cholesterol": 0,      // mg
        "max_cholesterol": 300     // mg
      }
    }
    ```
    
    ### 📈 Response Format
    
    Returns optimal food quantities, total cost, nutritional summary, and constraint satisfaction status.
    
    ### 🔍 Optimization Status
    
    - **optimal**: Solution found with minimum cost
    - **infeasible**: No combination of foods can meet all constraints
    - **unbounded**: Cost can be reduced indefinitely (indicates problem formulation error)
    
    ### 💡 Tips for Success
    
    1. **Units**: Double-check Vitamin A is in mcg, others in mg
    2. **Constraints**: Use realistic RDA values (see API docs for reference table)
    3. **Food Variety**: Include diverse foods to increase feasibility
    4. **Bounds**: Ensure max > min for all constraints
    
    ### 🏥 Common Use Cases
    
    - Personal diet planning with cost optimization
    - Institutional meal planning (hospitals, schools)
    - Nutritional research and analysis
    - Athletic nutrition optimization
    - Pregnancy and special dietary needs
    """,
    responses={
        200: {
            "description": "Successful optimization",
            "content": {
                "application/json": {
                    "example": {
                        "status": "optimal",
                        "total_cost": 12.45,
                        "optimal_quantities": [
                            {
                                "food_name": "Chicken Breast",
                                "quantity_100g": 1.5,
                                "quantity_grams": 150.0,
                                "cost": 4.80
                            }
                        ],
                        "nutritional_summary": {
                            "total_calories": 2000.0,
                            "total_protein": 150.0,
                            "total_carbs": 200.0,
                            "total_fat": 65.0,
                            "total_vitamin_a": 800.0,
                            "total_vitamin_c": 90.0,
                            "total_calcium": 1200.0,
                            "total_iron": 15.0,
                            "total_magnesium": 350.0,
                            "total_potassium": 4000.0,
                            "total_sodium": 2000.0,
                            "total_cholesterol": 250.0
                        },
                        "constraint_satisfaction": {
                            "calories_within_bounds": True,
                            "protein_within_bounds": True,
                            "carbs_within_bounds": True,
                            "fat_within_bounds": True,
                            "vitamin_a_within_bounds": True,
                            "vitamin_c_within_bounds": True,
                            "calcium_within_bounds": True,
                            "iron_within_bounds": True,
                            "magnesium_within_bounds": True,
                            "potassium_within_bounds": True,
                            "sodium_within_bounds": True,
                            "cholesterol_within_bounds": True
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid input or optimization error",
            "content": {
                "application/json": {
                    "example": {
                        "error": "optimization_error",
                        "message": "Constraints are inconsistent",
                        "details": "max_calories must be greater than min_calories"
                    }
                }
            }
        },
        408: {
            "description": "Solver timeout",
            "content": {
                "application/json": {
                    "example": {
                        "error": "solver_timeout",
                        "message": "Optimization timed out after 30 seconds",
                        "timeout": 30
                    }
                }
            }
        }
    }
)
async def optimize_diet(
    request: OptimizationRequest,
    optimizer: DietOptimizer = Depends(get_optimizer)
) -> OptimizationResult:
    """
    🎯 **Optimize Diet with Linear Programming**
    
    Find the minimum-cost combination of foods that meets all nutritional requirements.
    
    **⚠️ CRITICAL**: Vitamin A uses **mcg RAE**, all other nutrients use **mg**.
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
                "total_magnesium": 0.0,
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
                "magnesium_within_bounds": False,
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
                "total_magnesium": 0.0,
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
                "magnesium_within_bounds": False,
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


@router.get(
    "/health", 
    response_model=HealthCheckResponse,
    summary="API Health Check",
    description="""
    ## 🏥 Health Check Endpoint
    
    Verify that the Diet Optimizer API is running and responsive.
    
    ### ✅ What This Checks
    - API server status
    - Basic functionality  
    - Version information
    
    ### 📊 Response Format
    - **status**: "healthy" if API is operational
    - **version**: Current API version
    - **message**: Status description
    
    ### 🔍 Use Cases
    - Application monitoring
    - Load balancer health checks
    - Service discovery
    - Debugging connectivity issues
    """
)
async def health_check() -> HealthCheckResponse:
    """
    🏥 **API Health Check**
    
    Verify API status and connectivity.
    """
    return HealthCheckResponse(
        status="healthy",
        version=settings.app_version,
        message="Diet Optimizer API is running successfully"
    )


@router.get(
    "/",
    summary="API Information",
    description="""
    ## ℹ️ Root Endpoint
    
    Provides basic information about the Diet Optimizer API including available endpoints.
    
    ### 🔗 Available Endpoints
    - **POST /optimize**: Main optimization endpoint
    - **GET /health**: Health check
    - **GET /docs**: Interactive API documentation (Swagger UI)
    - **GET /redoc**: Alternative API documentation (ReDoc)
    """
)
async def root():
    """
    ℹ️ **API Information**
    
    Basic API details and available endpoints.
    """
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "status": "running",
        "description": "Enhanced Diet Optimizer API with 12 essential nutrients",
        "endpoints": {
            "optimize": "/optimize",
            "health": "/health",
            "docs": "/docs",
            "redoc": "/redoc"
        },
        "features": [
            "Linear programming optimization",
            "12 comprehensive nutrients",
            "USDA-compatible units",
            "Multiple diet profiles",
            "Constraint validation"
        ],
        "critical_info": {
            "vitamin_a_unit": "mcg RAE (micrograms)",
            "other_nutrients_unit": "mg (milligrams)",
            "note": "Pay attention to units to avoid optimization errors"
        }
    }