import streamlit as st
import pandas as pd
from fractions import Fraction
import re

# PAGE TITLE

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


# COMBINE INGREDIENTS FROM ALL SELECTED MEALS

combined_ingredients = {}

for _, meal in meal_plan.iterrows():

    meal_ingredients = ingredients[
        ingredients["Meal Name"].astype(str).str.strip().str.lower()
        == str(meal["Meal Name"]).strip().lower()
    ]

    serving_numbers = re.findall(r"\d+", str(meal["Servings"]))

    if serving_numbers:
        original_servings = max(map(int, serving_numbers))
    else:
        original_servings = 1

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

        # CALCULATE ESTIMATED INGREDIENT COST

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
        if quantity_text:
            quantity_text = f"{quantity_text}, {notes}"
        else:
            quantity_text = notes

    grocery_display.append({
        "Ingredient": item["Ingredient"],
        "Quantity Needed": f"{quantity_text} {item['Unit']}".strip(),
        "Estimated Cost": item["Estimated Cost"]
    })


# DISPLAY GROCERY LIST

st.divider()

st.subheader("Shopping Checklist")

st.write(
    "Check off each ingredient when you already have it "
    "or when you finish shopping for it."
)

if grocery_display:

    # KEEP TRACK OF CHECKED INGREDIENTS

    if "checked_ingredients" not in st.session_state:
        st.session_state["checked_ingredients"] = set()

    # COLUMN HEADINGS

    header1, header2, header3, header4 = st.columns([0.4, 2.6, 1.5, 1])

    with header2:
        st.caption("INGREDIENT")

    with header3:
        st.caption("QUANTITY")

    with header4:
        st.caption("COST")

    st.divider()

     # DISPLAY EACH INGREDIENT

    for index, item in enumerate(grocery_display):

        ingredient = item["Ingredient"]
        quantity = item["Quantity Needed"]
        cost = item["Estimated Cost"]

        ingredient_id = f"{ingredient}_{quantity}"

        checked = (
            ingredient_id
            in st.session_state["checked_ingredients"]
        )

        col1, col2, col3, col4 = st.columns(
            [0.4, 2.6, 1.5, 1],
            vertical_alignment="center"
        )

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
                st.markdown(f"~~{ingredient}~~")
            else:
                st.write(ingredient)

        with col3:
            if new_checked:
                st.markdown(f"~~{quantity}~~")
            else:
                st.write(quantity)

        with col4:
            if new_checked:
                st.markdown(f"~~${cost:.2f}~~")
            else:
                st.write(f"${cost:.2f}")

        st.divider()

    # CALCULATE TOTAL COST

    total_cost = sum(
        item["Estimated Cost"] for item in grocery_display
    )

    # COUNT CHECKED ITEMS

    current_ingredient_ids = {
        f"{item['Ingredient']}_{item['Quantity Needed']}"
        for item in grocery_display
    }

    checked_count = len(
        st.session_state["checked_ingredients"].intersection(
            current_ingredient_ids
        )
    )

    # DISPLAY SUMMARY

    st.subheader("Grocery List Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Estimated Ingredient Cost",
            f"${total_cost:.2f}"
        )

    with col2:
        st.metric(
            "Items Checked",
            f"{checked_count}/{len(grocery_display)}"
        )

else:

    st.info("No ingredients found for your selected meals.")
