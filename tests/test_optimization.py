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
    """Sample foods for testing with complete nutritional data."""
    return [
        {
            "name": "Chicken Breast",
            "cost_per_100g": 2.50,
            "calories_per_100g": 165,
            "carbs_per_100g": 0,
            "protein_per_100g": 31,
            "fat_per_100g": 3.6,
            "vitamin_a_per_100g": 9,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 15,
            "iron_per_100g": 0.9,
            "potassium_per_100g": 256,
            "sodium_per_100g": 74,
            "cholesterol_per_100g": 85
        },
        {
            "name": "Brown Rice",
            "cost_per_100g": 0.80,
            "calories_per_100g": 112,
            "carbs_per_100g": 23,
            "protein_per_100g": 2.6,
            "fat_per_100g": 0.9,
            "vitamin_a_per_100g": 0,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 10,
            "iron_per_100g": 0.4,
            "potassium_per_100g": 43,
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Broccoli",
            "cost_per_100g": 1.20,
            "calories_per_100g": 34,
            "carbs_per_100g": 7,
            "protein_per_100g": 2.8,
            "fat_per_100g": 0.4,
            "vitamin_a_per_100g": 623,
            "vitamin_c_per_100g": 89.2,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 47,
            "iron_per_100g": 0.7,
            "potassium_per_100g": 316,
            "sodium_per_100g": 33,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Sweet Potato",
            "cost_per_100g": 0.60,
            "calories_per_100g": 86,
            "carbs_per_100g": 20,
            "protein_per_100g": 1.6,
            "fat_per_100g": 0.1,
            "vitamin_a_per_100g": 961,
            "vitamin_c_per_100g": 2.4,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 30,
            "iron_per_100g": 0.6,
            "potassium_per_100g": 337,
            "sodium_per_100g": 54,
            "cholesterol_per_100g": 0
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
        "max_fat": 80,
        "min_vitamin_a": 700,
        "max_vitamin_a": 3000,
        "min_vitamin_c": 75,
        "max_vitamin_c": 2000,
        "min_calcium": 1000,
        "max_calcium": 2500,
        "min_iron": 8,
        "max_iron": 45,
        "min_potassium": 3500,
        "max_potassium": 10000,
        "min_sodium": 1500,
        "max_sodium": 2300,
        "min_cholesterol": 0,
        "max_cholesterol": 300
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
            expected_nutrients = [
                "total_calories", "total_protein", "total_carbs", "total_fat",
                "total_vitamin_a", "total_vitamin_c", "total_calcium", "total_iron",
                "total_potassium", "total_sodium", "total_cholesterol"
            ]
            for nutrient in expected_nutrients:
                assert nutrient in summary
                assert isinstance(summary[nutrient], (int, float))
                assert summary[nutrient] >= 0
            
            # Check constraint satisfaction structure
            satisfaction = result["constraint_satisfaction"]
            expected_constraints = [
                "calories_within_bounds", "protein_within_bounds", "carbs_within_bounds", 
                "fat_within_bounds", "vitamin_a_within_bounds", "vitamin_c_within_bounds",
                "calcium_within_bounds", "iron_within_bounds", "potassium_within_bounds",
                "sodium_within_bounds", "cholesterol_within_bounds"
            ]
            for constraint in expected_constraints:
                assert constraint in satisfaction
                assert isinstance(satisfaction[constraint], bool)
    
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
                    "fat_per_100g": 3.6,
                    "vitamin_a_per_100g": 9,
                    "vitamin_c_per_100g": 0,
                    "vitamin_d_per_100g": 0,
                    "calcium_per_100g": 15,
                    "iron_per_100g": 0.9,
                    "potassium_per_100g": 256,
                    "sodium_per_100g": 74,
                    "cholesterol_per_100g": 85
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
                "max_fat": 80,
                "min_vitamin_a": 700,
                "max_vitamin_a": 3000,
                "min_vitamin_c": 75,
                "max_vitamin_c": 2000,
                "min_calcium": 1000,
                "max_calcium": 2500,
                "min_iron": 8,
                "max_iron": 45,
                "min_potassium": 3500,
                "max_potassium": 10000,
                "min_sodium": 1500,
                "max_sodium": 2300,
                "min_cholesterol": 0,
                "max_cholesterol": 300
            }
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 422
    
    def test_missing_nutritional_fields(self, sample_constraints):
        """Test with missing required nutritional fields."""
        request = {
            "foods": [
                {
                    "name": "Incomplete Food",
                    "cost_per_100g": 2.50,
                    "calories_per_100g": 165,
                    "carbs_per_100g": 0,
                    "protein_per_100g": 31,
                    "fat_per_100g": 3.6
                    # Missing vitamin and mineral fields
                }
            ],
            "constraints": sample_constraints
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
                    "fat_per_100g": 3.6,
                    "vitamin_a_per_100g": 9,
                    "vitamin_c_per_100g": 0,
                    "vitamin_d_per_100g": 0,
                    "calcium_per_100g": 15,
                    "iron_per_100g": 0.9,
                    "potassium_per_100g": 256,
                    "sodium_per_100g": 74,
                    "cholesterol_per_100g": 85
                },
                {
                    "name": "Chicken Breast",  # Duplicate name
                    "cost_per_100g": 3.00,
                    "calories_per_100g": 160,
                    "carbs_per_100g": 0,
                    "protein_per_100g": 30,
                    "fat_per_100g": 4.0,
                    "vitamin_a_per_100g": 10,
                    "vitamin_c_per_100g": 0,
                    "vitamin_d_per_100g": 0,
                    "calcium_per_100g": 20,
                    "iron_per_100g": 1.0,
                    "potassium_per_100g": 300,
                    "sodium_per_100g": 80,
                    "cholesterol_per_100g": 90
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
                    "name": "Low Nutrient Food",
                    "cost_per_100g": 1.0,
                    "calories_per_100g": 10,  # Very low nutrients
                    "carbs_per_100g": 1,
                    "protein_per_100g": 1,
                    "fat_per_100g": 0.1,
                    "vitamin_a_per_100g": 1,
                    "vitamin_c_per_100g": 0.1,
                    "vitamin_d_per_100g": 0,
                    "calcium_per_100g": 1,
                    "iron_per_100g": 0.1,
                    "potassium_per_100g": 10,
                    "sodium_per_100g": 1,
                    "cholesterol_per_100g": 0
                }
            ],
            "constraints": {
                "min_calories": 5000,  # Impossible to reach
                "max_calories": 6000,
                "min_protein": 200,
                "max_protein": 300,
                "min_carbs": 100,
                "max_carbs": 200,
                "min_fat": 50,
                "max_fat": 100,
                "min_vitamin_a": 700,
                "max_vitamin_a": 3000,
                "min_vitamin_c": 75,
                "max_vitamin_c": 2000,
                "min_calcium": 1000,
                "max_calcium": 2500,
                "min_iron": 8,
                "max_iron": 45,
                "min_potassium": 3500,
                "max_potassium": 10000,
                "min_sodium": 1500,
                "max_sodium": 2300,
                "min_cholesterol": 0,
                "max_cholesterol": 300
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
                    "fat_per_100g": 2,
                    "vitamin_a_per_100g": 50,
                    "vitamin_c_per_100g": 5,
                    "vitamin_d_per_100g": 0,
                    "calcium_per_100g": 20,
                    "iron_per_100g": 1,
                    "potassium_per_100g": 100,
                    "sodium_per_100g": 10,
                    "cholesterol_per_100g": 0
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