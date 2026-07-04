from enum import Enum

# ==========================================
# 1. ENUMS
# ==========================================
class CuisineType(Enum):
    AMERICAN = "American"
    ITALIAN = "Italian"
    CHINESE = "Chinese"
    JAPANESE = "Japanese"
    MEXICAN_LATIN = "Mexican & Latin"
    ASIAN_FUSION = "Asian Fusion"
    INDIAN = "Indian"
    MEDITERRANEAN_MIDDLE_EAST = "Mediterranean & Middle East"
    EUROPEAN = "European"

class EstablishmentType(Enum):
    RESTAURANT = "Restaurant"
    BAR_PUB = "Bar & Pub"
    BAKERY_CONFECTIONERY = "Bakery & Confectionery"
    CAFE = "Cafe"

class MealType(Enum):
    BREAKFAST_BRUNCH = "Breakfast & Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"

class DiningStyle(Enum):
    GOURMET = "Gourmet / Fine Dining"
    FAST_FOOD = "Fast Food / Quick Bite"

class PopularFoodItem(Enum):
    HAMBURGER = "Hamburger"
    SUSHI = "Sushi"
    PIZZA_PASTA = "Pizza & Pasta"
    ICE_CREAM_DESSERT = "Ice Cream & Dessert"
    NOODLES_RAMEN = "Noodles & Ramen"
    SEAFOOD = "Seafood"
    CHICKEN = "Chicken"
    STEAK_BBQ = "Steak & BBQ"

class DietaryPreference(Enum):
    VEGAN = "Vegan"
    VEGETARIAN = "Vegetarian"
    KOSHER = "Kosher"
    HALAL = "Halal"
    GLUTEN_FREE = "Gluten-Free"

class Vibe(Enum):
    COZY = "Cozy"
    ROMANTIC = "Romantic"
    CASUAL = "Casual"
    UPSCALE = "Upscale"
    FAMILY_FRIENDLY = "Family Friendly"
    TRENDY = "Trendy"