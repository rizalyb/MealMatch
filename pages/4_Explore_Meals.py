import streamlit as st
import pandas as pd
from pathlib import Path
import streamlit.components.v1 as components
import base64
import re


# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("📖 Explore All Meals")
st.write("Browse meals, view ingredients, and explore recipes for your meal plan.")


# --------------------------------------------------
# IMAGE FOLDERS
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent.parent

IMAGE_DIR = APP_DIR / "images"
HOMEMADE_DIR = IMAGE_DIR / "homemade"
RESTAURANT_DIR = IMAGE_DIR / "restaurant"
INGREDIENTS_DIR = IMAGE_DIR / "ingredients"


# --------------------------------------------------
# LOAD MEALS AND INGREDIENTS
# --------------------------------------------------

meals = st.session_state.get("meals")
ingredients = st.session_state.get("ingredients")

if meals is None or ingredients is None:
    st.error("Meal data could not be loaded. Please return to the Home page and try again.")
    st.stop()


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------

def show_value(value):
    """Return a clean value or display a placeholder."""

    if pd.isna(value):
        return "N/A"

    return str(value)


def show_number(value):
    """Format numbers and remove existing units or currency symbols."""

    if pd.isna(value):
        return "N/A"

    cleaned_value = str(value).strip()

    cleaned_value = (
        cleaned_value
        .replace("$", "")
        .replace(",", "")
        .replace("g", "")
        .replace("mg", "")
        .replace("min", "")
        .strip()
    )

    try:
        number = float(cleaned_value)

        if number.is_integer():
            return f"{int(number):,}"

        return f"{number:,.2f}".rstrip("0").rstrip(".")

    except ValueError:
        return str(value)


def get_image_name(meal_name):
    """Create a consistent image filename from the recipe name."""

    image_name = meal_name.lower().strip()

    image_name = re.sub(r"[^a-z0-9]+", "_", image_name)

    return image_name.strip("_")


