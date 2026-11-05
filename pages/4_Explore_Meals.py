
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
st.write("Browse recipes, compare costs, and find meals that fit your preferences.")

st.divider()


# --------------------------------------------------
# LOAD MEAL DATA
# --------------------------------------------------

meals = st.session_state.get("meals")
ingredients = st.session_state.get("ingredients")

if meals is None or ingredients is None:
    st.error(
        "Meal data could not be found. "
        "Please return to the Home page and try again."
    )
    st.stop()

meals = meals.copy()
ingredients = ingredients.copy()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def show_value(value):
    """Return a clean value or a placeholder."""

    if pd.isna(value) or str(value).strip() == "":
        return "Not available"

    return str(value).strip()


def show_number(value):
    """Convert a value into a readable number."""

    if pd.isna(value) or str(value).strip() == "":
        return "Not available"

    return str(value).strip()


def get_image_name(meal_name):
    """Convert a meal name into a lowercase image filename."""

    name = str(meal_name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)
    name = name.strip("_")

    return name


# --------------------------------------------------
# PHOTO NAVIGATION
# --------------------------------------------------

def change_recipe_photo(state_key, direction, photo_count):
    """Change the selected photo in a recipe card."""

    current_index = st.session_state.get(state_key, 0)

    st.session_state[state_key] = (
        current_index + direction
    ) % photo_count


def change_large_photo(direction):
    """Change the photo inside the enlarged photo dialog."""

    image_paths = st.session_state.get("large_photo_paths", [])

    if not image_paths:
        return

    current_index = st.session_state.get("large_photo_index", 0)

    st.session_state["large_photo_index"] = (
        current_index + direction
    ) % len(image_paths)


# --------------------------------------------------
# ENLARGED PHOTO DIALOG
# --------------------------------------------------

@st.dialog("Enlarged Recipe Photo", width="large")
def show_large_photo():

    image_paths = st.session_state.get("large_photo_paths", [])

    if not image_paths:
        st.info("No recipe photos are available.")
        return

    current_index = st.session_state.get("large_photo_index", 0)

    # Display the enlarged photo.

    st.image(
        image_paths[current_index],
        use_container_width=True
    )

    # Photo navigation.

    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:

            st.button(
                "← Previous Photo",
                key="large_photo_previous",
                use_container_width=True,
                on_click=change_large_photo,
                args=(-1,)
            )

        with next_col:

            st.button(
                "Next Photo →",
                key="large_photo_next",
                use_container_width=True,
                on_click=change_large_photo,
                args=(1,)
            )


# --------------------------------------------------
# RECIPE PHOTO DISPLAY
# --------------------------------------------------

def show_recipe_images(
    homemade_path,
    restaurant_path,
    ingredients_path,
    meal_name
):

    # Collect available photos.

    image_paths = []

    if homemade_path.exists():
        image_paths.append(homemade_path)

    if restaurant_path.exists():
        image_paths.append(restaurant_path)

    if ingredients_path.exists():
        image_paths.append(ingredients_path)

    # Show a message if no photos exist.

    if not image_paths:
        st.info("📷 Recipe photos coming soon.")
        return

    # Create a unique session key for each recipe.

    state_key = f"photo_index_{get_image_name(meal_name)}"

    if state_key not in st.session_state:
        st.session_state[state_key] = 0

    current_index = st.session_state[state_key]

    # Display the selected photo.

    st.image(
        str(image_paths[current_index]),
        use_container_width=True
    )

    # Photo navigation buttons.

    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:

            st.button(
                "← Previous",
                key=f"{state_key}_previous",
                use_container_width=True,
                on_click=change_recipe_photo,
                args=(state_key, -1, len(image_paths))
            )

        with next_col:

            st.button(
                "Next →",
                key=f"{state_key}_next",
                use_container_width=True,
                on_click=change_recipe_photo,
                args=(state_key, 1, len(image_paths))
            )

    # Open the enlarged photo dialog.

    if st.button(
        "🔍 View Larger Photo",
        key=f"{state_key}_enlarge",
        use_container_width=True
    ):

        st.session_state["large_photo_paths"] = [
            str(path) for path in image_paths
        ]

        st.session_state["large_photo_index"] = (
            st.session_state[state_key]
        )

        show_large_photo()


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

    meal_matches = filtered_meals["Meal Name"].astype(str).str.lower().str.contains(
        search_query,
        na=False
    )

    ingredient_matches = ingredients[
        ingredients["Ingredients"].astype(str).str.lower().str.contains(
            search_query,
            na=False
        )
    ]["Meal Name"].dropna().unique()

    ingredient_matches = [
        str(name).lower() for name in ingredient_matches
    ]

    filtered_meals = filtered_meals[
        meal_matches |
        filtered_meals["Meal Name"].astype(str).str.lower().isin(
            ingredient_matches
        )
    ]


st.write(f"Showing {len(filtered_meals)} recipes.")

st.divider()


# --------------------------------------------------
# DISPLAY RECIPE CARDS
# --------------------------------------------------

if filtered_meals.empty:

    st.warning("No recipes matched your search. Try another meal or ingredient.")

else:

    meal_records = filtered_meals.to_dict("records")

    for start in range(0, len(meal_records), 3):

        columns = st.columns(3)

        for column, meal in zip(columns, meal_records[start:start + 3]):

            with column:

                meal_name = show_value(meal.get("Meal Name"))

                # Find the three possible recipe photos.

                image_name = get_image_name(meal_name)

                homemade_path = (
                    HOMEMADE_DIR / f"{image_name}_hm.jpeg"
                )

                restaurant_path = (
                    RESTAURANT_DIR / f"{image_name}_r.jpeg"
                )

                ingredients_path = (
                    INGREDIENTS_DIR / f"{image_name}_i.jpeg"
                )

                # Recipe card.

                with st.container(border=True):

                    st.subheader(meal_name)

                    show_recipe_images(
                        homemade_path,
                        restaurant_path,
                        ingredients_path,
                        meal_name
                    )

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

                    # Expandable recipe details.

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

                        # Ingredients.

                        st.markdown("### Ingredients")

                        meal_ingredients = ingredients[
                            ingredients["Meal Name"].astype(str).str.lower()
                            == meal_name.lower()
                        ].copy()

                        if not meal_ingredients.empty:

                            display_columns = [
                                column_name
                                for column_name in [
                                    "Ingredients",
                                    "Quantity",
                                    "Unit",
                                    "Estimated Cost"
                                ]
                                if column_name in meal_ingredients.columns
                            ]

                            st.dataframe(
                                meal_ingredients[display_columns],
                                hide_index=True,
                                use_container_width=True
                            )

                        else:

                            st.info("Ingredient details are not available.")

                        st.divider()

                        # Nutrition information.

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

                            st.info("Nutrition information is not available.")

                        st.divider()

                        # Cooking instructions.

                        st.markdown("### Cooking Instructions")

                        instructions = show_value(
                            meal.get("Cooking Instructions")
                        )

                        if instructions != "Not available":

                            st.write(instructions)

                        else:

                            st.info("Cooking instructions are not available.")
