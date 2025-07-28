#!/usr/bin/env python3
"""
Example usage of the Enhanced Diet Optimizer API with comprehensive nutritional data.

This script demonstrates how to use the Diet Optimizer API with 15 essential nutrients
including vitamins A, C, D, minerals, and macronutrients.
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
            "vitamin_d_per_100g": 0.1,    # mcg
            "vitamin_b12_per_100g": 0.3,  # mcg
            "folate_per_100g": 6,         # mcg DFE
            "vitamin_e_per_100g": 0.3,    # mg
            "vitamin_k_per_100g": 1.5,    # mcg
            "calcium_per_100g": 15,       # mg
            "iron_per_100g": 0.9,         # mg
            "magnesium_per_100g": 22,     # mg
            "potassium_per_100g": 256,    # mg
            "zinc_per_100g": 1.0,         # mg
            "sodium_per_100g": 74,        # mg
            "cholesterol_per_100g": 85,   # mg
            "fiber_per_100g": 0           # g
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
            "vitamin_d_per_100g": 14.2,   # mcg (salmon is rich in vitamin D)
            "vitamin_b12_per_100g": 3.8,  # mcg (salmon is rich in B12)
            "folate_per_100g": 25,        # mcg DFE
            "vitamin_e_per_100g": 1.5,    # mg
            "vitamin_k_per_100g": 0.1,    # mcg
            "calcium_per_100g": 12,
            "iron_per_100g": 0.8,
            "magnesium_per_100g": 26,
            "potassium_per_100g": 490,
            "zinc_per_100g": 0.6,         # mg
            "sodium_per_100g": 59,
            "cholesterol_per_100g": 70,
            "fiber_per_100g": 0           # g
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 8,         # mcg DFE
            "vitamin_e_per_100g": 0.1,    # mg
            "vitamin_k_per_100g": 0.4,    # mcg
            "calcium_per_100g": 10,
            "iron_per_100g": 0.4,
            "magnesium_per_100g": 44,
            "potassium_per_100g": 43,
            "zinc_per_100g": 1.1,         # mg
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 1.8         # g (brown rice has moderate fiber)
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 42,        # mcg DFE
            "vitamin_e_per_100g": 0.6,    # mg
            "vitamin_k_per_100g": 1.0,    # mcg
            "calcium_per_100g": 47,
            "iron_per_100g": 4.6,
            "magnesium_per_100g": 197,
            "potassium_per_100g": 563,
            "zinc_per_100g": 3.1,         # mg
            "sodium_per_100g": 5,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 7           # g (quinoa is high in fiber)
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 194,       # mcg DFE
            "vitamin_e_per_100g": 2.0,    # mg
            "vitamin_k_per_100g": 483,    # mcg
            "calcium_per_100g": 99,
            "iron_per_100g": 2.7,
            "magnesium_per_100g": 79,
            "potassium_per_100g": 558,
            "zinc_per_100g": 0.5,         # mg
            "sodium_per_100g": 79,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 2.2         # g
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 108,       # mcg DFE
            "vitamin_e_per_100g": 1.7,    # mg
            "vitamin_k_per_100g": 102,    # mcg
            "calcium_per_100g": 47,
            "iron_per_100g": 0.7,
            "magnesium_per_100g": 21,
            "potassium_per_100g": 316,
            "zinc_per_100g": 0.4,         # mg
            "sodium_per_100g": 33,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 2.6         # g
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 11,        # mcg DFE
            "vitamin_e_per_100g": 0.3,    # mg
            "vitamin_k_per_100g": 1.8,    # mcg
            "calcium_per_100g": 30,
            "iron_per_100g": 0.6,
            "magnesium_per_100g": 25,
            "potassium_per_100g": 337,
            "zinc_per_100g": 0.3,         # mg
            "sodium_per_100g": 54,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 3           # g
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
            "vitamin_d_per_100g": 0.9,    # mcg (small amount in yogurt)
            "vitamin_b12_per_100g": 0.5,  # mcg
            "folate_per_100g": 12,        # mcg DFE
            "vitamin_e_per_100g": 0.1,    # mg
            "vitamin_k_per_100g": 0.2,    # mcg
            "calcium_per_100g": 110,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 11,
            "potassium_per_100g": 141,
            "zinc_per_100g": 0.5,         # mg
            "sodium_per_100g": 36,
            "cholesterol_per_100g": 10,
            "fiber_per_100g": 0           # g (yogurt has no fiber)
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 44,        # mcg DFE
            "vitamin_e_per_100g": 25.6,   # mg (almonds are very high in vitamin E)
            "vitamin_k_per_100g": 0,      # mcg
            "calcium_per_100g": 269,
            "iron_per_100g": 3.7,
            "magnesium_per_100g": 270,
            "potassium_per_100g": 733,
            "zinc_per_100g": 3.1,         # mg
            "sodium_per_100g": 1,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 12.5        # g (almonds are very high in fiber)
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
            "vitamin_d_per_100g": 0,      # mcg
            "vitamin_b12_per_100g": 0,    # mcg
            "folate_per_100g": 30,        # mcg DFE
            "vitamin_e_per_100g": 0.2,    # mg
            "vitamin_k_per_100g": 0,      # mcg
            "calcium_per_100g": 40,
            "iron_per_100g": 0.1,
            "magnesium_per_100g": 10,
            "potassium_per_100g": 181,
            "zinc_per_100g": 0.07,        # mg
            "sodium_per_100g": 0,
            "cholesterol_per_100g": 0,
            "fiber_per_100g": 2.4         # g
        }
    ]
    
    # Nutritional constraints for a healthy adult (relaxed for feasibility)
    constraints = {
        "min_calories": 1500,
        "max_calories": 2500,
        "min_protein": 80,
        "max_protein": 200,
        "min_carbs": 100,
        "max_carbs": 300,
        "min_fat": 30,
        "max_fat": 100,
        "min_vitamin_a": 400,      # Relaxed from 700
        "max_vitamin_a": 3000,     # Upper limit
        "min_vitamin_c": 50,       # Relaxed from 75
        "max_vitamin_c": 2000,     # Upper limit
        "min_vitamin_d": 5,        # Relaxed from 15 (few foods have high vitamin D)
        "max_vitamin_d": 100,      # Upper limit
        "min_vitamin_b12": 2.4,    # mcg - critical for vegans/vegetarians
        "max_vitamin_b12": 1000,   # mcg - no established upper limit
        "min_folate": 400,         # mcg DFE - essential for pregnancy
        "max_folate": 1000,        # mcg DFE - upper limit from supplements
        "min_vitamin_e": 15,       # mg - major antioxidant
        "max_vitamin_e": 1000,     # mg - upper limit
        "min_vitamin_k": 90,       # mcg - bone health
        "max_vitamin_k": 10000,    # mcg - no established upper limit
        "min_calcium": 500,        # Relaxed from 1000
        "max_calcium": 2500,       # Upper limit
        "min_iron": 6,             # Relaxed from 8
        "max_iron": 45,            # Upper limit
        "min_magnesium": 200,      # Relaxed from 400
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 2000,     # Relaxed from 3500
        "max_potassium": 10000,    # Safe upper limit
        "min_zinc": 5,             # Relaxed from 8
        "max_zinc": 40,            # Upper limit
        "min_sodium": 1000,        # Relaxed from 1500
        "max_sodium": 2500,        # Relaxed upper limit
        "min_cholesterol": 0,      # No minimum requirement
        "max_cholesterol": 400,    # Relaxed limit
        "min_fiber": 15,           # Relaxed from 25
        "max_fiber": 80            # Safe upper limit
    }
    
    return {
        "foods": foods,
        "constraints": constraints
    }


def create_nutrient_density_request() -> Dict[str, Any]:
    """Create a nutrient density optimization request (equal costs = minimize weight)."""
    
    # Use the same food database but set all costs to 1
    foods = create_sample_request()["foods"]
    
    # Set all costs to 1 to optimize for nutrient density instead of cost
    for food in foods:
        food["cost_per_100g"] = 1.0
    
    # Use relaxed constraints suitable for nutrient density optimization
    density_constraints = {
        "min_calories": 1200,
        "max_calories": 1800,
        "min_protein": 60,
        "max_protein": 120,
        "min_carbs": 80,
        "max_carbs": 150,
        "min_fat": 25,
        "max_fat": 60,
        "min_vitamin_a": 300,
        "max_vitamin_a": 3000,
        "min_vitamin_c": 40,
        "max_vitamin_c": 2000,
        "min_vitamin_d": 3,
        "max_vitamin_d": 100,
        "min_vitamin_b12": 2.0,
        "max_vitamin_b12": 1000,
        "min_folate": 300,
        "max_folate": 1000,
        "min_vitamin_e": 12,
        "max_vitamin_e": 1000,
        "min_vitamin_k": 70,
        "max_vitamin_k": 10000,
        "min_calcium": 400,
        "max_calcium": 2500,
        "min_iron": 5,
        "max_iron": 45,
        "min_magnesium": 150,
        "max_magnesium": 800,
        "min_potassium": 1500,
        "max_potassium": 10000,
        "min_zinc": 4,
        "max_zinc": 40,
        "min_sodium": 800,
        "max_sodium": 2500,
        "min_cholesterol": 0,
        "max_cholesterol": 400,
        "min_fiber": 12,
        "max_fiber": 80
    }
    
    return {
        "foods": foods,
        "constraints": density_constraints
    }


def create_pregnancy_request() -> Dict[str, Any]:
    """Create a pregnancy nutrition optimization request."""
    
    # Use the same comprehensive food database
    foods = create_sample_request()["foods"]
    
    # Pregnancy-specific nutritional constraints (relaxed for feasibility)
    pregnancy_constraints = {
        "min_calories": 1600,      # Higher calorie needs (relaxed)
        "max_calories": 2800,
        "min_protein": 85,         # Higher protein needs (relaxed)
        "max_protein": 200,
        "min_carbs": 110,          # Higher carb needs (relaxed)
        "max_carbs": 320,
        "min_fat": 35,
        "max_fat": 120,
        "min_vitamin_a": 450,      # Pregnancy recommendation (relaxed)
        "max_vitamin_a": 3000,
        "min_vitamin_c": 55,       # Higher vitamin C needs (relaxed)
        "max_vitamin_c": 2000,
        "min_vitamin_d": 6,        # Relaxed (few foods have high vitamin D)
        "max_vitamin_d": 100,
        "min_vitamin_b12": 2.6,    # Slightly higher for pregnancy
        "max_vitamin_b12": 1000,
        "min_folate": 600,         # Much higher for pregnancy (critical!)
        "max_folate": 1000,
        "min_vitamin_e": 15,       # Same as adults
        "max_vitamin_e": 1000,
        "min_vitamin_k": 90,       # Same as adults
        "max_vitamin_k": 10000,
        "min_calcium": 600,        # Higher calcium needs (relaxed)
        "max_calcium": 2500,
        "min_iron": 12,            # Much higher iron needs (relaxed from 27)
        "max_iron": 45,
        "min_magnesium": 220,      # Pregnancy recommendation (relaxed)
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 2200,     # Higher potassium needs (relaxed)
        "max_potassium": 10000,
        "min_zinc": 6,             # Higher zinc needs during pregnancy (relaxed)
        "max_zinc": 40,
        "min_sodium": 1000,
        "max_sodium": 2600,
        "min_cholesterol": 0,
        "max_cholesterol": 450,
        "min_fiber": 16,           # Higher fiber needs during pregnancy (relaxed)
        "max_fiber": 80
    }
    
    return {
        "foods": foods,
        "constraints": pregnancy_constraints
    }


def create_heart_healthy_request() -> Dict[str, Any]:
    """Create a heart-healthy diet optimization request."""
    
    # Use the same comprehensive food database
    foods = create_sample_request()["foods"]
    
    # Heart-healthy nutritional constraints (relaxed for feasibility)
    heart_constraints = {
        "min_calories": 1400,
        "max_calories": 2200,
        "min_protein": 70,
        "max_protein": 150,
        "min_carbs": 100,
        "max_carbs": 250,
        "min_fat": 30,
        "max_fat": 80,
        "min_vitamin_a": 400,
        "max_vitamin_a": 3000,
        "min_vitamin_c": 60,       # Higher for antioxidant benefits (relaxed)
        "max_vitamin_c": 2000,
        "min_vitamin_d": 8,        # Higher for cardiovascular health (relaxed)
        "max_vitamin_d": 100,
        "min_vitamin_b12": 2.4,    # Important for heart health
        "max_vitamin_b12": 1000,
        "min_folate": 400,         # Helps reduce homocysteine
        "max_folate": 1000,
        "min_vitamin_e": 15,       # Antioxidant for heart health
        "max_vitamin_e": 1000,
        "min_vitamin_k": 90,       # Important for cardiovascular health
        "max_vitamin_k": 10000,
        "min_calcium": 600,        # Relaxed from 1200
        "max_calcium": 2500,
        "min_iron": 6,
        "max_iron": 45,
        "min_magnesium": 220,      # Good for heart health (relaxed)
        "max_magnesium": 800,      # Safe upper limit
        "min_potassium": 2200,     # High potassium for heart health (relaxed)
        "max_potassium": 10000,
        "min_zinc": 5,
        "max_zinc": 40,
        "min_sodium": 600,         # Low sodium for heart health
        "max_sodium": 1800,        # Slightly relaxed upper limit
        "min_cholesterol": 0,      # Minimize cholesterol
        "max_cholesterol": 200,    # Low cholesterol limit (relaxed)
        "min_fiber": 20,           # High fiber for heart health (relaxed)
        "max_fiber": 80
    }
    
    return {
        "foods": foods,
        "constraints": heart_constraints
    }


def optimize_diet(request_data: Dict[str, Any], api_url: str = "http://localhost:8002") -> None:
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
        
        # Calculate total weight for nutrient density analysis
        total_weight = sum(food['quantity_grams'] for food in result['optimal_quantities'])
        print(f"Total Weight: {total_weight:.1f}g")
        
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
        print(f"  Fiber:        {summary['total_fiber']:>7.1f}g")
        print(f"  Vitamin A:    {summary['total_vitamin_a']:>7.1f} mcg RAE")
        print(f"  Vitamin C:    {summary['total_vitamin_c']:>7.1f} mg")
        print(f"  Vitamin D:    {summary['total_vitamin_d']:>7.1f} mcg")
        print(f"  Calcium:      {summary['total_calcium']:>7.1f} mg")
        print(f"  Iron:         {summary['total_iron']:>7.1f} mg")
        print(f"  Magnesium:    {summary['total_magnesium']:>7.1f} mg")
        print(f"  Potassium:    {summary['total_potassium']:>7.1f} mg")
        print(f"  Zinc:         {summary['total_zinc']:>7.1f} mg")
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
            ("Fiber", satisfaction['fiber_within_bounds']),
            ("Vitamin A", satisfaction['vitamin_a_within_bounds']),
            ("Vitamin C", satisfaction['vitamin_c_within_bounds']),
            ("Vitamin D", satisfaction['vitamin_d_within_bounds']),
            ("Calcium", satisfaction['calcium_within_bounds']),
            ("Iron", satisfaction['iron_within_bounds']),
            ("Magnesium", satisfaction['magnesium_within_bounds']),
            ("Potassium", satisfaction['potassium_within_bounds']),
            ("Zinc", satisfaction['zinc_within_bounds']),
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
    print("Demonstrating 15-nutrient optimization across multiple use cases")
    
    # Check if API is running
    try:
        response = requests.get("http://localhost:8002/health", timeout=5)
        if response.status_code != 200:
            print("Error: API is not responding correctly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("Error: Cannot connect to API at http://localhost:8002")
        print("Please make sure the API server is running with Docker or uvicorn")
        sys.exit(1)
    
    # Example 1: Standard healthy adult diet (cost-optimized)
    print("\n1. COST-OPTIMIZED DIET PLANNING")
    print("   Objective: Minimize total cost while meeting nutritional needs")
    standard_request = create_sample_request()
    optimize_diet(standard_request)
    
    # Example 2: Nutrient density optimization (equal costs)
    print("\n\n2. NUTRIENT DENSITY OPTIMIZATION")
    print("   Objective: Minimize food weight (all costs = 1) for maximum nutrient density")
    print("   Perfect for: Space missions, backpacking, medical nutrition")
    density_request = create_nutrient_density_request()
    optimize_diet(density_request)
    
    # Example 3: Pregnancy nutrition
    print("\n\n3. PREGNANCY NUTRITION PROFILE")
    print("   Objective: Meet elevated nutritional needs during pregnancy")
    pregnancy_request = create_pregnancy_request()
    optimize_diet(pregnancy_request)
    
    # Example 4: Heart-healthy diet
    print("\n\n4. HEART-HEALTHY DIET PROFILE")
    print("   Objective: Optimize for cardiovascular health")
    heart_request = create_heart_healthy_request()
    optimize_diet(heart_request)
    
    print("\n" + "="*80)
    print("DEMO COMPLETE")
    print("="*80)
    print("The Enhanced Diet Optimizer API supports comprehensive nutritional optimization")
    print("across 15 essential nutrients with multiple optimization objectives!")


if __name__ == "__main__":
    main()