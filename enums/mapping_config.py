from enums.models_enums import CuisineType, EstablishmentType, MealType, DiningStyle, PopularFoodItem, DietaryPreference, Vibe

# ==========================================
# 2. EXCLUSIONS (Blacklist)
# ==========================================
EXCLUDED_CATEGORIES = {
    "Shopping mall", 
    "Outlet mall", 
    "Traditional market", 
    "Night market", 
    "Flea market", 
    "Clothes market", 
    "Market", 
    "Department store", 
    "Discount store", 
    "Stores and shopping", 
    "Supermarket", 
    "Grocery store", 
    "Convenience store", 
    "General store", 
    "Boutique",
    "Asian grocery store",
    "Indian grocery store",
    "Italian grocery store",
    "Japanese grocery store",
    "Mexican grocery store",
    "Russian grocery store"
}

# ==========================================
# 3. SUPPLEMENTARY FIELD MAPPINGS
# ==========================================
ATMOSPHERE_MAPPING = {
    "Casual": [Vibe.CASUAL],
    "Cosy": [Vibe.COZY],
    "Cozy": [Vibe.COZY],
    "Romantic": [Vibe.ROMANTIC],
    "Trending": [Vibe.TRENDY],
    "Lively": [Vibe.TRENDY],
    "Upmarket": [Vibe.UPSCALE],
    "Upscale": [Vibe.UPSCALE],
}

CROWD_MAPPING = {
    "Family friendly": [Vibe.FAMILY_FRIENDLY],
    "Family-friendly": [Vibe.FAMILY_FRIENDLY],
    "College students": [Vibe.CASUAL, Vibe.TRENDY],
    "University students": [Vibe.CASUAL, Vibe.TRENDY],
}

DINING_OPTIONS_MAPPING = {
    "Breakfast": [MealType.BREAKFAST_BRUNCH],
    "Lunch": [MealType.LUNCH],
    "Dinner": [MealType.DINNER],
    "Dessert": [PopularFoodItem.ICE_CREAM_DESSERT],
}

OFFERINGS_MAPPING = {
    "Vegetarian options": [DietaryPreference.VEGETARIAN],
    "Halal food": [DietaryPreference.HALAL],
    "Organic dishes": [DietaryPreference.VEGETARIAN],
    "Kids' menu": [Vibe.FAMILY_FRIENDLY],
    "Quick bite": [DiningStyle.FAST_FOOD],
    "Comfort food": [Vibe.COZY],
    "Small plates": [Vibe.TRENDY, DiningStyle.GOURMET],
}

