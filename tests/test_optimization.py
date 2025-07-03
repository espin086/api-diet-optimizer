"""Tests for the optimization API endpoints."""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

from app.main import app
from app.models.request import Food, NutritionalConstraints, OptimizationRequest
from app.models.response import OptimizationResult
from app.services.optimizer import DietOptimizer
from app.core.exceptions import InfeasibleProblemError, UnboundedProblemError, SolverTimeoutError

client = TestClient(app)


@pytest.fixture
def sample_foods():
    """Sample foods for testing."""
    return [
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
    ]


@pytest.fixture
def sample_constraints():
    """Sample nutritional constraints for testing."""
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


@pytest.fixture
def valid_request(sample_foods, sample_constraints):
    """Valid optimization request for testing."""
    return {
        "foods": sample_foods,
        "constraints": sample_constraints
    }


class TestOptimizationEndpoint:
    """Test cases for the /optimize endpoint."""
    
    def test_valid_optimization_request(self, valid_request):
        """Test successful optimization with valid input."""
        response = client.post("/optimize", json=valid_request)
        
        assert response.status_code == 200
        result = response.json()
        
        # Check response structure
        assert "status" in result
        assert "total_cost" in result
        assert "optimal_quantities" in result
        assert "nutritional_summary" in result
        assert "constraint_satisfaction" in result
        
        # Check status is one of expected values
        assert result["status"] in ["optimal", "infeasible", "unbounded"]
        
        if result["status"] == "optimal":
            assert result["total_cost"] >= 0
            assert isinstance(result["optimal_quantities"], list)
            
            # Check nutritional summary structure
            summary = result["nutritional_summary"]
            assert "total_calories" in summary
            assert "total_protein" in summary
            assert "total_carbs" in summary
            assert "total_fat" in summary
            
            # Check constraint satisfaction structure
            satisfaction = result["constraint_satisfaction"]
            assert "calories_within_bounds" in satisfaction
            assert "protein_within_bounds" in satisfaction
            assert "carbs_within_bounds" in satisfaction
            assert "fat_within_bounds" in satisfaction
    
    def test_empty_foods_list(self, sample_constraints):
        """Test with empty foods list."""
        request = {
            "foods": [],
            "constraints": sample_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422  # Validation error
    
    def test_invalid_food_data(self, sample_constraints):
        """Test with invalid food data."""
        request = {
            "foods": [
                {
                    "name": "",  # Empty name
                    "cost_per_100g": -1,  # Negative cost
                    "calories_per_100g": 165,
                    "carbs_per_100g": 0,
                    "protein_per_100g": 31,
                    "fat_per_100g": 3.6
                }
            ],
            "constraints": sample_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422
    
    def test_invalid_constraints(self, sample_foods):
        """Test with invalid constraints."""
        request = {
            "foods": sample_foods,
            "constraints": {
                "min_calories": 2000,
                "max_calories": 1800,  # Max < Min (invalid)
                "min_protein": 120,
                "max_protein": 180,
                "min_carbs": 150,
                "max_carbs": 250,
                "min_fat": 50,
                "max_fat": 80
            }
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422
    
    def test_duplicate_food_names(self, sample_constraints):
        """Test with duplicate food names."""
        request = {
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
                    "name": "Chicken Breast",  # Duplicate name
                    "cost_per_100g": 3.00,
                    "calories_per_100g": 160,
                    "carbs_per_100g": 0,
                    "protein_per_100g": 30,
                    "fat_per_100g": 4.0
                }
            ],
            "constraints": sample_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422
    
    def test_infeasible_problem(self):
        """Test infeasible optimization problem."""
        # Create an impossible constraint scenario
        request = {
            "foods": [
                {
                    "name": "Low Calorie Food",
                    "cost_per_100g": 1.0,
                    "calories_per_100g": 10,  # Very low calories
                    "carbs_per_100g": 1,
                    "protein_per_100g": 1,
                    "fat_per_100g": 0.1
                }
            ],
            "constraints": {
                "min_calories": 5000,  # Impossible to reach with given food
                "max_calories": 6000,
                "min_protein": 200,
                "max_protein": 300,
                "min_carbs": 100,
                "max_carbs": 200,
                "min_fat": 50,
                "max_fat": 100
            }
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        assert result["status"] == "infeasible"
    
    @patch('app.services.optimizer.DietOptimizer.optimize')
    def test_solver_timeout(self, mock_optimize, valid_request):
        """Test solver timeout handling."""
        mock_optimize.side_effect = SolverTimeoutError(30)
        
        response = client.post("/optimize", json=valid_request)
        assert response.status_code == 408
        result = response.json()
        assert "solver_timeout" in result["detail"]["error"]
    
    def test_missing_required_fields(self):
        """Test with missing required fields."""
        # Missing constraints
        request = {
            "foods": [
                {
                    "name": "Test Food",
                    "cost_per_100g": 1.0,
                    "calories_per_100g": 100,
                    "carbs_per_100g": 10,
                    "protein_per_100g": 5,
                    "fat_per_100g": 2
                }
            ]
            # Missing constraints field
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422


class TestHealthEndpoint:
    """Test cases for the /health endpoint."""
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        
        assert response.status_code == 200
        result = response.json()
        
        assert "status" in result
        assert "version" in result
        assert "message" in result
        assert result["status"] == "healthy"


class TestRootEndpoint:
    """Test cases for the root endpoint."""
    
    def test_root_endpoint(self):
        """Test root endpoint."""
        response = client.get("/")
        
        assert response.status_code == 200
        result = response.json()
        
        assert "name" in result
        assert "version" in result
        assert "status" in result
        assert "docs_url" in result
        assert "health_url" in result
        assert "optimize_url" in result


class TestErrorHandling:
    """Test error handling scenarios."""
    
    def test_invalid_json(self):
        """Test with invalid JSON."""
        response = client.post(
            "/optimize", 
            content="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_method_not_allowed(self):
        """Test wrong HTTP method."""
        response = client.get("/optimize")
        assert response.status_code == 405