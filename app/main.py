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
    A FastAPI implementation that solves the classic **Diet Problem** from linear programming 
    and optimization theory. This API uses linear programming to find the optimal combination 
    of foods that meets specified nutritional requirements while minimizing total cost.
    
    ## Features
    
    - **Linear Programming Optimization**: Uses SciPy's optimization algorithms
    - **Comprehensive Validation**: Pydantic models ensure data integrity
    - **Flexible Constraints**: Support for min/max bounds on all macronutrients
    - **Detailed Results**: Complete nutritional breakdown and cost analysis
    - **Error Handling**: Proper handling of infeasible and unbounded problems
    
    ## Quick Start
    
    1. POST your food list and constraints to `/optimize`
    2. Get the optimal diet solution with costs and quantities
    3. Check API health with `/health`
    
    ## Optimization Algorithm
    
    The API formulates the diet problem as a linear programming problem:
    
    - **Objective**: Minimize total food cost
    - **Variables**: Quantities of each food (in 100g units)
    - **Constraints**: Nutritional requirements (calories, protein, carbs, fat)
    - **Solver**: HiGHS algorithm via SciPy
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