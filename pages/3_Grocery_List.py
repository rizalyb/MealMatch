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
                "Other Notes": set(),
                "Estimated Cost": 0
            }

        # CALCULATE INGREDIENT COST

        cost_value = pd.to_numeric(
            str(item["Estimated Cost"]).replace("$", "").replace(",", ""),
            errors="coerce"
        )

        if pd.notna(cost_value):
            combined_ingredients[key]["Estimated Cost"] += (
                cost_value * scaling_factor
            )

        # CALCULATE INGREDIENT QUANTITY

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
        "Quantity Needed": f"{quantity_text} {item['Unit']}".strip(),
        "Estimated Cost": item["Estimated Cost"]
    })


# DISPLAY GROCERY LIST

st.divider()

st.subheader("🛒 Shopping Checklist")
st.write("Check off each ingredient as you shop or if you already have it.")

if grocery_display:

    if "checked_ingredients" not in st.session_state:
        st.session_state["checked_ingredients"] = set()

    # COLUMN HEADINGS

    header1, header2, header3 = st.columns([3, 1.5, 1])

    with header1:
        st.caption("INGREDIENT")

    with header2:
        st.caption("QUANTITY")

    with header3:
        st.caption("COST")

    st.divider()

    # INGREDIENT ROWS

    for index, item in enumerate(grocery_display):

        ingredient = item["Ingredient"]
        quantity = item["Quantity Needed"]
        cost = item["Estimated Cost"]

        ingredient_id = f"{ingredient}_{quantity}"

        checked = (
            ingredient_id
            in st.session_state["checked_ingredients"]
        )

        col1, col2, col3 = st.columns(
            [3, 1.5, 1],
            vertical_alignment="center"
        )

        with col1:
            new_checked = st.checkbox(
                ingredient,
                value=checked,
                key=f"check_{index}_{ingredient_id}"
            )

        if new_checked:
            st.session_state["checked_ingredients"].add(ingredient_id)
        else:
            st.session_state["checked_ingredients"].discard(ingredient_id)

        with col2:
            st.write(quantity)

        with col3:
            st.write(f"${cost:.2f}")

        st.divider()

    # TOTAL COST

    total_cost = sum(
        item["Estimated Cost"] for item in grocery_display
    )

    checked_count = len(
        st.session_state["checked_ingredients"].intersection(
            {
                f"{item['Ingredient']}_{item['Quantity Needed']}"
                for item in grocery_display
            }
        )
    )

    st.subheader("Estimated Grocery Cost")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Ingredient Cost", f"${total_cost:.2f}")

    with col2:
        st.metric(
            "Items Checked",
            f"{checked_count}/{len(grocery_display)}"
        )

else:
    st.info("No ingredients found for your selected meals.")

    # TOTAL GROCERY COST

    total_cost = sum(
        item["Estimated Cost"] for item in grocery_display
    )

    st.divider()
    st.subheader("Estimated Grocery Cost")

    st.metric(
        "Total Ingredient Cost",
        f"${total_cost:.2f}"
    )

    st.caption(
        f"{len(grocery_display)} unique ingredients "
        "in your grocery list."
    )

else:
    st.info("No ingredients found for your selected meals.")
