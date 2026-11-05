
import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components
import base64
import re
import mimetypes


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


def encode_image(image_path):
    """Convert an image into a format that HTML can display."""

    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode("utf-8")

    mime_type = mimetypes.guess_type(str(image_path))[0]

    if mime_type is None:
        mime_type = "image/jpeg"

    return f"data:{mime_type};base64,{encoded}"


# --------------------------------------------------
# RECIPE PHOTO DISPLAY
# --------------------------------------------------

def show_recipe_images(
    homemade_path,
    restaurant_path,
    ingredients_path
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

    # Use Streamlit's image viewer when only one photo exists.

    if len(image_paths) == 1:
        st.image(
            str(image_paths[0]),
            use_container_width=True
        )
        return

    # Convert available photos into HTML-compatible images.

    images = [
        encode_image(image_path)
        for image_path in image_paths
    ]

    image_sources = ", ".join(
        f'"{image}"' for image in images
    )

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

        <style>

            * {{
                box-sizing: border-box;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}

            .photo-container {{
                position: relative;
                width: 100%;
                height: 150px;
                overflow: hidden;
                border-radius: 8px;
                background: #eeeeee;
                cursor: zoom-in;
            }}

            .recipe-photo {{
                width: 100%;
                height: 150px;
                object-fit: cover;
                display: block;
            }}

            .arrow {{
                position: absolute;
                top: 50%;
                transform: translateY(-50%);
                border: none;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                background: rgba(0, 0, 0, 0.65);
                color: white;
                font-size: 20px;
                cursor: pointer;
                opacity: 0;
                transition: opacity 0.2s;
                z-index: 2;
            }}

            .photo-container:hover .arrow,
            .arrow:focus {{
                opacity: 1;
            }}

            .left-arrow {{
                left: 8px;
            }}

            .right-arrow {{
                right: 8px;
            }}

            @media (hover: none) {{
                .arrow {{
                    opacity: 1;
                }}
            }}

        </style>

    </head>

    <body>

        <div
            class="photo-container"
            onclick="openLargeImage()"
            title="Click to view larger image"
        >

            <img
                id="recipe-photo"
                class="recipe-photo"
                src="{images[0]}"
            >

            <button
                class="arrow left-arrow"
                onclick="changePhoto(-1, event)"
                aria-label="Previous photo"
            >
                &#8249;
            </button>

            <button
                class="arrow right-arrow"
                onclick="changePhoto(1, event)"
                aria-label="Next photo"
            >
                &#8250;
            </button>

        </div>

        <script>

            const imageSources = [{image_sources}];

            let currentPhoto = 0;

            function changePhoto(direction, event) {{

                if (event) {{
                    event.stopPropagation();
                }}

                currentPhoto = (
                    currentPhoto + direction + imageSources.length
                ) % imageSources.length;

                document.getElementById("recipe-photo").src =
                    imageSources[currentPhoto];

            }}

            function openLargeImage() {{

                const newTab = window.open("", "_blank");

                if (!newTab) {{
                    return;
                }}

                newTab.document.write(`
                    <!DOCTYPE html>
                    <html>

                    <head>

                        <title>MealMatch Recipe Photo</title>

                        <style>

                            body {{
                                margin: 0;
                                background: #111111;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                min-height: 100vh;
                            }}

                            img {{
                                max-width: 95vw;
                                max-height: 95vh;
                                object-fit: contain;
                            }}

                        </style>

                    </head>

                    <body>

                        <img src="${{imageSources[currentPhoto]}}">

                    </body>

                    </html>
                `);

                newTab.document.close();

            }}

        </script>

    </body>

    </html>
    """

    components.html(
        html,
        height=155,
        scrolling=False
    )


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
                        ingredients_path
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
