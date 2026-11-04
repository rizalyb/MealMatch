import streamlit as st

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)

home_page = st.Page(
    "pages/1_Home.py",
    title="Home",
    icon="🏠",
    default=True
)

planner_page = st.Page(
    "pages/4_Meal_Planner.py",
    title="Meal Planner",
    icon="🍽️"
)

grocery_page = st.Page(
    "pages/4_Grocery_List.py",
    title="Grocery List",
    icon="🛒"
)

st.session_state["planner_page"] = planner_page
st.session_state["grocery_page"] = grocery_page

navigation = st.navigation([
    home_page,
    planner_page,
    grocery_page
])

navigation.run()
