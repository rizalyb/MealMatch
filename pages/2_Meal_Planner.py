
import streamlit as st
import pandas as pd
import re
from pathlib import Path


# --------------------------------------------------
# LOAD DATA AND PREFERENCES
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

APP_DIR = Path(__file__).resolve().parent.parent

HOMEMADE_DIR = APP_DIR / "images" / "homemade"
RESTAURANT_DIR = APP_DIR / "images" / "restaurant"
INGREDIENTS_DIR = APP_DIR / "images" / "ingredients"


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def convert_price(value):
    if pd.isna(value):
        return float("nan")

    cleaned = (
        str(value)
        .replace("$", "")
        .replace(",", "")
        .strip()
    )

    return pd.to_numeric(cleaned, errors="coerce")


def get_original_servings(value):
    numbers = re.findall(r"\d+", str(value))
    return max(map(int, numbers)) if numbers else 1


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
# RECIPE PHOTO DISPLAY
# --------------------------------------------------

def show_recipe_images(meal_name, unique_id):

    image_paths = get_meal_photo_paths(meal_name)

    if not image_paths:
        st.caption("📷 Recipe photos coming soon.")
        return False

    photo_key = f"meal_photo_{unique_id}"

    if photo_key not in st.session_state:
        st.session_state[photo_key] = 0

    current_index = st.session_state[photo_key] % len(image_paths)

    image_col = st.columns([1, 2, 1])[1]

    with image_col:
        st.image(image_paths[current_index], use_container_width=True)

    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:
            if st.button(
                "← Previous",
                key=f"previous_photo_{unique_id}",
                use_container_width=True
            ):
                st.session_state[photo_key] = (
                    current_index - 1
                ) % len(image_paths)
                st.rerun()

        with next_col:
            if st.button(
                "Next →",
                key=f"next_photo_{unique_id}",
                use_container_width=True
            ):
                st.session_state[photo_key] = (
                    current_index + 1
                ) % len(image_paths)
                st.rerun()

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
# WALMART PACKAGE PRICE
# --------------------------------------------------

if "Total Grocery Cost" in filtered_meals.columns:

    filtered_meals["Walmart Package Price Number"] = (
        filtered_meals["Total Grocery Cost"].apply(convert_price)
    )

else:
    filtered_meals["Walmart Package Price Number"] = float("nan")


if "Price Total" in ingredients_data.columns:

    ingredients_data["Price Total Number"] = (
        ingredients_data["Price Total"].apply(convert_price)
    )

    price_by_meal = (
        ingredients_data.groupby("Meal Name Key")[
            "Price Total Number"
        ].sum(min_count=1)
    )

    fallback_prices = filtered_meals["Meal Name Key"].map(
        price_by_meal
    )

    filtered_meals["Walmart Package Price Number"] = (
        filtered_meals["Walmart Package Price Number"]
        .fillna(fallback_prices)
    )


# --------------------------------------------------
# CONVERT MEAL INFORMATION
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
# ADJUST COST FOR SERVINGS
# --------------------------------------------------

filtered_meals["Original Servings"] = (
    filtered_meals["Servings"].apply(get_original_servings)
)

filtered_meals["Serving Scaling Factor"] = (
    desired_servings / filtered_meals["Original Servings"]
)

