import streamlit as st

# PAGE TITLE

st.title("🥗 Welcome to MealMatch")

st.caption(
    "Plan. Cook. Enjoy."
)

st.write(
    "Plan affordable meals, explore recipes, "
    "and organize your grocery list in one place."
)

st.divider()


# MAIN NAVIGATION

st.header("Get Started")

st.write(
    "Choose what you would like to do."
)

col1, col2, col3 = st.columns(3, gap="medium")


# MEAL PLANNER

with col1:

    with st.container(border=True):

        st.markdown("## 🍽️")

        st.subheader("Meal Planner")

        st.write(
            "Create a meal plan based on your "
            "budget, schedule, and food preferences."
        )

        st.page_link(
            st.session_state["planner_page"],
            label="Start Planning",
            icon="📅",
            use_container_width=True
        )


# EXPLORE MEALS

with col2:

    with st.container(border=True):

        st.markdown("## 📖")

        st.subheader("Explore Meals")

        st.write(
            "Search recipes, compare costs, "
            "and view ingredients and instructions."
        )

        st.page_link(
            st.session_state["explore_page"],
            label="Browse Recipes",
            icon="🔎",
            use_container_width=True
        )


# GROCERY LIST

with col3:

    with st.container(border=True):

        st.markdown("## 🛒")

        st.subheader("Grocery List")

        st.write(
            "Review ingredients, quantities, "
            "and estimated shopping costs."
        )

        st.page_link(
            st.session_state["grocery_page"],
            label="View Grocery List",
            icon="🛍️",
            use_container_width=True
        )


st.divider()


# HOW IT WORKS

st.header("How MealMatch Works")

st.write(
    "Follow these three steps to organize your meals."
)

step1, step2, step3 = st.columns(3, gap="medium")


with step1:

    with st.container(border=True):

        st.markdown("## 1️⃣")

        st.subheader("Set Your Preferences")

        st.write(
            "Adjust your budget, cooking time, "
            "servings, dietary needs, and nutrition goals "
            "using the sidebar."
        )


with step2:

    with st.container(border=True):

        st.markdown("## 2️⃣")

        st.subheader("Plan Your Meals")

        st.write(
            "Generate a meal plan or browse recipes "
            "that match your preferences."
        )


with step3:

    with st.container(border=True):

        st.markdown("## 3️⃣")

        st.subheader("Prepare Your Groceries")

        st.write(
            "Use your grocery list to organize "
            "ingredients and track your shopping."
        )


# FOOTER

st.divider()

st.caption(
    "MealMatch | Plan. Cook. Enjoy."
)
