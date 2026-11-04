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

st.header("Explore MealMatch")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🍽️ Meal Planner")
    st.write(
        "Find recipes that match your preferences, "
        "explore alternatives, and organize your weekly meals."
    )

    if st.button("Open Meal Planner", use_container_width=True):
        st.switch_page("pages/4_Meal_Planner.py")

with col2:
    st.subheader("🛒 Grocery List")
    st.write(
        "View your combined ingredients and the quantities "
        "needed for your selected meals."
    )

    if st.button("Open Grocery List", use_container_width=True):
        st.switch_page("pages/4_Grocery_List.py")

st.divider()

st.info(
    "Start by adjusting your meal preferences in the sidebar. "
    "Then visit Meal Planner to find meals that match your needs."
)
