
import streamlit as st

# --------------------------------------------------
# PAGE STYLING
# --------------------------------------------------

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #e5efe5,
            #f4f1e7
        );
        padding: 3rem 2.5rem;
        border-radius: 22px;
        margin-bottom: 2rem;
        border: 1px solid #dce7da;
    }

    .hero-tag {
        color: #55765b;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #294b35;
        font-size: 2.7rem;
        font-weight: 750;
        line-height: 1.15;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #526557;
        font-size: 1.05rem;
        max-width: 650px;
        line-height: 1.7;
    }

    .section-label {
        color: #64816a;
        font-size: 0.8rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 5px;
    }

    .feature-icon {
        font-size: 2.2rem;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #68766b;
        font-size: 0.92rem;
        line-height: 1.6;
        min-height: 75px;
    }

    .step-number {
        color: #6b8c70;
        font-size: 0.85rem;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .footer {
        text-align: center;
        color: #849187;
        font-size: 0.85rem;
        padding-top: 1rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# WELCOME BANNER
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">YOUR MEAL PLANNING COMPANION</div>
        <div class="hero-title">
            Good food starts<br>with a good plan.
        </div>
        <div class="hero-description">
            Welcome to MealMatch! Find affordable recipes,
            plan meals around your preferences, and make
            grocery shopping easier.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# MAIN NAVIGATION
# --------------------------------------------------

st.markdown(
    '<div class="section-label">GET STARTED</div>',
    unsafe_allow_html=True
)

st.header("What would you like to do?")

st.write(
    "Choose a feature below to get started."
)

col1, col2, col3 = st.columns(3, gap="medium")


# MEAL PLANNER

with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="feature-icon">🍽️</div>',
            unsafe_allow_html=True
        )

        st.subheader("Meal Planner")

        st.markdown(
            """
            <div class="feature-description">
                Build a meal plan that fits your budget,
                schedule, servings, and dietary needs.
            </div>
            """,
            unsafe_allow_html=True
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

        st.markdown(
            '<div class="feature-icon">🥗</div>',
            unsafe_allow_html=True
        )

        st.subheader("Explore Meals")

        st.markdown(
            """
            <div class="feature-description">
                Browse recipes, compare costs,
                and explore ingredients and nutrition.
            </div>
            """,
            unsafe_allow_html=True
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

        st.markdown(
            '<div class="feature-icon">🛒</div>',
            unsafe_allow_html=True
        )

        st.subheader("Grocery List")

        st.markdown(
            """
            <div class="feature-description">
                Keep track of ingredients, quantities,
                and estimated grocery costs.
            </div>
            """,
            unsafe_allow_html=True
        )

        st.page_link(
            st.session_state["grocery_page"],
            label="View Grocery List",
            icon="🛍️",
            use_container_width=True
        )


# --------------------------------------------------
# HOW IT WORKS
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">SIMPLE MEAL PLANNING</div>',
    unsafe_allow_html=True
)

st.header("How MealMatch Works")

st.write(
    "Three simple steps to make meal planning easier."
)

step1, step2, step3 = st.columns(3, gap="medium")


with step1:

    with st.container(border=True):

        st.markdown(
            '<div class="step-number">STEP 01</div>',
            unsafe_allow_html=True
        )

        st.markdown("### ⚙️ Set Your Preferences")

       st.write(
            "Choose your budget, cooking time, "
            "servings, and food preferences."
        )

with step2:

    with st.container(border=True):

        st.markdown(
            '<div class="step-number">STEP 02</div>',
            unsafe_allow_html=True
        )

        st.markdown("### 🍽️ Plan Your Meals")

        st.write(
            "Generate a meal plan or browse recipes "
            "that fit your preferences."
        )

with step3:

    with st.container(border=True):

        st.markdown(
            '<div class="step-number">STEP 03</div>',
            unsafe_allow_html=True
        )

        st.markdown("### 🛒 Get Your Groceries")

        st.write(
            "Review your grocery list and "
            "keep track of your shopping."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown(
    """
    <div class="footer">
        MealMatch · Plan. Cook. Enjoy.
    </div>
    """,
    unsafe_allow_html=True
)
