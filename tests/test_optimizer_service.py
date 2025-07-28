"""Unit tests for the DietOptimizer service."""

import pytest
import numpy as np
from unittest.mock import Mock, patch

from app.services.optimizer import DietOptimizer
from app.models.request import Food, NutritionalConstraints
from app.models.response import OptimizationResult
from app.core.exceptions import (
    InfeasibleProblemError, 
    UnboundedProblemError, 
    OptimizationError,
    SolverTimeoutError
)


class TestDietOptimizer:
    """Test cases for the DietOptimizer class."""
    
    @pytest.fixture
    def optimizer(self):
        """Create optimizer instance for testing."""
        return DietOptimizer()
    
    @pytest.fixture
    def simple_foods(self):
        """Simple food set for mathematical verification."""
        return [
            Food(
                name="Cheap Protein",
                cost_per_100g=1.0,
                calories_per_100g=100,
                carbs_per_100g=0,
                protein_per_100g=25,
                fat_per_100g=5,  # Increased fat content
                vitamin_a_per_100g=10,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,
                calcium_per_100g=20,
                iron_per_100g=1.0,
                magnesium_per_100g=20,
                potassium_per_100g=200,
                sodium_per_100g=50,
                cholesterol_per_100g=0,
                fiber_per_100g=0
            ),
            Food(
                name="Cheap Carbs",
                cost_per_100g=0.5,
                calories_per_100g=150,
                carbs_per_100g=35,
                protein_per_100g=3,
                fat_per_100g=3,  # Increased fat content
                vitamin_a_per_100g=0,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,
                calcium_per_100g=5,
                iron_per_100g=0.5,
                magnesium_per_100g=44,
                potassium_per_100g=50,
                sodium_per_100g=10,
                cholesterol_per_100g=0,
                fiber_per_100g=1.5
            ),
            Food(
                name="Expensive Fat",
                cost_per_100g=3.0,
                calories_per_100g=200,
                carbs_per_100g=0,
                protein_per_100g=0,
                fat_per_100g=20,
                vitamin_a_per_100g=5,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,
                calcium_per_100g=10,
                iron_per_100g=0.2,
                magnesium_per_100g=5,
                potassium_per_100g=30,
                sodium_per_100g=20,
                cholesterol_per_100g=50,
                fiber_per_100g=0
            )
        ]
    
    @pytest.fixture
    def simple_constraints(self):
        """Simple constraints for mathematical verification."""
        return NutritionalConstraints(
            min_calories=300,
            max_calories=400,
            min_protein=20,
            max_protein=30,
            min_carbs=30,
            max_carbs=40,
            min_fat=10,
            max_fat=15,
            min_vitamin_a=10,
            max_vitamin_a=100,
            min_vitamin_c=0,
            max_vitamin_c=50,
            min_calcium=20,
            max_calcium=100,
            min_iron=1,
            max_iron=10,
            min_magnesium=50,
            max_magnesium=200,
            min_potassium=200,
            max_potassium=1000,
            min_sodium=50,
            max_sodium=500,
            min_cholesterol=0,
            max_cholesterol=100,
            min_fiber=5,
            max_fiber=20
        )
    
    def test_optimization_basic_functionality(self, optimizer, simple_foods, simple_constraints):
        """Test basic optimization functionality."""
        result = optimizer.optimize(simple_foods, simple_constraints)
        
        assert isinstance(result, OptimizationResult)
        assert result.status == "optimal"
        assert result.total_cost > 0
        assert len(result.optimal_quantities) > 0
        
        # Verify nutritional totals match constraints
        summary = result.nutritional_summary
        assert simple_constraints.min_calories <= summary.total_calories <= simple_constraints.max_calories
        assert simple_constraints.min_protein <= summary.total_protein <= simple_constraints.max_protein
        assert simple_constraints.min_carbs <= summary.total_carbs <= simple_constraints.max_carbs
        assert simple_constraints.min_fat <= summary.total_fat <= simple_constraints.max_fat
        
        # Verify constraint satisfaction
        satisfaction = result.constraint_satisfaction
        assert satisfaction.calories_within_bounds
        assert satisfaction.protein_within_bounds
        assert satisfaction.carbs_within_bounds
        assert satisfaction.fat_within_bounds
    
    def test_mathematical_accuracy(self, optimizer, simple_foods, simple_constraints):
        """Test mathematical accuracy of the optimization."""
        result = optimizer.optimize(simple_foods, simple_constraints)
        
        # Manually calculate nutritional totals from optimal quantities
        calculated_calories = 0
        calculated_protein = 0
        calculated_carbs = 0
        calculated_fat = 0
        calculated_cost = 0
        
        for optimal_food in result.optimal_quantities:
            # Find corresponding food
            food = next(f for f in simple_foods if f.name == optimal_food.food_name)
            quantity = optimal_food.quantity_100g
            
            calculated_calories += quantity * food.calories_per_100g
            calculated_protein += quantity * food.protein_per_100g
            calculated_carbs += quantity * food.carbs_per_100g
            calculated_fat += quantity * food.fat_per_100g
            calculated_cost += quantity * food.cost_per_100g
        
        # Check calculations match (within tolerance)
        tolerance = 0.01  # More reasonable tolerance for floating point operations
        assert abs(calculated_calories - result.nutritional_summary.total_calories) < tolerance
        assert abs(calculated_protein - result.nutritional_summary.total_protein) < tolerance
        assert abs(calculated_carbs - result.nutritional_summary.total_carbs) < tolerance
        assert abs(calculated_fat - result.nutritional_summary.total_fat) < tolerance
        assert abs(calculated_cost - result.total_cost) < tolerance
    
    def test_cost_minimization(self, optimizer):
        """Test that the optimizer actually minimizes cost."""
        # Create foods with obvious cost differences
        foods = [
            Food(
                name="Expensive Food",
                cost_per_100g=10.0,
                calories_per_100g=100,
                carbs_per_100g=20,
                protein_per_100g=10,
                fat_per_100g=5,
                vitamin_a_per_100g=50,
                vitamin_c_per_100g=10,
                vitamin_d_per_100g=0,
                calcium_per_100g=50,
                iron_per_100g=2,
                magnesium_per_100g=20,
                potassium_per_100g=300,
                sodium_per_100g=100,
                cholesterol_per_100g=20
            ),
            Food(
                name="Cheap Food",
                cost_per_100g=1.0,
                calories_per_100g=100,
                carbs_per_100g=20,
                protein_per_100g=10,
                fat_per_100g=5,
                vitamin_a_per_100g=50,
                vitamin_c_per_100g=10,
                vitamin_d_per_100g=0,
                calcium_per_100g=50,
                iron_per_100g=2,
                magnesium_per_100g=20,
                potassium_per_100g=300,
                sodium_per_100g=100,
                cholesterol_per_100g=20
            )
        ]
        
        constraints = NutritionalConstraints(
            min_calories=100,
            max_calories=200,
            min_protein=10,
            max_protein=20,
            min_carbs=20,
            max_carbs=40,
            min_fat=5,
            max_fat=10,
            min_vitamin_a=50,
            max_vitamin_a=100,
            min_vitamin_c=10,
            max_vitamin_c=20,
            min_calcium=50,
            max_calcium=100,
            min_iron=2,
            max_iron=5,
            min_magnesium=30,
            max_magnesium=60,
            min_potassium=300,
            max_potassium=600,
            min_sodium=100,
            max_sodium=200,
            min_cholesterol=0,
            max_cholesterol=50
        )
        
        result = optimizer.optimize(foods, constraints)
        
        # Should prefer the cheap food
        cheap_food_quantity = 0
        expensive_food_quantity = 0
        
        for optimal_food in result.optimal_quantities:
            if optimal_food.food_name == "Cheap Food":
                cheap_food_quantity = optimal_food.quantity_100g
            elif optimal_food.food_name == "Expensive Food":
                expensive_food_quantity = optimal_food.quantity_100g
        
        # Should use more cheap food than expensive food
        assert cheap_food_quantity > expensive_food_quantity
    
    def test_infeasible_problem(self, optimizer):
        """Test handling of infeasible optimization problems."""
        # Create impossible constraints
        foods = [
            Food(
                name="Low Nutrient Food",
                cost_per_100g=1.0,
                calories_per_100g=10,
                carbs_per_100g=1,
                protein_per_100g=1,
                fat_per_100g=0.1,
                vitamin_a_per_100g=1,
                vitamin_c_per_100g=0.1,
                vitamin_d_per_100g=0,
                calcium_per_100g=1,
                iron_per_100g=0.1,
                magnesium_per_100g=2,
                potassium_per_100g=10,
                sodium_per_100g=1,
                cholesterol_per_100g=0
            )
        ]
        
        constraints = NutritionalConstraints(
            min_calories=1000,  # Impossible with available food
            max_calories=1200,
            min_protein=100,
            max_protein=150,
            min_carbs=50,
            max_carbs=100,
            min_fat=20,
            max_fat=30,
            min_vitamin_a=500,
            max_vitamin_a=1000,
            min_vitamin_c=50,
            max_vitamin_c=100,
            min_calcium=500,
            max_calcium=1000,
            min_iron=10,
            max_iron=20,
            min_magnesium=100,
            max_magnesium=200,
            min_potassium=2000,
            max_potassium=4000,
            min_sodium=500,
            max_sodium=1000,
            min_cholesterol=0,
            max_cholesterol=100
        )
        
        with pytest.raises(InfeasibleProblemError):
            optimizer.optimize(foods, constraints)
    
    def test_input_validation(self, optimizer):
        """Test input validation in the optimizer."""
        valid_foods = [
            Food(
                name="Test Food",
                cost_per_100g=1.0,
                calories_per_100g=100,
                carbs_per_100g=20,
                protein_per_100g=10,
                fat_per_100g=5,
                vitamin_a_per_100g=25,
                vitamin_c_per_100g=5,
                vitamin_d_per_100g=0,
                calcium_per_100g=30,
                iron_per_100g=1.5,
                magnesium_per_100g=25,
                potassium_per_100g=200,
                sodium_per_100g=80,
                cholesterol_per_100g=15
            )
        ]
        
        valid_constraints = NutritionalConstraints(
            min_calories=50,
            max_calories=150,
            min_protein=5,
            max_protein=15,
            min_carbs=10,
            max_carbs=30,
            min_fat=2,
            max_fat=8,
            min_vitamin_a=20,
            max_vitamin_a=50,
            min_vitamin_c=3,
            max_vitamin_c=10,
            min_calcium=25,
            max_calcium=60,
            min_iron=1,
            max_iron=3,
            min_magnesium=20,
            max_magnesium=40,
            min_potassium=150,
            max_potassium=400,
            min_sodium=50,
            max_sodium=150,
            min_cholesterol=0,
            max_cholesterol=30
        )
        
        # Test with too many foods (mock the setting)
        with patch('app.services.optimizer.settings.max_foods', 1):
            too_many_foods = valid_foods * 2
            with pytest.raises(OptimizationError):
                optimizer.optimize(too_many_foods, valid_constraints)
    
    def test_zero_nutrient_validation(self, optimizer):
        """Test validation when foods provide zero nutrients."""
        # Foods with zero nutrients
        foods = [
            Food(
                name="Zero Calories",
                cost_per_100g=1.0,
                calories_per_100g=0,  # Zero calories
                carbs_per_100g=0,
                protein_per_100g=0,
                fat_per_100g=0,
                vitamin_a_per_100g=0,
                vitamin_c_per_100g=0,
                vitamin_d_per_100g=0,
                calcium_per_100g=0,
                iron_per_100g=0,
                magnesium_per_100g=0,
                potassium_per_100g=0,
                sodium_per_100g=0,
                cholesterol_per_100g=0
            )
        ]
        
        constraints = NutritionalConstraints(
            min_calories=100,  # Need calories but no food provides them
            max_calories=200,
            min_protein=0,
            max_protein=10,
            min_carbs=0,
            max_carbs=20,
            min_fat=0,
            max_fat=5,
            min_vitamin_a=0,
            max_vitamin_a=50,
            min_vitamin_c=0,
            max_vitamin_c=25,
            min_calcium=0,
            max_calcium=100,
            min_iron=0,
            max_iron=5,
            min_magnesium=0,
            max_magnesium=10,
            min_potassium=0,
            max_potassium=1000,
            min_sodium=0,
            max_sodium=500,
            min_cholesterol=0,
            max_cholesterol=50
        )
        
        with pytest.raises(InfeasibleProblemError):
            optimizer.optimize(foods, constraints)
    
    @patch('app.services.optimizer.linprog')
    def test_solver_timeout_handling(self, mock_linprog, optimizer, simple_foods, simple_constraints):
        """Test handling of solver timeout."""
        # Mock solver timeout
        mock_result = Mock()
        mock_result.success = False
        mock_result.message = "Time limit reached"
        mock_linprog.return_value = mock_result
        
        with pytest.raises(SolverTimeoutError):
            optimizer.optimize(simple_foods, simple_constraints)
    
    @patch('app.services.optimizer.linprog')
    def test_unbounded_problem_handling(self, mock_linprog, optimizer, simple_foods, simple_constraints):
        """Test handling of unbounded problems."""
        # Mock unbounded result
        mock_result = Mock()
        mock_result.success = False
        mock_result.message = "Problem is unbounded"
        mock_linprog.return_value = mock_result
        
        with pytest.raises(UnboundedProblemError):
            optimizer.optimize(simple_foods, simple_constraints)
    
    def test_problem_matrix_preparation(self, optimizer, simple_foods, simple_constraints):
        """Test the linear programming matrix preparation."""
        # This tests the internal _prepare_problem method
        c, A_ub, b_ub, A_eq, b_eq, bounds = optimizer._prepare_problem(simple_foods, simple_constraints)
        
        # Check dimensions
        n_foods = len(simple_foods)
        assert len(c) == n_foods
        assert A_ub.shape[1] == n_foods
        assert len(bounds) == n_foods
        
        # Check that all costs are positive (objective coefficients)
        assert all(cost > 0 for cost in c)
        
        # Check bounds are non-negative
        assert all(bound[0] == 0.0 for bound in bounds)
        assert all(bound[1] is None for bound in bounds)
        
        # Check constraint matrix structure
        # Should have 24 constraints (12 nutrients × 2 bounds each)
        assert A_ub.shape[0] == 24
        assert len(b_ub) == 24
    
    def test_result_processing_accuracy(self, optimizer, simple_foods, simple_constraints):
        """Test that result processing maintains numerical accuracy."""
        result = optimizer.optimize(simple_foods, simple_constraints)
        
        # Check that quantities are properly rounded but maintain accuracy
        total_cost_check = sum(
            optimal_food.quantity_100g * next(
                food.cost_per_100g for food in simple_foods 
                if food.name == optimal_food.food_name
            )
            for optimal_food in result.optimal_quantities
        )
        
        # Should match within rounding precision
        assert abs(total_cost_check - result.total_cost) < 0.01
        
        # Check that grams conversion is correct
        for optimal_food in result.optimal_quantities:
            expected_grams = optimal_food.quantity_100g * 100
            assert abs(optimal_food.quantity_grams - expected_grams) < 0.01
    
    def test_constraint_boundary_conditions(self, optimizer):
        """Test optimization at constraint boundaries."""
        # Create a scenario where solution should be at boundaries
        foods = [
            Food(
                name="Perfect Food",
                cost_per_100g=1.0,
                calories_per_100g=200,
                carbs_per_100g=25,
                protein_per_100g=25,
                fat_per_100g=10,
                vitamin_a_per_100g=100,
                vitamin_c_per_100g=20,
                vitamin_d_per_100g=0,
                calcium_per_100g=50,
                iron_per_100g=5,
                magnesium_per_100g=50,
                potassium_per_100g=500,
                sodium_per_100g=100,
                cholesterol_per_100g=25
            )
        ]
        
        # Tight constraints that should result in boundary solution
        constraints = NutritionalConstraints(
            min_calories=200,
            max_calories=200.1,  # Very close to boundary
            min_protein=25,
            max_protein=25.1,    # Very close to boundary
            min_carbs=25,
            max_carbs=25.1,      # Very close to boundary
            min_fat=10,
            max_fat=10.1,        # Very close to boundary
            min_vitamin_a=100,
            max_vitamin_a=100.1,
            min_vitamin_c=20,
            max_vitamin_c=20.1,
            min_calcium=50,
            max_calcium=50.1,
            min_iron=5,
            max_iron=5.1,
            min_magnesium=50,
            max_magnesium=50.1,
            min_potassium=500,
            max_potassium=500.1,
            min_sodium=100,
            max_sodium=100.1,
            min_cholesterol=25,
            max_cholesterol=25.1
        )
        
        result = optimizer.optimize(foods, constraints)
        
        # Should find solution at exactly 1 unit (100g) of the food
        assert len(result.optimal_quantities) == 1
        assert abs(result.optimal_quantities[0].quantity_100g - 1.0) < 0.01
        
        # All constraints should be satisfied very closely
        assert abs(result.nutritional_summary.total_calories - 200) < 0.1
        assert abs(result.nutritional_summary.total_protein - 25) < 0.1
        assert abs(result.nutritional_summary.total_carbs - 25) < 0.1
        assert abs(result.nutritional_summary.total_fat - 10) < 0.1