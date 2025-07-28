# Diet Optimizer API 🍎⚖️

A modern FastAPI implementation that solves the classic **Diet Problem** using linear programming to find the optimal combination of foods that meets nutritional requirements while minimizing cost.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](./tests/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)


## ⚠️ **IMPORTANT MEDICAL DISCLAIMER**

> **🏥 NOT MEDICAL OR DIETARY ADVICE**
> 
> This API and the nutritional information provided are for **educational and demonstration purposes only**. This software is **NOT intended to provide medical, dietary, or health advice** of any kind.
> 
> **Before using this application for any dietary planning:**
> - **Consult with a qualified physician** or registered dietitian who understands your specific health needs
> - **Individual nutritional requirements vary significantly** based on age, gender, health conditions, medications, activity level, and other factors
> - **The RDA values shown are general guidelines** and may not be appropriate for your specific situation
> 
> **The authors and contributors of this software:**
> - **Disclaim all responsibility** for any adverse health effects or consequences arising from the use or misuse of this API
> - **Make no warranties** regarding the accuracy, completeness, or suitability of any nutritional calculations
> - **Strongly recommend professional medical consultation** before making any significant dietary changes
> 
> **Use this tool at your own risk and discretion. Your health and safety are your responsibility.**



## 🎯 Features

- **🧮 Linear Programming Optimization** - Uses SciPy's HiGHS solver for robust mathematical optimization
- **🥗 Comprehensive Nutrition** - Optimizes across **15 essential nutrients** (macronutrients + vitamins/minerals)
- **💰 Cost Minimization** - Finds the cheapest food combination meeting all nutritional constraints
- **🎯 Nutrient Density Optimization** - Set equal costs to minimize food weight and maximize nutrient density
- **🏥 Health-Focused** - Supports specialized dietary profiles (pregnancy, heart-healthy, athletic)
- **⚡ Fast & Scalable** - Built with FastAPI for high-performance async processing
- **📊 Interactive Documentation** - Auto-generated Swagger UI with comprehensive examples
- **🐳 Docker Ready** - Containerized for easy deployment and scaling
- **🧪 Well Tested** - 100% test coverage with realistic nutritional scenarios

## 📚 Mathematical & Historical Background

### The Diet Problem

The **Diet Problem** is one of the earliest and most famous applications of linear programming, first formulated by Nobel Prize winner George Dantzig in 1945. Originally created to help the U.S. Army determine the most economical way to feed soldiers while meeting their nutritional needs, it has since become a cornerstone problem in optimization theory.

### Linear Programming Foundation

Linear programming is a mathematical method for finding the best outcome (such as minimum cost) in a mathematical model whose requirements are represented by linear relationships. The Diet Problem exemplifies this perfectly:

- **Objective**: Minimize total food cost (or total food weight for nutrient density)
- **Variables**: Quantities of each food item
- **Constraints**: Nutritional requirements (minimum/maximum bounds for each nutrient)
- **Method**: Simplex algorithm or modern interior-point methods






### Mathematical Formulation

```
Minimize: Σ(cost_per_100g[i] × quantity[i]) for all foods i

Subject to:
min_nutrient[j] ≤ Σ(nutrient_per_100g[j,i] × quantity[i]) ≤ max_nutrient[j]
for all nutrients j and foods i

quantity[i] ≥ 0 for all foods i
```

This API extends the classical 4-nutrient formulation to **15 comprehensive nutrients**, making it suitable for real-world dietary planning.

## 🥗 Supported Nutrients

### Macronutrients (grams)
- **Calories** - Total energy content
- **Protein** - Essential for muscle building and repair
- **Carbohydrates** - Primary energy source  
- **Fat** - Essential fatty acids and energy storage
- **Fiber** - Digestive health and satiety

