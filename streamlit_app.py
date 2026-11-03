import re
import streamlit as st
import pandas as pd
from pathlib import Path

# Find the folder containing this app
APP_DIR = Path(__file__).parent

# Load MealMatch data
@st.cache_data
def load_meal_data():
    meals = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Meals).csv",
        encoding="cp1252"
    )

    ingredients = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Ingredients).csv",
        encoding="cp1252"
    )

    return meals, ingredients

meals, ingredients = load_meal_data()

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Nunito', sans-serif;
}

.stApp {
    background-color: var(--background-color);
    color: var(--text-color);
}

h1, h2, h3 {
    color: var(--text-color);
}

[data-testid="stSidebar"] {
    background-color: var(--secondary-background-color);
}

.stButton > button {
    background-color: #477653;
    color: white;
    border-radius: 10px;
    border: none;
    font-weight: 700;
}

.stButton > button:hover {
    background-color: #315C45;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# Sidebar: Student Preferences

with st.sidebar:
    st.title("⚙️ Your Preferences")
    st.write("Customize your meal recommendations.")

    st.subheader("Budget")

    budget = st.slider(
        "Budget per meal ($)",
        min_value=1,
        max_value=30,
        value=10
    )

    use_weekly_budget = st.checkbox(
        "Set a weekly budget",
        value=False
    )

    if use_weekly_budget:
        weekly_budget = st.slider(
            "Weekly budget ($)",
            min_value=10,
            max_value=200,
            value=30,
            step=5
        )
    else:
        weekly_budget = None

    st.subheader("Cooking")

    use_time_limit = st.checkbox(
        "Set a maximum cooking time",
        value=True
    )

    if use_time_limit:
        max_time = st.slider(
            "Maximum cooking time (minutes)",
            min_value=5,
            max_value=120,
            value=30,
            step=5
        )
    else:
        max_time = None


    desired_servings = st.selectbox(
        "How many people are you cooking for?",
        options=[1, 2, 3, 4, 5, 6]
    )

    plan_days = st.selectbox(
        "How many days do you want to plan?",
        options=[1, 3, 5, 7]
    )

    st.subheader("Food Preferences")
    dietary_restrictions = st.selectbox(
        "Dietary restrictions",
        options=[
            "None",
            "Vegetarian",
            "Vegan",
            "Gluten-free",
            "Dairy-free"
        ]
    )

    food_preferences = st.text_input(
        "Foods to avoid",
        placeholder="e.g., seafood, mushrooms"
    )

    st.subheader("Nutrition Goals")

    use_calorie_limit = st.checkbox(
        "Set a maximum calorie limit",
        value=False
    )

    if use_calorie_limit:
        max_calories = st.number_input(
            "Maximum calories per serving",
            min_value=50,
            max_value=2000,
            value=500,
            step=50
        )
    else:
        max_calories = None

    use_protein_goal = st.checkbox(
        "Set a minimum protein goal",
        value=False
    )

    if use_protein_goal:
        min_protein = st.number_input(
            "Minimum protein per serving (g)",
            min_value=1,
            max_value=150,
            value=20,
            step=5
        )
    else:
        min_protein = None

st.title("🥗 MealMatch")
st.subheader("Meals that match your budget, schedule, and taste.")

st.write(
    "Welcome to MealMatch! Find affordable meals "
    "based on your preferences and lifestyle."
)

# MealMatch: Filter and Explore Recipes

st.divider()
st.header("🍽️ Meals That Match You")
st.write("Recipes that fit your preferences.")

# Start with all meals
filtered_meals = meals.copy()

# Convert cost and time to numbers for filtering
filtered_meals["Cost Number"] = pd.to_numeric(
    filtered_meals["Ingredient Cost"]
    .astype(str)
    .str.replace("$", "", regex=False),
    errors="coerce"
)

filtered_meals["Time Number"] = pd.to_numeric(
    filtered_meals["Total Time"]
    .astype(str)
    .str.extract(r"(\d+)")[0],
    errors="coerce"
)

# Apply budget and cooking-time preferences
if budget is not None:
    filtered_meals = filtered_meals[
        filtered_meals["Cost Number"] <= budget
    ]

if max_time is not None:
    filtered_meals = filtered_meals[
        filtered_meals["Time Number"] <= max_time
    ]

if dietary_restrictions != "None":
    filtered_meals = filtered_meals[
        filtered_meals["Dietary Type"]
        .astype(str)
        .str.contains(dietary_restrictions, case=False, na=False)
    ]

if max_calories is not None:
    filtered_meals = filtered_meals[
        pd.to_numeric(filtered_meals["Calories"], errors="coerce")
        <= max_calories
    ]

if min_protein is not None:
    filtered_meals = filtered_meals[
        pd.to_numeric(
            filtered_meals["Protein"].astype(str).str.replace("g", "", regex=False),
            errors="coerce"
        ) >= min_protein
    ]

if food_preferences.strip():
    foods_to_avoid = [
        food.strip().lower()
        for food in food_preferences.split(",")
        if food.strip()
    ]

    def contains_avoided_food(meal):
        meal_name = str(meal.get("Meal Name", "")).lower()
        ingredients_text = ingredients[
            ingredients["Meal Name"].astype(str).str.lower()
            == meal_name
        ]["Ingredients"].astype(str).str.lower().tolist()

        all_ingredients = " ".join(ingredients_text)

        return any(
            food in meal_name or food in all_ingredients
            for food in foods_to_avoid
        )

    filtered_meals = filtered_meals[
        ~filtered_meals.apply(contains_avoided_food, axis=1)
    ]

st.write(f"**{len(filtered_meals)} matching recipes found**")

if filtered_meals.empty:
    st.info(
        "No meals match your current preferences. "
        "Try adjusting your preferences in the sidebar."
    )

else:
    st.subheader("Your Weekly Meal Plan")

# Track preference changes so the meal plan refreshes when needed
current_preferences = (
    budget,
    weekly_budget,
    max_time,
    desired_servings,
    plan_days,
    dietary_restrictions,
    food_preferences.strip().lower(),
    max_calories,
    min_protein
)

# Generate a new plan when preferences change
if (
    "meal_plan" not in st.session_state
    or "meal_plan_preferences" not in st.session_state
    or st.session_state.meal_plan_preferences != current_preferences
    or len(st.session_state.meal_plan) != plan_days
):
    st.session_state.meal_plan = filtered_meals.sample(
        n=plan_days,
        replace=len(filtered_meals) < plan_days
    ).reset_index(drop=True)

    st.session_state.meal_plan_preferences = current_preferences

meal_plan = st.session_state.meal_plan

# Calculate adjusted servings and costs
meal_plan = meal_plan.copy()

# Use the higher number for serving ranges
def get_original_servings(value):
    numbers = re.findall(r"\d+", str(value))
    return max(map(int, numbers)) if numbers else 1

meal_plan["Original Servings"] = (
    meal_plan["Servings"].apply(get_original_servings)
)

meal_plan["Original Servings"] = (
    meal_plan["Original Servings"].fillna(1)
)

meal_plan["Scaling Factor"] = (
    desired_servings / meal_plan["Original Servings"]
)

meal_plan["Adjusted Cost"] = (
    meal_plan["Cost Number"] * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Calories"] = (
    pd.to_numeric(meal_plan["Calories"], errors="coerce")
    * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Protein"] = (
    pd.to_numeric(
        meal_plan["Protein"].astype(str).str.replace("g", "", regex=False),
        errors="coerce"
    )
    * meal_plan["Scaling Factor"]
)
total_plan_cost = 0

for day_index, (_, meal) in enumerate(meal_plan.iterrows(), start=1):
    meal_cost = meal["Adjusted Cost"]
    total_plan_cost += meal_cost

    with st.expander(
        f"Day {day_index}: {meal['Meal Name']}",
        expanded=True
    ):
        col1, col2 = st.columns(2)

        with col1:
            st.write("**Ingredient Cost**")
            st.write("**Servings**")
            st.write(f"{desired_servings} people")
            st.write(f"${meal_cost:.2f}")
            st.write("**Total Time**")
            st.write(f"{int(meal['Time Number'])} minutes")

        with col2:
            st.write("**Calories**")
            st.write(meal.get("Calories", "Not available"))
            st.write("**Protein**")
            st.write(meal.get("Protein", "Not available"))

        st.write("**Cooking Instructions**")
        st.write(meal.get("Cooking Instructions", "Not available"))

        # Allow users to view alternative meals
        show_options = st.checkbox(
            "Show more meal options",
            key=f"show_options_{day_index}_{meal['Meal Name']}"
        )

        if show_options:
            # Exclude meals already assigned to other days
            other_meals = meal_plan[
                meal_plan.index != day_index - 1
            ]["Meal Name"].tolist()

            available_options = filtered_meals[
                (~filtered_meals["Meal Name"].isin(other_meals))
                & (filtered_meals["Meal Name"] != meal["Meal Name"])
            ]

            if not available_options.empty:
                option_names = available_options["Meal Name"].tolist()

                selected_meal = st.selectbox(
                    "Choose an alternative meal:",
                    option_names,
                    key=f"replacement_{day_index}_{meal['Meal Name']}"
                )

                if st.button(
                    "Use this meal",
                    key=f"replace_{day_index}_{meal['Meal Name']}"
                ):
                    replacement = available_options[
                        available_options["Meal Name"] == selected_meal
                    ].iloc[0]

                    st.session_state.meal_plan.loc[
                        day_index - 1
                    ] = replacement

                    st.rerun()
            else:
                st.info("No other matching meals are available.")

st.divider()
st.subheader("Meal Plan Summary")
st.write(f"**Planned days:** {len(meal_plan)}")
st.write(f"**Estimated ingredient cost:** ${total_plan_cost:.2f}")

if weekly_budget is not None:
    if total_plan_cost <= weekly_budget:
        st.success("Your meal plan is within your weekly budget!")
    else:
        st.warning(
            "Your meal plan exceeds your weekly budget. "
            "Try adjusting your preferences."
        )

st.divider()
st.subheader("🛒 Your Grocery List")
st.write("Ingredients needed for your selected meal plan.")

grocery_total = 0

for day_index, (_, meal) in enumerate(meal_plan.iterrows(), start=1):

    meal_ingredients = ingredients[
        ingredients["Meal Name"].astype(str).str.strip()
        == str(meal["Meal Name"]).strip()
    ]

    scaling_factor = meal["Scaling Factor"]

    with st.container(border=True):

        st.markdown(f"### Day {day_index}: {meal['Meal Name']}")

        if not meal_ingredients.empty:

            grocery_display = []

            for _, item in meal_ingredients.iterrows():

                original_quantity = str(item["Quantity"]).strip()
                unit = item["Unit"]

                try:
                    quantity_number = float(original_quantity)
                    adjusted_quantity = quantity_number * scaling_factor

                    if adjusted_quantity.is_integer():
                        quantity_display = str(int(adjusted_quantity))
                    else:
                        quantity_display = (
                            f"{adjusted_quantity:.2f}"
                            .rstrip("0").rstrip(".")
                        )

                except (ValueError, TypeError):
                    quantity_display = original_quantity

                unit_display = "" if pd.isna(unit) else str(unit)

                grocery_display.append({
                    "Ingredient": item["Ingredients"],
                    "Quantity Needed": f"{quantity_display} {unit_display}".strip()
                })

                cost = pd.to_numeric(
                    str(item["Estimated Cost"]).replace("$", ""),
                    errors="coerce"
                )

                if pd.notna(cost):
                    grocery_total += cost * scaling_factor

            grocery_table = pd.DataFrame(grocery_display)

            st.dataframe(
                grocery_table,
                hide_index=True,
                use_container_width=True
            )

        else:
            st.info("No ingredient information found for this meal.")

st.divider()

st.subheader("Grocery Cost Summary")

st.metric(
    "Estimated cost of ingredients used",
    f"${grocery_total:.2f}"
)

grocery_items = []

for _, meal in meal_plan.iterrows():

    meal_ingredients = ingredients[
        ingredients["Meal Name"] == meal["Meal Name"]
    ]

    scaling_factor = meal["Scaling Factor"]

    st.write(f"**{meal['Meal Name']}**")

    for _, item in meal_ingredients.iterrows():

        original_quantity = str(item["Quantity"]).strip()
        unit = item["Unit"]
        
        # Adjust ingredient quantities when numeric
        try:
            quantity_number = float(original_quantity)
            adjusted_quantity = quantity_number * scaling_factor

            if adjusted_quantity.is_integer():
                quantity_display = str(int(adjusted_quantity))
            else:
                quantity_display = f"{adjusted_quantity:.2f}".rstrip("0").rstrip(".")

        except (ValueError, TypeError):
            quantity_display = original_quantity

        unit_display = "" if pd.isna(unit) else str(unit)

        st.write(
            f"- {item['Ingredients']}: "
            f"{quantity_display} {unit_display}"
        )

        # Calculate adjusted ingredient cost
        cost = pd.to_numeric(
            str(item["Estimated Cost"]).replace("$", ""),
            errors="coerce"
        )

        if pd.notna(cost):
            grocery_items.append(cost * scaling_factor)

if grocery_items:
    st.divider()
    st.write(
        f"**Estimated cost of ingredients used: "
        f"${sum(grocery_items):.2f}**"
    )