def encode_image(image_path):
    """Convert an image into a format that HTML can display."""

    with open(image_path, "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode("utf-8")

    return f"data:image/jpeg;base64,{image_data}"


# --------------------------------------------------
# HOMEMADE AND RESTAURANT PHOTO DISPLAY
# --------------------------------------------------

def show_recipe_images(homemade_path, restaurant_path, ingredients_path):

    images = []

    if homemade_path.exists():
        images.append(encode_image(homemade_path))

    if restaurant_path.exists():
        images.append(encode_image(restaurant_path))

    if ingredients_path.exists():
        images.append(encode_image(ingredients_path))

    if not images:
        st.info("📷 Recipe photos coming soon.")
        return

    if len(images) == 1:
        st.image(images[0], use_container_width=True)
        return

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
            }}

            .photo-container {{
                position: relative;
                width: 100%;
                height: 150px;
                overflow: hidden;
                border-radius: 8px;
                background: #eeeeee;
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

        <div class="photo-container">

            <img
                id="recipe-photo"
                class="recipe-photo"
                src="{images[0]}"
            >

            <button
                class="arrow left-arrow"
                onclick="changePhoto(-1)"
            >
                &#8249;
            </button>

            <button
                class="arrow right-arrow"
                onclick="changePhoto(1)"
            >
                &#8250;
            </button>

        </div>

        <script>

            const imageSources = [{image_sources}];

            let currentPhoto = 0;

            function changePhoto(direction) {{

                currentPhoto = (
                    currentPhoto + direction + imageSources.length
                ) % imageSources.length;

                document.getElementById("recipe-photo").src =
                    imageSources[currentPhoto];

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

    # If only one photo exists, display that photo.

    if homemade_exists and not restaurant_exists:
        st.image(str(homemade_path), use_container_width=True)
        return

    if restaurant_exists and not homemade_exists:
        st.image(str(restaurant_path), use_container_width=True)
        return

    # Convert both photos into displayable image data.

    homemade_image = encode_image(homemade_path)
    restaurant_image = encode_image(restaurant_path)

    # HTML photo viewer with arrows overlaid on the image.

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
            }}

            .recipe-photo {{
                width: 100%;
                height: 150px;
                object-fit: cover;
                display: none;
            }}

            .recipe-photo.active {{
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

        <div class="photo-container">

            <img
                id="homemade"
                class="recipe-photo active"
                src="{homemade_image}"
            >

            <img
                id="restaurant"
                class="recipe-photo"
                src="{restaurant_image}"
            >

            <button
                class="arrow left-arrow"
                onclick="changePhoto(-1)"
            >
                &#8249;
            </button>

            <button
                class="arrow right-arrow"
                onclick="changePhoto(1)"
            >
                &#8250;
            </button>

        </div>

        <script>

            let currentPhoto = 0;

            function changePhoto(direction) {{

                currentPhoto = (currentPhoto + direction + 2) % 2;

                const homemade = document.getElementById("homemade");
                const restaurant = document.getElementById("restaurant");

                if (currentPhoto === 0) {{

                    homemade.classList.add("active");
                    restaurant.classList.remove("active");

                }} else {{

                    restaurant.classList.add("active");
                    homemade.classList.remove("active");

                }}

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

st.subheader("Find a Meal")

search_term = st.text_input(
    "Search by meal name or ingredient",
    placeholder="Example: Chicken, Rice, or Egg"
)

filtered_meals = meals.copy()

if search_term:

    search_term = search_term.lower().strip()

    meal_name_match = (
        filtered_meals["Meal Name"]
        .astype(str)
        .str.lower()
        .str.contains(search_term, na=False)
    )

    ingredient_match = (
        ingredients.groupby("Meal Name")["Ingredients"]
        .apply(
            lambda items: items.astype(str)
            .str.lower()
            .str.contains(search_term, na=False)
            .any()
        )
    )

    matching_meals = ingredient_match[
        ingredient_match
    ].index.astype(str).tolist()

    ingredient_name_match = (
        filtered_meals["Meal Name"]
        .astype(str)
        .isin(matching_meals)
    )

    filtered_meals = filtered_meals[
        meal_name_match | ingredient_name_match
    ]


# --------------------------------------------------
# DISPLAY MEALS
# --------------------------------------------------

st.subheader("Available Meals")

st.write(f"Showing {len(filtered_meals)} meals.")

if filtered_meals.empty:

    st.warning("No meals found. Try another search.")

else:

    meal_rows = filtered_meals.to_dict("records")

    # Display three meal cards per row.

    for row_start in range(0, len(meal_rows), 3):

        columns = st.columns(3)

        for column_index, meal in enumerate(
            meal_rows[row_start:row_start + 3]
        ):

            with columns[column_index]:

                meal_name = show_value(meal.get("Meal Name"))

                with st.container(border=True):

                    # ----------------------------------
                    # RECIPE PHOTOS
                    # ----------------------------------

                    image_name = get_image_name(meal_name)

                    homemade_path = HOMEMADE_DIR / f"{image_name}_hm.jpeg"

                    restaurant_path = RESTAURANT_DIR / f"{image_name}_r.jpeg"

                    ingredients_path = INGREDIENTS_DIR / f"{image_name}_i.jpeg"

                    show_recipe_images(
                        homemade_path,
                        restaurant_path,
                        ingredients_path
                    )

                    # ----------------------------------
                    # MEAL NAME
                    # ----------------------------------

                    st.markdown(f"### {meal_name}")

                    # ----------------------------------
                    # BASIC MEAL INFORMATION
                    # ----------------------------------

                    cost = show_number(
                        meal.get("Ingredient Cost")
                    )

                    total_time = show_number(
                        meal.get("Total Time")
                    )

                    st.write(f"💰 Cost: ${cost}")

                    st.write(f"⏱️ Total Time: {total_time} min")

                    # ----------------------------------
                    # RECIPE DETAILS
                    # ----------------------------------

                    with st.expander("View Recipe Details"):

                        st.markdown("#### Meal Information")

                        st.write(
                            f"Prep Time: {show_number(meal.get('Prep Time'))} min"
                        )

                        st.write(
                            f"Cooking Time: {show_number(meal.get('Cooking Time'))} min"
                        )

                        st.write(
                            f"Servings: {show_value(meal.get('Servings'))}"
                        )

                        st.write(
                            f"Dietary Type: {show_value(meal.get('Dietary Type'))}"
                        )

                        st.write(
                            f"Food Preferences: {show_value(meal.get('Food Preferences'))}"
                        )

                        # ----------------------------------
                        # INGREDIENTS
                        # ----------------------------------

                        st.markdown("#### Ingredients")

                        meal_ingredients = ingredients[
                            ingredients["Meal Name"].astype(str) == str(meal_name)
                        ]

                        if not meal_ingredients.empty:

                            ingredient_display = meal_ingredients[
                                ["Ingredients", "Quantity", "Unit"]
                            ].copy()

                            ingredient_display.columns = [
                                "Ingredient",
                                "Quantity",
                                "Unit"
                            ]

                            st.dataframe(
                                ingredient_display,
                                hide_index=True,
                                use_container_width=True
                            )

                        else:

                            st.write("No ingredient information available.")

                        # ----------------------------------
                        # NUTRITION INFORMATION
                        # ----------------------------------

                        st.markdown("#### Nutrition Information")

                        nutrition_fields = {
                            "Calories": " kcal",
                            "Total Fat": " g",
                            "Cholesterol": " mg",
                            "Sodium": " mg",
                            "Total Carbohydrates": " g",
                            "Dietary Fiber": " g",
                            "Total Sugars": " g",
                            "Protein": " g"
                        }

                        nutrition_columns = st.columns(2)

                        for index, (field, unit) in enumerate(
                            nutrition_fields.items()
                        ):

                            value = meal.get(field)

                            with nutrition_columns[index % 2]:

                                st.write(
                                    f"**{field}:** {show_number(value)}{unit}"
                                )

                        # ----------------------------------
                        # COOKING INSTRUCTIONS
                        # ----------------------------------

                        st.markdown("#### Cooking Instructions")

                        instructions = show_value(
                            meal.get("Cooking Instructions")
                        )

                        st.write(instructions)
