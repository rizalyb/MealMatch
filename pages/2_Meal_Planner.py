import streamlit as st
import pandas as pd
import re


# LOAD SHARED DATA AND PREFERENCES

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


# PAGE TITLE

st.title("🍽️ Meal Planner")

st.write(
    "Find meals that match your budget, cooking time, "
    "food preferences, and nutrition goals."
)

st.divider()


# PREPARE MEAL DATA

filtered_meals = meals.copy()

filtered_meals["Cost Number"] = pd.to_numeric(
    filtered_meals["Ingredient Cost"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False),
    errors="coerce"
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


# FILTER BY BUDGET

filtered_meals = filtered_meals[
    filtered_meals["Cost Number"] <= budget
]


# FILTER BY COOKING TIME

if max_time is not None:
    filtered_meals = filtered_meals[
        filtered_meals["Time Number"] <= max_time
    ]


# FILTER BY DIETARY RESTRICTIONS

if dietary_restrictions != "None":

    filtered_meals = filtered_meals[
        filtered_meals["Dietary Type"]
        .astype(str)
        .str.contains(
            dietary_restrictions,
            case=False,
            na=False
        )
    ]


# FILTER BY CALORIES

if max_calories is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Calories Number"] <= max_calories
    ]


# FILTER BY PROTEIN

if min_protein is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Protein Number"] >= min_protein
    ]


# FILTER FOODS TO AVOID

if food_preferences.strip():

    foods_to_avoid = [
        food.strip().lower()
        for food in food_preferences.split(",")
        if food.strip()
    ]

    def contains_avoided_food(meal_name):

        meal_name = str(meal_name).lower()

        meal_ingredients = ingredients[
            ingredients["Meal Name"]
            .astype(str)
            .str.strip()
            .str.lower()
            == meal_name
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


# CHECK FOR MATCHING MEALS

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


# DETERMINE ORIGINAL SERVINGS

def get_original_servings(value):

    numbers = re.findall(r"\d+", str(value))

    return max(map(int, numbers)) if numbers else 1


filtered_meals["Original Servings"] = (
    filtered_meals["Servings"].apply(get_original_servings)
)

filtered_meals["Original Servings"] = (
    filtered_meals["Original Servings"].fillna(1)
)


# GENERATE MEAL PLAN

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

if (
    "meal_plan" not in st.session_state
    or "meal_plan_preferences" not in st.session_state
    or st.session_state.meal_plan_preferences != current_preferences
    or len(st.session_state.meal_plan) != plan_days
):

    st.session_state.meal_plan = (
        filtered_meals.sample(
            n=plan_days,
            replace=len(filtered_meals) < plan_days
        )
        .reset_index(drop=True)
    )

    st.session_state.meal_plan_preferences = current_preferences


meal_plan = st.session_state.meal_plan.copy()


# CALCULATE SERVING ADJUSTMENTS

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


# DISPLAY WEEKLY MEAL PLAN

st.divider()

st.subheader("📅 Your Meal Plan")

st.caption(
    f"Planning {plan_days} day(s) with {desired_servings} "
    "serving(s) per meal."
)

for index, meal in meal_plan.iterrows():

    st.subheader(f"Day {index + 1}: {meal['Meal Name']}")

    with st.expander("View Meal Details", expanded=True):

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Estimated Cost",
                f"${meal['Adjusted Cost']:.2f}"
            )

        with col2:
            st.metric(
                "Cooking Time",
                f"{meal['Time Number']:.0f} min"
            )

        with col3:
            st.metric(
                "Servings",
                desired_servings
            )

        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "Calories",
                f"{meal['Adjusted Calories']:.0f}"
            )

        with col5:
            st.metric(
                "Protein",
                f"{meal['Adjusted Protein']:.1f} g"
            )

        st.write("Dietary Type:", meal["Dietary Type"])

        st.write("Cooking Instructions:")

        st.write(meal["Cooking Instructions"])


        # ALTERNATIVE MEALS

        show_alternatives = st.checkbox(
            "Show more meal options",
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

                if st.button(
                    "Use This Meal",
                    key=f"use_alternative_{index}"
                ):

                    new_meal = other_meals[
                        other_meals["Meal Name"]
                        == selected_alternative
                    ].iloc[0]

                    st.session_state.meal_plan.loc[
                        index
                    ] = new_meal

                    st.rerun()


# MEAL PLAN SUMMARY

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
        plan_days
    )

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
    "Estimated costs reflect the ingredients used "
    "for your selected serving sizes."
)
