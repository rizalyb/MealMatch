
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
        background: linear-gradient(135deg, #e8f0e5, #f5f1e8);
        padding: 45px 35px;
        border-radius: 18px;
        margin-bottom: 25px;
        border: 1px solid #d9e4d5;
    }

    .hero-tag {
        color: #55745a;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }

    .hero-title {
        color: #294b35;
        font-size: 42px;
        font-weight: 750;
        margin-bottom: 12px;
    }

    .hero-description {
        color: #526456;
        font-size: 17px;
        line-height: 1.7;
        max-width: 700px;
    }

    .section-label {
        color: #65816a;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }

    .feature-icon {
        font-size: 34px;
        margin-bottom: 8px;
    }

    .feature-description {
        color: #647067;
        font-size: 14px;
        line-height: 1.6;
        min-height: 65px;
    }

    .step-number {
        color: #66836a;
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .footer {
        text-align: center;
        color: #718075;
        padding: 20px 0 5px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# WELCOME SECTION
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <div class="hero-tag">🥗 YOUR MEAL PLANNING COMPANION</div>
        <div class="hero-title">Good food starts with a good plan.</div>
        <div class="hero-description">
            Welcome to MealMatch! Plan affordable meals,
            find recipes that fit your preferences, and
            organize your groceries all in one place.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# QUICK TIP
# --------------------------------------------------

st.info(
    "💡 Start by setting your budget, cooking time, "
    "servings, and food preferences in the sidebar."
)


# --------------------------------------------------
# MAIN FEATURES
# --------------------------------------------------

st.markdown(
    '<div class="section-label">GET STARTED</div>',
    unsafe_allow_html=True
)

st.header("Explore MealMatch")

st.write("Choose a feature to get started.")

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
            '<div class="feature-description">'
            'Create meal plans based on your budget, '
            'schedule, servings, and food preferences.'
            '</div>',
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
            '<div class="feature-icon">📖</div>',
            unsafe_allow_html=True
        )

        st.subheader("Explore Meals")

        st.markdown(
            '<div class="feature-description">'
            'Browse recipes and view their ingredients, '
            'nutrition information, and cooking instructions.'
            '</div>',
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
            '<div class="feature-description">'
            'Keep track of your ingredients, quantities, '
            'estimated costs, and shopping progress.'
            '</div>',
            unsafe_allow_html=True
        )

        st.page_link(
            st.session_state["grocery_page"],
            label="View Grocery List",
            icon="🛍️",
            use_container_width=True
        )


# --------------------------------------------------
# HOW MEALMATCH WORKS
# --------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-label">HOW IT WORKS</div>',
    unsafe_allow_html=True
)

st.header("Meal planning in three simple steps")

st.write(
    "MealMatch helps you organize your meals from "
    "choosing your preferences to preparing your grocery list."
)

step1, step2, step3 = st.columns(3, gap="medium")


with step1:
    with st.container(border=True):
        st.markdown(
            '<div class="step-number">STEP 01</div>',
            unsafe_allow_html=True
        )

        st.markdown("## ⚙️")

        st.subheader("Set Your Preferences")

        st.write(
            "Choose your budget, cooking time, "
            "servings, and dietary needs."
        )


with step2:
    with st.container(border=True):
        st.markdown(
            '<div class="step-number">STEP 02</div>',
            unsafe_allow_html=True
        )

        st.markdown("## 🥗")

        st.subheader("Plan Your Meals")

        st.write(
            "Generate a meal plan or browse recipes "
            "that match your preferences."
        )


with step3:
    with st.container(border=True):
        st.markdown(
            '<div class="step-number">STEP 03</div>',
            unsafe_allow_html=True
        )

        st.markdown("## 🛒")

        st.subheader("Organize Your Groceries")

        st.write(
            "Review your grocery list, check off "
            "ingredients, and track your shopping."
        )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.markdown(
    """
    <div class="footer">
        <strong>Good food. Smart planning. Better choices.</strong>
        <br>
        <small>MealMatch | Plan. Cook. Enjoy.</small>
    </div>
    """,
    unsafe_allow_html=True
)
