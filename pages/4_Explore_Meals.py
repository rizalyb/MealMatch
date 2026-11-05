
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
# PHOTO HOVER CONTROLS
# --------------------------------------------------

st.markdown(
    """
    <style>

    /* Make each photo container the positioning reference */
    div[class*="st-key-photo_viewer_"] {
        position: relative;
    }

    /* Hide photo controls until the photo area is hovered */
    div[class*="st-key-photo_prev_"],
    div[class*="st-key-photo_next_"],
    div[class*="st-key-photo_expand_"] {
        position: absolute !important;
        z-index: 10;
        opacity: 0;
        transition: opacity 0.2s ease;
    }

    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_prev_"],
    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_next_"],
    div[class*="st-key-photo_viewer_"]:hover
    div[class*="st-key-photo_expand_"] {
        opacity: 1;
    }

    /* Left arrow */
    div[class*="st-key-photo_prev_"] {
        left: 8%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Right arrow */
    div[class*="st-key-photo_next_"] {
        right: 8%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Expand icon */
    div[class*="st-key-photo_expand_"] {
        right: 8%;
        bottom: 8px;
    }
    
    /* Style the control buttons */
    div[class*="st-key-photo_prev_"] button,
    div[class*="st-key-photo_next_"] button,
    div[class*="st-key-photo_expand_"] button {
        border-radius: 50%;
        background-color: rgba(0, 0, 0, 0.65);
        color: white;
        border: none;
        min-width: 38px;
        width: 38px;
        height: 38px;
        padding: 0;
        font-size: 22px;
    }

    div[class*="st-key-photo_prev_"] button:hover,
    div[class*="st-key-photo_next_"] button:hover,
    div[class*="st-key-photo_expand_"] button:hover {
        background-color: rgba(0, 0, 0, 0.85);
        color: white;
    }

    </style>
    """,
    unsafe_allow_html=True
)


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

    selected_photo = st.session_state.get(
        "large_photo_index", 0
    )

    selected_photo = selected_photo % len(image_paths)

    # Display the current enlarged photo
    st.image(
        image_paths[selected_photo],
        use_container_width=False,
        width=850
    )

    # Display photo category
    photo_name = Path(
        image_paths[selected_photo]
    ).stem

    if photo_name.endswith("_hm"):
        photo_label = "Homemade"
    elif photo_name.endswith("_r"):
        photo_label = "Restaurant"
    elif photo_name.endswith("_i"):
        photo_label = "Ingredients"
    else:
        photo_label = "Recipe Photo"

    st.caption(
        f"{photo_label} Photo ({selected_photo + 1} of {len(image_paths)})"
    )

    # Navigation arrows
    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:
            if st.button(
                "← Previous",
                use_container_width=True,
                key="dialog_previous_photo"
            ):
                st.session_state["large_photo_index"] = (
                    selected_photo - 1
                ) % len(image_paths)

                st.rerun(scope="fragment")

        with next_col:
            if st.button(
                "Next →",
                use_container_width=True,
                key="dialog_next_photo"
            ):
                st.session_state["large_photo_index"] = (
                    selected_photo + 1
                ) % len(image_paths)

                st.rerun(scope="fragment")


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

    # Keep track of the current photo
    photo_key = f"photo_index_{image_name}"

    if photo_key not in st.session_state:
        st.session_state[photo_key] = 0

    current_index = (
        st.session_state[photo_key] % len(image_paths)
    )

    viewer_key = f"photo_viewer_{image_name}"

    with st.container(key=viewer_key):

        # Make the regular photo slightly larger
        _, image_col, _ = st.columns([0.35, 2.3, 0.35])

        with image_col:
            st.image(
                image_paths[current_index],
                use_container_width=True
            )

        # Previous photo arrow
        if len(image_paths) > 1:

            if st.button(
                "‹",
                key=f"photo_prev_{image_name}"
            ):
                st.session_state[photo_key] = (
                    current_index - 1
                ) % len(image_paths)

                st.rerun()

            # Next photo arrow
            if st.button(
                "›",
                key=f"photo_next_{image_name}"
            ):
                st.session_state[photo_key] = (
                    current_index + 1
                ) % len(image_paths)

                st.rerun()

        # Single expand button
        if st.button(
            "⛶",
            key=f"photo_expand_{image_name}"
        ):

            st.session_state["large_photo_paths"] = [
                str(path) for path in image_paths
            ]

            st.session_state["large_photo_index"] = (
                current_index
            )

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
