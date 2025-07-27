#!/usr/bin/env python3
"""
Example usage of the Enhanced Diet Optimizer API with comprehensive nutritional data.

This script demonstrates how to use the Diet Optimizer API with the new nutritional
elements including vitamins A & C, calcium, iron, potassium, sodium, and cholesterol.
"""

import requests
import json
import sys
from typing import Dict, Any


def create_sample_request() -> Dict[str, Any]:
    """Create a sample optimization request with comprehensive nutritional data."""
    
    # Comprehensive food database with realistic nutritional values
    foods = [
        {
            "name": "Chicken Breast (Skinless)",
            "cost_per_100g": 3.20,
            "calories_per_100g": 165,
            "carbs_per_100g": 0,
            "protein_per_100g": 31,
            "fat_per_100g": 3.6,
            "vitamin_a_per_100g": 9,      # mcg RAE
            "vitamin_c_per_100g": 0,      # mg
            "calcium_per_100g": 15,       # mg
            "iron_per_100g": 0.9,         # mg
            "magnesium_per_100g": 22,     # mg
            "potassium_per_100g": 256,    # mg
            "sodium_per_100g": 74,        # mg
            "cholesterol_per_100g": 85    # mg
        },
        {
            "name": "Salmon Fillet",
            "cost_per_100g": 6.50,
            "calories_per_100g": 208,
            "carbs_per_100g": 0,
            "protein_per_100g": 25.4,
            "fat_per_100g": 12.4,
            "vitamin_a_per_100g": 58,
            "vitamin_c_per_100g": 0,
            "calcium_per_100g": 12,
            "iron_per_100g": 0.8,
            "magnesium_per_100g": 26,
            "potassium_per_100g": 490,
            "sodium_per_100g": 59,
            "cholesterol_per_100g": 70
        },
        {
            "name": "Brown Rice",
            "cost_per_100g": 1.10,
            "calories_per_100g": 112,
            "carbs_per_100g": 23,
            "protein_per_100g": 2.6,
            "fat_per_100g": 0.9,
            "vitamin_a_per_100g": 0,
            "vitamin_c_per_100g": 0,
            "calcium_per_100g": 10,
            "iron_per_100g": 0.4,
            "magnesium_per_100g": 44,
            "potassium_per_100g": 43,
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Quinoa",
            "cost_per_100g": 2.80,
            "calories_per_100g": 368,
            "carbs_per_100g": 64.2,
            "protein_per_100g": 14.1,
            "fat_per_100g": 6.1,
            "vitamin_a_per_100g": 1,
            "vitamin_c_per_100g": 0,
            "calcium_per_100g": 47,
            "iron_per_100g": 4.6,
            "magnesium_per_100g": 197,
            "potassium_per_100g": 563,
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Spinach",
            "cost_per_100g": 2.40,
            "calories_per_100g": 23,
            "carbs_per_100g": 3.6,
            "protein_per_100g": 2.9,
            "fat_per_100g": 0.4,
            "vitamin_a_per_100g": 469,
            "vitamin_c_per_100g": 28.1,
            "calcium_per_100g": 99,
            "iron_per_100g": 2.7,
            "magnesium_per_100g": 79,
            "potassium_per_100g": 558,
            "sodium_per_100g": 79,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Broccoli",
            "cost_per_100g": 1.80,
            "calories_per_100g": 34,
            "carbs_per_100g": 7,
            "protein_per_100g": 2.8,
            "fat_per_100g": 0.4,
            "vitamin_a_per_100g": 623,
            "vitamin_c_per_100g": 89.2,
            "calcium_per_100g": 47,
            "iron_per_100g": 0.7,
            "magnesium_per_100g": 21,
            "potassium_per_100g": 316,
            "sodium_per_100g": 33,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Sweet Potato",
            "cost_per_100g": 1.20,
            "calories_per_100g": 86,
            "carbs_per_100g": 20,
            "protein_per_100g": 1.6,
            "fat_per_100g": 0.1,
            "vitamin_a_per_100g": 961,
            "vitamin_c_per_100g": 2.4,
            "calcium_per_100g": 30,
            "iron_per_100g": 0.6,
            "magnesium_per_100g": 25,
            "potassium_per_100g": 337,
            "sodium_per_100g": 54,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Greek Yogurt (Plain)",
            "cost_per_100g": 2.00,
            "calories_per_100g": 97,
            "carbs_per_100g": 3.9,
            "protein_per_100g": 10,
            "fat_per_100g": 5,
            "vitamin_a_per_100g": 36,
            "vitamin_c_per_100g": 0,
            "calcium_per_100g": 110,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 11,
            "potassium_per_100g": 141,
            "sodium_per_100g": 36,
            "cholesterol_per_100g": 10
        },
        {
            "name": "Almonds",
            "cost_per_100g": 8.50,
            "calories_per_100g": 579,
            "carbs_per_100g": 21.6,
            "protein_per_100g": 21.2,
            "fat_per_100g": 49.9,
            "vitamin_a_per_100g": 0,
            "vitamin_c_per_100g": 0,
            "calcium_per_100g": 269,
            "iron_per_100g": 3.7,
            "magnesium_per_100g": 270,
            "potassium_per_100g": 733,
            "sodium_per_100g": 1,
            "cholesterol_per_100g": 0
        },
        {
            "name": "Orange",
            "cost_per_100g": 1.50,
            "calories_per_100g": 47,
            "carbs_per_100g": 11.8,
            "protein_per_100g": 0.9,
            "fat_per_100g": 0.1,
            "vitamin_a_per_100g": 11,
            "vitamin_c_per_100g": 53.2,
            "calcium_per_100g": 40,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 10,
            "potassium_per_100g": 181,
            "sodium_per_100g": 0,
            "cholesterol_per_100g": 0
        }
    ]
    
    # Nutritional constraints for a healthy adult
    constraints = {
        "min_calories": 1800,
        "max_calories": 2200,
        "min_protein": 120,
        "max_protein": 180,
        "min_carbs": 150,
        "max_carbs": 250,
        "min_fat": 50,
        "max_fat": 80,
        "min_vitamin_a": 700,      # Daily recommendation
        "max_vitamin_a": 3000,     # Upper limit
        "min_vitamin_c": 75,       # Daily recommendation
        "max_vitamin_c": 2000,     # Upper limit
        "min_calcium": 1000,       # Daily recommendation
        "max_calcium": 2500,       # Upper limit
        "min_iron": 8,             # Daily recommendation (men)
        "max_iron": 45,            # Upper limit
        "min_magnesium": 400,      # Daily recommendation for men
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 3500,     # Daily recommendation
        "max_potassium": 10000,    # Safe upper limit
        "min_sodium": 1500,        # Minimum needs
        "max_sodium": 2300,        # Daily recommendation limit
        "min_cholesterol": 0,      # No minimum requirement
        "max_cholesterol": 300     # Heart-healthy limit
    }
    
    return {
        "foods": foods,
        "constraints": constraints
    }


