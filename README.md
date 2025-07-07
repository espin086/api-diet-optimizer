# Diet Optimizer API

A FastAPI implementation that solves the classic **Diet Problem** from linear programming and optimization theory. This API uses linear programming to find the optimal combination of foods that meets specified nutritional requirements while minimizing total cost.

## Problem Description

The Diet Problem is a fundamental optimization challenge where the goal is to determine the minimum-cost combination of foods that satisfies specific nutritional constraints. This enhanced API optimizes **11 key nutrients**:

### Macronutrients (measured in grams)
- **Calories** - Total energy content
- **Protein** - Essential for muscle building and repair  
- **Carbohydrates** - Primary energy source
- **Fat** - Essential fatty acids and energy storage

### Vitamins & Minerals
- **Vitamin A** - Eye health, immune function (measured in **mcg RAE**)
- **Vitamin C** - Antioxidant, immune support (measured in **mg**)
- **Calcium** - Bone health, muscle function (measured in **mg**)
- **Iron** - Oxygen transport, energy metabolism (measured in **mg**)
- **Potassium** - Heart health, muscle function (measured in **mg**)
- **Sodium** - Fluid balance, nerve function (measured in **mg**)
- **Cholesterol** - Cardiovascular health monitoring (measured in **mg**)

> **Important Unit Note**: Most nutrients are measured in milligrams (mg), except for **Vitamin A** which uses micrograms RAE (mcg RAE - Retinol Activity Equivalents). This follows standard USDA nutritional labeling conventions.

## How It Works

The API accepts a list of available foods with their comprehensive nutritional profiles and cost information, along with the desired nutritional constraints (minimum and maximum values for each nutrient). It then formulates and solves a linear programming optimization problem to find the lowest-cost food combination that meets all specified requirements.

### Mathematical Formulation

**Objective Function:** Minimize total cost
```
Minimize: Σ(cost_per_100g[i] × quantity[i]) for all foods i
```

**Subject to constraints:**
```
min_calories ≤ Σ(calories_per_100g[i] × quantity[i]) ≤ max_calories
min_protein ≤ Σ(protein_per_100g[i] × quantity[i]) ≤ max_protein
min_carbs ≤ Σ(carbs_per_100g[i] × quantity[i]) ≤ max_carbs
min_fat ≤ Σ(fat_per_100g[i] × quantity[i]) ≤ max_fat
min_vitamin_a ≤ Σ(vitamin_a_per_100g[i] × quantity[i]) ≤ max_vitamin_a
min_vitamin_c ≤ Σ(vitamin_c_per_100g[i] × quantity[i]) ≤ max_vitamin_c
min_calcium ≤ Σ(calcium_per_100g[i] × quantity[i]) ≤ max_calcium
min_iron ≤ Σ(iron_per_100g[i] × quantity[i]) ≤ max_iron
min_potassium ≤ Σ(potassium_per_100g[i] × quantity[i]) ≤ max_potassium
min_sodium ≤ Σ(sodium_per_100g[i] × quantity[i]) ≤ max_sodium
min_cholesterol ≤ Σ(cholesterol_per_100g[i] × quantity[i]) ≤ max_cholesterol
quantity[i] ≥ 0 for all foods i
```

## API Specification

### Input Format

The API accepts JSON input with the following structure:

#### Foods List
Each food item must contain comprehensive nutritional data:
```json
{
  "name": "string",                    // Name of the food item
  "cost_per_100g": "number",          // Cost per 100 grams (currency units)
  "calories_per_100g": "number",      // Calories per 100 grams
  "carbs_per_100g": "number",         // Carbohydrates per 100 grams (g)
  "protein_per_100g": "number",       // Protein per 100 grams (g)
  "fat_per_100g": "number",           // Fat per 100 grams (g)
  "vitamin_a_per_100g": "number",     // Vitamin A per 100 grams (mcg RAE)
  "vitamin_c_per_100g": "number",     // Vitamin C per 100 grams (mg)
  "calcium_per_100g": "number",       // Calcium per 100 grams (mg)
  "iron_per_100g": "number",          // Iron per 100 grams (mg)
  "potassium_per_100g": "number",     // Potassium per 100 grams (mg)
  "sodium_per_100g": "number",        // Sodium per 100 grams (mg)
  "cholesterol_per_100g": "number"    // Cholesterol per 100 grams (mg)
}
```

