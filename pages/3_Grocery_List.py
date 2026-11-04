import streamlit as st
import pandas as pd
from fractions import Fraction
import re

st.title("🛒 Your Grocery List")

st.write(
    "View the combined ingredients needed for all meals "
    "in your current meal plan."
)

# LOAD SHARED DATA

if "meal_plan" not in st.session_state:
    st.info("Please visit the Meal Planner and generate a meal plan first.")
    st.stop()

meal_plan = st.session_state["meal_plan"]
ingredients = st.session_state["ingredients"]

# PARSE INGREDIENT QUANTITIES

def parse_quantity(value):
    if pd.isna(value):
        return None

    quantity = str(value).strip()

    try:
        parts = quantity.split()

        if len(parts) == 2 and "/" in parts[1]:
            return float(Fraction(parts[0]) + Fraction(parts[1]))

        return float(Fraction(quantity))

    except (ValueError, ZeroDivisionError):
        return None

# COMBINE INGREDIENTS

combined_ingredients = {}

for _, meal in meal_plan.iterrows():

    meal_ingredients = ingredients[
        ingredients["Meal Name"].astype(str).str.strip().str.lower()
        == str(meal["Meal Name"]).strip().lower()
    ]

    serving_numbers = re.findall(r"\d+", str(meal["Servings"]))

    original_servings = (
        max(map(int, serving_numbers))
        if serving_numbers else 1
    )

    desired_servings = st.session_state["desired_servings"]

    scaling_factor = desired_servings / original_servings

    for _, item in meal_ingredients.iterrows():

        ingredient_name = str(item["Ingredients"]).strip()

        if pd.isna(item["Unit"]):
            unit = ""
        else:
            unit = str(item["Unit"]).strip()

        key = (ingredient_name.lower(), unit.lower())

        if key not in combined_ingredients:
            combined_ingredients[key] = {
                "Ingredient": ingredient_name,
                "Unit": unit,
                "Quantity": 0,
                "Has Number": False,
                "Other Notes": set()
            }

        quantity = parse_quantity(item["Quantity"])

        if quantity is not None:
            combined_ingredients[key]["Quantity"] += (
                quantity * scaling_factor
            )

            combined_ingredients[key]["Has Number"] = True

        else:
            if pd.notna(item["Quantity"]):
                combined_ingredients[key]["Other Notes"].add(
                    str(item["Quantity"]).strip()
                )


# FORMAT GROCERY LIST

grocery_display = []

for item in combined_ingredients.values():

    if item["Has Number"]:
        quantity = item["Quantity"]

        if quantity.is_integer():
            quantity_text = str(int(quantity))
        else:
            quantity_text = (
                f"{quantity:.2f}".rstrip("0").rstrip(".")
            )
    else:
        quantity_text = ""

    notes = ", ".join(sorted(item["Other Notes"]))

    if notes:
        quantity_text = (
            f"{quantity_text}, {notes}"
            if quantity_text else notes
        )

    grocery_display.append({
        "Ingredient": item["Ingredient"],
        "Quantity Needed": f"{quantity_text} {item['Unit']}".strip()
    })


# DISPLAY GROCERY LIST

st.divider()
st.subheader("Ingredients Needed")
st.write("Check off ingredients you already have.")

if grocery_display:

    if "checked_ingredients" not in st.session_state:
        st.session_state["checked_ingredients"] = set()

    for index, item in enumerate(grocery_display):

        ingredient = item["Ingredient"]
        quantity = item["Quantity Needed"]

        ingredient_id = f"{ingredient}_{quantity}"

        checked = ingredient_id in st.session_state["checked_ingredients"]

        col1, col2 = st.columns([0.06, 0.94], vertical_alignment="center")

        with col1:
            new_checked = st.checkbox(
                " ",
                value=checked,
                key=f"check_{index}_{ingredient_id}"
            )

        if new_checked:
            st.session_state["checked_ingredients"].add(ingredient_id)
        else:
            st.session_state["checked_ingredients"].discard(ingredient_id)

       with col2:

    if new_checked:
        text_style = (
            "text-decoration: line-through; opacity: 0.5;"
        )
    else:
        text_style = ""

    st.markdown(
        f"""
        <div style="
            {text_style}
            line-height: 38px;
            margin: 0;
            padding: 0;
        ">
            {ingredient} | {quantity}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        f"{len(grocery_display)} unique ingredients "
        "in your grocery list."
    )

else:
    st.info("No ingredients found for your selected meals.")