def create_pregnancy_request() -> Dict[str, Any]:
    """Create a pregnancy nutrition optimization request."""
    
    # Use the same comprehensive food database
    foods = create_sample_request()["foods"]
    
    # Pregnancy-specific nutritional constraints
    pregnancy_constraints = {
        "min_calories": 2200,      # Higher calorie needs
        "max_calories": 2500,
        "min_protein": 110,        # Higher protein needs
        "max_protein": 160,
        "min_carbs": 175,          # Higher carb needs
        "max_carbs": 250,
        "min_fat": 60,
        "max_fat": 90,
        "min_vitamin_a": 770,      # Pregnancy recommendation
        "max_vitamin_a": 3000,
        "min_vitamin_c": 85,       # Higher vitamin C needs
        "max_vitamin_c": 2000,
        "min_calcium": 1200,       # Higher calcium needs
        "max_calcium": 2500,
        "min_iron": 27,            # Much higher iron needs
        "max_iron": 45,
        "min_magnesium": 350,      # Pregnancy recommendation
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 4700,     # Higher potassium needs
        "max_potassium": 10000,
        "min_sodium": 1500,
        "max_sodium": 2300,
        "min_cholesterol": 0,
        "max_cholesterol": 300
    }
    
    return {
        "foods": foods,
        "constraints": pregnancy_constraints
    }


def create_heart_healthy_request() -> Dict[str, Any]:
    """Create a heart-healthy diet optimization request."""
    
    # Use the same comprehensive food database
    foods = create_sample_request()["foods"]
    
    # Heart-healthy nutritional constraints
    heart_constraints = {
        "min_calories": 1600,
        "max_calories": 2000,
        "min_protein": 80,
        "max_protein": 130,
        "min_carbs": 130,
        "max_carbs": 200,
        "min_fat": 40,
        "max_fat": 65,
        "min_vitamin_a": 700,
        "max_vitamin_a": 3000,
        "min_vitamin_c": 90,       # Higher for antioxidant benefits
        "max_vitamin_c": 2000,
        "min_calcium": 1200,
        "max_calcium": 2500,
        "min_iron": 8,
        "max_iron": 45,
        "min_magnesium": 420,      # Good for heart health
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 5000,     # High potassium for heart health
        "max_potassium": 10000,
        "min_sodium": 800,         # Low sodium for heart health
        "max_sodium": 1500,
        "min_cholesterol": 0,      # Minimize cholesterol
        "max_cholesterol": 150     # Very low cholesterol limit
    }
    
    return {
        "foods": foods,
        "constraints": heart_constraints
    }