#### Nutritional Constraints
The API accepts upper and lower bounds for each nutrient:
```json
{
  "min_calories": "number",           // Minimum daily calories
  "max_calories": "number",           // Maximum daily calories
  "min_protein": "number",            // Minimum daily protein (g)
  "max_protein": "number",            // Maximum daily protein (g)
  "min_carbs": "number",              // Minimum daily carbs (g)
  "max_carbs": "number",              // Maximum daily carbs (g)
  "min_fat": "number",                // Minimum daily fat (g)
  "max_fat": "number",                // Maximum daily fat (g)
  "min_vitamin_a": "number",          // Minimum daily vitamin A (mcg RAE)
  "max_vitamin_a": "number",          // Maximum daily vitamin A (mcg RAE)
  "min_vitamin_c": "number",          // Minimum daily vitamin C (mg)
  "max_vitamin_c": "number",          // Maximum daily vitamin C (mg)
  "min_calcium": "number",            // Minimum daily calcium (mg)
  "max_calcium": "number",            // Maximum daily calcium (mg)
  "min_iron": "number",               // Minimum daily iron (mg)
  "max_iron": "number",               // Maximum daily iron (mg)
  "min_potassium": "number",          // Minimum daily potassium (mg)
  "max_potassium": "number",          // Maximum daily potassium (mg)
  "min_sodium": "number",             // Minimum daily sodium (mg)
  "max_sodium": "number",             // Maximum daily sodium (mg)
  "min_cholesterol": "number",        // Minimum daily cholesterol (mg)
  "max_cholesterol": "number"         // Maximum daily cholesterol (mg)
}
```

### Recommended Daily Values (RDA) Reference

Use these values as guidance for setting realistic constraints:

| Nutrient | Adult RDA/AI | Upper Limit | Units |
|----------|--------------|-------------|-------|
| Calories | 1800-2400 | 3000+ | kcal |
| Protein | 46-56g | 200g+ | g |
| Carbohydrates | 130g | 300g+ | g |
| Fat | 20-35% of calories | 100g+ | g |
| **Vitamin A** | **700-900** | **3000** | **mcg RAE** |
| **Vitamin C** | **65-90** | **2000** | **mg** |
| **Calcium** | **1000-1200** | **2500** | **mg** |
| **Iron** | **8-18** | **45** | **mg** |
| **Potassium** | **3500-4700** | **10000** | **mg** |
| **Sodium** | **1500** | **2300** | **mg** |
| **Cholesterol** | **0 (no requirement)** | **300** | **mg** |

### Complete Request Example
```json
{
  "foods": [
    {
      "name": "Chicken Breast (Skinless)",
      "cost_per_100g": 3.20,
      "calories_per_100g": 165,
      "carbs_per_100g": 0,
      "protein_per_100g": 31,
      "fat_per_100g": 3.6,
      "vitamin_a_per_100g": 9,        // mcg RAE
      "vitamin_c_per_100g": 0,        // mg
      "calcium_per_100g": 15,         // mg
      "iron_per_100g": 0.9,           // mg
      "potassium_per_100g": 256,      // mg
      "sodium_per_100g": 74,          // mg
      "cholesterol_per_100g": 85      // mg
    },
    {
      "name": "Spinach",
      "cost_per_100g": 2.40,
      "calories_per_100g": 23,
      "carbs_per_100g": 3.6,
      "protein_per_100g": 2.9,
      "fat_per_100g": 0.4,
      "vitamin_a_per_100g": 469,      // mcg RAE - Very high!
      "vitamin_c_per_100g": 28.1,     // mg
      "calcium_per_100g": 99,         // mg
      "iron_per_100g": 2.7,           // mg
      "potassium_per_100g": 558,      // mg
      "sodium_per_100g": 79,          // mg
      "cholesterol_per_100g": 0       // mg
    }
  ],
  "constraints": {
    "min_calories": 1800,
    "max_calories": 2200,
    "min_protein": 120,
    "max_protein": 180,
    "min_carbs": 150,
    "max_carbs": 250,
    "min_fat": 50,
    "max_fat": 80,
    "min_vitamin_a": 700,             // mcg RAE
    "max_vitamin_a": 3000,            // mcg RAE
    "min_vitamin_c": 75,              // mg
    "max_vitamin_c": 2000,            // mg
    "min_calcium": 1000,              // mg
    "max_calcium": 2500,              // mg
    "min_iron": 8,                    // mg
    "max_iron": 45,                   // mg
    "min_potassium": 3500,            // mg
    "max_potassium": 10000,           // mg
    "min_sodium": 1500,               // mg
    "max_sodium": 2300,               // mg
    "min_cholesterol": 0,             // mg
    "max_cholesterol": 300            // mg
  }
}
```

### Output Format

