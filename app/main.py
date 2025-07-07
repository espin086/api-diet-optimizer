"""Main FastAPI application for the Diet Optimizer API."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from app.core.config import settings
from app.core.exceptions import (
    OptimizationError,
    optimization_exception_handler,
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from app.routers import optimization


# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"Debug mode: {settings.debug}")
    
    yield
    
    # Shutdown
    logger.info(f"Shutting down {settings.app_name}")


# Create FastAPI application
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    # Diet Optimizer API
    
    A comprehensive FastAPI implementation that solves the classic **Diet Problem** from linear programming 
    and optimization theory. This enhanced API uses linear programming to find the optimal combination 
    of foods that meets specified nutritional requirements while minimizing total cost.
    
    ## 🍎 Enhanced Nutritional Coverage
    
    This API now supports **11 essential nutrients** for comprehensive diet optimization:
    
    ### Macronutrients (grams)
    - **Calories** - Total energy content
    - **Protein** - Muscle building and repair
    - **Carbohydrates** - Primary energy source  
    - **Fat** - Essential fatty acids and energy storage
    
    ### Vitamins & Minerals
    - **Vitamin A** - Eye health, immune function (⚠️ **mcg RAE**)
    - **Vitamin C** - Antioxidant, immune support (**mg**)
    - **Calcium** - Bone health, muscle function (**mg**)
    - **Iron** - Oxygen transport, energy metabolism (**mg**)
    - **Potassium** - Heart health, muscle function (**mg**)
    - **Sodium** - Fluid balance, nerve function (**mg**)
    - **Cholesterol** - Cardiovascular health monitoring (**mg**)
    
    ## ⚠️ Critical Unit Information
    
    **IMPORTANT**: Pay attention to nutrient units to avoid errors:
    
    | Nutrient | Unit | Example Value |
    |----------|------|---------------|
    | **Vitamin A** | **mcg RAE** | `469` (spinach) |
    | **All Others** | **mg** | `28.1` (vitamin C in spinach) |
    
    > **Vitamin A is the ONLY nutrient measured in micrograms (mcg)**. All other nutrients use milligrams (mg).
    
    ## 🚀 Key Features
    
    - **🎯 Linear Programming Optimization**: Uses SciPy's HiGHS algorithm for guaranteed optimal solutions
    - **📊 Comprehensive Validation**: Pydantic models ensure data integrity and proper units
    - **🔧 Flexible Constraints**: Support for min/max bounds on all 11 nutrients
    - **📈 Detailed Results**: Complete nutritional breakdown, cost analysis, and constraint satisfaction
    - **🛡️ Robust Error Handling**: Proper handling of infeasible and unbounded problems
    - **🏥 Health-focused**: Supports various dietary profiles (pregnancy, heart-healthy, athletic)
    - **📋 USDA Compatible**: Units follow USDA FoodData Central standards
    
    ## 📝 Quick Start Guide
    
    1. **Prepare Food Data**: Ensure all nutrients use correct units (see examples below)
    2. **Set Constraints**: Use realistic daily values based on RDA guidelines  
    3. **POST to `/optimize`**: Get optimal diet solution with costs and quantities
    4. **Validate Results**: Check constraint satisfaction and nutritional summary
    5. **Monitor Health**: Use `/health` endpoint for API status
    
    ## 🍽️ Example Food Item (Correct Units)
    
    ```json
    {
      "name": "Salmon Fillet",
      "cost_per_100g": 6.50,
      "calories_per_100g": 208,
      "carbs_per_100g": 0,
      "protein_per_100g": 25.4,
      "fat_per_100g": 12.4,
      "vitamin_a_per_100g": 58,     // mcg RAE ⚠️
      "vitamin_c_per_100g": 0,      // mg
      "calcium_per_100g": 12,       // mg  
      "iron_per_100g": 0.8,         // mg
      "potassium_per_100g": 490,    // mg
      "sodium_per_100g": 59,        // mg
      "cholesterol_per_100g": 70    // mg
    }
    ```
    
    ## 📊 RDA Reference Values
    
    | Nutrient | Adult RDA/AI | Upper Limit | Units |
    |----------|--------------|-------------|-------|
    | Calories | 1800-2400 | 3000+ | kcal |
    | Protein | 46-56 | 200+ | g |
    | Vitamin A | **700-900** | **3000** | **mcg RAE** |
    | Vitamin C | **65-90** | **2000** | **mg** |
    | Calcium | **1000-1200** | **2500** | **mg** |
    | Iron | **8-18** | **45** | **mg** |
    | Potassium | **3500-4700** | **10000** | **mg** |
    | Sodium | **1500** | **2300** | **mg** |
    
    ## 🧮 Optimization Algorithm
    
    The API formulates the diet problem as a linear programming problem:
    
    **Objective Function:**
    ```
    Minimize: Σ(cost_per_100g[i] × quantity[i]) for all foods i
    ```
    
    **Subject to Constraints:**
    ```
    min_nutrient ≤ Σ(nutrient_per_100g[i] × quantity[i]) ≤ max_nutrient
    for all 11 nutrients and all foods i
    quantity[i] ≥ 0 for all foods i
    ```
    
    **Solver**: HiGHS algorithm via SciPy (state-of-the-art linear programming)
    
    ## 🎯 Specialized Diet Profiles
    
    The API supports optimization for various dietary needs:
    - **👨‍⚕️ Standard Adult**: General healthy eating guidelines
    - **🤰 Pregnancy**: Higher iron, calcium, and vitamin requirements  
    - **❤️ Heart-Healthy**: Low sodium, low cholesterol, high potassium
    - **🏃‍♂️ Athletic**: High protein, balanced macronutrients
    - **⚖️ Weight Management**: Calorie-controlled with nutrient density
    
    ## 🔗 Additional Resources
    
    - **Nutrient Units Guide**: See `NUTRIENT_UNITS_REFERENCE.md` for comprehensive unit documentation
    - **Example Usage**: Check `example_usage.py` for complete implementation examples
    - **Health Endpoints**: Use `/health` for API monitoring and status checks
    
    ---
    
    **🏗️ Built with**: FastAPI, Pydantic, SciPy, NumPy | **📊 Data Standards**: USDA FoodData Central
    """,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=settings.cors_allow_credentials,
    allow_methods=settings.cors_allow_methods,
    allow_headers=settings.cors_allow_headers,
)

# Add exception handlers
app.add_exception_handler(OptimizationError, optimization_exception_handler)
app.add_exception_handler(ValidationError, validation_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Include routers
app.include_router(optimization.router, tags=["optimization"])

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower()
    )