import streamlit as st

# PAGE TITLE

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)

# CUSTOM DESIGN

st.markdown(
    """
    <style>

    /* MAIN BACKGROUND */

    .stApp {
        background-color: #F8F7F0;
    }

    /* MAIN CONTENT */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    /* HEADINGS */

    h1, h2, h3 {
        color: #294B35 !important;
    }

    /* NORMAL TEXT */

    p {
        color: #39483B;
    }

    /* SIDEBAR */

    [data-testid="stSidebar"] {
        background-color: #E8EEDF;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 {
        color: #294B35;
    }

    /* BUTTONS */

    .stButton button,
    .stLinkButton a {
        background-color: #426548;
        color: white;
        border-radius: 12px;
        border: none;
    }

    .stButton button:hover,
    .stLinkButton a:hover {
        background-color: #294B35;
        color: white;
    }

    /* DIVIDERS */

    hr {
        border-color: #D5DEC9;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# WELCOME BANNER

st.markdown(
    """
    <div style="
        background: linear-gradient(110deg, #E5EEDC, #F4EBDD);
        padding: 45px 40px;
        border-radius: 22px;
        border: 1px solid #D9E2D0;
        margin-bottom: 25px;
    ">

        <div style="
            color: #64845D;
            font-size: 17px;
            font-weight: 600;
        ">
            🥗 YOUR MEAL PLANNING COMPANION
        </div>

        <h1 style="
            color: #294B35;
            font-size: 43px;
            margin-top: 12px;
            margin-bottom: 10px;
        ">
            Welcome to MealMatch!
        </h1>

        <h3 style="
            color: #526D50;
            font-size: 22px;
            font-weight: 500;
        ">
            Plan meals around your budget, schedule, and taste.
        </h3>

        <p style="
            color: #455344;
            font-size: 17px;
            max-width: 650px;
            line-height: 1.6;
        ">
            Find affordable recipes, organize your weekly meals,
            and create a grocery list based on your needs.
            Everything you need for easier meal planning in one place.
        </p>

        <div style="
            color: #426548;
            font-size: 15px;
            font-weight: 600;
            margin-top: 20px;
        ">
            PLAN SMARTER. EAT BETTER. SPEND WISELY.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# QUICK INFORMATION

st.info(
    "💡 Start by adjusting your budget, cooking time, "
    "food preferences, and nutrition goals in the sidebar."
)


# MAIN NAVIGATION

st.markdown(
    """
    <h2 style="margin-bottom: 5px;">
        Explore MealMatch
    </h2>

    <p style="color: #657461;">
        Choose where you would like to start.
    </p>
    """,
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3, gap="medium")


# MEAL PLANNER CARD

with col1:

    with st.container(border=True):

        st.markdown(
            """
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 42px;">🍽️</div>
                <h3>Meal Planner</h3>
                <p>
                    Find recipes that fit your budget,
                    schedule, and preferences.
                </p>
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


# EXPLORE MEALS CARD

with col2:

    with st.container(border=True):

        st.markdown(
            """
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 42px;">📖</div>
                <h3>Explore Meals</h3>
                <p>
                    Browse recipes, ingredients,
                    nutrition, and cooking instructions.
                </p>
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


# GROCERY LIST CARD

with col3:

    with st.container(border=True):

        st.markdown(
            """
            <div style="text-align: center; padding: 10px;">
                <div style="font-size: 42px;">🛒</div>
                <h3>Grocery List</h3>
                <p>
                    Organize ingredients, quantities,
                    and estimated grocery costs.
                </p>
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


st.divider()


# HOW MEALMATCH WORKS

st.markdown(
    """
    <h2 style="text-align: center;">
        How MealMatch Works
    </h2>

    <p style="
        text-align: center;
        color: #657461;
        margin-bottom: 25px;
    ">
        Three simple steps to organize your meals.
    </p>
    """,
    unsafe_allow_html=True
)

step1, step2, step3 = st.columns(3)

with step1:

    st.markdown(
        """
        <div style="
            background-color: #E8EEDF;
            padding: 22px;
            border-radius: 15px;
            text-align: center;
            min-height: 155px;
        ">
            <div style="font-size: 35px;">⚙️</div>
            <h3>1. Set Your Preferences</h3>
            <p>Choose your budget, cooking time,
            servings, and dietary needs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with step2:

    st.markdown(
        """
        <div style="
            background-color: #F3EBDD;
            padding: 22px;
            border-radius: 15px;
            text-align: center;
            min-height: 155px;
        ">
            <div style="font-size: 35px;">🥗</div>
            <h3>2. Plan Your Meals</h3>
            <p>Explore recipes and select meals
            that match your preferences.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with step3:

    st.markdown(
        """
        <div style="
            background-color: #E8EEDF;
            padding: 22px;
            border-radius: 15px;
            text-align: center;
            min-height: 155px;
        ">
            <div style="font-size: 35px;">🛒</div>
            <h3>3. Get Your Grocery List</h3>
            <p>Review combined ingredients,
            quantities, and estimated costs.</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# FOOTER

st.divider()

st.markdown(
    """
    <div style="
        text-align: center;
        padding: 15px;
        color: #526D50;
    ">
        <h3 style="font-style: italic;">
            Good food. Smart planning. Better choices.
        </h3>

        <p style="font-size: 13px;">
            MealMatch | Plan. Cook. Enjoy.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
