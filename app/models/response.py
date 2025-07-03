"""Response models for the Diet Optimizer API."""

from typing import List, Literal
from pydantic import BaseModel, Field


class OptimalFood(BaseModel):
    """Model for an optimized food item with quantities and cost."""
    
    food_name: str = Field(..., description="Name of the food item")
    quantity_100g: float = Field(..., ge=0, description="Amount in 100-gram units")
    quantity_grams: float = Field(..., ge=0, description="Total grams of this food")
    cost: float = Field(..., ge=0, description="Cost contribution of this food")


class NutritionalSummary(BaseModel):
    """Model for total nutritional content achieved."""
    
    total_calories: float = Field(..., ge=0, description="Total calories achieved")
    total_protein: float = Field(..., ge=0, description="Total protein achieved (grams)")
    total_carbs: float = Field(..., ge=0, description="Total carbohydrates achieved (grams)")
    total_fat: float = Field(..., ge=0, description="Total fat achieved (grams)")


class ConstraintSatisfaction(BaseModel):
    """Model for constraint satisfaction status."""
    
    calories_within_bounds: bool = Field(..., description="Whether calories are within bounds")
    protein_within_bounds: bool = Field(..., description="Whether protein is within bounds")
    carbs_within_bounds: bool = Field(..., description="Whether carbs are within bounds")
    fat_within_bounds: bool = Field(..., description="Whether fat is within bounds")


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