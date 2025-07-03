# Diet Optimizer API

A FastAPI implementation that solves the classic **Diet Problem** from linear programming and optimization theory. This API uses linear programming to find the optimal combination of foods that meets specified nutritional requirements while minimizing total cost.

## Problem Description

The Diet Problem is a fundamental optimization challenge where the goal is to determine the minimum-cost combination of foods that satisfies specific nutritional constraints. This API optimizes four key macronutrients:

- **Calories** - Total energy content
- **Protein** - Essential for muscle building and repair
- **Carbohydrates** - Primary energy source
- **Fat** - Essential fatty acids and energy storage

## How It Works

The API accepts a list of available foods with their nutritional profiles and cost information, along with the desired nutritional constraints (minimum and maximum values for each macronutrient). It then formulates and solves a linear programming optimization problem to find the lowest-cost food combination that meets all specified requirements.

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
quantity[i] ≥ 0 for all foods i
```

## API Specification

### Input Format

The API accepts JSON input with the following structure:

#### Foods List
Each food item must contain:
```json
{
  "name": "string",              // Name of the food item
  "cost_per_100g": "number",     // Cost per 100 grams (in currency units)
  "calories_per_100g": "number", // Calories per 100 grams
  "carbs_per_100g": "number",    // Carbohydrates per 100 grams (in grams)
  "protein_per_100g": "number",  // Protein per 100 grams (in grams)
  "fat_per_100g": "number"       // Fat per 100 grams (in grams)
}
```

#### Nutritional Constraints
The API accepts upper and lower bounds for each macronutrient:
```json
{
  "min_calories": "number",      // Minimum daily calories required
  "max_calories": "number",      // Maximum daily calories allowed
  "min_protein": "number",       // Minimum daily protein required (grams)
  "max_protein": "number",       // Maximum daily protein allowed (grams)
  "min_carbs": "number",         // Minimum daily carbohydrates required (grams)
  "max_carbs": "number",         // Maximum daily carbohydrates allowed (grams)
  "min_fat": "number",           // Minimum daily fat required (grams)
  "max_fat": "number"            // Maximum daily fat allowed (grams)
}
```

### Complete Request Example
```json
{
  "foods": [
    {
      "name": "Chicken Breast",
      "cost_per_100g": 2.50,
      "calories_per_100g": 165,
      "carbs_per_100g": 0,
      "protein_per_100g": 31,
      "fat_per_100g": 3.6
    },
    {
      "name": "Brown Rice",
      "cost_per_100g": 0.80,
      "calories_per_100g": 112,
      "carbs_per_100g": 23,
      "protein_per_100g": 2.6,
      "fat_per_100g": 0.9
    },
    {
      "name": "Broccoli",
      "cost_per_100g": 1.20,
      "calories_per_100g": 34,
      "carbs_per_100g": 7,
      "protein_per_100g": 2.8,
      "fat_per_100g": 0.4
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
    "max_fat": 80
  }
}
```

### Output Format

The API returns the optimal solution containing:
```json
{
  "status": "string",                    // "optimal", "infeasible", or "unbounded"
  "total_cost": "number",                // Minimum total cost achieved
  "optimal_quantities": [                // Quantities of each food (in 100g units)
    {
      "food_name": "string",
      "quantity_100g": "number",         // Amount in 100-gram units
      "quantity_grams": "number",        // Total grams of this food
      "cost": "number"                   // Cost contribution of this food
    }
  ],
  "nutritional_summary": {               // Total nutritional content achieved
    "total_calories": "number",
    "total_protein": "number",
    "total_carbs": "number",
    "total_fat": "number"
  },
  "constraint_satisfaction": {           // Whether each constraint is met
    "calories_within_bounds": "boolean",
    "protein_within_bounds": "boolean",
    "carbs_within_bounds": "boolean",
    "fat_within_bounds": "boolean"
  }
}
```

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