### Vitamins & Minerals
- **Vitamin A** (mcg RAE) - Eye health, immune function
- **Vitamin C** (mg) - Antioxidant, immune support
- **Vitamin D** (mcg) - Bone health, immune function
- **Calcium** (mg) - Bone health, muscle function
- **Iron** (mg) - Oxygen transport, energy metabolism
- **Magnesium** (mg) - Muscle and nerve function, energy production
- **Potassium** (mg) - Heart health, muscle function
- **Zinc** (mg) - Immune function, wound healing, protein synthesis
- **Sodium** (mg) - Fluid balance, nerve function
- **Cholesterol** (mg) - Cardiovascular health monitoring

> ⚠️ **Important**: Vitamin A is measured in **micrograms (mcg RAE)**, Vitamin D in **micrograms (mcg)**, all other nutrients in **milligrams (mg)**. Fiber is measured in **grams (g)**.

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Poetry (recommended) or pip

### Local Development Setup

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/api-diet-optimizer.git
cd api-diet-optimizer
```

2. **Install dependencies**
```bash
# Using Poetry (recommended)
poetry install

# Or using pip
pip install -r requirements.txt
```

3. **Start the development server**
```bash
# Using Poetry
poetry run uvicorn app.main:app --reload

# Or directly
uvicorn app.main:app --reload
```

4. **Access the API**
- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Or with Docker directly
docker build -t diet-optimizer .
docker run -p 8000:8000 diet-optimizer
```

### Run Tests

```bash
# Using Poetry
poetry run pytest tests/ -v

# With coverage report
poetry run pytest tests/ --cov=app --cov-report=html
```

## 🔌 API Endpoints

### `POST /optimize` - Diet Optimization

The main endpoint that solves the diet optimization problem.

**Request Body:**
```json
{
  "foods": [
    {
      "name": "Chicken Breast",
      "cost_per_100g": 3.20,
      "calories_per_100g": 165,
      "carbs_per_100g": 0,
      "protein_per_100g": 31,
      "fat_per_100g": 3.6,
      "vitamin_a_per_100g": 9,         // mcg RAE
      "vitamin_c_per_100g": 0,         // mg
      "vitamin_d_per_100g": 0.1,       // mcg
      "calcium_per_100g": 15,          // mg
      "iron_per_100g": 0.9,            // mg
      "magnesium_per_100g": 22,        // mg
      "potassium_per_100g": 256,       // mg
      "zinc_per_100g": 1.0,            // mg
      "sodium_per_100g": 74,           // mg
      "cholesterol_per_100g": 85,      // mg
      "fiber_per_100g": 0              // g
    }
  ],
  "constraints": {
    "min_calories": 1800, "max_calories": 2200,
    "min_protein": 120, "max_protein": 180,
    "min_carbs": 150, "max_carbs": 250,
    "min_fat": 50, "max_fat": 80,
    "min_vitamin_a": 700, "max_vitamin_a": 3000,      // mcg RAE
    "min_vitamin_c": 75, "max_vitamin_c": 2000,       // mg
    "min_vitamin_d": 15, "max_vitamin_d": 100,        // mcg
    "min_calcium": 1000, "max_calcium": 2500,         // mg
    "min_iron": 8, "max_iron": 45,                    // mg
    "min_magnesium": 310, "max_magnesium": 800,       // mg
    "min_potassium": 3500, "max_potassium": 4700,     // mg
    "min_zinc": 8, "max_zinc": 40,                    // mg
    "min_sodium": 1500, "max_sodium": 2300,           // mg
    "min_cholesterol": 0, "max_cholesterol": 300,     // mg
    "min_fiber": 25, "max_fiber": 70                  // g
  }
}
```

