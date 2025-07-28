"""Tests for enhanced nutritional functionality with vitamins and minerals."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.optimizer import DietOptimizer
from app.models.request import Food, NutritionalConstraints, OptimizationRequest

client = TestClient(app)


@pytest.fixture
def comprehensive_foods():
    """Comprehensive food database with realistic nutritional data."""
    return [
        {
            "name": "Salmon Fillet",
            "cost_per_100g": 4.50,
            "calories_per_100g": 208,
            "carbs_per_100g": 0,
            "protein_per_100g": 25.4,
            "fat_per_100g": 12.4,
            "vitamin_a_per_100g": 58,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 12,
            "iron_per_100g": 0.8,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 490,
            "sodium_per_100g": 59,
            "cholesterol_per_100g": 70
        },
        {
            "name": "Spinach",
            "cost_per_100g": 1.80,
            "calories_per_100g": 23,
            "carbs_per_100g": 3.6,
            "protein_per_100g": 2.9,
            "fat_per_100g": 0.4,
            "vitamin_a_per_100g": 469,
            "vitamin_c_per_100g": 28.1,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 99,
            "iron_per_100g": 2.7,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 558,
            "sodium_per_100g": 79,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Quinoa",
            "cost_per_100g": 2.20,
            "calories_per_100g": 368,
            "carbs_per_100g": 64.2,
            "protein_per_100g": 14.1,
            "fat_per_100g": 6.1,
            "vitamin_a_per_100g": 1,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 47,
            "iron_per_100g": 4.6,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 563,
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Greek Yogurt",
            "cost_per_100g": 1.50,
            "calories_per_100g": 97,
            "carbs_per_100g": 3.9,
            "protein_per_100g": 10,
            "fat_per_100g": 5,
            "vitamin_a_per_100g": 36,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 110,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 141,
            "sodium_per_100g": 36,
            "cholesterol_per_100g": 10
        },
        {
            "name": "Almonds",
            "cost_per_100g": 6.00,
            "calories_per_100g": 579,
            "carbs_per_100g": 21.6,
            "protein_per_100g": 21.2,
            "fat_per_100g": 49.9,
            "vitamin_a_per_100g": 0,
            "vitamin_c_per_100g": 0,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 269,
            "iron_per_100g": 3.7,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 733,
            "sodium_per_100g": 1,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Orange",
            "cost_per_100g": 0.90,
            "calories_per_100g": 47,
            "carbs_per_100g": 11.8,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.1,
            "vitamin_a_per_100g": 11,
            "vitamin_c_per_100g": 53.2,
            "vitamin_d_per_100g": 0,
            "calcium_per_100g": 40,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 20,
            "potassium_per_100g": 181,
            "sodium_per_100g": 0,
            "cholesterol_per_100g": 0
        }
    ]


@pytest.fixture
def vitamin_focused_constraints():
    """Constraints focused on vitamin requirements."""
    return {
        "min_calories": 1500,
        "max_calories": 2000,
        "min_protein": 80,
        "max_protein": 150,
        "min_carbs": 100,
        "max_carbs": 200,
        "min_fat": 40,
        "max_fat": 70,
        "min_vitamin_a": 900,  # High vitamin A requirement
        "max_vitamin_a": 3000,
        "min_vitamin_c": 90,   # High vitamin C requirement
        "max_vitamin_c": 2000,
        "min_calcium": 1200,   # High calcium requirement
        "max_calcium": 2500,
        "min_iron": 18,        # High iron requirement (women's needs)
        "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
        "min_potassium": 4700,
        "max_potassium": 10000,
        "min_sodium": 1500,
        "max_sodium": 2300,
        "min_cholesterol": 0,
        "max_cholesterol": 300
    }


@pytest.fixture
def mineral_focused_constraints():
    """Constraints focused on mineral requirements."""
    return {
        "min_calories": 1800,
        "max_calories": 2200,
        "min_protein": 100,
        "max_protein": 160,
        "min_carbs": 130,
        "max_carbs": 220,
        "min_fat": 50,
        "max_fat": 80,
        "min_vitamin_a": 700,
        "max_vitamin_a": 3000,
        "min_vitamin_c": 75,
        "max_vitamin_c": 2000,
        "min_calcium": 1300,   # Very high calcium
        "max_calcium": 2500,
        "min_iron": 15,        # High iron
        "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
        "min_potassium": 5000, # Very high potassium
        "max_potassium": 10000,
        "min_sodium": 1000,    # Lower sodium for health
        "max_sodium": 1500,
        "min_cholesterol": 0,
        "max_cholesterol": 200 # Lower cholesterol
    }


class TestVitaminOptimization:
    """Test vitamin-specific optimization scenarios."""
    
    def test_high_vitamin_a_optimization(self, comprehensive_foods):
        """Test optimization for high vitamin A requirements."""
        constraints = {
            "min_calories": 1200,
            "max_calories": 1800,
            "min_protein": 50,
            "max_protein": 100,
            "min_carbs": 80,
            "max_carbs": 150,
            "min_fat": 30,
            "max_fat": 60,
            "min_vitamin_a": 1200,  # Very high vitamin A
            "max_vitamin_a": 3000,
            "min_vitamin_c": 60,
            "max_vitamin_c": 2000,
            "min_calcium": 800,
            "max_calcium": 2500,
            "min_iron": 8,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 3000,
            "max_potassium": 10000,
            "min_sodium": 1200,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            assert result["nutritional_summary"]["total_vitamin_a"] >= constraints["min_vitamin_a"]
            assert result["constraint_satisfaction"]["vitamin_a_within_bounds"] == True
    
    def test_high_vitamin_c_optimization(self, comprehensive_foods):
        """Test optimization for high vitamin C requirements."""
        constraints = {
            "min_calories": 1000,
            "max_calories": 1500,
            "min_protein": 40,
            "max_protein": 80,
            "min_carbs": 60,
            "max_carbs": 120,
            "min_fat": 20,
            "max_fat": 50,
            "min_vitamin_a": 500,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 120,  # Very high vitamin C
            "max_vitamin_c": 2000,
            "min_calcium": 600,
            "max_calcium": 2500,
            "min_iron": 6,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 2500,
            "max_potassium": 10000,
            "min_sodium": 1000,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            assert result["nutritional_summary"]["total_vitamin_c"] >= constraints["min_vitamin_c"]
            assert result["constraint_satisfaction"]["vitamin_c_within_bounds"] == True


class TestMineralOptimization:
    """Test mineral-specific optimization scenarios."""
    
    def test_high_calcium_optimization(self, comprehensive_foods):
        """Test optimization for high calcium requirements."""
        constraints = {
            "min_calories": 1400,
            "max_calories": 1900,
            "min_protein": 60,
            "max_protein": 120,
            "min_carbs": 100,
            "max_carbs": 180,
            "min_fat": 35,
            "max_fat": 65,
            "min_vitamin_a": 600,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 65,
            "max_vitamin_c": 2000,
            "min_calcium": 1400,  # Very high calcium
            "max_calcium": 2500,
            "min_iron": 10,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 3200,
            "max_potassium": 10000,
            "min_sodium": 1100,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            assert result["nutritional_summary"]["total_calcium"] >= constraints["min_calcium"]
            assert result["constraint_satisfaction"]["calcium_within_bounds"] == True
    
    def test_high_iron_optimization(self, comprehensive_foods):
        """Test optimization for high iron requirements."""
        constraints = {
            "min_calories": 1300,
            "max_calories": 1700,
            "min_protein": 55,
            "max_protein": 95,
            "min_carbs": 90,
            "max_carbs": 140,
            "min_fat": 30,
            "max_fat": 55,
            "min_vitamin_a": 550,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 70,
            "max_vitamin_c": 2000,
            "min_calcium": 900,
            "max_calcium": 2500,
            "min_iron": 20,        # Very high iron (pregnancy needs)
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 2800,
            "max_potassium": 10000,
            "min_sodium": 1000,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            assert result["nutritional_summary"]["total_iron"] >= constraints["min_iron"]
            assert result["constraint_satisfaction"]["iron_within_bounds"] == True
    
    def test_high_potassium_low_sodium(self, comprehensive_foods):
        """Test optimization for high potassium, low sodium (heart healthy)."""
        constraints = {
            "min_calories": 1600,
            "max_calories": 2100,
            "min_protein": 70,
            "max_protein": 130,
            "min_carbs": 110,
            "max_carbs": 190,
            "min_fat": 40,
            "max_fat": 75,
            "min_vitamin_a": 650,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 80,
            "max_vitamin_c": 2000,
            "min_calcium": 1000,
            "max_calcium": 2500,
            "min_iron": 12,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 5500,  # Very high potassium
            "max_potassium": 10000,
            "min_sodium": 800,      # Very low sodium
            "max_sodium": 1200,
            "min_cholesterol": 0,
            "max_cholesterol": 200
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            assert result["nutritional_summary"]["total_potassium"] >= constraints["min_potassium"]
            assert result["nutritional_summary"]["total_sodium"] <= constraints["max_sodium"]
            assert result["constraint_satisfaction"]["potassium_within_bounds"] == True
            assert result["constraint_satisfaction"]["sodium_within_bounds"] == True


class TestSpecialDietaryNeeds:
    """Test optimization for special dietary needs."""
    
    def test_pregnancy_nutrition_profile(self, comprehensive_foods):
        """Test optimization for pregnancy nutritional needs."""
        pregnancy_constraints = {
            "min_calories": 2200,
            "max_calories": 2500,
            "min_protein": 110,
            "max_protein": 160,
            "min_carbs": 175,
            "max_carbs": 250,
            "min_fat": 60,
            "max_fat": 90,
            "min_vitamin_a": 770,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 85,
            "max_vitamin_c": 2000,
            "min_calcium": 1200,
            "max_calcium": 2500,
            "min_iron": 27,        # High iron for pregnancy
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 4700,
            "max_potassium": 10000,
            "min_sodium": 1500,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": pregnancy_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        # Pregnancy nutrition is challenging, so infeasible is acceptable
        assert result["status"] in ["optimal", "infeasible"]
        
        if result["status"] == "optimal":
            # Check that high-priority pregnancy nutrients are met
            assert result["nutritional_summary"]["total_iron"] >= pregnancy_constraints["min_iron"]
            assert result["nutritional_summary"]["total_calcium"] >= pregnancy_constraints["min_calcium"]
    
    def test_senior_nutrition_profile(self, comprehensive_foods):
        """Test optimization for senior nutritional needs."""
        senior_constraints = {
            "min_calories": 1600,
            "max_calories": 2000,
            "min_protein": 80,     # Higher protein for seniors
            "max_protein": 120,
            "min_carbs": 100,
            "max_carbs": 160,
            "min_fat": 40,
            "max_fat": 70,
            "min_vitamin_a": 900,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 90,
            "max_vitamin_c": 2000,
            "min_calcium": 1300,   # Higher calcium for bone health
            "max_calcium": 2500,
            "min_iron": 8,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 4700,
            "max_potassium": 10000,
            "min_sodium": 1000,    # Lower sodium for heart health
            "max_sodium": 1500,
            "min_cholesterol": 0,
            "max_cholesterol": 200 # Lower cholesterol
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": senior_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        if result["status"] == "optimal":
            # Check senior-specific nutritional priorities
            assert result["nutritional_summary"]["total_protein"] >= senior_constraints["min_protein"]
            assert result["nutritional_summary"]["total_calcium"] >= senior_constraints["min_calcium"]
            assert result["nutritional_summary"]["total_sodium"] <= senior_constraints["max_sodium"]


class TestNutritionalEdgeCases:
    """Test edge cases in nutritional optimization."""
    
    def test_zero_nutrient_foods(self):
        """Test with foods that have zero values for some nutrients."""
        zero_nutrient_foods = [
            {
                "name": "Pure Sugar",
                "cost_per_100g": 0.50,
                "calories_per_100g": 387,
                "carbs_per_100g": 100,
                "protein_per_100g": 0,
                "fat_per_100g": 0,
                "vitamin_a_per_100g": 0,
                "vitamin_c_per_100g": 0,
                "vitamin_d_per_100g": 0,
                "calcium_per_100g": 0,
                "iron_per_100g": 0,
            "magnesium_per_100g": 20,
                "potassium_per_100g": 0,
                "sodium_per_100g": 0,
                "cholesterol_per_100g": 0
            },
            {
                "name": "Multivitamin Supplement",
                "cost_per_100g": 50.00,
                "calories_per_100g": 5,
                "carbs_per_100g": 1,
                "protein_per_100g": 0,
                "fat_per_100g": 0,
                "vitamin_a_per_100g": 2000,
                "vitamin_c_per_100g": 1000,
                "vitamin_d_per_100g": 0,
                "calcium_per_100g": 500,
                "iron_per_100g": 20,
            "magnesium_per_100g": 20,
                "potassium_per_100g": 100,
                "sodium_per_100g": 10,
                "cholesterol_per_100g": 0
            }
        ]
        
        constraints = {
            "min_calories": 800,
            "max_calories": 1200,
            "min_protein": 30,
            "max_protein": 60,
            "min_carbs": 60,
            "max_carbs": 120,
            "min_fat": 20,
            "max_fat": 40,
            "min_vitamin_a": 500,
            "max_vitamin_a": 3000,
            "min_vitamin_c": 50,
            "max_vitamin_c": 2000,
            "min_calcium": 400,
            "max_calcium": 2500,
            "min_iron": 6,
            "max_iron": 45,
        "min_magnesium": 310,
        "max_magnesium": 800,
            "min_potassium": 2000,
            "max_potassium": 10000,
            "min_sodium": 800,
            "max_sodium": 2300,
            "min_cholesterol": 0,
            "max_cholesterol": 300
        }
        
        request = {
            "foods": zero_nutrient_foods,
            "constraints": constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        # This should likely be infeasible due to protein requirements
        assert result["status"] in ["optimal", "infeasible"]
    
    def test_extremely_tight_constraints(self, comprehensive_foods):
        """Test with very tight nutritional constraints."""
        tight_constraints = {
            "min_calories": 1950,
            "max_calories": 2000,  # Very narrow range
            "min_protein": 98,
            "max_protein": 102,    # Very narrow range
            "min_carbs": 148,
            "max_carbs": 152,      # Very narrow range
            "min_fat": 68,
            "max_fat": 72,         # Very narrow range
            "min_vitamin_a": 850,
            "max_vitamin_a": 870,  # Very narrow range
            "min_vitamin_c": 88,
            "max_vitamin_c": 92,   # Very narrow range
            "min_calcium": 1190,
            "max_calcium": 1210,   # Very narrow range
            "min_iron": 14,
            "max_iron": 16,
        "min_magnesium": 310,
        "max_magnesium": 800,        # Very narrow range
            "min_potassium": 4690,
            "max_potassium": 4710, # Very narrow range
            "min_sodium": 1490,
            "max_sodium": 1510,    # Very narrow range
            "min_cholesterol": 45,
            "max_cholesterol": 55  # Very narrow range
        }
        
        request = {
            "foods": comprehensive_foods,
            "constraints": tight_constraints
        }
        
        response = client.post("/optimize", json=request)
        assert response.status_code == 200
        result = response.json()
        
        # Very tight constraints will likely be infeasible
        assert result["status"] in ["optimal", "infeasible"]