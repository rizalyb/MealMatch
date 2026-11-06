import streamlit as st
import pandas as pd
import re
from pathlib import Path


# --------------------------------------------------
# IMAGE FOLDERS
# --------------------------------------------------

APP_DIR = Path(__file__).resolve().parent.parent

HOMEMADE_DIR = APP_DIR / "images" / "homemade"
RESTAURANT_DIR = APP_DIR / "images" / "restaurant"
INGREDIENTS_DIR = APP_DIR / "images" / "ingredients"


# --------------------------------------------------
# LOAD SHARED DATA AND PREFERENCES
# --------------------------------------------------

meals = st.session_state["meals"]
ingredients = st.session_state["ingredients"]

budget = st.session_state["budget"]
weekly_budget = st.session_state["weekly_budget"]
use_weekly_budget = st.session_state["use_weekly_budget"]

max_time = st.session_state["max_time"]
desired_servings = st.session_state["desired_servings"]
plan_days = st.session_state["plan_days"]

dietary_restrictions = st.session_state["dietary_restrictions"]
food_preferences = st.session_state["food_preferences"]

max_calories = st.session_state["max_calories"]
min_protein = st.session_state["min_protein"]


# --------------------------------------------------
# PHOTO HOVER CONTROLS
# --------------------------------------------------

