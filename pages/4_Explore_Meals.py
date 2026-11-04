
import streamlit as st
import pandas as pd

# PAGE TITLE

st.title("📖 Explore All Meals")

st.write(
    "Browse the full MealMatch recipe collection. "
    "Select a meal to view its ingredients, nutrition, "
    "and cooking instructions."
)

# LOAD DATA

meals = st.session_state["meals"]
ingredients = st.session_state["ingredients"]

st.divider()

# SEARCH MEALS

search_term = st.text_input(
    "🔍 Search for a meal",
    placeholder="Example: chicken, pasta, yogurt..."
)

# SHOW ALL MEALS BY DEFAULT

display_meals = meals.copy()

if search_term.strip():

    display_meals = display_meals[
        display_meals["Meal Name"]
        .astype(str)
        .str.contains(search_term.strip(), case=False, na=False)
    ]

st.caption(
    f"Showing {len(display_meals)} of {len(meals)} meals."
)

st.divider()


# HELPER FUNCTION FOR DISPLAYING VALUES

def show_value(value):

    if pd.isna(value):
        return "Not listed"

    return str(value).strip()


def show_number(value, unit=""):

    if pd.isna(value):
        return "Not listed"

    try:
        number = float(
            str(value).replace("$", "").replace(",", "").strip()
        )

        if number.is_integer():
            return f"{int(number)}{unit}"

        return f"{number:g}{unit}"

    except (ValueError, TypeError):
        return f"{value}{unit}"


# DISPLAY EACH MEAL

for _, meal in display_meals.iterrows():

    meal_name = str(meal["Meal Name"]).strip()

    total_time = show_number(meal["Total Time"])
    if total_time != "Not listed":
        total_time = total_time.replace(" min", "").replace("min", "") + " min"

    ingredient_cost = show_number(
        meal["Ingredient Cost"]
    )

    # FIND INGREDIENTS FOR THIS MEAL

    meal_ingredients = ingredients[
        ingredients["Meal Name"].astype(str).str.strip().str.lower()
        == meal_name.lower()
    ]

    # CREATE DROPDOWN FOR EACH MEAL

    with st.expander(
        f"🍽️ {meal_name} | {total_time} | ${ingredient_cost}"
    ):

        # MEAL INFORMATION

        st.subheader("Meal Information")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Time",
                total_time
            )

        with col2:
            st.metric(
                "Preparation Time",
                show_number(meal["Prep Time"])
            )

        with col3:
            st.metric(
                "Cooking Time",
                show_number(meal["Cooking Time"])
            )

        col1, col2 = st.columns(2)

        with col1:
            st.write(
                f"**Original Servings:** "
                f"{show_value(meal['Servings'])}"
            )

        with col2:
            st.write(
                f"**Dietary Type:** "
                f"{show_value(meal['Dietary Type'])}"
            )

        st.write(
            f"**Food Preferences:** "
            f"{show_value(meal['Food Preferences'])}"
        )

        st.write(
            f"**Estimated Ingredient Cost:** "
            f"${ingredient_cost}"
        )

        st.divider()

        # INGREDIENTS

        st.subheader("🥕 Ingredients")

        if not meal_ingredients.empty:

            for _, item in meal_ingredients.iterrows():

                ingredient_name = show_value(item["Ingredients"])
                quantity = show_value(item["Quantity"])
                unit = show_value(item["Unit"])

                if unit == "Not listed" or unit == "N/A":
                    st.write(
                        f"• {ingredient_name}: {quantity}"
                    )
                else:
                    st.write(
                        f"• {ingredient_name}: {quantity} {unit}"
                    )

        else:
            st.info("No ingredient information found.")

        st.divider()

        # NUTRITION INFORMATION

        st.subheader("❤️ Nutrition Information")

        nutrition_fields = [
            ("Calories", ""),
            ("Total Fat", " g"),
            ("Cholesterol", " mg"),
            ("Sodium", " mg"),
            ("Total Carbohydrates", " g"),
            ("Dietary Fiber", " g"),
            ("Total Sugars", " g"),
            ("Protein", " g")
        ]

        nutrition_columns = st.columns(4)

        for index, (field, unit) in enumerate(nutrition_fields):

            with nutrition_columns[index % 4]:

                if field in meal.index:

                    st.metric(
                        field,
                        show_number(meal[field], unit)
                    )

                else:
                    st.metric(field, "Not listed")

        st.divider()

        # COOKING INSTRUCTIONS

        st.subheader("👨‍🍳 Cooking Instructions")

        instructions = show_value(
            meal["Cooking Instructions"]
        )

        if instructions != "Not listed":
            st.markdown(instructions)
        else:
            st.info("No cooking instructions available.")

        st.divider()

        st.caption(
            "Recipe information is based on the MealMatch recipe dataset."
        )


# NO SEARCH RESULTS

if display_meals.empty:

    st.warning(
        "No meals matched your search. Try another meal name."
    )
