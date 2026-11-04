st.title("🥗 Welcome to MealMatch")

st.subheader(
    "Meals that match your budget, schedule, and taste."
)

st.write(
    """
    MealMatch helps you find affordable meals based on your
    budget, cooking time, food preferences, and nutrition goals.

    Plan your meals, explore recipes, and organize your
    grocery list in one place.
    """
)

st.divider()

st.header("What would you like to do?")

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚙️ Meal Preferences")
    st.write(
        "Set your budget, cooking time, servings, "
        "dietary restrictions, and nutrition goals."
    )

with col2:
    st.subheader("🍽️ Meal Planner")
    st.write(
        "Explore matching recipes, choose alternatives, "
        "and organize your weekly meal plan."
    )

st.divider()

st.subheader("🛒 Grocery List")

st.write(
    "View your combined ingredient list and the quantities "
    "needed for your selected meals."
)

st.info(
    "Start by setting your preferences in the Meal Preferences page."
)
