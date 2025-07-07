# Nutrient Units Reference Guide

## Overview

This document provides a comprehensive reference for all nutrient units used in the Diet Optimizer API. Understanding the correct units is crucial for accurate nutritional analysis and optimization.

## Quick Reference

| Nutrient | Unit | Symbol | Notes |
|----------|------|--------|-------|
| **Calories** | Kilocalories | kcal | Energy content |
| **Protein** | Grams | g | Macronutrient |
| **Carbohydrates** | Grams | g | Macronutrient |
| **Fat** | Grams | g | Macronutrient |
| **Vitamin A** | **Micrograms RAE** | **mcg RAE** | ⚠️ **MICROGRAMS**, not milligrams |
| **Vitamin C** | Milligrams | mg | Water-soluble vitamin |
| **Calcium** | Milligrams | mg | Mineral |
| **Iron** | Milligrams | mg | Mineral |
| **Potassium** | Milligrams | mg | Mineral |
| **Sodium** | Milligrams | mg | Mineral |
| **Cholesterol** | Milligrams | mg | Lipid |

## Detailed Unit Information

### Macronutrients (Grams)

#### Protein, Carbohydrates, Fat
- **Unit**: Grams (g)
- **Typical Daily Amounts**: 50-300g depending on nutrient
- **API Fields**: `protein_per_100g`, `carbs_per_100g`, `fat_per_100g`

### Vitamins

#### Vitamin A
- **Unit**: Micrograms RAE (mcg RAE)
- **Full Name**: Retinol Activity Equivalents
- **⚠️ CRITICAL**: This is in **MICROGRAMS** (mcg), not milligrams (mg)
- **Conversion**: 1,000 mcg = 1 mg
- **Daily Range**: 700-3000 mcg for adults
- **API Field**: `vitamin_a_per_100g`

**Example Values:**
```json
{
  "name": "Spinach",
  "vitamin_a_per_100g": 469  // 469 mcg RAE (very high in Vitamin A)
}
```

#### Vitamin C
- **Unit**: Milligrams (mg)
- **Daily Range**: 65-2000 mg for adults
- **API Field**: `vitamin_c_per_100g`

**Example Values:**
```json
{
  "name": "Orange",
  "vitamin_c_per_100g": 53.2  // 53.2 mg (good source)
}
```

### Minerals (All in Milligrams)

#### Calcium
- **Unit**: Milligrams (mg)
- **Daily Range**: 1000-2500 mg for adults
- **API Field**: `calcium_per_100g`

#### Iron
- **Unit**: Milligrams (mg)
- **Daily Range**: 8-45 mg for adults
- **API Field**: `iron_per_100g`

#### Potassium
- **Unit**: Milligrams (mg)
- **Daily Range**: 3500-10000 mg for adults
- **API Field**: `potassium_per_100g`

#### Sodium
- **Unit**: Milligrams (mg)
- **Daily Range**: 1500-2300 mg for adults
- **API Field**: `sodium_per_100g`

#### Cholesterol
- **Unit**: Milligrams (mg)
- **Daily Range**: 0-300 mg for adults
- **API Field**: `cholesterol_per_100g`

## Common Mistakes to Avoid

### ❌ Wrong: Using mg for Vitamin A
```json
{
  "vitamin_a_per_100g": 0.469  // WRONG - This is too small
}
```

### ✅ Correct: Using mcg for Vitamin A
```json
{
  "vitamin_a_per_100g": 469  // CORRECT - This is in mcg RAE
}
```

### ❌ Wrong: Using mcg for other nutrients
```json
{
  "vitamin_c_per_100g": 53200,  // WRONG - This should be in mg
  "calcium_per_100g": 99000     // WRONG - This should be in mg
}
```

### ✅ Correct: Using mg for other nutrients
```json
{
  "vitamin_c_per_100g": 53.2,  // CORRECT - mg
  "calcium_per_100g": 99       // CORRECT - mg
}
```

## Realistic Value Ranges

### Per 100g Serving Expectations

| Nutrient | Low Values | Moderate Values | High Values | Exceptional Values |
|----------|------------|-----------------|-------------|-------------------|
| **Calories** | 10-50 | 100-200 | 300-500 | 500+ |
| **Protein (g)** | 0-2 | 5-15 | 20-30 | 30+ |
| **Carbs (g)** | 0-5 | 10-30 | 40-70 | 70+ |
| **Fat (g)** | 0-1 | 2-10 | 15-30 | 30+ |
| **Vitamin A (mcg)** | 0-10 | 50-200 | 400-800 | 800+ |
| **Vitamin C (mg)** | 0-5 | 10-30 | 50-100 | 100+ |
| **Calcium (mg)** | 0-20 | 30-100 | 150-300 | 300+ |
| **Iron (mg)** | 0-1 | 1-3 | 4-8 | 8+ |
| **Potassium (mg)** | 0-100 | 200-400 | 500-800 | 800+ |
| **Sodium (mg)** | 0-50 | 100-300 | 400-800 | 800+ |
| **Cholesterol (mg)** | 0 | 10-50 | 60-100 | 100+ |