**Response:**
```json
{
  "status": "optimal",
  "total_cost": 12.45,
  "optimal_quantities": [
    {
      "food_name": "Chicken Breast",
      "quantity_100g": 1.5,
      "quantity_grams": 150.0,
      "cost": 4.80
    }
  ],
  "nutritional_summary": {
    "total_calories": 2000.0,
    "total_protein": 150.0,
    "total_carbs": 200.0,
    "total_fat": 65.0,
    "total_vitamin_a": 800.0,
    "total_vitamin_c": 90.0,
    "total_vitamin_d": 18.0,
    "total_calcium": 1200.0,
    "total_iron": 15.0,
    "total_magnesium": 350.0,
    "total_potassium": 4000.0,
    "total_zinc": 12.0,
    "total_sodium": 2000.0,
    "total_cholesterol": 250.0,
    "total_fiber": 30.0
  },
  "constraint_satisfaction": {
    "calories_within_bounds": true,
    "protein_within_bounds": true,
    "carbs_within_bounds": true,
    "fat_within_bounds": true,
    "vitamin_a_within_bounds": true,
    "vitamin_c_within_bounds": true,
    "vitamin_d_within_bounds": true,
    "calcium_within_bounds": true,
    "iron_within_bounds": true,
    "magnesium_within_bounds": true,
    "potassium_within_bounds": true,
    "zinc_within_bounds": true,
    "sodium_within_bounds": true,
    "cholesterol_within_bounds": true,
    "fiber_within_bounds": true
  }
}
```

**Response Status Values:**
- `optimal` - Solution found with minimum cost
- `infeasible` - No combination of foods can meet all constraints
- `unbounded` - Cost can be reduced indefinitely (problem formulation error)

### `GET /health` - Health Check

Returns API health status and version information.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "message": "Diet Optimizer API is running"
}
```

### `GET /` - API Information

Returns basic API information and available endpoints.

### `GET /docs` - Interactive Documentation

Swagger UI with interactive API testing capabilities.

## 🏥 Common Use Cases

### 1. **Cost-Optimized Diet Planning**
```python
# Example: Budget-conscious healthy eating
constraints = {
    "min_calories": 1800, "max_calories": 2000,
    "min_protein": 100, "max_protein": 150,
    # ... other constraints
}
foods = [
    {"name": "Chicken", "cost_per_100g": 3.20, ...},
    {"name": "Rice", "cost_per_100g": 1.10, ...}
]
```

### 2. **Nutrient Density Optimization** 🆕
Set all food costs to 1 to minimize total food weight and maximize nutrient density:

```python
# Example: Maximum nutrient density (space-constrained scenarios)
foods = [
    {"name": "Chicken", "cost_per_100g": 1, ...},  # Equal costs
    {"name": "Spinach", "cost_per_100g": 1, ...},  # Equal costs
    {"name": "Quinoa", "cost_per_100g": 1, ...}    # Equal costs
]
# Result: Optimizer selects most nutrient-dense foods with minimal weight
```

**Perfect for:**
- 🚀 **Space missions** - Minimize weight/volume while meeting nutrition
- 🏕️ **Backpacking/camping** - Lightweight, nutritionally complete meals
- 🏥 **Medical nutrition** - Maximum nutrients in smallest portions
- 📊 **Nutrition analysis** - Identify most nutrient-dense food combinations

### 3. **Specialized Dietary Profiles**

**Pregnancy Nutrition:**
- High iron (27mg daily)
- Elevated calcium (1200mg)
- Increased calories for fetal development

**Heart-Healthy Diet:**
- High potassium (≥4700mg)
- Low sodium (≤1500mg)
- Limited cholesterol (≤150mg)

**Athletic Performance:**
- High protein for muscle recovery
- Optimized carbohydrates for energy
- Balanced micronutrients for performance

## 📊 Recommended Daily Values (RDA)

| Nutrient | Adult RDA | Upper Limit | Units |
|----------|-----------|-------------|-------|
| Calories | 1800-2400 | 3000+ | kcal |
| Protein | 46-56g | 200g+ | g |
| Carbohydrates | 130g | 300g+ | g |
| Fat | 20-35% calories | 100g+ | g |
| **Fiber** | **25-38** | **70** | **g** |
| **Vitamin A** | **700-900** | **3000** | **mcg RAE** |
| **Vitamin C** | **65-90** | **2000** | **mg** |
| **Vitamin D** | **15-20** | **100** | **mcg** |
| **Calcium** | **1000-1200** | **2500** | **mg** |
| **Iron** | **8-18** | **45** | **mg** |
| **Magnesium** | **310-420** | **800** | **mg** |
| **Potassium** | **3500-4700** | **10000** | **mg** |
| **Zinc** | **8-11** | **40** | **mg** |
| **Sodium** | **1500** | **2300** | **mg** |
| **Cholesterol** | **0** | **300** | **mg** |

## 🧪 Example Usage

### **📄 Comprehensive Demo Script**

The [`example_usage.py`](./example_usage.py) file provides a complete demonstration of all API capabilities with realistic food databases and nutritional constraints. This script showcases **4 distinct optimization scenarios** with detailed output formatting.

### **🚀 Running the Examples**

**Prerequisites:** Ensure the API is running locally on **port 8002** (either via Docker or uvicorn):

```bash
# Option 1: Using Docker (recommended)
docker-compose up --build
# API will be available on http://localhost:8002