The API returns the optimal solution containing comprehensive nutritional analysis:
```json
{
  "status": "string",                    // "optimal", "infeasible", or "unbounded"
  "total_cost": "number",                // Minimum total cost achieved
  "optimal_quantities": [                // Quantities of each food
    {
      "food_name": "string",
      "quantity_100g": "number",         // Amount in 100-gram units
      "quantity_grams": "number",        // Total grams of this food
      "cost": "number"                   // Cost contribution of this food
    }
  ],
  "nutritional_summary": {               // Total nutritional content achieved
    "total_calories": "number",
    "total_protein": "number",           // g
    "total_carbs": "number",             // g
    "total_fat": "number",               // g
    "total_vitamin_a": "number",         // mcg RAE
    "total_vitamin_c": "number",         // mg
    "total_calcium": "number",           // mg
    "total_iron": "number",              // mg
    "total_potassium": "number",         // mg
    "total_sodium": "number",            // mg
    "total_cholesterol": "number"        // mg
  },
  "constraint_satisfaction": {           // Whether each constraint is met
    "calories_within_bounds": "boolean",
    "protein_within_bounds": "boolean",
    "carbs_within_bounds": "boolean",
    "fat_within_bounds": "boolean",
    "vitamin_a_within_bounds": "boolean",
    "vitamin_c_within_bounds": "boolean",
    "calcium_within_bounds": "boolean",
    "iron_within_bounds": "boolean",
    "potassium_within_bounds": "boolean",
    "sodium_within_bounds": "boolean",
    "cholesterol_within_bounds": "boolean"
  }
}
```

## Key Features

### Comprehensive Nutritional Analysis
- **11 Essential Nutrients**: Complete coverage of major vitamins, minerals, and macronutrients
- **Standard Units**: Follows USDA and international nutritional labeling standards
- **Constraint Validation**: Ensures all nutritional requirements are met within safe limits

### Specialized Diet Profiles
The API supports optimization for various dietary needs:
- **Standard Adult Diet**: General healthy eating guidelines
- **Pregnancy Nutrition**: Higher requirements for iron, calcium, and vitamins
- **Heart-Healthy Diet**: Low sodium, low cholesterol, high potassium
- **Athletic Performance**: High protein, balanced macronutrients
- **Weight Management**: Calorie-controlled with nutrient density

### Linear Programming Optimization
- **Guaranteed Optimal Solution**: Mathematical proof of minimum cost
- **Constraint Satisfaction**: All nutritional bounds are respected
- **Scalable**: Handles large food databases efficiently
- **Robust Error Handling**: Clear feedback for infeasible problems

## Technical Requirements

### Core Dependencies
- **FastAPI** - Web framework for building the API with automatic OpenAPI documentation
- **Pydantic** - Data validation, serialization, and settings management (fully integrated with FastAPI)
- **SciPy** or **PuLP** - Linear programming solver for optimization
- **NumPy** - Numerical computations and matrix operations
- **Poetry** - Python dependency management and packaging tool
- **pytest** - Testing framework for comprehensive API testing
- **Docker** - Containerization for consistent deployment environments

### Development Requirements
- **Python 3.8+** - Minimum Python version
- **Poetry** - Exclusive package manager for dependency management
- **Type Hints** - Full type annotation following PEP 484
- **Black** - Code formatting
- **isort** - Import sorting
- **mypy** - Static type checking
- **flake8** or **ruff** - Linting and code quality

### API Endpoints

#### `POST /optimize`
Main optimization endpoint that accepts the food list and constraints, then returns the optimal diet solution.

#### `GET /health`
Health check endpoint to verify API status.

#### `GET /docs`
Automatic Swagger/OpenAPI documentation (provided by FastAPI).

### Error Handling

The API should handle the following scenarios:
- **Infeasible Problem**: When no combination of foods can meet the specified constraints
- **Invalid Input**: When required fields are missing or contain invalid data types
- **Numerical Issues**: When the optimization algorithm encounters computational problems

### Performance Considerations

- Validate input data using Pydantic models
- Implement proper error responses with meaningful messages
- Support for problems with varying numbers of foods (scalable solution)
- Reasonable timeout handling for complex optimization problems

## FastAPI Best Practices

### Pydantic Integration
- **Request Models**: Create Pydantic models for all API input validation
- **Response Models**: Define Pydantic models for consistent API responses
- **Field Validation**: Use Pydantic validators for custom field validation (e.g., positive numbers, valid ranges)
- **Configuration**: Use Pydantic Settings for environment-based configuration management

### Code Structure
```
api-diet-optimizer/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models/              # Pydantic models
│   │   ├── __init__.py
│   │   ├── request.py       # Input models (Food, Constraints)
│   │   └── response.py      # Output models (OptimizationResult)
│   ├── routers/             # API route handlers
│   │   ├── __init__.py
│   │   └── optimization.py
│   ├── services/            # Business logic
│   │   ├── __init__.py
│   │   └── optimizer.py     # Linear programming logic
│   ├── core/                # Core configuration
│   │   ├── __init__.py
│   │   ├── config.py        # Pydantic Settings
│   │   └── exceptions.py    # Custom exception handlers
│   └── utils/               # Utility functions
│       ├── __init__.py
│       └── validators.py    # Custom Pydantic validators
├── tests/                   # pytest test suite
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml          # Poetry configuration
└── README.md
```

