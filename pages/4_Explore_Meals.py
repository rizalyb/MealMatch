import streamlit as st
import pandas as pd
from pathlib import Path
import re


# --------------------------------------------------
# PAGE SETUP
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = APP_DIR / "images"
HOMEMADE_DIR = IMAGE_DIR / "homemade"
RESTAURANT_DIR = IMAGE_DIR / "restaurant"
INGREDIENTS_DIR = IMAGE_DIR / "ingredients"

st.title("Explore Meals")

st.write(
    "Browse recipes, compare costs, and find meals "
    "that fit your preferences."
)

st.divider()


# --------------------------------------------------
# LOAD MEAL DATA
# --------------------------------------------------

meals = st.session_state.get("meals")
ingredients = st.session_state.get("ingredients")

if meals is None or ingredients is None:
    st.error("Meal data could not be found. Please return to Home.")
    st.stop()

meals = meals.copy()
ingredients = ingredients.copy()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def show_value(value):

    if pd.isna(value) or str(value).strip() == "":
        return "Not available"

    return str(value).strip()


def get_image_name(meal_name):

    name = str(meal_name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")


# --------------------------------------------------
# RECIPE PHOTO DIALOG
# --------------------------------------------------

@st.dialog("Recipe Photos", width="large")
def show_large_photo():

    image_paths = st.session_state.get(
        "large_photo_paths", []
    )

    if not image_paths:
        st.info("No recipe photos are available.")
        return

    if len(image_paths) > 1:

        selected_photo = st.selectbox(
            "Choose a photo",
            range(len(image_paths)),
            format_func=lambda index: Path(
                image_paths[index]
            ).stem.replace("_", " ").title()
        )

    else:
        selected_photo = 0

    st.image(
        image_paths[selected_photo],
        use_container_width=True
    )


# --------------------------------------------------
# RECIPE PHOTO DISPLAY
# --------------------------------------------------

def show_recipe_images(meal_name):

    image_name = get_image_name(meal_name)

    possible_images = [
        HOMEMADE_DIR / f"{image_name}_hm.jpeg",
        RESTAURANT_DIR / f"{image_name}_r.jpeg",
        INGREDIENTS_DIR / f"{image_name}_i.jpeg"
    ]

    image_paths = [
        path for path in possible_images
        if path.exists()
    ]

    if not image_paths:
        st.info("📷 Recipe photos coming soon.")
        return False

    st.image(
        image_paths[0],
        use_container_width=True
    )

    if len(image_paths) > 1:
        st.caption(
            f"{len(image_paths)} recipe photos available."
        )

    if st.button(
        "View Photos",
        key=f"view_photos_{image_name}",
        use_container_width=True
    ):

        st.session_state["large_photo_paths"] = [
            str(path) for path in image_paths
        ]

        return True

    return False


# --------------------------------------------------
# SEARCH MEALS
# --------------------------------------------------

st.subheader("Find a Recipe")

search_query = st.text_input(
    "Search by meal name or ingredient",
    placeholder="Example: Chicken, pasta, or burrito"
)

filtered_meals = meals.copy()

if search_query.strip():

    search_query = search_query.lower().strip()

    meal_matches = (
        filtered_meals["Meal Name"]
        .astype(str)
        .str.lower()
        .str.contains(search_query, regex=False, na=False)
    )

    ingredient_matches = ingredients[
        ingredients["Ingredients"]
        .astype(str)
        .str.lower()
        .str.contains(search_query, regex=False, na=False)
    ]["Meal Name"].dropna().astype(str).str.lower().unique()

    filtered_meals = filtered_meals[
        meal_matches |
        filtered_meals["Meal Name"]
        .astype(str)
        .str.lower()
        .isin(ingredient_matches)
    ]


st.write(f"Showing {len(filtered_meals)} recipes.")

st.divider()


# --------------------------------------------------
# DISPLAY RECIPE CARDS
# --------------------------------------------------

open_large_photo = False

if filtered_meals.empty:

    st.warning(
        "No recipes matched your search. "
        "Try another meal or ingredient."
    )

else:

    meal_records = filtered_meals.to_dict("records")

    for start in range(0, len(meal_records), 3):

        columns = st.columns(3)

        for column, meal in zip(
            columns,
            meal_records[start:start + 3]
        ):

            with column:

                meal_name = show_value(
                    meal.get("Meal Name")
                )

                with st.container(border=True):

                    st.subheader(meal_name)

                    photo_requested = show_recipe_images(
                        meal_name
                    )

                    if photo_requested:
                        open_large_photo = True

                    st.write(
                        f"**Estimated ingredient cost:** "
                        f"{show_value(meal.get('Ingredient Cost'))}"
                    )

                    st.write(
                        f"**Total time:** "
                        f"{show_value(meal.get('Total Time'))}"
                    )

                    st.write(
                        f"**Servings:** "
                        f"{show_value(meal.get('Servings'))}"
                    )

                    with st.expander("View Recipe Details"):

                        st.markdown("### Meal Information")

                        st.write(
                            f"**Dietary type:** "
                            f"{show_value(meal.get('Dietary Type'))}"
                        )

                        st.write(
                            f"**Food preferences:** "
                            f"{show_value(meal.get('Food Preferences'))}"
                        )

                        st.write(
                            f"**Preparation time:** "
                            f"{show_value(meal.get('Prep Time'))}"
                        )

                        st.write(
                            f"**Cooking time:** "
                            f"{show_value(meal.get('Cooking Time'))}"
                        )

                        st.divider()

                        st.markdown("### Ingredients")

                        meal_ingredients = ingredients[
                            ingredients["Meal Name"]
                            .astype(str)
                            .str.lower()
                            == meal_name.lower()
                        ].copy()

                        if not meal_ingredients.empty:

                            display_columns = [
                                name for name in [
                                    "Ingredients",
                                    "Quantity",
                                    "Unit",
                                    "Estimated Cost"
                                ]
                                if name in meal_ingredients.columns
                            ]

                            st.dataframe(
                                meal_ingredients[display_columns],
                                hide_index=True,
                                use_container_width=True
                            )

                        else:
                            st.info(
                                "Ingredient details are not available."
                            )

                        st.divider()

                        st.markdown("### Nutrition Information")

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

                            value = show_value(
                                meal.get(column_name)
                            )

                            if value != "Not available":

                                nutrition_values.append(
                                    f"**{label}:** {value}"
                                )

                        if nutrition_values:

                            for value in nutrition_values:
                                st.write(value)

                        else:
                            st.info(
                                "Nutrition information is not available."
                            )

                        st.divider()

                        st.markdown("### Cooking Instructions")

                        instructions = show_value(
                            meal.get("Cooking Instructions")
                        )

                        if instructions != "Not available":
                            st.write(instructions)

                        else:
                            st.info(
                                "Cooking instructions are not available."
                            )


# --------------------------------------------------
# OPEN PHOTO DIALOG
# --------------------------------------------------

if open_large_photo:
    show_large_photo()
