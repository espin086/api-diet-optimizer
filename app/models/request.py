"""Request models for the Diet Optimizer API."""

from typing import List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Food(BaseModel):
    """Model for a food item with nutritional information and cost."""
    
    name: str = Field(..., description="Name of the food item")
    cost_per_100g: float = Field(..., gt=0, description="Cost per 100 grams (in currency units)")
    calories_per_100g: float = Field(..., ge=0, description="Calories per 100 grams")
    carbs_per_100g: float = Field(..., ge=0, description="Carbohydrates per 100 grams (in grams)")
    protein_per_100g: float = Field(..., ge=0, description="Protein per 100 grams (in grams)")
    fat_per_100g: float = Field(..., ge=0, description="Fat per 100 grams (in grams)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that food name is not empty."""
        if not v.strip():
            raise ValueError('Food name cannot be empty')
        return v.strip()


class NutritionalConstraints(BaseModel):
    """Model for nutritional constraints (min/max bounds for each macronutrient)."""
    
    min_calories: float = Field(..., ge=0, description="Minimum daily calories required")
    max_calories: float = Field(..., gt=0, description="Maximum daily calories allowed")
    min_protein: float = Field(..., ge=0, description="Minimum daily protein required (grams)")
    max_protein: float = Field(..., gt=0, description="Maximum daily protein allowed (grams)")
    min_carbs: float = Field(..., ge=0, description="Minimum daily carbohydrates required (grams)")
    max_carbs: float = Field(..., gt=0, description="Maximum daily carbohydrates allowed (grams)")
    min_fat: float = Field(..., ge=0, description="Minimum daily fat required (grams)")
    max_fat: float = Field(..., gt=0, description="Maximum daily fat allowed (grams)")

    @field_validator('max_calories')
    @classmethod
    def validate_calories_bounds(cls, v: float, info) -> float:
        """Validate that max_calories > min_calories."""
        if info.data.get('min_calories') is not None and v <= info.data['min_calories']:
            raise ValueError('max_calories must be greater than min_calories')
        return v

    @field_validator('max_protein')
    @classmethod
    def validate_protein_bounds(cls, v: float, info) -> float:
        """Validate that max_protein > min_protein."""
        if info.data.get('min_protein') is not None and v <= info.data['min_protein']:
            raise ValueError('max_protein must be greater than min_protein')
        return v

    @field_validator('max_carbs')
    @classmethod
    def validate_carbs_bounds(cls, v: float, info) -> float:
        """Validate that max_carbs > min_carbs."""
        if info.data.get('min_carbs') is not None and v <= info.data['min_carbs']:
            raise ValueError('max_carbs must be greater than min_carbs')
        return v

    @field_validator('max_fat')
    @classmethod
    def validate_fat_bounds(cls, v: float, info) -> float:
        """Validate that max_fat > min_fat."""
        if info.data.get('min_fat') is not None and v <= info.data['min_fat']:
            raise ValueError('max_fat must be greater than min_fat')
        return v


class OptimizationRequest(BaseModel):
    """Complete optimization request model."""
    
    foods: List[Food] = Field(..., min_length=1, description="List of available foods")
    constraints: NutritionalConstraints = Field(..., description="Nutritional constraints")

    @field_validator('foods')
    @classmethod
    def validate_foods_unique(cls, v: List[Food]) -> List[Food]:
        """Validate that food names are unique."""
        food_names = [food.name.lower() for food in v]
        if len(food_names) != len(set(food_names)):
            raise ValueError('Food names must be unique (case-insensitive)')
        return v