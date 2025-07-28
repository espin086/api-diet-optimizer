"""Request models for the Diet Optimizer API."""

from typing import List
from pydantic import BaseModel, Field, field_validator, ConfigDict


class Food(BaseModel):
    """Model for a food item with nutritional information and cost.
    
    All nutritional values are per 100g serving size.
    Units follow standard nutritional labeling conventions:
    - Macronutrients (protein, carbs, fat): grams (g)
    - Vitamin A: micrograms RAE (mcg)
    - Other vitamins and minerals: milligrams (mg)
    - Fiber: grams (g)
    """
    
    name: str = Field(..., description="Name of the food item")
    cost_per_100g: float = Field(..., gt=0, description="Cost per 100 grams (in currency units)")
    calories_per_100g: float = Field(..., ge=0, description="Calories per 100 grams")
    carbs_per_100g: float = Field(..., ge=0, description="Carbohydrates per 100 grams (g)")
    protein_per_100g: float = Field(..., ge=0, description="Protein per 100 grams (g)")
    fat_per_100g: float = Field(..., ge=0, description="Fat per 100 grams (g)")
    
    # Vitamins - Note different units
    vitamin_a_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin A per 100 grams (mcg RAE - Retinol Activity Equivalents). "
                   "Note: This is in MICROGRAMS, not milligrams."
    )
    vitamin_c_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin C per 100 grams (mg - milligrams)"
    )
    vitamin_d_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin D per 100 grams (mcg - micrograms). "
                   "Note: 1 mcg = 40 IU"
    )
    vitamin_b12_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin B12 per 100 grams (mcg - micrograms). "
                   "Critical for vegans/vegetarians, nerve function"
    )
    folate_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Folate/Folic Acid per 100 grams (mcg - micrograms). "
                   "Essential for pregnancy, DNA synthesis"
    )
    vitamin_e_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin E per 100 grams (mg - milligrams). "
                   "Major antioxidant, often deficient"
    )
    vitamin_k_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Vitamin K per 100 grams (mcg - micrograms). "
                   "Bone health, blood clotting"
    )
    
    # Minerals - All in milligrams
    calcium_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Calcium per 100 grams (mg - milligrams)"
    )
    iron_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Iron per 100 grams (mg - milligrams)"
    )
    magnesium_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Magnesium per 100 grams (mg - milligrams)"
    )
    potassium_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Potassium per 100 grams (mg - milligrams)"
    )
    zinc_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Zinc per 100 grams (mg - milligrams)"
    )
    sodium_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Sodium per 100 grams (mg - milligrams)"
    )
    cholesterol_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Cholesterol per 100 grams (mg - milligrams)"
    )
    
    # Fiber - in grams
    fiber_per_100g: float = Field(
        ..., 
        ge=0, 
        description="Dietary fiber per 100 grams (g - grams)"
    )

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate that food name is not empty."""
        if not v.strip():
            raise ValueError('Food name cannot be empty')
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Chicken Breast (Skinless)",
                "cost_per_100g": 3.20,
                "calories_per_100g": 165,
                "carbs_per_100g": 0,
                "protein_per_100g": 31,
                "fat_per_100g": 3.6,
                "vitamin_a_per_100g": 9,      # mcg RAE
                "vitamin_c_per_100g": 0,      # mg
                "vitamin_d_per_100g": 0,      # mcg
                "vitamin_b12_per_100g": 0.3,  # mcg
                "folate_per_100g": 6,         # mcg
                "vitamin_e_per_100g": 0.3,    # mg
                "vitamin_k_per_100g": 1.5,    # mcg
                "calcium_per_100g": 15,       # mg
                "iron_per_100g": 0.9,         # mg
                "magnesium_per_100g": 20,     # mg
                "potassium_per_100g": 256,    # mg
                "zinc_per_100g": 1.0,         # mg
                "sodium_per_100g": 74,        # mg
                "cholesterol_per_100g": 85,   # mg
                "fiber_per_100g": 0           # g
            }
        }
    )


class NutritionalConstraints(BaseModel):
    """Model for nutritional constraints (min/max bounds for each nutrient).
    
    Daily recommended values and upper limits.
    Units match the Food model:
    - Macronutrients: grams (g)
    - Vitamin A: micrograms RAE (mcg)
    - Other nutrients: milligrams (mg)
    - Fiber: grams (g)
    """
    
    # Macronutrients
    min_calories: float = Field(..., ge=0, description="Minimum daily calories required")
    max_calories: float = Field(..., gt=0, description="Maximum daily calories allowed")
    min_protein: float = Field(..., ge=0, description="Minimum daily protein required (g)")
    max_protein: float = Field(..., gt=0, description="Maximum daily protein allowed (g)")
    min_carbs: float = Field(..., ge=0, description="Minimum daily carbohydrates required (g)")
    max_carbs: float = Field(..., gt=0, description="Maximum daily carbohydrates allowed (g)")
    min_fat: float = Field(..., ge=0, description="Minimum daily fat required (g)")
    max_fat: float = Field(..., gt=0, description="Maximum daily fat allowed (g)")
    
    # Vitamins
    min_vitamin_a: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin A required (mcg RAE). "
                   "RDA: 700-900 mcg for adults"
    )
    max_vitamin_a: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin A allowed (mcg RAE). "
                   "Upper limit: 3000 mcg for adults"
    )
    min_vitamin_c: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin C required (mg). "
                   "RDA: 65-90 mg for adults"
    )
    max_vitamin_c: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin C allowed (mg). "
                   "Upper limit: 2000 mg for adults"
    )
    min_vitamin_d: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin D required (mcg). "
                   "RDA: 15-20 mcg (600-800 IU) for adults"
    )
    max_vitamin_d: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin D allowed (mcg). "
                   "Upper limit: 100 mcg (4000 IU) for adults"
    )
    min_vitamin_b12: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin B12 required (mcg). "
                   "RDA: 2.4 mcg for adults, critical for vegans/vegetarians"
    )
    max_vitamin_b12: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin B12 allowed (mcg). "
                   "No established upper limit - safe at high doses"
    )
    min_folate: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily folate required (mcg DFE). "
                   "RDA: 400 mcg for adults, 600 mcg for pregnancy"
    )
    max_folate: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily folate allowed (mcg DFE). "
                   "Upper limit: 1000 mcg for adults (from supplements)"
    )
    min_vitamin_e: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin E required (mg alpha-tocopherol). "
                   "RDA: 15 mg for adults"
    )
    max_vitamin_e: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin E allowed (mg alpha-tocopherol). "
                   "Upper limit: 1000 mg for adults"
    )
    min_vitamin_k: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily vitamin K required (mcg). "
                   "Adequate Intake: 90 mcg (women), 120 mcg (men)"
    )
    max_vitamin_k: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily vitamin K allowed (mcg). "
                   "No established upper limit - safe from food sources"
    )
    
    # Minerals
    min_calcium: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily calcium required (mg). "
                   "RDA: 1000-1200 mg for adults"
    )
    max_calcium: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily calcium allowed (mg). "
                   "Upper limit: 2500 mg for adults"
    )
    min_iron: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily iron required (mg). "
                   "RDA: 8 mg (men), 18 mg (women) for adults"
    )
    max_iron: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily iron allowed (mg). "
                   "Upper limit: 45 mg for adults"
    )
    min_magnesium: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily magnesium required (mg). "
                   "RDA: 310-420 mg for adults"
    )
    max_magnesium: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily magnesium allowed (mg). "
                   "Upper limit: 350 mg from supplements (no limit for food sources)"
    )
    min_potassium: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily potassium required (mg). "
                   "Adequate Intake: 3500-4700 mg for adults"
    )
    max_potassium: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily potassium allowed (mg). "
                   "Generally well-tolerated up to 10000 mg"
    )
    min_zinc: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily zinc required (mg). "
                   "RDA: 8 mg (women), 11 mg (men) for adults"
    )
    max_zinc: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily zinc allowed (mg). "
                   "Upper limit: 40 mg for adults"
    )
    min_sodium: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily sodium required (mg). "
                   "Adequate Intake: 1500 mg minimum needs"
    )
    max_sodium: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily sodium allowed (mg). "
                   "Recommended limit: 2300 mg for adults"
    )
    min_cholesterol: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily cholesterol required (mg). "
                   "No dietary requirement - can be 0"
    )
    max_cholesterol: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily cholesterol allowed (mg). "
                   "Heart-healthy limit: <300 mg"
    )
    
    # Fiber
    min_fiber: float = Field(
        ..., 
        ge=0, 
        description="Minimum daily fiber required (g). "
                   "RDA: 25-38 g for adults"
    )
    max_fiber: float = Field(
        ..., 
        gt=0, 
        description="Maximum daily fiber allowed (g). "
                   "Generally well-tolerated up to 70 g"
    )

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

    @field_validator('max_vitamin_d')
    @classmethod
    def validate_vitamin_d_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_d > min_vitamin_d."""
        if info.data.get('min_vitamin_d') is not None and v <= info.data['min_vitamin_d']:
            raise ValueError('max_vitamin_d must be greater than min_vitamin_d')
        return v

    @field_validator('max_vitamin_b12')
    @classmethod
    def validate_vitamin_b12_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_b12 > min_vitamin_b12."""
        if info.data.get('min_vitamin_b12') is not None and v <= info.data['min_vitamin_b12']:
            raise ValueError('max_vitamin_b12 must be greater than min_vitamin_b12')
        return v

    @field_validator('max_folate')
    @classmethod
    def validate_folate_bounds(cls, v: float, info) -> float:
        """Validate that max_folate > min_folate."""
        if info.data.get('min_folate') is not None and v <= info.data['min_folate']:
            raise ValueError('max_folate must be greater than min_folate')
        return v

    @field_validator('max_vitamin_e')
    @classmethod
    def validate_vitamin_e_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_e > min_vitamin_e."""
        if info.data.get('min_vitamin_e') is not None and v <= info.data['min_vitamin_e']:
            raise ValueError('max_vitamin_e must be greater than min_vitamin_e')
        return v

    @field_validator('max_vitamin_k')
    @classmethod
    def validate_vitamin_k_bounds(cls, v: float, info) -> float:
        """Validate that max_vitamin_k > min_vitamin_k."""
        if info.data.get('min_vitamin_k') is not None and v <= info.data['min_vitamin_k']:
            raise ValueError('max_vitamin_k must be greater than min_vitamin_k')
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

    @field_validator('max_magnesium')
    @classmethod
    def validate_magnesium_bounds(cls, v: float, info) -> float:
        """Validate that max_magnesium > min_magnesium."""
        if info.data.get('min_magnesium') is not None and v <= info.data['min_magnesium']:
            raise ValueError('max_magnesium must be greater than min_magnesium')
        return v

    @field_validator('max_potassium')
    @classmethod
    def validate_potassium_bounds(cls, v: float, info) -> float:
        """Validate that max_potassium > min_potassium."""
        if info.data.get('min_potassium') is not None and v <= info.data['min_potassium']:
            raise ValueError('max_potassium must be greater than min_potassium')
        return v

    @field_validator('max_zinc')
    @classmethod
    def validate_zinc_bounds(cls, v: float, info) -> float:
        """Validate that max_zinc > min_zinc."""
        if info.data.get('min_zinc') is not None and v <= info.data['min_zinc']:
            raise ValueError('max_zinc must be greater than min_zinc')
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

    @field_validator('max_fiber')
    @classmethod
    def validate_fiber_bounds(cls, v: float, info) -> float:
        """Validate that max_fiber > min_fiber."""
        if info.data.get('min_fiber') is not None and v <= info.data['min_fiber']:
            raise ValueError('max_fiber must be greater than min_fiber')
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "min_calories": 1800,
                "max_calories": 2200,
                "min_protein": 120,
                "max_protein": 180,
                "min_carbs": 150,
                "max_carbs": 250,
                "min_fat": 50,
                "max_fat": 80,
                "min_vitamin_a": 700,      # mcg RAE
                "max_vitamin_a": 3000,     # mcg RAE
                "min_vitamin_c": 75,       # mg
                "max_vitamin_c": 2000,     # mg
                "min_vitamin_d": 15,       # mcg
                "max_vitamin_d": 100,      # mcg
                "min_vitamin_b12": 2.4,    # mcg
                "max_vitamin_b12": 1000,   # mcg
                "min_folate": 400,        # mcg DFE
                "max_folate": 1000,       # mcg DFE
                "min_vitamin_e": 15,       # mg
                "max_vitamin_e": 1000,     # mg
                "min_vitamin_k": 90,       # mcg
                "max_vitamin_k": 10000,    # mcg (no established upper limit)
                "min_calcium": 1000,       # mg
                "max_calcium": 2500,       # mg
                "min_iron": 8,             # mg
                "max_iron": 45,            # mg
                "min_magnesium": 310,      # mg
                "max_magnesium": 350,      # mg
                "min_potassium": 3500,     # mg
                "max_potassium": 10000,    # mg
                "min_zinc": 8,             # mg
                "max_zinc": 40,            # mg
                "min_sodium": 1500,        # mg
                "max_sodium": 2300,        # mg
                "min_cholesterol": 0,      # mg
                "max_cholesterol": 300,    # mg
                "min_fiber": 25,          # g
                "max_fiber": 70           # g
            }
        }
    )


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