"""Optimization service for solving the diet problem using linear programming."""

import numpy as np
from scipy.optimize import linprog
from typing import List, Tuple, Sequence, Optional
import logging

from app.models.request import Food, NutritionalConstraints
from app.models.response import (
    OptimizationResult, 
    OptimalFood, 
    NutritionalSummary, 
    ConstraintSatisfaction
)
from app.core.exceptions import (
    InfeasibleProblemError, 
    UnboundedProblemError, 
    OptimizationError,
    SolverTimeoutError
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class DietOptimizer:
    """Linear programming optimizer for the diet problem."""
    
    def __init__(self):
        """Initialize the optimizer."""
        self.tolerance = 1e-6
    
    def optimize(self, foods: List[Food], constraints: NutritionalConstraints) -> OptimizationResult:
        """
        Solve the diet optimization problem using linear programming.
        
        Args:
            foods: List of available foods with nutritional data
            constraints: Nutritional constraints (min/max bounds)
            
        Returns:
            OptimizationResult: The optimal solution or error status
            
        Raises:
            OptimizationError: If optimization fails
        """
        try:
            logger.info(f"Starting optimization with {len(foods)} foods")
            
            # Validate inputs
            self._validate_inputs(foods, constraints)
            
            # Prepare the linear programming problem
            c, A_ub, b_ub, A_eq, b_eq, bounds = self._prepare_problem(foods, constraints)
            
            # Solve the optimization problem
            result = linprog(
                c=c,
                A_ub=A_ub,
                b_ub=b_ub,
                A_eq=A_eq,
                b_eq=b_eq,
                bounds=bounds,
                method='highs',
                options={'maxiter': 10000, 'time_limit': settings.solver_timeout}
            )
            
            # Process the result
            return self._process_result(result, foods, constraints)
            
        except (InfeasibleProblemError, UnboundedProblemError, SolverTimeoutError):
            raise
        except Exception as e:
            logger.exception(f"Unexpected error during optimization: {e}")
            raise OptimizationError(f"Optimization failed: {str(e)}")
    
    def _validate_inputs(self, foods: List[Food], constraints: NutritionalConstraints) -> None:
        """Validate input data before optimization."""
        if len(foods) > settings.max_foods:
            raise OptimizationError(f"Too many foods: {len(foods)} > {settings.max_foods}")
        
        # Check if any food can theoretically meet minimum requirements
        max_calories = max(food.calories_per_100g for food in foods)
        max_protein = max(food.protein_per_100g for food in foods)
        max_carbs = max(food.carbs_per_100g for food in foods)
        max_fat = max(food.fat_per_100g for food in foods)
        max_vitamin_a = max(food.vitamin_a_per_100g for food in foods)
        max_vitamin_c = max(food.vitamin_c_per_100g for food in foods)
        max_calcium = max(food.calcium_per_100g for food in foods)
        max_iron = max(food.iron_per_100g for food in foods)
        max_potassium = max(food.potassium_per_100g for food in foods)
        max_sodium = max(food.sodium_per_100g for food in foods)
        max_cholesterol = max(food.cholesterol_per_100g for food in foods)
        
        if (max_calories == 0 and constraints.min_calories > 0) or \
           (max_protein == 0 and constraints.min_protein > 0) or \
           (max_carbs == 0 and constraints.min_carbs > 0) or \
           (max_fat == 0 and constraints.min_fat > 0) or \
           (max_vitamin_a == 0 and constraints.min_vitamin_a > 0) or \
           (max_vitamin_c == 0 and constraints.min_vitamin_c > 0) or \
           (max_calcium == 0 and constraints.min_calcium > 0) or \
           (max_iron == 0 and constraints.min_iron > 0) or \
           (max_potassium == 0 and constraints.min_potassium > 0) or \
           (max_sodium == 0 and constraints.min_sodium > 0) or \
           (max_cholesterol == 0 and constraints.min_cholesterol > 0):
            raise InfeasibleProblemError(
                "No food provides the required nutrients to meet minimum constraints"
            )
    
    def _prepare_problem(
        self, 
        foods: List[Food], 
        constraints: NutritionalConstraints
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, Optional[np.ndarray], Optional[np.ndarray], Sequence[Tuple[float, Optional[float]]]]:
        """
        Prepare the linear programming problem matrices.
        
        Variables: x[i] = quantity of food i (in 100g units)
        Objective: minimize sum(cost_per_100g[i] * x[i])
        
        Constraints:
        - min_calories <= sum(calories_per_100g[i] * x[i]) <= max_calories
        - min_protein <= sum(protein_per_100g[i] * x[i]) <= max_protein
        - min_carbs <= sum(carbs_per_100g[i] * x[i]) <= max_carbs
        - min_fat <= sum(fat_per_100g[i] * x[i]) <= max_fat
        - min_vitamin_a <= sum(vitamin_a_per_100g[i] * x[i]) <= max_vitamin_a
        - min_vitamin_c <= sum(vitamin_c_per_100g[i] * x[i]) <= max_vitamin_c
        - min_calcium <= sum(calcium_per_100g[i] * x[i]) <= max_calcium
        - min_iron <= sum(iron_per_100g[i] * x[i]) <= max_iron
        - min_potassium <= sum(potassium_per_100g[i] * x[i]) <= max_potassium
        - min_sodium <= sum(sodium_per_100g[i] * x[i]) <= max_sodium
        - min_cholesterol <= sum(cholesterol_per_100g[i] * x[i]) <= max_cholesterol
        - x[i] >= 0 for all i
        """
        n_foods = len(foods)
        
        # Objective function coefficients (minimize cost)
        c = np.array([food.cost_per_100g for food in foods])
        
        # Nutritional content matrix (11 nutrients)
        nutrition_matrix = np.array([
            [food.calories_per_100g for food in foods],
            [food.protein_per_100g for food in foods],
            [food.carbs_per_100g for food in foods],
            [food.fat_per_100g for food in foods],
            [food.vitamin_a_per_100g for food in foods],
            [food.vitamin_c_per_100g for food in foods],
            [food.calcium_per_100g for food in foods],
            [food.iron_per_100g for food in foods],
            [food.potassium_per_100g for food in foods],
            [food.sodium_per_100g for food in foods],
            [food.cholesterol_per_100g for food in foods]
        ])
        
        # Inequality constraints (A_ub * x <= b_ub)
        # We need both upper and lower bounds, so we convert:
        # min_val <= nutrition <= max_val becomes:
        # -nutrition <= -min_val and nutrition <= max_val
        A_ub = np.vstack([
            -nutrition_matrix,  # For lower bounds (negated)
            nutrition_matrix    # For upper bounds
        ])
        
        b_ub = np.array([
            -constraints.min_calories,
            -constraints.min_protein, 
            -constraints.min_carbs,
            -constraints.min_fat,
            -constraints.min_vitamin_a,
            -constraints.min_vitamin_c,
            -constraints.min_calcium,
            -constraints.min_iron,
            -constraints.min_potassium,
            -constraints.min_sodium,
            -constraints.min_cholesterol,
            constraints.max_calories,
            constraints.max_protein,
            constraints.max_carbs,
            constraints.max_fat,
            constraints.max_vitamin_a,
            constraints.max_vitamin_c,
            constraints.max_calcium,
            constraints.max_iron,
            constraints.max_potassium,
            constraints.max_sodium,
            constraints.max_cholesterol
        ])
        
        # No equality constraints for this problem
        A_eq = None
        b_eq = None
        
        # Variable bounds (all quantities must be non-negative)
        bounds = [(0.0, None) for _ in range(n_foods)]
        
        return c, A_ub, b_ub, A_eq, b_eq, bounds
    
    def _process_result(
        self, 
        result, 
        foods: List[Food], 
        constraints: NutritionalConstraints
    ) -> OptimizationResult:
        """Process the optimization result and create response."""
        
        if not result.success:
            if result.message and "infeasible" in result.message.lower():
                raise InfeasibleProblemError()
            elif result.message and "unbounded" in result.message.lower():
                raise UnboundedProblemError()
            elif result.message and "time" in result.message.lower():
                raise SolverTimeoutError(settings.solver_timeout)
            else:
                raise OptimizationError(f"Solver failed: {result.message}")
        
        # Extract solution
        quantities = result.x
        total_cost = result.fun
        
        logger.info(f"Optimization successful. Total cost: {total_cost:.2f}")
        
        # Calculate nutritional totals
        total_calories = sum(q * food.calories_per_100g for q, food in zip(quantities, foods))
        total_protein = sum(q * food.protein_per_100g for q, food in zip(quantities, foods))
        total_carbs = sum(q * food.carbs_per_100g for q, food in zip(quantities, foods))
        total_fat = sum(q * food.fat_per_100g for q, food in zip(quantities, foods))
        total_vitamin_a = sum(q * food.vitamin_a_per_100g for q, food in zip(quantities, foods))
        total_vitamin_c = sum(q * food.vitamin_c_per_100g for q, food in zip(quantities, foods))
        total_calcium = sum(q * food.calcium_per_100g for q, food in zip(quantities, foods))
        total_iron = sum(q * food.iron_per_100g for q, food in zip(quantities, foods))
        total_potassium = sum(q * food.potassium_per_100g for q, food in zip(quantities, foods))
        total_sodium = sum(q * food.sodium_per_100g for q, food in zip(quantities, foods))
        total_cholesterol = sum(q * food.cholesterol_per_100g for q, food in zip(quantities, foods))
        
        # Create optimal food list (only include foods with non-zero quantities)
        optimal_foods = []
        for i, (quantity, food) in enumerate(zip(quantities, foods)):
            if quantity > self.tolerance:  # Only include significant quantities
                optimal_foods.append(OptimalFood(
                    food_name=food.name,
                    quantity_100g=round(quantity, 4),
                    quantity_grams=round(quantity * 100, 2),
                    cost=round(quantity * food.cost_per_100g, 2)
                ))
        
        # Create nutritional summary
        nutritional_summary = NutritionalSummary(
            total_calories=round(total_calories, 2),
            total_protein=round(total_protein, 2),
            total_carbs=round(total_carbs, 2),
            total_fat=round(total_fat, 2),
            total_vitamin_a=round(total_vitamin_a, 2),
            total_vitamin_c=round(total_vitamin_c, 2),
            total_calcium=round(total_calcium, 2),
            total_iron=round(total_iron, 2),
            total_potassium=round(total_potassium, 2),
            total_sodium=round(total_sodium, 2),
            total_cholesterol=round(total_cholesterol, 2)
        )
        
        # Check constraint satisfaction
        constraint_satisfaction = ConstraintSatisfaction(
            calories_within_bounds=constraints.min_calories <= total_calories <= constraints.max_calories,
            protein_within_bounds=constraints.min_protein <= total_protein <= constraints.max_protein,
            carbs_within_bounds=constraints.min_carbs <= total_carbs <= constraints.max_carbs,
            fat_within_bounds=constraints.min_fat <= total_fat <= constraints.max_fat,
            vitamin_a_within_bounds=constraints.min_vitamin_a <= total_vitamin_a <= constraints.max_vitamin_a,
            vitamin_c_within_bounds=constraints.min_vitamin_c <= total_vitamin_c <= constraints.max_vitamin_c,
            calcium_within_bounds=constraints.min_calcium <= total_calcium <= constraints.max_calcium,
            iron_within_bounds=constraints.min_iron <= total_iron <= constraints.max_iron,
            potassium_within_bounds=constraints.min_potassium <= total_potassium <= constraints.max_potassium,
            sodium_within_bounds=constraints.min_sodium <= total_sodium <= constraints.max_sodium,
            cholesterol_within_bounds=constraints.min_cholesterol <= total_cholesterol <= constraints.max_cholesterol
        )
        
        return OptimizationResult(
            status="optimal",
            total_cost=round(total_cost, 2),
            optimal_quantities=optimal_foods,
            nutritional_summary=nutritional_summary,
            constraint_satisfaction=constraint_satisfaction
        )