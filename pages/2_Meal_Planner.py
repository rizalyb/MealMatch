import streamlit as st
import pandas as pd
import re
from pathlib import Path


# --------------------------------------------------
# IMAGE FOLDERS
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent.parent

HOMEMADE_DIR = APP_DIR / "images" / "homemade"
RESTAURANT_DIR = APP_DIR / "images" / "restaurant"
INGREDIENTS_DIR = APP_DIR / "images" / "ingredients"


# --------------------------------------------------
# LOAD SHARED DATA AND PREFERENCES
# --------------------------------------------------

meals = st.session_state["meals"]
ingredients = st.session_state["ingredients"]

budget = st.session_state["budget"]
weekly_budget = st.session_state["weekly_budget"]
use_weekly_budget = st.session_state["use_weekly_budget"]

max_time = st.session_state["max_time"]
desired_servings = st.session_state["desired_servings"]
plan_days = st.session_state["plan_days"]

dietary_restrictions = st.session_state["dietary_restrictions"]
food_preferences = st.session_state["food_preferences"]

max_calories = st.session_state["max_calories"]
min_protein = st.session_state["min_protein"]


# --------------------------------------------------
# HELPER FUNCTION FOR PRICE CONVERSION
# --------------------------------------------------

def convert_price(value):

    if pd.isna(value):
        return float("nan")

    cleaned_value = (
        str(value)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    return pd.to_numeric(cleaned_value, errors="coerce")


# --------------------------------------------------
# PHOTO HOVER CONTROLS
# --------------------------------------------------

st.markdown(
    """
    <style>

    div[class*="st-key-photo_viewer_"] {
        position: relative;
    }

    div[class*="st-key-photo_prev_"],
    div[class*="st-key-photo_next_"],
    div[class*="st-key-photo_expand_"] {
        position: absolute !important;
        z-index: 10;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_prev_"],
    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_next_"],
    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_expand_"] {
        opacity: 1;
    }

    /* Left arrow */
    div[class*="st-key-photo_prev_"] {
        left: 30%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Right arrow */
    div[class*="st-key-photo_next_"] {
        right: 30%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Expand icon */
    div[class*="st-key-photo_expand_"] {
        right: 30%;
        bottom: 8px;
    }

    /* Button appearance */
    div[class*="st-key-photo_prev_"] button,
    div[class*="st-key-photo_next_"] button,
    div[class*="st-key-photo_expand_"] button {
        border-radius: 50%;
        background-color: rgba(0, 0, 0, 0.65);
        color: white;
        border: none;
        min-width: 38px;
        width: 38px;
        height: 38px;
        padding: 0;
        font-size: 22px;
    }

    div[class*="st-key-photo_prev_"] button:hover,
    div[class*="st-key-photo_next_"] button:hover,
    div[class*="st-key-photo_expand_"] button:hover {
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# PHOTO HELPER FUNCTIONS
# --------------------------------------------------

def get_image_name(meal_name):

    name = str(meal_name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")


def get_meal_photo_paths(meal_name):

    image_name = get_image_name(meal_name)

    possible_photos = [
        (HOMEMADE_DIR, f"{image_name}_hm"),
        (RESTAURANT_DIR, f"{image_name}_r"),
        (INGREDIENTS_DIR, f"{image_name}_i")
    ]

    image_paths = []

    for folder, filename in possible_photos:

        for extension in [".jpeg", ".jpg", ".png"]:

            photo_path = folder / f"{filename}{extension}"

            if photo_path.exists():

                image_paths.append(photo_path)
                break

    return image_paths


# --------------------------------------------------
# ENLARGED RECIPE PHOTO DIALOG
# --------------------------------------------------

@st.dialog("Recipe Photos", width="large")
def show_large_photo():

    image_paths = st.session_state.get(
        "large_photo_paths", []
    )

    if not image_paths:
        st.info("No recipe photos are available.")
        return

    selected_photo = st.session_state.get(
        "large_photo_index", 0
    )

    selected_photo = selected_photo % len(image_paths)

    st.image(
        image_paths[selected_photo],
        use_container_width=False,
        width=720
    )

    photo_name = Path(
        image_paths[selected_photo]
    ).stem

    if photo_name.endswith("_hm"):
        photo_label = "Homemade"

    elif photo_name.endswith("_r"):
        photo_label = "Restaurant"

    elif photo_name.endswith("_i"):
        photo_label = "Ingredients"

    else:
        photo_label = "Recipe Photo"

    st.caption(
        f"{photo_label} Photo "
        f"({selected_photo + 1} of {len(image_paths)})"
    )

    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:

            if st.button(
                "← Previous",
                use_container_width=True,
                key="meal_planner_dialog_previous_photo"
            ):

                st.session_state["large_photo_index"] = (
                    selected_photo - 1
                ) % len(image_paths)

                st.rerun(scope="fragment")

        with next_col:

            if st.button(
                "Next →",
                use_container_width=True,
                key="meal_planner_dialog_next_photo"
            ):

                st.session_state["large_photo_index"] = (
                    selected_photo + 1
                ) % len(image_paths)

                st.rerun(scope="fragment")


# --------------------------------------------------
# RECIPE PHOTO CAROUSEL
# --------------------------------------------------

def show_recipe_images(meal_name, unique_id):

    image_name = get_image_name(meal_name)

    image_paths = get_meal_photo_paths(meal_name)

    if not image_paths:
        st.caption("📷 Recipe photos coming soon.")
        return False

    photo_key = (
        f"meal_planner_photo_index_{unique_id}_{image_name}"
    )

    if photo_key not in st.session_state:
        st.session_state[photo_key] = 0

    current_index = (
        st.session_state[photo_key] % len(image_paths)
    )

    viewer_key = (
        f"photo_viewer_{unique_id}_{image_name}"
    )

    with st.container(key=viewer_key):

        _, image_col, _ = st.columns([1, 1.5, 1])

        with image_col:
            st.image(
                image_paths[current_index],
                width=800
            )

        if len(image_paths) > 1:

            if st.button(
                "‹",
                key=f"photo_prev_{unique_id}_{image_name}"
            ):

                st.session_state[photo_key] = (
                    current_index - 1
                ) % len(image_paths)

                st.rerun()

            if st.button(
                "›",
                key=f"photo_next_{unique_id}_{image_name}"
            ):

                st.session_state[photo_key] = (
                    current_index + 1
                ) % len(image_paths)

                st.rerun()

        if st.button(
            "⛶",
            key=f"photo_expand_{unique_id}_{image_name}"
        ):

            st.session_state["large_photo_paths"] = [
                str(path) for path in image_paths
            ]

            st.session_state["large_photo_index"] = (
                current_index
            )

            return True

    return False


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("🍽️ Meal Planner")

st.write(
    "Find meals that match your budget, cooking time, "
    "food preferences, and nutrition goals."
)

st.divider()


# --------------------------------------------------
# PREPARE MEAL DATA
# --------------------------------------------------

filtered_meals = meals.copy()

# Standardize meal names for matching
filtered_meals["Meal Name Key"] = (
    filtered_meals["Meal Name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

ingredients_data = ingredients.copy()

ingredients_data["Meal Name Key"] = (
    ingredients_data["Meal Name"]
    .astype(str)
    .str.strip()
    .str.lower()
)


# --------------------------------------------------
# GET WALMART PACKAGE PRICE TOTALS
# --------------------------------------------------

# First, use Total Grocery Cost from the Meals CSV.
# If a meal does not have a value, calculate its
# package price using the Price Total column
# in the Ingredients CSV.

if "Total Grocery Cost" in filtered_meals.columns:

    filtered_meals["Walmart Package Price Number"] = (
        filtered_meals["Total Grocery Cost"].apply(convert_price)
    )

else:

    filtered_meals["Walmart Package Price Number"] = float("nan")


# Calculate package totals from the Ingredients CSV
if "Price Total" in ingredients_data.columns:

    ingredients_data["Price Total Number"] = (
        ingredients_data["Price Total"].apply(convert_price)
    )

    price_by_meal = (
        ingredients_data.groupby("Meal Name Key")[
            "Price Total Number"
        ].sum(min_count=1)
    )

    fallback_prices = (
        filtered_meals["Meal Name Key"]
        .map(price_by_meal)
    )

    # Use the Ingredients CSV when the Meals CSV
    # does not contain a package price for a meal.
    filtered_meals["Walmart Package Price Number"] = (
        filtered_meals["Walmart Package Price Number"]
        .fillna(fallback_prices)
    )


# --------------------------------------------------
# CONVERT MEAL INFORMATION TO NUMBERS
# --------------------------------------------------

filtered_meals["Cost Number"] = (
    filtered_meals["Ingredient Cost"].apply(convert_price)
)

filtered_meals["Time Number"] = pd.to_numeric(
    filtered_meals["Total Time"]
    .astype(str)
    .str.extract(r"(\d+)")[0],
    errors="coerce"
)

filtered_meals["Calories Number"] = pd.to_numeric(
    filtered_meals["Calories"],
    errors="coerce"
)

filtered_meals["Protein Number"] = pd.to_numeric(
    filtered_meals["Protein"]
    .astype(str)
    .str.replace("g", "", regex=False),
    errors="coerce"
)


# --------------------------------------------------
# CONVERT ORIGINAL SERVINGS AND ADJUSTED MEAL COST
# --------------------------------------------------

def get_original_servings(value):

    numbers = re.findall(r"\d+", str(value))

    return max(map(int, numbers)) if numbers else 1


filtered_meals["Original Servings"] = (
    filtered_meals["Servings"]
    .apply(get_original_servings)
).fillna(1)


filtered_meals["Serving Scaling Factor"] = (
    desired_servings /
    filtered_meals["Original Servings"]
)


filtered_meals["Adjusted Cost"] = (
    filtered_meals["Cost Number"] *
    filtered_meals["Serving Scaling Factor"]
)


# --------------------------------------------------
# FILTER BY PER-MEAL BUDGET
# --------------------------------------------------

filtered_meals = filtered_meals[
    filtered_meals["Adjusted Cost"].notna()
    & (filtered_meals["Adjusted Cost"] <= budget)
]
# --------------------------------------------------
# FILTER BY COOKING TIME
# --------------------------------------------------

if max_time is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Time Number"] <= max_time
    ]


# --------------------------------------------------
# FILTER BY DIETARY RESTRICTIONS
# --------------------------------------------------

def get_dietary_tags(value):
    return {
        tag.strip().casefold()
        for tag in str(value).splitlines()
        if tag.strip()
    }


def get_dietary_types(value):
    return {
        tag.strip().casefold()
        for tag in str(value).split(",")
        if tag.strip()
    }


if dietary_restrictions == "Vegetarian":

    filtered_meals = filtered_meals[
        filtered_meals["Dietary Type"].apply(
            lambda value: bool(
                get_dietary_types(value)
                & {"vegetarian", "vegan"}
            )
        )
    ]


elif dietary_restrictions == "Vegan":

    filtered_meals = filtered_meals[
        filtered_meals["Dietary Type"].apply(
            lambda value: "vegan" in get_dietary_types(value)
        )
    ]


elif dietary_restrictions == "Dairy-free":

    filtered_meals = filtered_meals[
        filtered_meals["Food Preferences"].apply(
            lambda value: "dairy-free" in get_dietary_tags(value)
        )
    ]


elif dietary_restrictions == "Gluten-free":

    filtered_meals = filtered_meals[
        filtered_meals["Food Preferences"].apply(
            lambda value: bool(
                get_dietary_tags(value)
                & {"gluten-free", "no gluten"}
            )
        )
    ]

# --------------------------------------------------
# FILTER BY CALORIES
# --------------------------------------------------

if max_calories is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Calories Number"] <= max_calories
    ]


# --------------------------------------------------
# FILTER BY PROTEIN
# --------------------------------------------------

if min_protein is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Protein Number"] >= min_protein
    ]


# --------------------------------------------------
# FILTER FOODS TO AVOID
# --------------------------------------------------

if food_preferences.strip():

    foods_to_avoid = [
        food.strip().lower()
        for food in food_preferences.split(",")
        if food.strip()
    ]

    def contains_avoided_food(meal_name):

        meal_name = str(meal_name).lower().strip()

        meal_ingredients = ingredients_data[
            ingredients_data["Meal Name Key"] == meal_name
        ]

        ingredient_names = " ".join(
            meal_ingredients["Ingredients"]
            .astype(str)
            .str.lower()
        )

        searchable_text = meal_name + " " + ingredient_names

        return any(
            food in searchable_text
            for food in foods_to_avoid
        )

    filtered_meals = filtered_meals[
        ~filtered_meals["Meal Name"].apply(
            contains_avoided_food
        )
    ]


# --------------------------------------------------
# CHECK FOR MATCHING MEALS
# --------------------------------------------------

# Remove duplicate recipe entries
filtered_meals = filtered_meals.drop_duplicates(
    subset=["Meal Name"]
).reset_index(drop=True)

# Count unique matching recipes
matching_meal_count = filtered_meals["Meal Name"].nunique()

st.subheader("Your Matching Meals")

st.write(
    f"{matching_meal_count} unique meals match "
    "your current preferences."
)

# Warn users when there are not enough unique meals
if matching_meal_count > 0 and matching_meal_count < plan_days:

    st.warning(
        f"Limited Meal Options: Only {matching_meal_count} "
        f"unique meals match your current preferences, "
        f"but you selected {plan_days} days. "
        "Some meals will repeat in your meal plan. "
        "Try adjusting your dietary restrictions, budget, "
        "or cooking time to see more options."
    )

if filtered_meals.empty:

    st.warning(
        "No meals match your current preferences. "
        "Try increasing your budget or adjusting your filters."
    )

    st.stop()

# --------------------------------------------------
# DETERMINE ORIGINAL SERVINGS
# --------------------------------------------------

def get_original_servings(value):

    numbers = re.findall(r"\d+", str(value))

    return max(map(int, numbers)) if numbers else 1


filtered_meals["Original Servings"] = (
    filtered_meals["Servings"].apply(get_original_servings)
)

filtered_meals["Original Servings"] = (
    filtered_meals["Original Servings"].fillna(1)
)


# --------------------------------------------------
# GENERATE MEAL PLAN
# --------------------------------------------------

current_preferences = (
    budget,
    weekly_budget,
    use_weekly_budget,
    max_time,
    desired_servings,
    plan_days,
    dietary_restrictions,
    food_preferences.strip().lower(),
    max_calories,
    min_protein
)


def choose_meal_plan(candidates, number_of_days, weekly_limit):

    candidates = candidates.copy().reset_index(drop=True)

    candidates = candidates[
        candidates["Adjusted Cost"].notna()
        & (candidates["Adjusted Cost"] >= 0)
    ].reset_index(drop=True)

    if candidates.empty:
        return None, None

    costs = candidates["Adjusted Cost"].astype(float)

    allow_repeats = len(candidates) < number_of_days

    # UNIQUE MEALS
    if not allow_repeats:

        cheapest_indices = (
            costs.nsmallest(number_of_days).index.tolist()
        )

        cheapest_total = float(
            costs.loc[cheapest_indices].sum()
        )

        best_indices = None
        best_total = float("-inf")

        # Search for affordable combinations
        for _ in range(4000):

            indices = candidates.sample(
                n=number_of_days,
                replace=False
            ).index.tolist()

            total = float(costs.loc[indices].sum())

            if total <= weekly_limit and total > best_total:

                best_indices = indices
                best_total = total

                if abs(best_total - weekly_limit) < 0.005:
                    break

        # Use the cheapest combination if it fits
        if best_indices is None or cheapest_total > best_total:

            if cheapest_total <= weekly_limit:

                best_indices = cheapest_indices
                best_total = cheapest_total

        if best_indices is not None:

            return (
                candidates.loc[best_indices].reset_index(drop=True),
                True
            )

        # No combination fits the budget.
        # Display the cheapest available combination.

        return (
            candidates.loc[cheapest_indices].reset_index(drop=True),
            False
        )

    # ALLOW REPEATED MEALS IF NOT ENOUGH RECIPES

    best_indices = None
    best_total = float("-inf")

    for _ in range(4000):

        indices = candidates.sample(
            n=number_of_days,
            replace=True
        ).index.tolist()

        total = float(costs.loc[indices].sum())

        if total <= weekly_limit and total > best_total:

            best_indices = indices
            best_total = total

            if abs(best_total - weekly_limit) < 0.005:
                break

    if best_indices is not None:

        return (
            candidates.loc[best_indices].reset_index(drop=True),
            True
        )

    # Cheapest repeated meal as fallback

    cheapest_index = int(costs.idxmin())

    cheapest_indices = [
        cheapest_index
    ] * number_of_days

    return (
        candidates.loc[cheapest_indices].reset_index(drop=True),
        False
    )


# CHECK WHETHER PREFERENCES CHANGED

preferences_changed = (
    "meal_plan" not in st.session_state
    or "meal_plan_preferences" not in st.session_state
    or st.session_state.meal_plan_preferences != current_preferences
    or len(st.session_state.meal_plan) != plan_days
)


if preferences_changed:

    if filtered_meals.empty:

        st.session_state.meal_plan = pd.DataFrame()

        st.session_state.meal_plan_preferences = (
            current_preferences
        )

        st.session_state["weekly_budget_met"] = False

    elif use_weekly_budget:

        selected_plan, budget_met = choose_meal_plan(
            filtered_meals,
            plan_days,
            weekly_budget
        )

        st.session_state.meal_plan = selected_plan

        st.session_state["weekly_budget_met"] = budget_met

        st.session_state.meal_plan_preferences = (
            current_preferences
        )

    else:

        st.session_state.meal_plan = (
            filtered_meals.sample(
                n=plan_days,
                replace=len(filtered_meals) < plan_days
            )
            .reset_index(drop=True)
        )

        st.session_state["weekly_budget_met"] = None

        st.session_state.meal_plan_preferences = (
            current_preferences
        )


meal_plan = st.session_state.meal_plan.copy()


if meal_plan.empty:

    st.warning(
        "No meals match your current preferences and "
        "per-meal budget. Try increasing your budget "
        "or changing your filters."
    )

    st.stop()


# Refresh the Walmart package prices even when
# Streamlit reuses an older saved meal plan.

meal_plan["Meal Name Key"] = (
    meal_plan["Meal Name"]
    .astype(str)
    .str.strip()
    .str.lower()
)

walmart_price_lookup = (
    filtered_meals
    .drop_duplicates("Meal Name Key")
    .set_index("Meal Name Key")["Walmart Package Price Number"]
)

meal_plan["Walmart Package Price Number"] = (
    meal_plan["Meal Name Key"].map(walmart_price_lookup)
)


# --------------------------------------------------
# CALCULATE SERVING ADJUSTMENTS
# --------------------------------------------------

meal_plan["Original Servings"] = (
    meal_plan["Servings"].apply(get_original_servings)
)

meal_plan["Scaling Factor"] = (
    desired_servings / meal_plan["Original Servings"]
)

meal_plan["Adjusted Cost"] = (
    meal_plan["Cost Number"] * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Calories"] = (
    meal_plan["Calories Number"] * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Protein"] = (
    meal_plan["Protein Number"] * meal_plan["Scaling Factor"]
)


# --------------------------------------------------
# DISPLAY WEEKLY MEAL PLAN
# --------------------------------------------------

st.divider()

st.subheader("📅 Your Meal Plan")

st.caption(
    f"Planning {len(meal_plan)} day(s) with "
    f"{desired_servings} serving(s) per meal."
)

# TEMPORARY CHECK
st.caption(f"Meals generated: {len(meal_plan)}")

open_large_photo = False

for index, meal in meal_plan.iterrows():

    st.subheader(
        f"Day {index + 1}: {meal['Meal Name']}"
    )

    # DISPLAY MEAL PHOTO CAROUSEL

    if show_recipe_images(meal["Meal Name"], index):
        open_large_photo = True

    with st.expander("View Meal Details", expanded=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estimated Cost",
                f"${meal['Adjusted Cost']:.2f}"
            )

        with col2:
            st.metric(
                "Walmart Package Price",
                (
                    f"${meal['Walmart Package Price Number']:.2f}"
                    if pd.notna(meal["Walmart Package Price Number"])
                    else "N/A"
                )
            )

        with col3:
            st.metric(
                "Cooking Time",
                f"{meal['Time Number']:.0f} min"
            )

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("Servings", desired_servings)

        with col5:
            st.metric(
                "Calories",
                f"{meal['Adjusted Calories']:.0f}"
            )

        with col6:
            st.metric(
                "Protein",
                f"{meal['Adjusted Protein']:.1f} g"
            )

st.write("Dietary Type:", meal["Dietary Type"])

# --------------------------------------------------
# INGREDIENTS AND NUTRITION BUTTON
# --------------------------------------------------

details_key = f"show_ingredients_nutrition_{index}"

if details_key not in st.session_state:
    st.session_state[details_key] = False

if st.button(
    "Hide Ingredients & Nutrition"
    if st.session_state[details_key]
    else "Show Ingredients & Nutrition",
    key=f"ingredients_nutrition_button_{index}",
    use_container_width=True
):
    st.session_state[details_key] = (
        not st.session_state[details_key]
    )


# DISPLAY INGREDIENTS AND NUTRITION

if st.session_state[details_key]:

    st.divider()

    # INGREDIENTS

    st.markdown("### 🥕 Ingredients")

    meal_name_key = (
        str(meal["Meal Name"]).strip().lower()
    )

    meal_ingredients = ingredients_data[
        ingredients_data["Meal Name Key"] == meal_name_key
    ].copy()

    if not meal_ingredients.empty:

        ingredient_columns = [
            column for column in [
                "Ingredients",
                "Quantity",
                "Unit",
                "Estimated Cost"
            ]
            if column in meal_ingredients.columns
        ]

        ingredient_display = meal_ingredients[
            ingredient_columns
        ]

        st.dataframe(
            ingredient_display,
            hide_index=True,
            use_container_width=True
        )

    else:
        st.info("Ingredient details are not available.")


    st.divider()

    # NUTRITION INFORMATION

    st.markdown("### ❤️ Nutrition Information")

    nutrition_columns = [
        ("Calories", "Calories"),
        ("Total Fat", "Total Fat"),
        ("Cholesterol", "Cholesterol"),
        ("Sodium", "Sodium"),
        ("Total Carbohydrates", "Carbohydrates"),
        ("Dietary Fiber", "Dietary Fiber"),
        ("Total Sugars", "Total Sugars"),
        ("Protein", "Protein")
    ]

    nutrition_values = []

    for column_name, label in nutrition_columns:

        value = meal.get(column_name)

        if pd.notna(value) and str(value).strip():

            nutrition_values.append(
                (label, value)
            )

    if nutrition_values:

        nutrition_cols = st.columns(2)

        for i, (label, value) in enumerate(nutrition_values):

            with nutrition_cols[i % 2]:
                st.metric(label, str(value))

    else:
        st.info("Nutrition information is not available.")


# COOKING INSTRUCTIONS

st.write("Cooking Instructions:")
st.write(meal["Cooking Instructions"])


        # ALTERNATIVE MEALS

        with st.expander(
            "🔄 Explore Other Meals",
            expanded=False
        ):

            st.caption(
                "Looking for something different? "
                "Browse other recipes that match your preferences."
            )

            # Keep the existing alternative meal code here
            
            show_alternatives = st.toggle(
                "Explore Other Meals",
                key=f"show_alternatives_{index}"
            )

        if show_alternatives:

            other_meals = filtered_meals[
                ~filtered_meals["Meal Name"].isin(
                    meal_plan["Meal Name"]
                )
            ]

            if other_meals.empty:

                st.info(
                    "No additional matching meals are available."
                )

            else:

                alternative_names = (
                    other_meals["Meal Name"].tolist()
                )

                selected_alternative = st.selectbox(
                    "Choose an alternative meal:",
                    alternative_names,
                    key=f"alternative_{index}"
                )

                alternative_meal = other_meals[
                    other_meals["Meal Name"]
                    == selected_alternative
                ].iloc[0]

                # Calculate nutrition and cost for selected servings
                alternative_servings = get_original_servings(
                    alternative_meal["Servings"]
                )

                alternative_scaling = (
                    desired_servings / alternative_servings
                )

                alternative_cost = (
                    alternative_meal["Cost Number"]
                    * alternative_scaling
                )

                alternative_calories = (
                    alternative_meal["Calories Number"]
                    * alternative_scaling
                )

                alternative_protein = (
                    alternative_meal["Protein Number"]
                    * alternative_scaling
                )

                # Display alternative meal information
                st.markdown("**Alternative Meal Details**")

                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric(
                        "Estimated Cost",
                        f"${alternative_cost:.2f}"
                    )

                with col2:
                    st.metric(
                        "Cooking Time",
                        f"{alternative_meal['Time Number']:.0f} min"
                    )

                with col3:
                    st.metric(
                        "Calories",
                        f"{alternative_calories:.0f}"
                    )

                with col4:
                    st.metric(
                        "Protein",
                        f"{alternative_protein:.1f} g"
                    )

                st.write(
                    "Dietary Type:",
                    alternative_meal["Dietary Type"]
                )

                # Replace meal while checking weekly budget
                if st.button(
                    "Use This Meal",
                    key=f"use_alternative_{index}"
                ):

                    current_total = float(
                        meal_plan["Adjusted Cost"].sum()
                    )

                    revised_total = (
                        current_total
                        - float(meal["Adjusted Cost"])
                        + float(alternative_cost)
                    )

                    if (
                        use_weekly_budget
                        and revised_total > weekly_budget
                    ):

                        st.warning(
                            f"This replacement would bring your plan to "
                            f"${revised_total:.2f}, which is above your "
                            f"${weekly_budget:.2f} weekly budget. "
                            "Choose a less expensive alternative or increase "
                            "your weekly budget."
                        )

                    else:

                        st.session_state.meal_plan.loc[index] = (
                            alternative_meal
                        )

                        st.session_state["weekly_budget_met"] = (
                            revised_total <= weekly_budget
                            if use_weekly_budget
                            else None
                        )

                        st.rerun()

# --------------------------------------------------
# OPEN ENLARGED PHOTO DIALOG
# --------------------------------------------------

if open_large_photo:
    show_large_photo()

# --------------------------------------------------
# MEAL PLAN SUMMARY
# --------------------------------------------------

st.divider()

st.subheader("💰 Meal Plan Summary")

total_cost = meal_plan["Adjusted Cost"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Estimated Cost",
        f"${total_cost:.2f}"
    )

with col2:
    st.metric(
        "Planned Meals",
        len(meal_plan)
    )


# --------------------------------------------------
# WEEKLY BUDGET CHECK
# --------------------------------------------------

if use_weekly_budget:

    if total_cost <= weekly_budget:

        st.success(
            f"Your meal plan is within your "
            f"${weekly_budget:.2f} weekly budget."
        )

    else:

        st.warning(
            f"Your meal plan exceeds your weekly budget "
            f"by ${total_cost - weekly_budget:.2f}."
        )


st.caption(
    "Total Estimated Cost reflects the ingredient amounts "
    "used for your selected serving sizes."
)

# --------------------------------------------------
# SUMMARY EXPLANATION
# --------------------------------------------------

st.caption(
    "Estimated Cost reflects the ingredient amounts "
    "used for your selected serving sizes. "
    "Walmart Package Price reflects the full grocery "
    "package costs recorded in the dataset. "
    "The package price is based on the original recipe "
    "quantities and does not automatically adjust for "
    "additional servings. Actual store prices may vary."
)