st.markdown(
    """
    <style>

    div[class*="st-key-photo_viewer_"] {
        position: relative;
    }

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
        left: 35%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Right arrow */
    div[class*="st-key-photo_next_"] {
        right: 35%;
        top: 50%;
        transform: translateY(-50%);
    }

    /* Expand icon */
    div[class*="st-key-photo_expand_"] {
        right: 35%;
        bottom: 8px;
    }

    /* Button appearance */
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
# PHOTO HELPER FUNCTIONS
# --------------------------------------------------

def get_image_name(meal_name):

    name = str(meal_name).lower().strip()
    name = re.sub(r"[^a-z0-9]+", "_", name)

    return name.strip("_")


def get_meal_photo_paths(meal_name):

    image_name = get_image_name(meal_name)

    possible_photos = [
        (HOMEMADE_DIR, f"{image_name}_hm"),
        (RESTAURANT_DIR, f"{image_name}_r"),
        (INGREDIENTS_DIR, f"{image_name}_i")
    ]

    image_paths = []

    for folder, filename in possible_photos:

        for extension in [".jpeg", ".jpg", ".png"]:

            photo_path = folder / f"{filename}{extension}"

            if photo_path.exists():

                image_paths.append(photo_path)
                break

    return image_paths


# --------------------------------------------------
# ENLARGED RECIPE PHOTO DIALOG
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

    # Display enlarged photo
    st.image(
        image_paths[selected_photo],
        use_container_width=False,
        width=720
    )

    # Identify photo category
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
        f"{photo_label} Photo "
        f"({selected_photo + 1} of {len(image_paths)})"
    )

    # Dialog navigation arrows
    if len(image_paths) > 1:

        previous_col, next_col = st.columns(2)

        with previous_col:

            if st.button(
                "← Previous",
                use_container_width=True,
                key="meal_planner_dialog_previous_photo"
            ):

                st.session_state["large_photo_index"] = (
                    selected_photo - 1
                ) % len(image_paths)

                st.rerun(scope="fragment")

        with next_col:

            if st.button(
                "Next →",
                use_container_width=True,
                key="meal_planner_dialog_next_photo"
            ):

                st.session_state["large_photo_index"] = (
                    selected_photo + 1
                ) % len(image_paths)

                st.rerun(scope="fragment")


# --------------------------------------------------
# RECIPE PHOTO CAROUSEL
# --------------------------------------------------

def show_recipe_images(meal_name, unique_id):

    image_name = get_image_name(meal_name)

    image_paths = get_meal_photo_paths(meal_name)

    if not image_paths:
        st.caption("📷 Recipe photos coming soon.")
        return False

    # Unique photo index for each planned meal
    photo_key = (
        f"meal_planner_photo_index_{unique_id}_{image_name}"
    )

    if photo_key not in st.session_state:
        st.session_state[photo_key] = 0

    # Get the current photo index
    current_index = (
        st.session_state[photo_key] % len(image_paths)
    )

    viewer_key = (
        f"photo_viewer_{unique_id}_{image_name}"
    )

    with st.container(key=viewer_key):

        # Center the photo and reduce its displayed width
        _, image_col, _ = st.columns([1, 2, 1])

        with image_col:
            st.image(
                image_paths[current_index],
                width=800
            )

        # Previous photo arrow
        if len(image_paths) > 1:

            if st.button(
                "‹",
                key=f"photo_prev_{unique_id}_{image_name}"
            ):

                st.session_state[photo_key] = (
                    current_index - 1
                ) % len(image_paths)

                st.rerun()

            # Next photo arrow
            if st.button(
                "›",
                key=f"photo_next_{unique_id}_{image_name}"
            ):

                st.session_state[photo_key] = (
                    current_index + 1
                ) % len(image_paths)

                st.rerun()

        # Expand photo button
        if st.button(
            "⛶",
            key=f"photo_expand_{unique_id}_{image_name}"
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
# PAGE TITLE
# --------------------------------------------------

st.title("🍽️ Meal Planner")

st.write(
    "Find meals that match your budget, cooking time, "
    "food preferences, and nutrition goals."
)

st.divider()


# --------------------------------------------------
# PREPARE MEAL DATA
# --------------------------------------------------

filtered_meals = meals.copy()

filtered_meals["Cost Number"] = pd.to_numeric(
    filtered_meals["Ingredient Cost"]
    .astype(str)
    .str.replace("$", "", regex=False)
    .str.replace(",", "", regex=False),
    errors="coerce"
)

filtered_meals["Time Number"] = pd.to_numeric(
    filtered_meals["Total Time"]
    .astype(str)
    .str.extract(r"(\d+)")[0],
    errors="coerce"
)

filtered_meals["Calories Number"] = pd.to_numeric(
    filtered_meals["Calories"],
    errors="coerce"
)

filtered_meals["Protein Number"] = pd.to_numeric(
    filtered_meals["Protein"]
    .astype(str)
    .str.replace("g", "", regex=False),
    errors="coerce"
)


# --------------------------------------------------
# FILTER BY BUDGET
# --------------------------------------------------

filtered_meals = filtered_meals[
    filtered_meals["Cost Number"] <= budget
]


# --------------------------------------------------
# FILTER BY COOKING TIME
# --------------------------------------------------

if max_time is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Time Number"] <= max_time
    ]


# --------------------------------------------------
# FILTER BY DIETARY RESTRICTIONS
# --------------------------------------------------

if dietary_restrictions != "None":

    filtered_meals = filtered_meals[
        filtered_meals["Dietary Type"]
        .astype(str)
        .str.contains(
            dietary_restrictions,
            case=False,
            na=False
        )
    ]


# --------------------------------------------------
# FILTER BY CALORIES
# --------------------------------------------------

if max_calories is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Calories Number"] <= max_calories
    ]


# --------------------------------------------------
# FILTER BY PROTEIN
# --------------------------------------------------

if min_protein is not None:

    filtered_meals = filtered_meals[
        filtered_meals["Protein Number"] >= min_protein
    ]


# --------------------------------------------------
# FILTER FOODS TO AVOID
# --------------------------------------------------

if food_preferences.strip():

    foods_to_avoid = [
        food.strip().lower()
        for food in food_preferences.split(",")
        if food.strip()
    ]

    def contains_avoided_food(meal_name):

        meal_name = str(meal_name).lower()

        meal_ingredients = ingredients[
            ingredients["Meal Name"]
            .astype(str)
            .str.strip()
            .str.lower()
            == meal_name
        ]

        ingredient_names = " ".join(
            meal_ingredients["Ingredients"]
            .astype(str)
            .str.lower()
        )

        searchable_text = meal_name + " " + ingredient_names

        return any(
            food in searchable_text
            for food in foods_to_avoid
        )

    filtered_meals = filtered_meals[
        ~filtered_meals["Meal Name"].apply(
            contains_avoided_food
        )
    ]


# --------------------------------------------------
# CHECK FOR MATCHING MEALS
# --------------------------------------------------

st.subheader("Your Matching Meals")

st.write(
    f"{len(filtered_meals)} meals match your current preferences."
)

if filtered_meals.empty:

    st.warning(
        "No meals match your current preferences. "
        "Try increasing your budget or adjusting your filters."
    )

    st.stop()


# --------------------------------------------------
# DETERMINE ORIGINAL SERVINGS
# --------------------------------------------------

def get_original_servings(value):

    numbers = re.findall(r"\d+", str(value))

    return max(map(int, numbers)) if numbers else 1


filtered_meals["Original Servings"] = (
    filtered_meals["Servings"].apply(get_original_servings)
)

filtered_meals["Original Servings"] = (
    filtered_meals["Original Servings"].fillna(1)
)


# --------------------------------------------------
# GENERATE MEAL PLAN
# --------------------------------------------------

current_preferences = (
    budget,
    weekly_budget,
    use_weekly_budget,
    max_time,
    desired_servings,
    plan_days,
    dietary_restrictions,
    food_preferences.strip().lower(),
    max_calories,
    min_protein
)

if (
    "meal_plan" not in st.session_state
    or "meal_plan_preferences" not in st.session_state
    or st.session_state.meal_plan_preferences != current_preferences
    or len(st.session_state.meal_plan) != plan_days
):

    st.session_state.meal_plan = (
        filtered_meals.sample(
            n=plan_days,
            replace=len(filtered_meals) < plan_days
        )
        .reset_index(drop=True)
    )

    st.session_state.meal_plan_preferences = current_preferences


meal_plan = st.session_state.meal_plan.copy()


# --------------------------------------------------
# CALCULATE SERVING ADJUSTMENTS
# --------------------------------------------------

meal_plan["Original Servings"] = (
    meal_plan["Servings"].apply(get_original_servings)
)

meal_plan["Scaling Factor"] = (
    desired_servings / meal_plan["Original Servings"]
)

meal_plan["Adjusted Cost"] = (
    meal_plan["Cost Number"] * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Calories"] = (
    meal_plan["Calories Number"] * meal_plan["Scaling Factor"]
)

meal_plan["Adjusted Protein"] = (
    meal_plan["Protein Number"] * meal_plan["Scaling Factor"]
)


# --------------------------------------------------
# DISPLAY WEEKLY MEAL PLAN
# --------------------------------------------------

st.divider()

st.subheader("📅 Your Meal Plan")

st.caption(
    f"Planning {plan_days} day(s) with {desired_servings} "
    "serving(s) per meal."
)

open_large_photo = False

for index, meal in meal_plan.iterrows():

    st.subheader(f"Day {index + 1}: {meal['Meal Name']}")

    # DISPLAY MEAL PHOTO CAROUSEL

    if show_recipe_images(meal["Meal Name"], index):
        open_large_photo = True

    with st.expander("View Meal Details", expanded=True):

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Estimated Cost",
                f"${meal['Adjusted Cost']:.2f}"
            )

        with col2:

            st.metric(
                "Cooking Time",
                f"{meal['Time Number']:.0f} min"
            )

        with col3:

            st.metric(
                "Servings",
                desired_servings
            )

        col4, col5 = st.columns(2)

        with col4:

            st.metric(
                "Calories",
                f"{meal['Adjusted Calories']:.0f}"
            )

        with col5:

            st.metric(
                "Protein",
                f"{meal['Adjusted Protein']:.1f} g"
            )

        st.write("Dietary Type:", meal["Dietary Type"])

        st.write("Cooking Instructions:")

        st.write(meal["Cooking Instructions"])


        # ALTERNATIVE MEALS

        show_alternatives = st.checkbox(
            "Show more meal options",
            key=f"show_alternatives_{index}"
        )

        if show_alternatives:

            other_meals = filtered_meals[
                ~filtered_meals["Meal Name"].isin(
                    meal_plan["Meal Name"]
                )
            ]

            if other_meals.empty:

                st.info(
                    "No additional matching meals are available."
                )

            else:

                alternative_names = (
                    other_meals["Meal Name"].tolist()
                )

                selected_alternative = st.selectbox(
                    "Choose an alternative meal:",
                    alternative_names,
                    key=f"alternative_{index}"
                )

                if st.button(
                    "Use This Meal",
                    key=f"use_alternative_{index}"
                ):

                    new_meal = other_meals[
                        other_meals["Meal Name"]
                        == selected_alternative
                    ].iloc[0]

                    st.session_state.meal_plan.loc[
                        index
                    ] = new_meal

                    st.rerun()


# --------------------------------------------------
# OPEN ENLARGED PHOTO DIALOG
# --------------------------------------------------

if open_large_photo:
    show_large_photo()


# --------------------------------------------------
# MEAL PLAN SUMMARY
# --------------------------------------------------

st.divider()

st.subheader("💰 Meal Plan Summary")

total_cost = meal_plan["Adjusted Cost"].sum()

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Total Estimated Cost",
        f"${total_cost:.2f}"
    )

with col2:

    st.metric(
        "Planned Meals",
        plan_days
    )


if use_weekly_budget:

    if total_cost <= weekly_budget:

        st.success(
            f"Your meal plan is within your "
            f"${weekly_budget:.2f} weekly budget."
        )

    else:

        st.warning(
            f"Your meal plan exceeds your weekly budget "
            f"by ${total_cost - weekly_budget:.2f}."
        )


st.caption(
    "Estimated costs reflect the ingredients used "
    "for your selected serving sizes."
)
