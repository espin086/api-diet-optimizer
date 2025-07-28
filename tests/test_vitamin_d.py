"""Test vitamin D functionality in the Diet Optimizer API."""

import pytest
from app.models.request import Food, NutritionalConstraints, OptimizationRequest
from app.models.response import (
    OptimizationResult,
    OptimalFood,
    NutritionalSummary,
    ConstraintSatisfaction
)
from app.services.optimizer import DietOptimizer
from app.core.exceptions import InfeasibleProblemError


class TestVitaminD:
    """Test suite for vitamin D functionality."""
    
    def test_food_model_with_vitamin_d(self):
        """Test that Food model properly handles vitamin D."""
        food = Food(
            name="Salmon",
            cost_per_100g=6.50,
            calories_per_100g=208,
            carbs_per_100g=0,
            protein_per_100g=25.4,
            fat_per_100g=12.4,
            vitamin_a_per_100g=58,
            vitamin_c_per_100g=0,
            vitamin_d_per_100g=14.2,  # Salmon is rich in vitamin D
            calcium_per_100g=12,
            iron_per_100g=0.8,
            potassium_per_100g=490,
            sodium_per_100g=59,
            cholesterol_per_100g=70
        )
        
        assert food.vitamin_d_per_100g == 14.2
        assert food.name == "Salmon"
    
    def test_nutritional_constraints_with_vitamin_d(self):
        """Test that NutritionalConstraints model properly handles vitamin D bounds."""
        constraints = NutritionalConstraints(
            min_calories=1800,
            max_calories=2200,
            min_protein=50,
            max_protein=150,
            min_carbs=130,
            max_carbs=250,
            min_fat=40,
            max_fat=80,
            min_vitamin_a=700,
            max_vitamin_a=3000,
            min_vitamin_c=75,
            max_vitamin_c=2000,
            min_vitamin_d=15,  # 600 IU
            max_vitamin_d=100, # 4000 IU
            min_calcium=1000,
            max_calcium=2500,
            min_iron=8,
            max_iron=45,
            min_potassium=3500,
            max_potassium=10000,
            min_sodium=1500,
            max_sodium=2300,
            min_cholesterol=0,
            max_cholesterol=300
        )
        
        assert constraints.min_vitamin_d == 15
        assert constraints.max_vitamin_d == 100
    
    def test_vitamin_d_bounds_validation(self):
        """Test that vitamin D bounds are properly validated."""
        with pytest.raises(ValueError, match="max_vitamin_d must be greater than min_vitamin_d"):
            NutritionalConstraints(
                min_calories=1800,
                max_calories=2200,
                min_protein=50,
                max_protein=150,
                min_carbs=130,
                max_carbs=250,
                min_fat=40,
                max_fat=80,
                min_vitamin_a=700,
                max_vitamin_a=3000,
                min_vitamin_c=75,
                max_vitamin_c=2000,
                min_vitamin_d=100,  # Min greater than max
                max_vitamin_d=50,   # Max less than min
                min_calcium=1000,
                max_calcium=2500,
                min_iron=8,
                max_iron=45,
                min_potassium=3500,
                max_potassium=10000,
                min_sodium=1500,
                max_sodium=2300,
                min_cholesterol=0,
                max_cholesterol=300
            )
    
    def test_optimization_with_vitamin_d_constraint(self):
        """Test that optimization properly considers vitamin D constraints."""
        # Create foods with varying vitamin D content
        foods = [
            Food(
                name="Salmon",
                cost_per_100g=6.50,
                calories_per_100g=208,
                carbs_per_100g=0,
                protein_per_100g=25.4,
                fat_per_100g=12.4,
                vitamin_a_per_100g=58,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=14.2,  # High vitamin D
                calcium_per_100g=12,
                iron_per_100g=0.8,
                potassium_per_100g=490,
                sodium_per_100g=59,
                cholesterol_per_100g=70
            ),
            Food(
                name="Fortified Milk",
                cost_per_100g=0.80,
                calories_per_100g=60,
                carbs_per_100g=5,
                protein_per_100g=3.4,
                fat_per_100g=3.3,
                vitamin_a_per_100g=58,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=3.0,   # Moderate vitamin D
                calcium_per_100g=125,
                iron_per_100g=0,
                potassium_per_100g=150,
                sodium_per_100g=50,
                cholesterol_per_100g=10
            ),
            Food(
                name="Rice",
                cost_per_100g=0.50,
                calories_per_100g=130,
                carbs_per_100g=28,
                protein_per_100g=2.7,
                fat_per_100g=0.3,
                vitamin_a_per_100g=0,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,     # No vitamin D
                calcium_per_100g=10,
                iron_per_100g=0.8,
                potassium_per_100g=35,
                sodium_per_100g=5,
                cholesterol_per_100g=0
            )
        ]
        
        # Create constraints requiring vitamin D
        constraints = NutritionalConstraints(
            min_calories=2000,
            max_calories=2500,
            min_protein=50,
            max_protein=150,
            min_carbs=200,
            max_carbs=300,
            min_fat=50,
            max_fat=80,
            min_vitamin_a=100,      # Reduced from 700 to make feasible
            max_vitamin_a=3000,
            min_vitamin_c=0,       # No vitamin C requirement for this test
            max_vitamin_c=2000,
            min_vitamin_d=15,      # Require vitamin D
            max_vitamin_d=100,
            min_calcium=200,       # Reduced from 1000 to make feasible
            max_calcium=2500,
            min_iron=3,            # Reduced from 8 to make feasible
            max_iron=45,
            min_potassium=500,     # Reduced from 2000 to make feasible
            max_potassium=10000,
            min_sodium=100,        # Reduced from 1000 to make feasible
            max_sodium=2300,
            min_cholesterol=0,
            max_cholesterol=300
        )
        
        # Run optimization
        optimizer = DietOptimizer()
        result = optimizer.optimize(foods, constraints)
        
        # Check that optimization succeeded
        assert result.status == "optimal"
        
        # Check that vitamin D requirement is met
        assert result.nutritional_summary.total_vitamin_d >= 15
        assert result.nutritional_summary.total_vitamin_d <= 100
        assert result.constraint_satisfaction.vitamin_d_within_bounds is True
        
        # Check that foods with vitamin D are included
        food_names = [food.food_name for food in result.optimal_quantities]
        assert any("Salmon" in name or "Milk" in name for name in food_names)
    
    def test_infeasible_vitamin_d_constraint(self):
        """Test that impossible vitamin D constraints are detected."""
        # Create foods with no vitamin D
        foods = [
            Food(
                name="Rice",
                cost_per_100g=0.50,
                calories_per_100g=130,
                carbs_per_100g=28,
                protein_per_100g=2.7,
                fat_per_100g=0.3,
                vitamin_a_per_100g=0,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,  # No vitamin D
                calcium_per_100g=10,
                iron_per_100g=0.8,
                potassium_per_100g=35,
                sodium_per_100g=5,
                cholesterol_per_100g=0
            ),
            Food(
                name="Pasta",
                cost_per_100g=0.60,
                calories_per_100g=131,
                carbs_per_100g=25,
                protein_per_100g=5,
                fat_per_100g=1.1,
                vitamin_a_per_100g=0,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,  # No vitamin D
                calcium_per_100g=7,
                iron_per_100g=0.9,
                potassium_per_100g=44,
                sodium_per_100g=1,
                cholesterol_per_100g=0
            )
        ]
        
        # Create constraints requiring vitamin D
        constraints = NutritionalConstraints(
            min_calories=1800,
            max_calories=2200,
            min_protein=50,
            max_protein=150,
            min_carbs=130,
            max_carbs=250,
            min_fat=40,
            max_fat=80,
            min_vitamin_a=0,
            max_vitamin_a=3000,
            min_vitamin_c=0,
            max_vitamin_c=2000,
            min_vitamin_d=15,      # Require vitamin D but foods have none
            max_vitamin_d=100,
            min_calcium=0,
            max_calcium=2500,
            min_iron=0,
            max_iron=45,
            min_potassium=0,
            max_potassium=10000,
            min_sodium=0,
            max_sodium=2300,
            min_cholesterol=0,
            max_cholesterol=300
        )
        
        # Run optimization - should raise InfeasibleProblemError
        optimizer = DietOptimizer()
        with pytest.raises(InfeasibleProblemError):
            optimizer.optimize(foods, constraints)
    
    def test_vitamin_d_calculation_accuracy(self):
        """Test that vitamin D totals are calculated accurately."""
        # Create a simple scenario with known quantities
        foods = [
            Food(
                name="Test Food 1",
                cost_per_100g=1.0,
                calories_per_100g=100,
                carbs_per_100g=10,
                protein_per_100g=10,
                fat_per_100g=5,
                vitamin_a_per_100g=100,
                vitamin_c_per_100g=10,
                vitamin_d_per_100g=5.0,   # 5 mcg per 100g
                calcium_per_100g=100,
                iron_per_100g=1,
                potassium_per_100g=100,
                sodium_per_100g=50,
                cholesterol_per_100g=10
            ),
            Food(
                name="Test Food 2",
                cost_per_100g=2.0,
                calories_per_100g=200,
                carbs_per_100g=20,
                protein_per_100g=20,
                fat_per_100g=10,
                vitamin_a_per_100g=200,
                vitamin_c_per_100g=20,
                vitamin_d_per_100g=10.0,  # 10 mcg per 100g
                calcium_per_100g=200,
                iron_per_100g=2,
                potassium_per_100g=200,
                sodium_per_100g=100,
                cholesterol_per_100g=20
            )
        ]
        
        # Create constraints that will result in specific quantities
        constraints = NutritionalConstraints(
            min_calories=300,
            max_calories=301,      # Slightly higher to pass validation
            min_protein=30,
            max_protein=31,        # Slightly higher to pass validation
            min_carbs=30,
            max_carbs=31,          # Slightly higher to pass validation
            min_fat=15,
            max_fat=16,            # Slightly higher to pass validation
            min_vitamin_a=0,
            max_vitamin_a=1000,
            min_vitamin_c=0,
            max_vitamin_c=1000,
            min_vitamin_d=15,      # This will require both foods
            max_vitamin_d=100,
            min_calcium=0,
            max_calcium=1000,
            min_iron=0,
            max_iron=100,
            min_potassium=0,
            max_potassium=10000,
            min_sodium=0,
            max_sodium=2300,
            min_cholesterol=0,
            max_cholesterol=300
        )
        
        # Run optimization
        optimizer = DietOptimizer()
        result = optimizer.optimize(foods, constraints)
        
        # Check that optimization succeeded
        assert result.status == "optimal"
        
        # Verify vitamin D calculation
        # With the constraints, we should get 1 unit of each food (100g each)
        # Total vitamin D should be 5.0 + 10.0 = 15.0 mcg
        assert abs(result.nutritional_summary.total_vitamin_d - 15.0) < 0.1