def optimize_diet(request_data: Dict[str, Any], api_url: str = "http://localhost:8000") -> None:
    """Send optimization request to the API and display results."""
    
    try:
        print(f"Sending optimization request to {api_url}/optimize...")
        response = requests.post(f"{api_url}/optimize", json=request_data, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            display_results(result)
        else:
            print(f"Error: HTTP {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")


def display_results(result: Dict[str, Any]) -> None:
    """Display optimization results in a user-friendly format."""
    
    print("\n" + "="*80)
    print("DIET OPTIMIZATION RESULTS")
    print("="*80)
    
    print(f"Status: {result['status'].upper()}")
    
    if result['status'] == 'optimal':
        print(f"Total Cost: ${result['total_cost']:.2f}")
        
        print("\nOptimal Food Quantities:")
        print("-" * 60)
        for food in result['optimal_quantities']:
            print(f"  {food['food_name']:<25} "
                  f"{food['quantity_grams']:>6.1f}g "
                  f"(${food['cost']:>5.2f})")
        
        print("\nNutritional Summary:")
        print("-" * 60)
        summary = result['nutritional_summary']
        print(f"  Calories:     {summary['total_calories']:>7.1f}")
        print(f"  Protein:      {summary['total_protein']:>7.1f}g")
        print(f"  Carbs:        {summary['total_carbs']:>7.1f}g")
        print(f"  Fat:          {summary['total_fat']:>7.1f}g")
        print(f"  Vitamin A:    {summary['total_vitamin_a']:>7.1f} mcg RAE")
        print(f"  Vitamin C:    {summary['total_vitamin_c']:>7.1f} mg")
        print(f"  Calcium:      {summary['total_calcium']:>7.1f} mg")
        print(f"  Iron:         {summary['total_iron']:>7.1f} mg")
        print(f"  Magnesium:    {summary['total_magnesium']:>7.1f} mg")
        print(f"  Potassium:    {summary['total_potassium']:>7.1f} mg")
        print(f"  Sodium:       {summary['total_sodium']:>7.1f} mg")
        print(f"  Cholesterol:  {summary['total_cholesterol']:>7.1f} mg")
        
        print("\nConstraint Satisfaction:")
        print("-" * 60)
        satisfaction = result['constraint_satisfaction']
        constraints_status = [
            ("Calories", satisfaction['calories_within_bounds']),
            ("Protein", satisfaction['protein_within_bounds']),
            ("Carbs", satisfaction['carbs_within_bounds']),
            ("Fat", satisfaction['fat_within_bounds']),
            ("Vitamin A", satisfaction['vitamin_a_within_bounds']),
            ("Vitamin C", satisfaction['vitamin_c_within_bounds']),
            ("Calcium", satisfaction['calcium_within_bounds']),
            ("Iron", satisfaction['iron_within_bounds']),
            ("Magnesium", satisfaction['magnesium_within_bounds']),
            ("Potassium", satisfaction['potassium_within_bounds']),
            ("Sodium", satisfaction['sodium_within_bounds']),
            ("Cholesterol", satisfaction['cholesterol_within_bounds'])
        ]
        
        for nutrient, satisfied in constraints_status:
            status_icon = "✓" if satisfied else "✗"
            print(f"  {nutrient:<12} {status_icon}")
            
    elif result['status'] == 'infeasible':
        print("\nThe problem is INFEASIBLE - no combination of foods can meet all constraints.")
        print("Consider:")
        print("  - Relaxing some nutritional constraints")
        print("  - Adding more diverse food options")
        print("  - Adjusting minimum/maximum bounds")
        
    elif result['status'] == 'unbounded':
        print("\nThe problem is UNBOUNDED - cost can be reduced indefinitely.")
        print("This usually indicates an issue with the problem formulation.")


def main():
    """Main function to demonstrate the enhanced Diet Optimizer API."""
    
    print("Enhanced Diet Optimizer API - Example Usage")
    print("==========================================")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code != 200:
            print("Error: API is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("Error: Cannot connect to API at http://localhost:8000")
        print("Please make sure the API server is running with: uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Example 1: Standard healthy adult diet
    print("\n1. STANDARD HEALTHY ADULT DIET")
    standard_request = create_sample_request()
    optimize_diet(standard_request)
    
    # Example 2: Pregnancy nutrition
    print("\n\n2. PREGNANCY NUTRITION PROFILE")
    pregnancy_request = create_pregnancy_request()
    optimize_diet(pregnancy_request)
    
    # Example 3: Heart-healthy diet
    print("\n\n3. HEART-HEALTHY DIET PROFILE")
    heart_request = create_heart_healthy_request()
    optimize_diet(heart_request)
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("The Enhanced Diet Optimizer API now supports comprehensive nutritional optimization")
    print("including vitamins A & C, calcium, iron, potassium, sodium, and cholesterol!")


if __name__ == "__main__":
    main()