# Option 2: Using Poetry/uvicorn directly
poetry run uvicorn app.main:app --reload --port 8002
```

**Run the demonstration:**
```bash
# Execute all 4 optimization scenarios
python example_usage.py

# Or with Poetry
poetry run python example_usage.py
```

### **🎯 Demonstrated Use Cases**

#### **1. Cost-Optimized Diet Planning**
- **Objective**: Minimize total food cost while meeting all nutritional requirements
- **Typical Result**: ~$44 for 2kg of nutritionally complete food
- **Best For**: Budget-conscious meal planning, institutional feeding

#### **2. Nutrient Density Optimization** 🆕
- **Objective**: Minimize total food weight (all costs = 1) for maximum nutrient density
- **Typical Result**: ~1.6kg of highly concentrated nutrition
- **Best For**: Space missions, backpacking, emergency rations, medical nutrition

#### **3. Pregnancy Nutrition Profile**
- **Objective**: Meet elevated nutritional needs during pregnancy
- **Key Features**: Higher iron (15mg), calcium (600mg), and caloric requirements
- **Best For**: Maternal nutrition planning, prenatal dietary guidance

#### **4. Heart-Healthy Diet Profile**
- **Objective**: Optimize for cardiovascular health
- **Key Features**: Low sodium (≤600mg), high potassium, omega-3 rich foods
- **Best For**: Cardiac rehabilitation, preventive cardiology, hypertension management

### **📊 Example Output Format**

Each optimization scenario provides:
- **Optimization Status**: OPTIMAL/INFEASIBLE/UNBOUNDED
- **Total Cost & Weight**: Economic and practical metrics
- **Food Quantities**: Precise amounts in grams with individual costs
- **Nutritional Summary**: Complete breakdown of all 15 nutrients
- **Constraint Satisfaction**: ✓/✗ status for each nutritional requirement

### **🔧 Customization**

The script serves as a template for creating your own optimization scenarios:
- **Food Database**: Modify nutritional values or add new foods
- **Constraints**: Adjust min/max bounds for specific dietary needs
- **Objectives**: Change cost coefficients to optimize for different goals

## 🛠️ Technology Stack

- **Backend**: FastAPI 0.104+ with Pydantic validation
- **Optimization**: SciPy 1.16.0 with HiGHS solver
- **Mathematical**: NumPy for numerical computations
- **Containerization**: Docker with multi-stage builds
- **Testing**: Pytest with 100% coverage
- **Documentation**: Auto-generated OpenAPI/Swagger

## 🧪 Testing

The API includes comprehensive tests covering:

- Mathematical accuracy verification
- All 15 nutritional constraints
- Edge cases and error handling
- Specialized dietary scenarios
- API endpoint functionality

```bash
# Run all tests
poetry run pytest tests/ -v

# Run with coverage
poetry run pytest tests/ --cov=app --cov-report=html

# Run specific test categories
poetry run pytest tests/test_optimization.py -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- George Dantzig for pioneering linear programming and the original Diet Problem formulation
- The SciPy community for providing robust optimization algorithms
- FastAPI team for the excellent web framework
- USDA for nutritional data standards and guidelines

## 📞 Support

- **Documentation**: Visit `/docs` for interactive API documentation
- **Issues**: Please use GitHub Issues for bug reports and feature requests
- **Examples**: See `example_usage.py` for working examples

---

**Built with ❤️ for optimal nutrition and cost-effective meal planning** 
