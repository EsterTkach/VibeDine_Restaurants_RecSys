"""
Central mapping layer between user-facing preference strings (produced by the
frontend Vibe Matcher / Onboarding flows) and the enum-backed MongoDB fields
consumed by `get_filtered_restaurants_repo`.

All caller code should route through this module so that legacy Google-Maps
tag names (`atmosphere`, `crowd`, `dining_options`, `offerings`, …) can be
translated into the current `Vibe` / `MealType` / `DietaryPreference` /
`is_accessible` fields that are actually stored on restaurant documents.
"""

from __future__ import annotations

from datetime import datetime

from enums.models_enums import (
    CuisineType,
    DietaryPreference,
    MealType,
    PopularFoodItem,
    Vibe,
)


# ---------------------------------------------------------------------------
# Meal-time (server clock) -> MealType enum
# ---------------------------------------------------------------------------
def map_hour_to_meal_type(hour: int | None = None) -> MealType:
    """
    Server hour -> MealType enum.
      05:00 - 11:59 -> BREAKFAST_BRUNCH
      12:00 - 16:59 -> LUNCH
      17:00 - 04:59 -> DINNER
    """
    if hour is None:
        hour = datetime.now().hour

    if 5 <= hour < 12:
        return MealType.BREAKFAST_BRUNCH
    if 12 <= hour < 17:
        return MealType.LUNCH
    return MealType.DINNER


# ---------------------------------------------------------------------------
# Accessibility (string / list) -> strict boolean
# ---------------------------------------------------------------------------
def map_accessibility_to_bool(value) -> bool | None:
    """
    Onboarding stores accessibility as a single string ("Required" /
    "Not Required"). Vibe Matcher / group filters may still send a list of
    tag strings. Any of these forms are normalized to a strict boolean, or
    None when the user did not express a preference.
    """
    if value is None:
        return None

    if isinstance(value, bool):
        return value

    if isinstance(value, str):
        cleaned = value.strip().lower()
        if not cleaned or cleaned == "not required":
            return None
        if cleaned == "required":
            return True
        # Any other non-empty string (e.g. "Wheelchair accessible entrance")
        # is treated as an explicit accessibility request.
        return True

    if isinstance(value, (list, tuple, set)):
        return True if any(item for item in value) else None

    return None


# ---------------------------------------------------------------------------
# Dietary preference (single string or list) -> list[DietaryPreference values]
# ---------------------------------------------------------------------------
_DIETARY_ALIASES = {
    "gluten free": DietaryPreference.GLUTEN_FREE,
    "gluten-free": DietaryPreference.GLUTEN_FREE,
    "vegan": DietaryPreference.VEGAN,
    "vegetarian": DietaryPreference.VEGETARIAN,
    "kosher": DietaryPreference.KOSHER,
    "halal": DietaryPreference.HALAL,
}


def map_dietary_to_enum_values(value) -> list[str] | None:
    """
    Accepts a single string, a list of strings, or None. Returns the matching
    `DietaryPreference.value` strings suitable for `dietary_preferences=` on
    the repo call. "None" and empty inputs return None.
    """
    if value is None:
        return None

    if isinstance(value, str):
        raw_values = [value]
    elif isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        return None

    mapped: list[str] = []
    for raw in raw_values:
        if not raw:
            continue
        key = str(raw).strip().lower()
        if key in ("", "none"):
            continue
        pref = _DIETARY_ALIASES.get(key)
        if pref is not None:
            mapped.append(pref.value)

    # De-duplicate while preserving order
    seen = set()
    unique = [v for v in mapped if not (v in seen or seen.add(v))]

    return unique or None


# ---------------------------------------------------------------------------
# Vibe (list of user strings) -> list[Vibe values]
# ---------------------------------------------------------------------------
_VIBE_ALIASES = {
    "cozy": Vibe.COZY,
    "cosy": Vibe.COZY,
    "romantic": Vibe.ROMANTIC,
    "casual": Vibe.CASUAL,
    "upscale": Vibe.UPSCALE,
    "upmarket": Vibe.UPSCALE,
    "family friendly": Vibe.FAMILY_FRIENDLY,
    "family-friendly": Vibe.FAMILY_FRIENDLY,
    "trendy": Vibe.TRENDY,
    "trending": Vibe.TRENDY,
    "lively": Vibe.TRENDY,
}


def map_vibe_to_enum_values(value) -> list[str] | None:
    """
    Accepts a single string or a list of vibe strings from onboarding / vibe
    matcher. Returns matching `Vibe.value` strings.
    """
    if value is None:
        return None
    if isinstance(value, str):
        raw_values = [value]
    elif isinstance(value, (list, tuple, set)):
        raw_values = list(value)
    else:
        return None

    mapped: list[str] = []
    for raw in raw_values:
        if not raw:
            continue
        vibe = _VIBE_ALIASES.get(str(raw).strip().lower())
        if vibe is not None:
            mapped.append(vibe.value)

    seen = set()
    unique = [v for v in mapped if not (v in seen or seen.add(v))]

    return unique or None


# ---------------------------------------------------------------------------
# Onboarding "favorite_categories" (mixed popular-foods + cuisines,
# optionally prefixed by an emoji) -> (categories, popular_items)
# ---------------------------------------------------------------------------
_POPULAR_ITEM_VALUES = {item.value for item in PopularFoodItem}
_CUISINE_VALUES = {c.value for c in CuisineType}


def _strip_emoji_prefix(label: str) -> str:
    """`"🍣 Sushi"` -> `"Sushi"`; leaves plain labels untouched."""
    if not label:
        return ""
    stripped = label.strip()
    if " " in stripped and not stripped[0].isalpha():
        return stripped.split(" ", 1)[1].strip()
    return stripped


def split_favorite_categories(favorite_categories) -> tuple[list[str] | None, list[str] | None]:
    """
    Split the user's `favorite_categories` selection into the two
    enum-aligned buckets consumed by the repo:
        - `categories`      -> CuisineType values
        - `popular_items`   -> PopularFoodItem values
    Unknown labels are dropped silently.
    """
    if not favorite_categories:
        return None, None

    cuisines: list[str] = []
    popular: list[str] = []

    for raw in favorite_categories:
        clean = _strip_emoji_prefix(str(raw))
        if not clean:
            continue
        if clean in _POPULAR_ITEM_VALUES:
            popular.append(clean)
        elif clean in _CUISINE_VALUES:
            cuisines.append(clean)
        # else: silently ignore unknown labels

    def _dedupe(items: list[str]) -> list[str] | None:
        seen = set()
        result = [i for i in items if not (i in seen or seen.add(i))]
        return result or None

    return _dedupe(cuisines), _dedupe(popular)