filtered_meals["Adjusted Cost"] = (
    filtered_meals["Cost Number"]
    * filtered_meals["Serving Scaling Factor"]
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

elif dietary_restrictions == "Gluten-free":

    filtered_meals = filtered_meals[
        filtered_meals["Food Preferences"].apply(
            lambda value: bool(
                get_dietary_tags(value)
                & {"gluten-free", "no gluten"}
            )
        )
    ]

elif dietary_restrictions == "Dairy-free":

    filtered_meals = filtered_meals[
        filtered_meals["Food Preferences"].apply(
            lambda value: "dairy-free" in get_dietary_tags(value)
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
        ~filtered_meals["Meal Name"].apply(contains_avoided_food)
    ]


# --------------------------------------------------
# CHECK MATCHING MEALS
# --------------------------------------------------

st.subheader("Your Matching Meals")

st.write(
    f"{len(filtered_meals)} meals match your current preferences."
)

if filtered_meals.empty:

    st.warning(
        "No meals match your current preferences. "
        "Try increasing your budget or adjusting your filters."
    )

    st.stop()


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

    costs = candidates["Adjusted Cost"].astype(float)

    allow_repeats = len(candidates) < number_of_days

    if not allow_repeats:

        cheapest_indices = costs.nsmallest(
            number_of_days
        ).index.tolist()

        cheapest_total = float(costs.loc[cheapest_indices].sum())

        best_indices = None
        best_total = float("-inf")

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

        if best_indices is None:

            if cheapest_total <= weekly_limit:
                best_indices = cheapest_indices

        if best_indices is not None:
            return candidates.loc[best_indices].reset_index(drop=True), True

        return candidates.loc[cheapest_indices].reset_index(drop=True), False

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
        return candidates.loc[best_indices].reset_index(drop=True), True

    cheapest_index = int(costs.idxmin())
    cheapest_indices = [cheapest_index] * number_of_days

    return candidates.loc[cheapest_indices].reset_index(drop=True), False


preferences_changed = (
    "meal_plan" not in st.session_state
    or "meal_plan_preferences" not in st.session_state
    or st.session_state.meal_plan_preferences != current_preferences
    or len(st.session_state.meal_plan) != plan_days
)

if preferences_changed:

    if use_weekly_budget:

        selected_plan, budget_met = choose_meal_plan(
            filtered_meals,
            plan_days,
            weekly_budget
        )

        st.session_state.meal_plan = selected_plan
        st.session_state["weekly_budget_met"] = budget_met

    else:

        st.session_state.meal_plan = (
            filtered_meals.sample(
                n=plan_days,
                replace=len(filtered_meals) < plan_days
            )
            .reset_index(drop=True)
        )

        st.session_state["weekly_budget_met"] = None

    st.session_state.meal_plan_preferences = current_preferences


meal_plan = st.session_state.meal_plan.copy()

if meal_plan.empty:
    st.warning("No matching meals are available.")
    st.stop()


# --------------------------------------------------
# UPDATE PACKAGE PRICES
# --------------------------------------------------

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
    f"Planning {plan_days} day(s) with {desired_servings} "
    "serving(s) per meal."
)

for index, meal in meal_plan.iterrows():

    st.subheader(f"Day {index + 1}: {meal['Meal Name']}")

    show_recipe_images(meal["Meal Name"], index)

    with st.expander("View Meal Details", expanded=True):

        # COST AND COOKING INFORMATION

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

                st.dataframe(
                    meal_ingredients[ingredient_columns],
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

                    nutrition_values.append((label, value))

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


        # --------------------------------------------------
        # ALTERNATIVE MEALS
        # --------------------------------------------------

        st.divider()

        show_alternatives = st.checkbox(
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

                selected_alternative = st.selectbox(
                    "Choose an alternative meal:",
                    other_meals["Meal Name"].tolist(),
                    key=f"alternative_{index}"
                )

                if st.button(
                    "Use This Meal",
                    key=f"use_alternative_{index}"
                ):

                    new_meal = other_meals[
                        other_meals["Meal Name"] == selected_alternative
                    ].iloc[0]

                    replacement_cost = (
                        new_meal["Cost Number"]
                        * desired_servings
                        / get_original_servings(new_meal["Servings"])
                    )

                    current_total = float(
                        meal_plan["Adjusted Cost"].sum()
                    )

                    revised_total = (
                        current_total
                        - float(meal["Adjusted Cost"])
                        + float(replacement_cost)
                    )

                    if (
                        use_weekly_budget
                        and revised_total > weekly_budget
                    ):

                        st.warning(
                            f"This replacement brings your plan to "
                            f"${revised_total:.2f}, above your "
                            f"${weekly_budget:.2f} weekly budget."
                        )

                    else:

                        st.session_state.meal_plan.loc[index] = new_meal

                        st.rerun()


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
            f"by ${total_cost - weekly_budget:.2f}. "
            "Try adjusting your preferences or increasing your budget."
        )


# --------------------------------------------------
# SUMMARY EXPLANATION
# --------------------------------------------------

st.caption(
    "Estimated Cost reflects the ingredient amounts used "
    "for your selected serving sizes. Walmart Package Price "
    "reflects the full grocery package costs recorded in the dataset. "
    "Actual store prices may vary."
)