### API Best Practices
- **Dependency Injection**: Use FastAPI's dependency injection system
- **Exception Handling**: Implement custom exception handlers with proper HTTP status codes
- **Logging**: Structured logging with correlation IDs for request tracing
- **CORS**: Configure CORS appropriately for frontend integration
- **Rate Limiting**: Implement rate limiting for production deployment
- **Health Checks**: Comprehensive health check endpoints for monitoring

## Testing Strategy

### pytest Configuration
- **Test Structure**: Mirror the app structure in the `tests/` directory
- **Fixtures**: Use pytest fixtures for test data and API client setup
- **Parametrized Tests**: Test multiple scenarios with pytest.mark.parametrize
- **Async Testing**: Use pytest-asyncio for testing async FastAPI endpoints

### Test Coverage Areas
1. **Unit Tests**: Individual functions and business logic
2. **Integration Tests**: End-to-end API endpoint testing
3. **Edge Cases**: Invalid inputs, boundary conditions, infeasible problems
4. **Performance Tests**: Optimization algorithm performance with large datasets

### Example Test Structure
```python
# tests/test_optimization.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def sample_foods():
    return [
        {
            "name": "Chicken Breast",
            "cost_per_100g": 2.50,
            "calories_per_100g": 165,
            "carbs_per_100g": 0,
            "protein_per_100g": 31,
            "fat_per_100g": 3.6
        }
    ]

@pytest.fixture
def sample_constraints():
    return {
        "min_calories": 1800,
        "max_calories": 2200,
        "min_protein": 120,
        "max_protein": 180,
        "min_carbs": 150,
        "max_carbs": 250,
        "min_fat": 50,
        "max_fat": 80
    }

def test_valid_optimization(sample_foods, sample_constraints):
    response = client.post("/optimize", json={
        "foods": sample_foods,
        "constraints": sample_constraints
    })
    assert response.status_code == 200
    assert "total_cost" in response.json()
```

## Docker Deployment

### Dockerfile Requirements
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy Poetry files
COPY pyproject.toml poetry.lock ./

# Configure Poetry and install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy application code
COPY ./app ./app

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=production
    volumes:
      - ./app:/app/app:ro
    restart: unless-stopped
```

### Production Considerations
- **Multi-stage builds**: Separate build and runtime stages for smaller images
- **Non-root user**: Run container as non-root user for security
- **Health checks**: Include Docker health checks
- **Environment variables**: Use .env files for configuration
- **Logging**: Configure proper log aggregation

## Development Setup

### Poetry Configuration
The project uses Poetry for dependency management. The `pyproject.toml` should include:

```toml
[tool.poetry]
name = "api-diet-optimizer"
version = "0.1.0"
description = "FastAPI implementation of the diet optimization problem using linear programming"
authors = ["Your Name <your.email@example.com>"]

[tool.poetry.dependencies]
python = "^3.8"
fastapi = "^0.104.0"
uvicorn = {extras = ["standard"], version = "^0.24.0"}
pydantic = "^2.4.0"
scipy = "^1.11.0"
numpy = "^1.24.0"
pydantic-settings = "^2.0.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
httpx = "^0.25.0"
black = "^23.9.0"
isort = "^5.12.0"
mypy = "^1.6.0"
flake8 = "^6.1.0"
pytest-cov = "^4.1.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py38']

[tool.isort]
profile = "black"
multi_line_output = 3

[tool.mypy]
python_version = "3.8"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = "--cov=app --cov-report=html --cov-report=term-missing"
```

### Development Commands
```bash
# Install dependencies
poetry install

# Run the application
poetry run uvicorn app.main:app --reload

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=app

# Format code
poetry run black .
poetry run isort .

# Type checking
poetry run mypy app/

# Linting
poetry run flake8 app/
```

### Environment Configuration
Create a `.env` file for local development:
```env
ENVIRONMENT=development
LOG_LEVEL=INFO
CORS_ORIGINS=["http://localhost:3000"]
SOLVER_TIMEOUT=30
```

## Use Cases

This API is suitable for:
- **Personal Diet Planning**: Individuals seeking cost-effective meal planning
- **Institutional Food Services**: Hospitals, schools, and cafeterias optimizing food procurement
- **Nutritional Research**: Academic studies on diet optimization
- **Fitness Applications**: Apps helping users meet specific macro targets economically

## Implementation Notes

The linear programming formulation ensures that:
1. All nutritional constraints are satisfied
2. The solution minimizes total food cost
3. Food quantities are non-negative (cannot have negative amounts)
4. The optimization is mathematically rigorous and reproducible

The API processes the optimization problem by converting the input data into matrix form suitable for linear programming solvers, then interpreting the solution back into a user-friendly format with practical food quantities and cost breakdowns. 
