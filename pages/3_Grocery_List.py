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

import streamlit.components.v1 as components
import json

st.divider()
st.subheader("Ingredients Needed")
st.write("Check off ingredients you already have.")

if grocery_display:

    grocery_items = json.dumps(grocery_display)

    components.html(
        f"""
        <div id="grocery-list"></div>

        <style>
            .grocery-item {{
                display: flex;
                align-items: center;
                gap: 10px;
                padding: 9px 4px;
                border-bottom: 1px solid rgba(128, 128, 128, 0.3);
                font-family: sans-serif;
                font-size: 15px;
                color: var(--grocery-text);
            }}

            .grocery-item input {{
                width: 17px;
                height: 17px;
                cursor: pointer;
                flex-shrink: 0;
            }}

            .grocery-item.checked span {{
                text-decoration: line-through;
                opacity: 0.55;
            }}
        </style>

        <script>
            const items = {grocery_items};
            const container = document.getElementById("grocery-list");

            const appContainer = window.parent.document.querySelector(
                '[data-testid="stAppViewContainer"]'
            );

            const themeText = window.parent.getComputedStyle(
                appContainer
            ).color;

            container.style.setProperty(
                "--grocery-text",
                themeText
            );

            items.forEach((item, index) => {{

                const row = document.createElement("label");
                row.className = "grocery-item";

                const checkbox = document.createElement("input");
                checkbox.type = "checkbox";

                const text = document.createElement("span");

                text.textContent =
                    item["Ingredient"] + " | " +
                    item["Quantity Needed"];

                checkbox.addEventListener("change", function() {{
                    row.classList.toggle(
                        "checked",
                        checkbox.checked
                    );
                }});

                row.appendChild(checkbox);
                row.appendChild(text);

                container.appendChild(row);
            }});
        </script>
        """,
        height=max(150, len(grocery_display) * 42 + 20),
        scrolling=False
    )

    st.caption(
        f"{len(grocery_display)} unique ingredients "
        "in your grocery list."
    )

else:
    st.info("No ingredients found for your selected meals.")
