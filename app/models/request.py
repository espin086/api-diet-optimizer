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
    vitamin_a_per_100g: float = Field(..., ge=0, description="Vitamin A per 100 grams (in mcg RAE)")
    vitamin_c_per_100g: float = Field(..., ge=0, description="Vitamin C per 100 grams (in mg)")
    calcium_per_100g: float = Field(..., ge=0, description="Calcium per 100 grams (in mg)")
    iron_per_100g: float = Field(..., ge=0, description="Iron per 100 grams (in mg)")
    potassium_per_100g: float = Field(..., ge=0, description="Potassium per 100 grams (in mg)")
    sodium_per_100g: float = Field(..., ge=0, description="Sodium per 100 grams (in mg)")
    cholesterol_per_100g: float = Field(..., ge=0, description="Cholesterol per 100 grams (in mg)")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that food name is not empty."""
        if not v.strip():
            raise ValueError('Food name cannot be empty')
        return v.strip()


class NutritionalConstraints(BaseModel):
    """Model for nutritional constraints (min/max bounds for each nutrient)."""
    
    min_calories: float = Field(..., ge=0, description="Minimum daily calories required")
    max_calories: float = Field(..., gt=0, description="Maximum daily calories allowed")
    min_protein: float = Field(..., ge=0, description="Minimum daily protein required (grams)")
    max_protein: float = Field(..., gt=0, description="Maximum daily protein allowed (grams)")
    min_carbs: float = Field(..., ge=0, description="Minimum daily carbohydrates required (grams)")
    max_carbs: float = Field(..., gt=0, description="Maximum daily carbohydrates allowed (grams)")
    min_fat: float = Field(..., ge=0, description="Minimum daily fat required (grams)")
    max_fat: float = Field(..., gt=0, description="Maximum daily fat allowed (grams)")
    min_vitamin_a: float = Field(..., ge=0, description="Minimum daily vitamin A required (mcg RAE)")
    max_vitamin_a: float = Field(..., gt=0, description="Maximum daily vitamin A allowed (mcg RAE)")
    min_vitamin_c: float = Field(..., ge=0, description="Minimum daily vitamin C required (mg)")
    max_vitamin_c: float = Field(..., gt=0, description="Maximum daily vitamin C allowed (mg)")
    min_calcium: float = Field(..., ge=0, description="Minimum daily calcium required (mg)")
    max_calcium: float = Field(..., gt=0, description="Maximum daily calcium allowed (mg)")
    min_iron: float = Field(..., ge=0, description="Minimum daily iron required (mg)")
    max_iron: float = Field(..., gt=0, description="Maximum daily iron allowed (mg)")
    min_potassium: float = Field(..., ge=0, description="Minimum daily potassium required (mg)")
    max_potassium: float = Field(..., gt=0, description="Maximum daily potassium allowed (mg)")
    min_sodium: float = Field(..., ge=0, description="Minimum daily sodium required (mg)")
    max_sodium: float = Field(..., gt=0, description="Maximum daily sodium allowed (mg)")
    min_cholesterol: float = Field(..., ge=0, description="Minimum daily cholesterol required (mg)")
    max_cholesterol: float = Field(..., gt=0, description="Maximum daily cholesterol allowed (mg)")

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

    @field_validator('max_vitamin_a')
    @classmethod
    def validate_vitamin_a_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_a > min_vitamin_a."""
        if info.data.get('min_vitamin_a') is not None and v <= info.data['min_vitamin_a']:
            raise ValueError('max_vitamin_a must be greater than min_vitamin_a')
        return v

    @field_validator('max_vitamin_c')
    @classmethod
    def validate_vitamin_c_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_c > min_vitamin_c."""
        if info.data.get('min_vitamin_c') is not None and v <= info.data['min_vitamin_c']:
            raise ValueError('max_vitamin_c must be greater than min_vitamin_c')
        return v

    @field_validator('max_calcium')
    @classmethod
    def validate_calcium_bounds(cls, v: float, info) -> float:
        """Validate that max_calcium > min_calcium."""
        if info.data.get('min_calcium') is not None and v <= info.data['min_calcium']:
            raise ValueError('max_calcium must be greater than min_calcium')
        return v

    @field_validator('max_iron')
    @classmethod
    def validate_iron_bounds(cls, v: float, info) -> float:
        """Validate that max_iron > min_iron."""
        if info.data.get('min_iron') is not None and v <= info.data['min_iron']:
            raise ValueError('max_iron must be greater than min_iron')
        return v

    @field_validator('max_potassium')
    @classmethod
    def validate_potassium_bounds(cls, v: float, info) -> float:
        """Validate that max_potassium > min_potassium."""
        if info.data.get('min_potassium') is not None and v <= info.data['min_potassium']:
            raise ValueError('max_potassium must be greater than min_potassium')
        return v

    @field_validator('max_sodium')
    @classmethod
    def validate_sodium_bounds(cls, v: float, info) -> float:
        """Validate that max_sodium > min_sodium."""
        if info.data.get('min_sodium') is not None and v <= info.data['min_sodium']:
            raise ValueError('max_sodium must be greater than min_sodium')
        return v

    @field_validator('max_cholesterol')
    @classmethod
    def validate_cholesterol_bounds(cls, v: float, info) -> float:
        """Validate that max_cholesterol > min_cholesterol."""
        if info.data.get('min_cholesterol') is not None and v <= info.data['min_cholesterol']:
            raise ValueError('max_cholesterol must be greater than min_cholesterol')
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