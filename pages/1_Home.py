import streamlit as st

st.title("🥗 Welcome to MealMatch")

st.subheader(
    "Plan meals around your budget, schedule, and taste."
)

st.write(
    """
    MealMatch helps you find affordable recipes based on your
    budget, cooking time, food preferences, and nutrition goals.

    Plan your meals, explore recipes, and organize your
    grocery list in one place.
    """
)

st.divider()

st.info(
    "Before exploring meals, adjust your budget, cooking time, "
    "and food preferences in the sidebar."
)

st.header("Explore MealMatch")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍽️ Meal Planner")

    st.write(
        "Find recipes that match your preferences, "
        "explore alternatives, and organize your weekly meals."
    )

    st.page_link(
        "pages/4_Meal_Planner.py",
        label="Open Meal Planner",
        icon="🍽️",
        use_container_width=True
    )

with col2:
    st.subheader("🛒 Grocery List")

    st.write(
        "View your combined ingredients and the quantities "
        "needed for your selected meals."
    )

    st.page_link(
        "pages/4_Grocery_List.py",
        label="Open Grocery List",
        icon="🛒",
        use_container_width=True
    )

st.divider()

st.header("Explore All Meal Options")

st.write(
    "Want to browse recipes without filtering by your current "
    "preferences? Explore the full MealMatch recipe collection."
)

st.page_link(
    "pages/4_Meal_Planner.py",
    label="Explore All Meals",
    icon="📖",
    use_container_width=True
)
