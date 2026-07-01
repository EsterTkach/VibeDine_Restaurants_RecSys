from enum import Enum

class CuisineType(Enum):
    """ סוגי מטבחים ומוצא גיאוגרפי """
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
    """ סוג המבנה / העסק """
    RESTAURANT = "Restaurant"
    BAR_PUB = "Bar & Pub"
    BAKERY_CONFECTIONERY = "Bakery & Confectionery"
    CAFE = "Cafe"

class MealType(Enum):
    """ סוג הארוחה לפי שעות היום """
    BREAKFAST_BRUNCH = "Breakfast & Brunch"
    LUNCH = "Lunch"
    DINNER = "Dinner"

class DiningStyle(Enum):
    """ סגנון ומהירות השירות """
    GOURMET = "Gourmet / Fine Dining"
    FAST_FOOD = "Fast Food / Quick Bite"

class PopularFoodItem(Enum):
    """ מאכלים פופולריים ספציפיים לסינון ממוקד """
    HAMBURGER = "Hamburger"
    SUSHI = "Sushi"
    PIZZA_PASTA = "Pizza & Pasta"
    ICE_CREAM_DESSERT = "Ice Cream & Dessert"
    NOODLES_RAMEN = "Noodles & Ramen"
    SEAFOOD = "Seafood"
    CHICKEN = "Chicken"
    STEAK_BBQ = "Steak & BBQ"

class DietaryPreference(Enum):
    """ העדפות דיאטטיות ודתיות """
    VEGAN = "Vegan"
    VEGETARIAN = "Vegetarian"
    KOSHER = "Kosher"
    HALAL = "Halal"
    GLUTEN_FREE = "Gluten-Free"