# ==========================================
# 4. IMAGE MAPPING
# ==========================================
# 1. מילון תמונות מלא - עכשיו עם מערך של אופציות לכל ENUM לבחירה רנדומלית
IMAGE_MAPPING = {
    # Popular Food Items (עדיפות 1)
    "PopularFoodItem.HAMBURGER": [
        "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500",
        "https://images.unsplash.com/photo-1586190848861-99aa4a171e90?w=500"
    ],
    "PopularFoodItem.SUSHI": [
        "https://images.unsplash.com/photo-1579871494447-9811cf80d66c?w=500",
        "https://images.unsplash.com/photo-1553621042-f6e147245754?w=500"
    ],
    "PopularFoodItem.PIZZA_PASTA": [
        "https://images.unsplash.com/photo-1513104890138-7c749659a591?w=500",
        "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=500",
        "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=500"
    ],
    "PopularFoodItem.ICE_CREAM_DESSERT": [
        "https://images.unsplash.com/photo-1501443762994-82bd5dace89a?w=500",
        "https://images.unsplash.com/photo-1563805042-7684c8e9e5cb?w=500"
    ],
    "PopularFoodItem.NOODLES_RAMEN": [
        "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=500",
        "https://images.unsplash.com/photo-1552611052-3ba9d739a133?w=500"
    ],
    "PopularFoodItem.SEAFOOD": [
        "https://images.unsplash.com/photo-1519708227418-c8fd9a32b7a2?w=500",
        "https://images.unsplash.com/photo-1615141982883-c7da0e69cb00?w=500"
    ],
    "PopularFoodItem.CHICKEN": [
        "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=500",
        "https://images.unsplash.com/photo-1569058242253-1df69450c5e7?w=500"
    ],
    "PopularFoodItem.STEAK_BBQ": [
        "https://images.unsplash.com/photo-1544025162-d76694265947?w=500",
        "https://images.unsplash.com/photo-1594041680534-e8c8cdebd659?w=500"
    ],
    
    # Cuisine Types (עדיפות 2)
    "CuisineType.AMERICAN": [
        "https://images.unsplash.com/photo-1550547660-d9450f859349?w=500",
        "https://images.unsplash.com/photo-1525351484163-7529414344d8?w=500"
    ],
    "CuisineType.ITALIAN": [
        "https://images.unsplash.com/photo-1533777857889-4be7c70b33f7?w=500",
        "https://images.unsplash.com/photo-1551183053-bf91a1d81141?w=500"
    ],
    "CuisineType.CHINESE": [
        "https://images.unsplash.com/photo-1525755662778-989d0524087e?w=500",
        "https://images.unsplash.com/photo-1541614101331-1a5a3a194e92?w=500"
    ],
    "CuisineType.JAPANESE": [
        "https://images.unsplash.com/photo-1583623025817-d180a2221d0a?w=500",
        "https://images.unsplash.com/photo-1611143669185-af224c5e3252?w=500"
    ],
    "CuisineType.MEXICAN_LATIN": [
        "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?w=500",
        "https://images.unsplash.com/photo-1551504734-5ee1c4a1479b?w=500"
    ],
    "CuisineType.ASIAN_FUSION": [
        "https://images.unsplash.com/photo-1512058564366-18510be2db19?w=500",
        "https://images.unsplash.com/photo-1564834724105-918b73d1b9e0?w=500"
    ],
    "CuisineType.INDIAN": [
        "https://images.unsplash.com/photo-1585938338392-50a59970d2ee?w=500",
        "https://images.unsplash.com/photo-1565557623262-b51c2513a641?w=500"
    ],
    "CuisineType.MEDITERRANEAN_MIDDLE_EAST": [
        "https://images.unsplash.com/photo-1541518763669-27fef04b14ea?w=500",
        "https://images.unsplash.com/photo-1529312266912-b33cfce2eefd?w=500"
    ],
    "CuisineType.EUROPEAN": [
        "https://images.unsplash.com/photo-1595855759920-86582396756a?w=500",
        "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=500"
    ],
    
    # Establishment Types (עדיפות 3)
    "EstablishmentType.RESTAURANT": [
        "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=500",
        "https://images.unsplash.com/photo-1550966871-3ed3cdb5ed0c?w=500"
    ],
    "EstablishmentType.BAR_PUB": [
        "https://images.unsplash.com/photo-1514933651103-005eec06c04b?w=500",
        "https://images.unsplash.com/photo-1574096079513-d8259312b78a?w=500"
    ],
    "EstablishmentType.CAFE": [
        "https://images.unsplash.com/photo-1501339847302-ac426a4a7cbb?w=500",
        "https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=500"
    ],
    "EstablishmentType.BAKERY_CONFECTIONERY": [
        "https://images.unsplash.com/photo-1509440159596-0249088772ff?w=500",
        "https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=500"
    ]
}