## Example Food Profiles

### High Vitamin A Foods (mcg RAE per 100g)
```json
{
  "name": "Sweet Potato",
  "vitamin_a_per_100g": 961  // Very high in Vitamin A
}
```

### High Vitamin C Foods (mg per 100g)
```json
{
  "name": "Red Bell Pepper",
  "vitamin_c_per_100g": 127.7  // Excellent source
}
```

### High Calcium Foods (mg per 100g)
```json
{
  "name": "Cheddar Cheese",
  "calcium_per_100g": 721  // Very high in calcium
}
```

### High Iron Foods (mg per 100g)
```json
{
  "name": "Beef Liver",
  "iron_per_100g": 6.5  // Excellent iron source
}
```

## Validation Rules

The API validates that all nutritional values are:
- **Non-negative**: Cannot be less than 0
- **Realistic**: Values should fall within expected ranges for real foods
- **Consistent**: Units must match the specified format

### Automatic Validation

The Pydantic models automatically validate:
```python
vitamin_a_per_100g: float = Field(..., ge=0, description="Vitamin A per 100 grams (mcg RAE)")
vitamin_c_per_100g: float = Field(..., ge=0, description="Vitamin C per 100 grams (mg)")
```

## Integration with USDA Standards

The API units follow:
- **USDA FoodData Central** standards
- **Dietary Reference Intakes (DRI)** guidelines
- **FDA Nutrition Facts Label** conventions

## API Usage Examples

### Complete Food Item
```json
{
  "name": "Salmon Fillet",
  "cost_per_100g": 6.50,
  "calories_per_100g": 208,
  "carbs_per_100g": 0,
  "protein_per_100g": 25.4,
  "fat_per_100g": 12.4,
  "vitamin_a_per_100g": 58,     // mcg RAE
  "vitamin_c_per_100g": 0,      // mg
  "calcium_per_100g": 12,       // mg
  "iron_per_100g": 0.8,         // mg
  "potassium_per_100g": 490,    // mg
  "sodium_per_100g": 59,        // mg
  "cholesterol_per_100g": 70    // mg
}
```

### Nutritional Constraints
```json
{
  "min_vitamin_a": 700,      // mcg RAE - Adult RDA
  "max_vitamin_a": 3000,     // mcg RAE - Upper limit
  "min_vitamin_c": 75,       // mg - Adult RDA
  "max_vitamin_c": 2000,     // mg - Upper limit
  "min_calcium": 1000,       // mg - Adult RDA
  "max_calcium": 2500,       // mg - Upper limit
  "min_iron": 8,             // mg - Adult RDA (men)
  "max_iron": 45,            // mg - Upper limit
  "min_potassium": 3500,     // mg - Adequate Intake
  "max_potassium": 10000,    // mg - Safe limit
  "min_sodium": 1500,        // mg - Minimum needs
  "max_sodium": 2300,        // mg - Recommended limit
  "min_cholesterol": 0,      // mg - No requirement
  "max_cholesterol": 300     // mg - Heart-healthy limit
}
```

## Troubleshooting

### "My optimization is infeasible"
Check if your vitamin A constraints are in the correct units:
- ❌ `"min_vitamin_a": 0.7` (This is only 0.7 mcg - too low)
- ✅ `"min_vitamin_a": 700` (This is 700 mcg - appropriate)

### "My food values seem too high/low"
Verify you're using the correct units:
- Vitamin A should be in hundreds of mcg (e.g., 400-800 for high sources)
- Other nutrients should be in mg (typically 10-100s for minerals)

### "API validation errors"
Ensure all values are positive and in the correct unit scale:
```python
# This will fail validation
{"vitamin_a_per_100g": -10}  # Negative values not allowed

# This will pass validation
{"vitamin_a_per_100g": 469}  # Positive mcg RAE value
```

---

## Summary

**Remember the key distinction:**
- **Vitamin A**: Micrograms RAE (mcg) - typically 100-1000 range
- **All other nutrients**: Milligrams (mg) - typically 1-1000 range

This follows standard nutritional science conventions and ensures compatibility with USDA food databases and international nutrition standards.