import streamlit as st
import pandas as pd
from pathlib import Path

# PAGE TITLE

st.title("📖 Explore All Meals")

st.write(
    "Browse the full MealMatch recipe collection. "
    "Select a recipe to view its ingredients, nutrition, "
    "and cooking instructions."
)

# LOAD DATA

meals = st.session_state["meals"]
ingredients = st.session_state["ingredients"]

APP_DIR = Path(__file__).resolve().parent.parent
IMAGE_DIR = APP_DIR / "images"


# RECIPE IMAGE FILENAMES

recipe_images = {
    "Egg Burrito": "egg_burrito.jpg",
    "Chicken Stir-Fry": "chicken_stir_fry.jpg",
    "Pizza Melts": "pizza_melts.jpg",
    "Spinach and Feta Grilled Cheese": "spinach_feta_grilled_cheese.jpg",
    "Chicken-Vegetable Soup": "chicken_vegetable_soup.jpg",
    "Vegetable Curry": "vegetable_curry.jpg",
    "Pasta with Bacon and Peas": "pasta_bacon_peas.jpg",
    "Simple Macaroni and Cheese": "macaroni_cheese.jpg",
    "Sloppy Joe": "sloppy_joe.jpg",
    "Chicken Wings": "chicken_wings.jpg",
    "Taco Nachos": "taco_nachos.jpg",
    "Egg Salad Sandwich": "egg_salad_sandwich.jpg",
    "Protein Waffles": "protein_waffles.jpg",
    "Homemade Chicken Nuggets": "chicken_nuggets.jpg",
    "Honey Garlic Shrimp": "honey_garlic_shrimp.jpg",
    "Shrimp Fried Rice": "shrimp_fried_rice.jpg",
    "Yogurt Berry Bowl": "yogurt_berry_bowl.jpg",
    "Classic Yogurt Bowl": "classic_yogurt_bowl.jpg",
    "Tropical Yogurt Bowl": "tropical_yogurt_bowl.jpg",
    "Meat-Loaf": "meat_loaf.jpg",
    "BBLT Chopped Salad": "bblt_chopped_salad.jpg",
    "Lemon Basil Salmon": "lemon_basil_salmon.jpg",
    "Chicken Caesar Salad": "chicken_caesar_salad.jpg"
}


# HELPER FUNCTIONS

def show_value(value):

    if pd.isna(value):
        return "Not listed"

    return str(value).strip()


def show_number(value, unit=""):

    if pd.isna(value):
        return "Not listed"

    try:
        cleaned_value = (
            str(value)
            .replace("$", "")
            .replace(",", "")
            .replace("mg", "")
            .replace("g", "")
            .replace("min.", "")
            .replace("min", "")
            .strip()
        )

        number = float(cleaned_value)

        if number.is_integer():
            return f"{int(number)}{unit}"

        return f"{number:g}{unit}"

    except (ValueError, TypeError):
        return str(value).strip()


# SEARCH MEALS

st.divider()

search_term = st.text_input(
    "🔍 Search for a meal",
    placeholder="Example: chicken, pasta, yogurt..."
)

display_meals = meals.copy()

if search_term.strip():

    search = search_term.strip().lower()

    matching_meals = meals[
        meals["Meal Name"]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]["Meal Name"].tolist()

    matching_ingredients = ingredients[
        ingredients["Ingredients"]
        .astype(str)
        .str.contains(search, case=False, na=False)
    ]["Meal Name"].tolist()

    matching_names = set(matching_meals + matching_ingredients)

    display_meals = meals[
        meals["Meal Name"].isin(matching_names)
    ]

st.caption(
    f"Showing {len(display_meals)} of {len(meals)} meals."
)

st.divider()


# DISPLAY RECIPE CARDS

if display_meals.empty:

    st.warning(
        "No meals matched your search. Try another meal name."
    )

else:

    # CREATE THREE-COLUMN GRID

    for start in range(0, len(display_meals), 3):

        meal_group = display_meals.iloc[start:start + 3]
        columns = st.columns(3)

        for column, (_, meal) in zip(columns, meal_group.iterrows()):

            meal_name = str(meal["Meal Name"]).strip()

            total_time = show_number(
                meal["Total Time"], " min"
            )

            ingredient_cost = show_number(
                meal["Ingredient Cost"]
            )

            image_filename = recipe_images.get(meal_name)

            if image_filename:
                image_path = IMAGE_DIR / image_filename
            else:
                image_path = None

            # FIND INGREDIENTS

            meal_ingredients = ingredients[
                ingredients["Meal Name"]
                .astype(str)
                .str.strip()
                .str.lower()
                == meal_name.lower()
            ]

            with column:

                with st.container(border=True):

                    # RECIPE IMAGE

                    if image_path and image_path.exists():

                        st.image(
                            str(image_path),
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "📷 Recipe photo coming soon."
                        )

                    # RECIPE NAME AND SUMMARY

                    st.subheader(meal_name)

                    st.caption(
                        f"💰 ${ingredient_cost} estimated cost"
                    )

                    st.caption(
                        f"⏱️ {total_time}"
                    )

                    # RECIPE DETAILS

                    with st.expander("View Recipe"):

                        st.subheader("Meal Information")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.metric(
                                "Total Time",
                                total_time
                            )

                        with col2:
                            st.metric(
                                "Original Servings",
                                show_value(meal["Servings"])
                            )

                        st.write(
                            f"**Preparation Time:** "
                            f"{show_number(meal['Prep Time'], ' min')}"
                        )

                        st.write(
                            f"**Cooking Time:** "
                            f"{show_number(meal['Cooking Time'], ' min')}"
                        )

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

                                ingredient_name = show_value(
                                    item["Ingredients"]
                                )

                                quantity = show_value(
                                    item["Quantity"]
                                )

                                unit = show_value(item["Unit"])

                                if unit in ["Not listed", "N/A"]:
                                    st.write(
                                        f"• {ingredient_name}: {quantity}"
                                    )
                                else:
                                    st.write(
                                        f"• {ingredient_name}: "
                                        f"{quantity} {unit}"
                                    )

                        else:
                            st.info(
                                "No ingredient information found."
                            )

                        st.divider()

                        # NUTRITION

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

                        nutrition_columns = st.columns(2)

                        for index, (field, unit) in enumerate(
                            nutrition_fields
                        ):

                            with nutrition_columns[index % 2]:

                                if field in meal.index:

                                    st.metric(
                                        field,
                                        show_number(meal[field], unit)
                                    )

                                else:
                                    st.metric(
                                        field,
                                        "Not listed"
                                    )

                        st.divider()

                        # COOKING INSTRUCTIONS

                        st.subheader("👨‍🍳 Cooking Instructions")

                        instructions = show_value(
                            meal["Cooking Instructions"]
                        )

                        if instructions != "Not listed":
                            st.markdown(instructions)

                        else:
                            st.info(
                                "No cooking instructions available."
                            )

                        st.divider()

                        st.caption(
                            "Recipe information is based on "
                            "the MealMatch recipe dataset."
                        )