# ==========================================
# 5. MAIN CATEGORY MAPPING (Merged & Complete)
# ==========================================
RAW_CATEGORY_MAPPING = {
    # --- American ---
    "American restaurant": [CuisineType.AMERICAN, Vibe.CASUAL],
    "Traditional American restaurant": [CuisineType.AMERICAN, Vibe.FAMILY_FRIENDLY],
    "Southern restaurant (US)": [CuisineType.AMERICAN, Vibe.COZY],
    "Southwestern restaurant (US)": [CuisineType.AMERICAN, Vibe.CASUAL],
    "Cajun restaurant": [CuisineType.AMERICAN, Vibe.CASUAL],
    "Creole restaurant": [CuisineType.AMERICAN, Vibe.COZY],
    "Contemporary Louisiana restaurant": [CuisineType.AMERICAN, Vibe.TRENDY],
    "Canadian restaurant": [CuisineType.AMERICAN, Vibe.CASUAL],
    "New American restaurant": [CuisineType.AMERICAN, DiningStyle.GOURMET, Vibe.TRENDY],
    "Californian restaurant": [CuisineType.AMERICAN, Vibe.TRENDY, DietaryPreference.VEGETARIAN],
    "Pacific Northwest restaurant (US)": [CuisineType.AMERICAN, PopularFoodItem.SEAFOOD, Vibe.UPSCALE],
    "Cheesesteak restaurant": [CuisineType.AMERICAN, PopularFoodItem.HAMBURGER, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Po’ boys restaurant": [CuisineType.AMERICAN, PopularFoodItem.SEAFOOD, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Soul food restaurant": [CuisineType.AMERICAN, Vibe.COZY],
    "Hot dog restaurant": [CuisineType.AMERICAN, DiningStyle.FAST_FOOD],
    "Hot dog stand": [CuisineType.AMERICAN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Native American restaurant": [CuisineType.AMERICAN, Vibe.COZY],
    "Hoagie restaurant": [CuisineType.AMERICAN, DiningStyle.FAST_FOOD, Vibe.CASUAL],

    # --- Italian ---
    "Italian restaurant": [CuisineType.ITALIAN, Vibe.ROMANTIC, Vibe.FAMILY_FRIENDLY],
    "Northern Italian restaurant": [CuisineType.ITALIAN, Vibe.UPSCALE],
    "Southern Italian restaurant": [CuisineType.ITALIAN, Vibe.COZY],
    "Sicilian restaurant": [CuisineType.ITALIAN, Vibe.CASUAL],
    "Roman restaurant": [CuisineType.ITALIAN, Vibe.UPSCALE],
    "Tuscan restaurant": [CuisineType.ITALIAN, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Neapolitan restaurant": [CuisineType.ITALIAN, PopularFoodItem.PIZZA_PASTA, Vibe.CASUAL],
    "Pizza": [CuisineType.ITALIAN, PopularFoodItem.PIZZA_PASTA, Vibe.CASUAL],
    "Pizza restaurant": [CuisineType.ITALIAN, EstablishmentType.RESTAURANT, PopularFoodItem.PIZZA_PASTA, Vibe.FAMILY_FRIENDLY],
    "Pizza Takeout": [CuisineType.ITALIAN, DiningStyle.FAST_FOOD, PopularFoodItem.PIZZA_PASTA, Vibe.CASUAL],
    "Pizza takeaway": [CuisineType.ITALIAN, DiningStyle.FAST_FOOD, PopularFoodItem.PIZZA_PASTA, Vibe.CASUAL],
    "Pizza delivery": [CuisineType.ITALIAN, DiningStyle.FAST_FOOD, PopularFoodItem.PIZZA_PASTA],
    "Pasta shop": [CuisineType.ITALIAN, PopularFoodItem.PIZZA_PASTA, Vibe.CASUAL],

    # --- Chinese ---
    "Chinese restaurant": [CuisineType.CHINESE, EstablishmentType.RESTAURANT, Vibe.FAMILY_FRIENDLY],
    "Chinese food": [CuisineType.CHINESE, Vibe.CASUAL],
    "Delivery Chinese restaurant": [CuisineType.CHINESE, DiningStyle.FAST_FOOD],
    "Chinese takeaway": [CuisineType.CHINESE, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Dim sum restaurant": [CuisineType.CHINESE, EstablishmentType.RESTAURANT, Vibe.TRENDY],
    "Cantonese restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Hunan restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Sichuan restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Shanghainese restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Mandarin restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Hong Kong style fast food restaurant": [CuisineType.CHINESE, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Chinese noodle restaurant": [CuisineType.CHINESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL],
    "Dumpling restaurant": [CuisineType.CHINESE, Vibe.CASUAL],
    "Dan Dan noodle restaurant": [CuisineType.CHINESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL],

    # --- Japanese ---
    "Japanese restaurant": [CuisineType.JAPANESE, EstablishmentType.RESTAURANT, Vibe.UPSCALE],
    "Authentic Japanese restaurant": [CuisineType.JAPANESE, EstablishmentType.RESTAURANT, Vibe.UPSCALE],
    "Japanese food": [CuisineType.JAPANESE, Vibe.CASUAL],
    "Sushi restaurant": [CuisineType.JAPANESE, EstablishmentType.RESTAURANT, PopularFoodItem.SUSHI, Vibe.TRENDY],
    "Sushi takeaway": [CuisineType.JAPANESE, DiningStyle.FAST_FOOD, PopularFoodItem.SUSHI, Vibe.CASUAL],
    "Conveyor belt sushi restaurant": [CuisineType.JAPANESE, EstablishmentType.RESTAURANT, PopularFoodItem.SUSHI, Vibe.FAMILY_FRIENDLY, Vibe.CASUAL],
    "Izakaya restaurant": [CuisineType.JAPANESE, EstablishmentType.BAR_PUB, Vibe.TRENDY, Vibe.CASUAL],
    "Modern izakaya restaurants": [CuisineType.JAPANESE, EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Kaiseki restaurant": [CuisineType.JAPANESE, DiningStyle.GOURMET, Vibe.UPSCALE, Vibe.ROMANTIC],
    "Teppanyaki restaurant": [CuisineType.JAPANESE, EstablishmentType.RESTAURANT, Vibe.TRENDY],
    "Tempura restaurant": [CuisineType.JAPANESE, Vibe.CASUAL],
    "Ramen restaurant": [CuisineType.JAPANESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL, Vibe.COZY],
    "Udon noodle restaurant": [CuisineType.JAPANESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL],
    "Soba noodle shop": [CuisineType.JAPANESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL],
    "Katsudon restaurant": [CuisineType.JAPANESE, Vibe.CASUAL],
    "Sukiyaki restaurant": [CuisineType.JAPANESE, Vibe.COZY],
    "Sukiyaki and Shabu Shabu restaurant": [CuisineType.JAPANESE, Vibe.FAMILY_FRIENDLY],
    "Shabu-shabu restaurant": [CuisineType.JAPANESE, Vibe.COZY],
    "Tonkatsu restaurant": [CuisineType.JAPANESE, Vibe.CASUAL],
    "Yakitori restaurant": [CuisineType.JAPANESE, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Yakiniku restaurant": [CuisineType.JAPANESE, PopularFoodItem.STEAK_BBQ, Vibe.TRENDY],
    "Yakisoba Restaurant": [CuisineType.JAPANESE, PopularFoodItem.NOODLES_RAMEN, Vibe.CASUAL],
    "Takoyaki restaurant": [CuisineType.JAPANESE, Vibe.CASUAL],
    "Anago restaurant": [CuisineType.JAPANESE],
    "Angler fish restaurant": [CuisineType.JAPANESE, PopularFoodItem.SEAFOOD],
    "Seafood donburi restaurant": [CuisineType.JAPANESE, PopularFoodItem.SEAFOOD, PopularFoodItem.SUSHI, Vibe.CASUAL],
    "Kyoto style Japanese restaurant": [CuisineType.JAPANESE, DiningStyle.GOURMET, Vibe.UPSCALE],
    "Japanese curry restaurant": [CuisineType.JAPANESE, Vibe.CASUAL, Vibe.COZY],
    "Japanese sweets restaurant": [CuisineType.JAPANESE, PopularFoodItem.ICE_CREAM_DESSERT],
    "Kushiyaki restaurant": [CuisineType.JAPANESE, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Okonomiyaki restaurant": [CuisineType.JAPANESE, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],
    "Japanese regional restaurant": [CuisineType.JAPANESE, Vibe.COZY],
    "Japanese steakhouse": [CuisineType.JAPANESE, PopularFoodItem.STEAK_BBQ, DiningStyle.GOURMET, Vibe.UPSCALE],

    # --- Mexican & Latin ---
    "Mexican restaurant": [CuisineType.MEXICAN_LATIN, EstablishmentType.RESTAURANT, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],
    "Mexican food": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Mexican goods store": [CuisineType.MEXICAN_LATIN],
    "Mexican torta restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Taco restaurant": [CuisineType.MEXICAN_LATIN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Tex-Mex restaurant": [CuisineType.MEXICAN_LATIN, Vibe.FAMILY_FRIENDLY],
    "Burrito restaurant": [CuisineType.MEXICAN_LATIN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Tamale shop": [CuisineType.MEXICAN_LATIN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Tortilla shop": [CuisineType.MEXICAN_LATIN],
    "Pozole restaurant": [CuisineType.MEXICAN_LATIN, Vibe.COZY],
    "Oaxacan restaurant": [CuisineType.MEXICAN_LATIN, Vibe.COZY],
    "Yucatan restaurant": [CuisineType.MEXICAN_LATIN],
    "Spanish restaurant": [CuisineType.MEXICAN_LATIN, Vibe.UPSCALE],
    "Tapas restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY, Vibe.ROMANTIC],
    "Tapas bar": [CuisineType.MEXICAN_LATIN, EstablishmentType.BAR_PUB, Vibe.TRENDY, Vibe.CASUAL],
    "Latin American restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "South American restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Central American restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Brazilian restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY],
    "Argentinian restaurant": [CuisineType.MEXICAN_LATIN, Vibe.UPSCALE],
    "Peruvian restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY],
    "Colombian restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Venezuelan restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Salvadoran restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Cuban restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY],
    "Dominican restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Puerto Rican restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Guatemalan restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Honduran restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Nicaraguan restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Pan-Latin restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY],
    "Nuevo Latino restaurant": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY, Vibe.UPSCALE],
    "Basque restaurant": [CuisineType.MEXICAN_LATIN, Vibe.UPSCALE],
    "Caribbean restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Jamaican restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Chilean restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Ecuadorian restaurant": [CuisineType.MEXICAN_LATIN, Vibe.CASUAL],
    "Churreria": [CuisineType.MEXICAN_LATIN, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.CASUAL],

    # --- Asian Fusion & Others ---
    "Asian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Asian fusion restaurant": [CuisineType.ASIAN_FUSION, Vibe.TRENDY],
    "Pan-Asian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Southeast Asian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "South Asian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Thai restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Vietnamese restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Pho restaurant": [CuisineType.ASIAN_FUSION, PopularFoodItem.NOODLES_RAMEN, Vibe.COZY, Vibe.CASUAL],
    "Korean restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Korean barbecue restaurant": [CuisineType.ASIAN_FUSION, PopularFoodItem.STEAK_BBQ, Vibe.TRENDY, Vibe.FAMILY_FRIENDLY],
    "Korean beef restaurant": [CuisineType.ASIAN_FUSION, PopularFoodItem.STEAK_BBQ, Vibe.TRENDY],
    "Korean rib restaurant": [CuisineType.ASIAN_FUSION, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Soondae restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Taiwanese restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Malaysian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Singaporean restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Indonesian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Cambodian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Laotian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Burmese restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Nepalese restaurant": [CuisineType.ASIAN_FUSION, Vibe.COZY],
    "Tibetan restaurant": [CuisineType.ASIAN_FUSION, Vibe.COZY],
    "Afghani restaurant": [CuisineType.ASIAN_FUSION, Vibe.COZY],
    "Pakistani restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Bangladeshi restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Filipino restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Hawaiian restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Poke bar": [CuisineType.ASIAN_FUSION, PopularFoodItem.SUSHI, DiningStyle.FAST_FOOD, Vibe.TRENDY],
    "Hot pot restaurant": [CuisineType.ASIAN_FUSION, Vibe.FAMILY_FRIENDLY, Vibe.COZY],
    "Wok restaurant": [CuisineType.ASIAN_FUSION, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Polynesian restaurant": [CuisineType.ASIAN_FUSION, Vibe.TRENDY],
    "Tofu restaurant": [CuisineType.ASIAN_FUSION, DietaryPreference.VEGAN, DietaryPreference.VEGETARIAN],
    "Pacific Rim restaurant": [CuisineType.ASIAN_FUSION, Vibe.UPSCALE],
    "Sundanese restaurant": [CuisineType.ASIAN_FUSION, Vibe.CASUAL],
    "Mongolian barbecue restaurant": [CuisineType.ASIAN_FUSION, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],
    "Noodle shop": [CuisineType.ASIAN_FUSION, PopularFoodItem.NOODLES_RAMEN, DiningStyle.FAST_FOOD, Vibe.CASUAL],

    # --- Indian ---
    "Indian restaurant": [CuisineType.INDIAN, EstablishmentType.RESTAURANT, Vibe.FAMILY_FRIENDLY],
    "Modern Indian restaurant": [CuisineType.INDIAN, DiningStyle.GOURMET, Vibe.TRENDY, Vibe.UPSCALE],
    "South Indian restaurant": [CuisineType.INDIAN, Vibe.CASUAL],
    "Punjabi restaurant": [CuisineType.INDIAN, Vibe.FAMILY_FRIENDLY],
    "Biryani restaurant": [CuisineType.INDIAN, Vibe.CASUAL],
    "Indian Muslim restaurant": [CuisineType.INDIAN, DietaryPreference.HALAL, Vibe.CASUAL],
    "Indian sizzler restaurant": [CuisineType.INDIAN, Vibe.TRENDY],
    "Indian takeaway": [CuisineType.INDIAN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Sri Lankan restaurant": [CuisineType.INDIAN, Vibe.CASUAL],
    "Indian sweets shop": [CuisineType.INDIAN, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.CASUAL],

    # --- Mediterranean & Middle East ---
    "Mediterranean restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, EstablishmentType.RESTAURANT, Vibe.FAMILY_FRIENDLY],
    "Middle Eastern restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],
    "Israeli restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],
    "Falafel restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Kebab shop": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Halal restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, DietaryPreference.HALAL, Vibe.FAMILY_FRIENDLY],
    "Kosher restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, DietaryPreference.KOSHER, Vibe.FAMILY_FRIENDLY],
    "Greek restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],
    "Gyro restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Lebanese restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.UPSCALE],
    "Syrian restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],
    "Turkish restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.COZY],
    "Yemenite restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.COZY],
    "Armenian restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.COZY],
    "Persian restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.UPSCALE],
    "Egyptian restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],
    "Moroccan restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.COZY],
    "Tunisian restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],
    "North African restaurant": [CuisineType.MEDITERRANEAN_MIDDLE_EAST, Vibe.CASUAL],

    # --- European ---
    "European restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Continental restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Modern European restaurant": [CuisineType.EUROPEAN, DiningStyle.GOURMET, Vibe.TRENDY, Vibe.ROMANTIC],
    "Western restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Brasserie": [CuisineType.EUROPEAN, EstablishmentType.RESTAURANT, Vibe.COZY, Vibe.CASUAL],
    "Bistro": [CuisineType.EUROPEAN, EstablishmentType.RESTAURANT, Vibe.COZY, Vibe.ROMANTIC],
    "Provence restaurant": [CuisineType.EUROPEAN, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Southwest France restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Alsace restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Belgian restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Swiss restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Austrian restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "German restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "British restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Modern British restaurant": [CuisineType.EUROPEAN, DiningStyle.GOURMET, Vibe.TRENDY],
    "English restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Irish restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Irish pub": [CuisineType.EUROPEAN, EstablishmentType.BAR_PUB, Vibe.CASUAL, Vibe.COZY],
    "Portuguese restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Romanian restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Czech restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Hungarian restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Polish restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Ukrainian restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Russian restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Uzbeki restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Georgian restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Croatian restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Serbian restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "Scandinavian restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Swedish restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Danish restaurant": [CuisineType.EUROPEAN, Vibe.TRENDY],
    "French restaurant": [CuisineType.EUROPEAN, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Haute French restaurant": [CuisineType.EUROPEAN, DiningStyle.GOURMET, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Modern French restaurant": [CuisineType.EUROPEAN, DiningStyle.GOURMET, Vibe.TRENDY, Vibe.ROMANTIC],
    "Eastern European restaurant": [CuisineType.EUROPEAN, Vibe.COZY],
    "Catalonian restaurant": [CuisineType.EUROPEAN, Vibe.UPSCALE],
    "Fondue restaurant": [CuisineType.EUROPEAN, Vibe.ROMANTIC, Vibe.COZY],
    "Australian restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "New Zealand restaurant": [CuisineType.EUROPEAN, Vibe.CASUAL],
    "French steakhouse restaurant": [CuisineType.EUROPEAN, PopularFoodItem.STEAK_BBQ, DiningStyle.GOURMET, Vibe.UPSCALE],

    # --- Africa & Miscellaneous Ethnics ---
    "African restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "East African restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "West African restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "South African restaurant": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Ethiopian restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY, DietaryPreference.VEGETARIAN],
    "Eritrean restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "Jewish restaurant": [EstablishmentType.RESTAURANT, DietaryPreference.KOSHER, Vibe.FAMILY_FRIENDLY, Vibe.COZY],

    # --- General Establishments & Meals ---
    "Restaurant": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Restaurant or cafe": [EstablishmentType.RESTAURANT, EstablishmentType.CAFE, Vibe.CASUAL],
    "Buffet restaurant": [EstablishmentType.RESTAURANT, MealType.LUNCH, Vibe.FAMILY_FRIENDLY],
    "Family restaurant": [EstablishmentType.RESTAURANT, Vibe.FAMILY_FRIENDLY],
    "Cafeteria": [EstablishmentType.RESTAURANT, MealType.LUNCH, Vibe.CASUAL],
    "Diner": [EstablishmentType.RESTAURANT, MealType.BREAKFAST_BRUNCH, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],
    "Traditional restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "Eclectic restaurant": [EstablishmentType.RESTAURANT, Vibe.TRENDY],
    "Dinner theater": [EstablishmentType.RESTAURANT, MealType.DINNER, Vibe.UPSCALE],
    "Meat dish restaurant": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Down home cooking restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY, Vibe.FAMILY_FRIENDLY],
    "Country food restaurant": [EstablishmentType.RESTAURANT, Vibe.COZY],
    "Dance restaurant": [EstablishmentType.RESTAURANT, Vibe.TRENDY],
    "Ethnic restaurant": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Fusion restaurant": [CuisineType.ASIAN_FUSION, Vibe.TRENDY],
    "Bed & breakfast": [MealType.BREAKFAST_BRUNCH, Vibe.COZY],

    # --- Bars, Pubs & Nightlife ---
    "Bar": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Pub": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Bar & grill": [EstablishmentType.BAR_PUB, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Gastropub": [EstablishmentType.BAR_PUB, DiningStyle.GOURMET, Vibe.TRENDY],
    "Beer garden": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Beer hall": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Brewpub": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Brewery": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Cider bar": [EstablishmentType.BAR_PUB, Vibe.COZY],
    "Wine bar": [EstablishmentType.BAR_PUB, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Tiki bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Salsa bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Cocktail bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY, Vibe.UPSCALE],
    "Hookah bar": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Piano bar": [EstablishmentType.BAR_PUB, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Dart bar": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Sports bar": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Lounge": [EstablishmentType.BAR_PUB, Vibe.UPSCALE],
    "Stand bar": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Wine cellar": [EstablishmentType.BAR_PUB, Vibe.ROMANTIC],
    "Wine club": [EstablishmentType.BAR_PUB, Vibe.UPSCALE],
    "Winery": [EstablishmentType.BAR_PUB, Vibe.UPSCALE],
    "Sake brewery": [EstablishmentType.BAR_PUB, Vibe.UPSCALE],
    "Club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Dance club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Disco club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Night club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Live music bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Jazz club": [EstablishmentType.BAR_PUB, Vibe.ROMANTIC, Vibe.UPSCALE],
    "Blues club": [EstablishmentType.BAR_PUB, Vibe.COZY, Vibe.CASUAL],
    "Rock music club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Gay bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Gay night club": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Cabaret club": [EstablishmentType.BAR_PUB, Vibe.TRENDY, Vibe.UPSCALE],
    "Comedy club": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Karaoke": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Video karaoke": [EstablishmentType.BAR_PUB, Vibe.TRENDY],

    # --- Bakery, Confectionery & Desserts ---
    "Bakery": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.COZY],
    "Chinese bakery": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.COZY],
    "Wholesale bakery": [EstablishmentType.BAKERY_CONFECTIONERY],
    "Wedding bakery": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.UPSCALE],
    "Pastry shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.COZY],
    "Patisserie": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.UPSCALE, Vibe.ROMANTIC],
    "Cake shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.FAMILY_FRIENDLY],
    "Cookie shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.FAMILY_FRIENDLY],
    "Cupcake shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.FAMILY_FRIENDLY],
    "Pie shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.COZY],
    "Donut shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.CASUAL],
    "Pretzel store": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.CASUAL],
    "Steamed bun shop": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.CASUAL],
    "Chocolate shop": [EstablishmentType.BAKERY_CONFECTIONERY, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.ROMANTIC],
    "Chocolate cafe": [EstablishmentType.BAKERY_CONFECTIONERY, EstablishmentType.CAFE, Vibe.COZY, Vibe.ROMANTIC],
    "Chocolate artisan": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.UPSCALE],
    "Confectionery": [EstablishmentType.BAKERY_CONFECTIONERY, Vibe.COZY],
    "Bagel shop": [EstablishmentType.BAKERY_CONFECTIONERY, MealType.BREAKFAST_BRUNCH, Vibe.CASUAL],
    "Candy store": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.FAMILY_FRIENDLY],

    # --- Cafe & Coffee ---
    "Cafe": [EstablishmentType.CAFE, Vibe.COZY, Vibe.CASUAL],
    "Coffee shop": [EstablishmentType.CAFE, Vibe.COZY, Vibe.CASUAL],
    "Coffee stand": [EstablishmentType.CAFE, Vibe.CASUAL],
    "Coffee store": [EstablishmentType.CAFE, Vibe.CASUAL],
    "Espresso bar": [EstablishmentType.CAFE, Vibe.TRENDY],
    "Coffee": [EstablishmentType.CAFE, Vibe.CASUAL],
    "Coffee roasters": [EstablishmentType.CAFE, Vibe.TRENDY],
    "Tea house": [EstablishmentType.CAFE, Vibe.COZY],
    "Chinese tea house": [EstablishmentType.CAFE, Vibe.COZY],
    "Bubble tea store": [EstablishmentType.CAFE, Vibe.TRENDY],
    "Internet cafe": [EstablishmentType.CAFE, Vibe.CASUAL],
    "Art cafe": [EstablishmentType.CAFE, Vibe.TRENDY, Vibe.COZY],
    "Childrens cafe": [EstablishmentType.CAFE, Vibe.FAMILY_FRIENDLY],
    "Dog cafe": [EstablishmentType.CAFE, Vibe.CASUAL],
    "Creperie": [EstablishmentType.CAFE, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.ROMANTIC],

    # --- Fast Food, Quick Bites & Casual ---
    "Breakfast restaurant": [MealType.BREAKFAST_BRUNCH, EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Brunch restaurant": [MealType.BREAKFAST_BRUNCH, EstablishmentType.RESTAURANT, Vibe.TRENDY],
    "Pancake restaurant": [MealType.BREAKFAST_BRUNCH, Vibe.FAMILY_FRIENDLY],
    "Lunch restaurant": [MealType.LUNCH, EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Box lunch supplier": [MealType.LUNCH, Vibe.CASUAL],
    "Dinner": [MealType.DINNER, Vibe.CASUAL],
    "Fine dining restaurant": [DiningStyle.GOURMET, EstablishmentType.RESTAURANT, Vibe.UPSCALE, Vibe.ROMANTIC],
    "Gourmet grocery store": [DiningStyle.GOURMET, Vibe.UPSCALE],
    "Fast food restaurant": [DiningStyle.FAST_FOOD, EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Takeout Restaurant": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Takeout restaurant": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Delivery Restaurant": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Sandwich shop": [DiningStyle.FAST_FOOD, EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Deli": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Japanese delicatessen": [DiningStyle.FAST_FOOD, CuisineType.JAPANESE, Vibe.CASUAL],
    "Salad shop": [DiningStyle.FAST_FOOD, DietaryPreference.VEGETARIAN, Vibe.CASUAL],
    "Snack bar": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Soup shop": [DiningStyle.FAST_FOOD, Vibe.COZY],
    "Soup restaurant": [DiningStyle.FAST_FOOD, EstablishmentType.RESTAURANT, Vibe.COZY],
    "Porridge restaurant": [DiningStyle.FAST_FOOD, Vibe.COZY],
    "Quick bite": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Food court": [DiningStyle.FAST_FOOD, MealType.LUNCH, Vibe.CASUAL],
    "Juice shop": [DiningStyle.FAST_FOOD, DietaryPreference.VEGETARIAN, Vibe.CASUAL],
    "Small plates restaurant": [DiningStyle.GOURMET, Vibe.TRENDY, Vibe.UPSCALE],
    "Rice restaurant": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Butcher shop deli": [DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Cheese shop": [DiningStyle.GOURMET, Vibe.COZY],
    "Charcuterie": [DiningStyle.GOURMET, Vibe.UPSCALE, Vibe.ROMANTIC],

    # --- Popular Food Items (Burgers, Sweets, Seafood, Meat, etc.) ---
    "Hamburger restaurant": [PopularFoodItem.HAMBURGER, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Grill": [PopularFoodItem.HAMBURGER, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Ice cream shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.FAMILY_FRIENDLY],
    "Frozen yogurt shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.FAMILY_FRIENDLY],
    "Fruit parlor": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.CASUAL],
    "Açaí shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.TRENDY],
    "Sweets and dessert buffet": [PopularFoodItem.ICE_CREAM_DESSERT, MealType.DINNER, Vibe.FAMILY_FRIENDLY],
    "Dessert restaurant": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.ROMANTIC],
    "Dessert shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.FAMILY_FRIENDLY],
    "Seafood": [PopularFoodItem.SEAFOOD],
    "Seafood restaurant": [PopularFoodItem.SEAFOOD, EstablishmentType.RESTAURANT, Vibe.UPSCALE],
    "Fish and seafood restaurant": [PopularFoodItem.SEAFOOD, EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Oyster bar restaurant": [PopularFoodItem.SEAFOOD, EstablishmentType.BAR_PUB, Vibe.UPSCALE, Vibe.ROMANTIC],
    "Crab house": [PopularFoodItem.SEAFOOD, PopularFoodItem.STEAK_BBQ, Vibe.CASUAL],
    "Fish & chips restaurant": [PopularFoodItem.SEAFOOD, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Fish and chips takeaway": [PopularFoodItem.SEAFOOD, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Chicken restaurant": [PopularFoodItem.CHICKEN, Vibe.CASUAL],
    "Chicken shop": [PopularFoodItem.CHICKEN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Chicken wings restaurant": [PopularFoodItem.CHICKEN, EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Fried chicken takeaway": [PopularFoodItem.CHICKEN, DiningStyle.FAST_FOOD, Vibe.CASUAL],
    "Steak house": [PopularFoodItem.STEAK_BBQ, EstablishmentType.RESTAURANT, Vibe.UPSCALE],
    "Chophouse restaurant": [PopularFoodItem.STEAK_BBQ, DiningStyle.GOURMET, Vibe.UPSCALE],
    "Barbecue restaurant": [PopularFoodItem.STEAK_BBQ, Vibe.CASUAL, Vibe.FAMILY_FRIENDLY],

    # --- Dietary & Healthy ---
    "Vegan restaurant": [DietaryPreference.VEGAN, DietaryPreference.VEGETARIAN, Vibe.TRENDY],
    "Vegetarian restaurant": [DietaryPreference.VEGETARIAN, Vibe.CASUAL],
    "Vegetarian cafe and deli": [DietaryPreference.VEGETARIAN, EstablishmentType.CAFE, Vibe.COZY],
    "Organic restaurant": [DietaryPreference.VEGETARIAN, Vibe.TRENDY],
    "Raw food restaurant": [DietaryPreference.VEGETARIAN, Vibe.TRENDY],
    "Health food restaurant": [DietaryPreference.VEGETARIAN, Vibe.CASUAL],
    "Gluten-free restaurant": [DietaryPreference.GLUTEN_FREE, Vibe.CASUAL],

    # --- Missing from parquet scan ---
    "Bar & Pub": [EstablishmentType.BAR_PUB, Vibe.CASUAL],
    "Nightlife": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Food": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Food and drink": [EstablishmentType.RESTAURANT, Vibe.CASUAL],
    "Karaoke bar": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Live music venue": [EstablishmentType.BAR_PUB, Vibe.TRENDY],
    "Steakhouse": [PopularFoodItem.STEAK_BBQ, EstablishmentType.RESTAURANT, Vibe.UPSCALE],
    "Tapas": [CuisineType.MEXICAN_LATIN, Vibe.TRENDY],
    "Izakaya": [CuisineType.JAPANESE, EstablishmentType.BAR_PUB, Vibe.TRENDY],

    # --- Encoding variants (parquet stores these with special chars) ---
    "Crêperie": [EstablishmentType.CAFE, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.ROMANTIC],
    "CrÃªperie": [EstablishmentType.CAFE, PopularFoodItem.ICE_CREAM_DESSERT, Vibe.ROMANTIC],
    "Açaí shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.TRENDY],
    "AÃ§aÃ­ shop": [PopularFoodItem.ICE_CREAM_DESSERT, Vibe.TRENDY],
    "Poâ€™ boys restaurant": [CuisineType.AMERICAN, PopularFoodItem.SEAFOOD, DiningStyle.FAST_FOOD, Vibe.CASUAL],
}