"""Response models for the Diet Optimizer API."""

from typing import List, Literal
from pydantic import BaseModel, Field, ConfigDict


class OptimalFood(BaseModel):
    """Model for an optimized food item with quantities and cost."""
    
    food_name: str = Field(..., description="Name of the food item")
    quantity_100g: float = Field(..., ge=0, description="Amount in 100-gram units")
    quantity_grams: float = Field(..., ge=0, description="Total grams of this food")
    cost: float = Field(..., ge=0, description="Cost contribution of this food")


class NutritionalSummary(BaseModel):
    """Model for total nutritional content achieved.
    
    Units follow standard nutritional conventions:
    - Macronutrients: grams (g)
    - Vitamin A: micrograms RAE (mcg)
    - Other nutrients: milligrams (mg)
    """
    
    total_calories: float = Field(..., ge=0, description="Total calories achieved")
    total_protein: float = Field(..., ge=0, description="Total protein achieved (g)")
    total_carbs: float = Field(..., ge=0, description="Total carbohydrates achieved (g)")
    total_fat: float = Field(..., ge=0, description="Total fat achieved (g)")
    total_vitamin_a: float = Field(
        ..., 
        ge=0, 
        description="Total vitamin A achieved (mcg RAE - Retinol Activity Equivalents)"
    )
    total_vitamin_c: float = Field(..., ge=0, description="Total vitamin C achieved (mg)")
    total_calcium: float = Field(..., ge=0, description="Total calcium achieved (mg)")
    total_iron: float = Field(..., ge=0, description="Total iron achieved (mg)")
    total_magnesium: float = Field(..., ge=0, description="Total magnesium achieved (mg)")
    total_potassium: float = Field(..., ge=0, description="Total potassium achieved (mg)")
    total_sodium: float = Field(..., ge=0, description="Total sodium achieved (mg)")
    total_cholesterol: float = Field(..., ge=0, description="Total cholesterol achieved (mg)")


class ConstraintSatisfaction(BaseModel):
    """Model for constraint satisfaction status."""
    
    calories_within_bounds: bool = Field(..., description="Whether calories are within bounds")
    protein_within_bounds: bool = Field(..., description="Whether protein is within bounds")
    carbs_within_bounds: bool = Field(..., description="Whether carbs are within bounds")
    fat_within_bounds: bool = Field(..., description="Whether fat is within bounds")
    vitamin_a_within_bounds: bool = Field(..., description="Whether vitamin A is within bounds")
    vitamin_c_within_bounds: bool = Field(..., description="Whether vitamin C is within bounds")
    calcium_within_bounds: bool = Field(..., description="Whether calcium is within bounds")
    iron_within_bounds: bool = Field(..., description="Whether iron is within bounds")
    magnesium_within_bounds: bool = Field(..., description="Whether magnesium is within bounds")
    potassium_within_bounds: bool = Field(..., description="Whether potassium is within bounds")
    sodium_within_bounds: bool = Field(..., description="Whether sodium is within bounds")
    cholesterol_within_bounds: bool = Field(..., description="Whether cholesterol is within bounds")


class OptimizationResult(BaseModel):
    """Complete optimization result model."""
    
    status: Literal["optimal", "infeasible", "unbounded"] = Field(
        ..., description="Optimization status"
    )
    total_cost: float = Field(..., ge=0, description="Minimum total cost achieved")
    optimal_quantities: List[OptimalFood] = Field(
        ..., description="Quantities of each food (in 100g units)"
    )
    nutritional_summary: NutritionalSummary = Field(
        ..., description="Total nutritional content achieved"
    )
    constraint_satisfaction: ConstraintSatisfaction = Field(
        ..., description="Whether each constraint is met"
    )


class HealthCheckResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="API status")
    version: str = Field(..., description="API version")
    message: str = Field(..., description="Status message")