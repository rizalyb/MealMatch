
import streamlit as st
import pandas as pd
from pathlib import Path

# PAGE CONFIGURATION

st.set_page_config(
    page_title="MealMatch",
    page_icon="🥗",
    layout="wide"
)

APP_DIR = Path(__file__).parent



# GLOBAL MEALMATCH DESIGN

st.markdown(
    """
    <style>

    /* LIGHT MODE */

    :root {
        --mm-green: #426548;
        --mm-dark-green: #294B35;
        --mm-light-green: #E8EEDF;
        --mm-cream: #F8F7F0;
        --mm-border: #D5DEC9;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #F8F7F0;
        color: #294B35;
    }

    [data-testid="stSidebar"] {
        background-color: #E8EEDF;
        color: #294B35;
    }

    [data-testid="stAppViewContainer"] h1,
    [data-testid="stAppViewContainer"] h2,
    [data-testid="stAppViewContainer"] h3 {
        color: #294B35;
    }

    [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #F4F5ED;
        border: 1px solid #D5DEC9;
        border-radius: 12px;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1250px;
    }

    [data-testid="stSlider"] [data-testid="stThumbValue"] {
        opacity: 1 !important;
        visibility: visible !important;
        font-weight: 700 !important;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #D5DEC9;
        border-radius: 14px;
    }

    .stButton button,
    .stLinkButton a {
        background-color: #426548;
        color: white !important;
        border: none;
        border-radius: 10px;
    }

    .stButton button:hover,
    .stLinkButton a:hover {
        background-color: #294B35;
        color: white !important;
    }

    hr {
        border-color: #D5DEC9;
    }


    /* DARK MODE */

    [data-theme="dark"] [data-testid="stAppViewContainer"],
    [data-theme="dark"] .stApp {
        background-color: #17251D !important;
        color: #E8EFE6 !important;
    }

    [data-theme="dark"] [data-testid="stMain"],
    [data-theme="dark"] [data-testid="stMainBlockContainer"] {
        background-color: #17251D !important;
        color: #E8EFE6 !important;
    }

    /* MAIN TEXT */

    [data-theme="dark"] [data-testid="stAppViewContainer"] h1,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h2,
    [data-theme="dark"] [data-testid="stAppViewContainer"] h3,
    [data-theme="dark"] [data-testid="stAppViewContainer"] p,
    [data-theme="dark"] [data-testid="stAppViewContainer"] li,
    [data-theme="dark"] [data-testid="stAppViewContainer"] label,
    [data-theme="dark"] [data-testid="stAppViewContainer"] strong,
    [data-theme="dark"] [data-testid="stAppViewContainer"] [data-testid="stMarkdownContainer"],
    [data-theme="dark"] [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] {
        color: #E8EFE6 !important;
    }

    /* SIDEBAR */

    [data-theme="dark"] [data-testid="stSidebar"] {
        background-color: #24372B !important;
        color: #E8EFE6 !important;
    }

    [data-theme="dark"] [data-testid="stSidebar"] h1,
    [data-theme="dark"] [data-testid="stSidebar"] h2,
    [data-theme="dark"] [data-testid="stSidebar"] h3,
    [data-theme="dark"] [data-testid="stSidebar"] p,
    [data-theme="dark"] [data-testid="stSidebar"] label,
    [data-theme="dark"] [data-testid="stSidebar"] span,
    [data-theme="dark"] [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #E8EFE6 !important;
    }

    /* EXPANDERS AND CARDS */

    [data-theme="dark"] [data-testid="stExpander"],
    [data-theme="dark"] [data-testid="stSidebar"] [data-testid="stExpander"] {
        background-color: #304638 !important;
        border: 1px solid #506653 !important;
        border-radius: 12px;
    }

    [data-theme="dark"] [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #223329 !important;
        border-color: #506653 !important;
    }

    /* INPUT FIELDS */

    [data-theme="dark"] input,
    [data-theme="dark"] textarea,
    [data-theme="dark"] [data-baseweb="select"] > div {
        background-color: #304638 !important;
        color: #F0F4ED !important;
        border-color: #607764 !important;
    }

    [data-theme="dark"] input::placeholder,
    [data-theme="dark"] textarea::placeholder {
        color: #C0CEBE !important;
    }

    /* CHECKBOXES, RADIO BUTTONS, AND SLIDERS */

    [data-theme="dark"] [data-testid="stCheckbox"],
    [data-theme="dark"] [data-testid="stRadio"],
    [data-theme="dark"] [data-testid="stSlider"],
    [data-theme="dark"] [data-testid="stSelectbox"],
    [data-theme="dark"] [data-testid="stNumberInput"] {
        color: #E8EFE6 !important;
    }

    [data-theme="dark"] [data-testid="stSlider"] [data-testid="stThumbValue"] {
        color: #F0F4ED !important;
        opacity: 1 !important;
        visibility: visible !important;
    }

    /* ALERTS AND NOTICES */

    [data-theme="dark"] [data-testid="stAlert"] {
        background-color: #304638 !important;
        color: #F0F4ED !important;
    }

    [data-theme="dark"] [data-testid="stAlert"] p,
    [data-theme="dark"] [data-testid="stAlert"] span {
        color: #F0F4ED !important;
    }

    /* BUTTONS */

    [data-theme="dark"] .stButton button,
    [data-theme="dark"] .stLinkButton a {
        background-color: #58765B !important;
        color: #FFFFFF !important;
        border: 1px solid #789278 !important;
    }

    [data-theme="dark"] .stButton button:hover,
    [data-theme="dark"] .stLinkButton a:hover {
        background-color: #6B896D !important;
    }

    /* DIVIDERS AND HEADER */

    [data-theme="dark"] hr {
        border-color: #506653 !important;
    }

    [data-testid="stHeader"] {
        background-color: transparent !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# LOAD CSV DATA

@st.cache_data
def load_meal_data():

    meals = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Meals).csv",
        encoding="cp1252"
    )

    ingredients = pd.read_csv(
        APP_DIR / "Rizaly Barlam - MealMatch CSV(Ingredients).csv",
        encoding="cp1252"
    )

    return meals, ingredients


meals, ingredients = load_meal_data()

st.session_state["meals"] = meals
st.session_state["ingredients"] = ingredients


# SIDEBAR PREFERENCES

st.sidebar.title("🥗 MealMatch")

st.sidebar.caption(
    "Customize your meal recommendations."
)

st.sidebar.divider()


# BUDGET

with st.sidebar.expander("💰 Budget", expanded=True):

    budget = st.slider(
        "Budget per meal ($)",
        1,
        30,
        10,
        key="budget"
    )

    use_weekly_budget = st.checkbox(
        "Set a weekly budget",
        value=False,
        key="use_weekly_budget"
    )

    if use_weekly_budget:

        weekly_budget = st.slider(
            "Weekly budget ($)",
            10,
            200,
            30,
            step=5,
            key="weekly_budget"
        )

    else:
        weekly_budget = 30
        st.session_state["weekly_budget"] = weekly_budget

st.session_state["weekly_budget"] = weekly_budget


# COOKING AND PLANNING

with st.sidebar.expander("⏱️ Cooking & Planning", expanded=True):

    use_time_limit = st.checkbox(
        "Set maximum cooking time",
        value=True,
        key="use_time_limit"
    )

    if use_time_limit:

        max_time = st.slider(
            "Maximum cooking time (minutes)",
            5,
            120,
            30,
            step=5,
            key="max_time"
        )

    else:
        max_time = None
        st.session_state["max_time"] = None

    desired_servings = st.selectbox(
        "Number of servings",
        [1, 2, 3, 4, 5, 6],
        key="desired_servings"
    )

    plan_days = st.selectbox(
        "Number of days to plan",
        [1, 3, 5, 7],
        key="plan_days"
    )


# FOOD PREFERENCES

with st.sidebar.expander("🥦 Food Preferences", expanded=False):

    dietary_restrictions = st.selectbox(
        "Dietary restrictions",
        [
            "None",
            "Vegetarian",
            "Vegan",
            "Gluten-free",
            "Dairy-free"
        ],
        key="dietary_restrictions"
    )

    food_preferences = st.text_input(
        "Foods to avoid",
        placeholder="Example: seafood, mushrooms",
        key="food_preferences"
    )


# NUTRITION GOALS

with st.sidebar.expander("❤️ Nutrition Goals", expanded=False):

    use_calorie_limit = st.checkbox(
        "Set maximum calories",
        value=False,
        key="use_calorie_limit"
    )

    if use_calorie_limit:

        max_calories = st.number_input(
            "Maximum calories per serving",
            50,
            2000,
            500,
            step=50,
            key="max_calories"
        )

    else:
        max_calories = None
        st.session_state["max_calories"] = None

    use_protein_goal = st.checkbox(
        "Set minimum protein goal",
        value=False,
        key="use_protein_goal"
    )

    if use_protein_goal:

        min_protein = st.number_input(
            "Minimum protein (g)",
            1,
            150,
            20,
            step=5,
            key="min_protein"
        )

    else:
        min_protein = None
        st.session_state["min_protein"] = None


# PAGE NAVIGATION

home_page = st.Page(
    "pages/1_Home.py",
    title="Home",
    icon="🏠",
    default=True
)

planner_page = st.Page(
    "pages/2_Meal_Planner.py",
    title="Meal Planner",
    icon="🍽️"
)

grocery_page = st.Page(
    "pages/3_Grocery_List.py",
    title="Grocery List",
    icon="🛒"
)

explore_page = st.Page(
    "pages/4_Explore_Meals.py",
    title="Explore Meals",
    icon="📖"
)

st.session_state["planner_page"] = planner_page
st.session_state["grocery_page"] = grocery_page
st.session_state["explore_page"] = explore_page

navigation = st.navigation([
    home_page,
    planner_page,
    grocery_page,
    explore_page
])

navigation.run()
