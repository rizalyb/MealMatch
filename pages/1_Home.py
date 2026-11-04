import streamlit as st

# PAGE TITLE

st.title("🥗 Welcome to MealMatch")

st.caption("Plan. Cook. Enjoy.")

# WELCOME BANNER

with st.container(border=True):

    st.markdown(
        "🥗 YOUR MEAL PLANNING COMPANION"
    )

    st.title("Welcome to MealMatch!")

    st.subheader(
        "Plan meals around your budget, schedule, and taste."
    )

    st.write(
        "Find affordable recipes, organize your weekly meals, "
        "and create a grocery list based on your needs. "
        "Everything you need for easier meal planning in one place."
    )

    st.success(
        "PLAN SMARTER. EAT BETTER. SPEND WISELY."
    )


# QUICK INFORMATION

st.info(
    "💡 Start by adjusting your budget, cooking time, "
    "food preferences, and nutrition goals in the sidebar."
)


# MAIN NAVIGATION

st.header("Explore MealMatch")

st.write(
    "Choose where you would like to start."
)

col1, col2, col3 = st.columns(3, gap="medium")


# MEAL PLANNER CARD

with col1:

    with st.container(border=True):

        st.markdown("## 🍽️")

        st.subheader("Meal Planner")

        st.write(
            "Find recipes that fit your budget, "
            "schedule, and preferences."
        )

        st.page_link(
            st.session_state["planner_page"],
            label="Start Planning",
            icon="📅",
            use_container_width=True
        )


# EXPLORE MEALS CARD

with col2:

    with st.container(border=True):

        st.markdown("## 📖")

        st.subheader("Explore Meals")

        st.write(
            "Browse recipes, ingredients, nutrition, "
            "and cooking instructions."
        )

        st.page_link(
            st.session_state["explore_page"],
            label="Browse Recipes",
            icon="🔎",
            use_container_width=True
        )


# GROCERY LIST CARD

with col3:

    with st.container(border=True):

        st.markdown("## 🛒")

        st.subheader("Grocery List")

        st.write(
            "Organize ingredients, quantities, "
            "and estimated grocery costs."
        )

        st.page_link(
            st.session_state["grocery_page"],
            label="View Grocery List",
            icon="🛍️",
            use_container_width=True
        )


st.divider()


# HOW MEALMATCH WORKS

st.header("How MealMatch Works")

st.write(
    "Three simple steps to organize your meals."
)

step1, step2, step3 = st.columns(3, gap="medium")


with step1:

    with st.container(border=True):

        st.markdown("## ⚙️")

        st.subheader("1. Set Your Preferences")

        st.write(
            "Choose your budget, cooking time, "
            "servings, and dietary needs."
        )


with step2:

    with st.container(border=True):

        st.markdown("## 🥗")

        st.subheader("2. Plan Your Meals")

        st.write(
            "Explore recipes and select meals "
            "that match your preferences."
        )


with step3:

    with st.container(border=True):

        st.markdown("## 🛒")

        st.subheader("3. Get Your Grocery List")

        st.write(
            "Review combined ingredients, "
            "quantities, and estimated costs."
        )


# FOOTER

st.divider()

with st.container():

    st.markdown(
        "### Good food. Smart planning. Better choices."
    )

    st.caption(
        "MealMatch | Plan. Cook. Enjoy."
    )
