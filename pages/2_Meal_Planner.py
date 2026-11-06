        with col3:
            st.metric(
                "Servings",
                desired_servings
            )

        col4, col5 = st.columns(2)

        with col4:
            st.metric(
                "Calories",
                f"{meal['Adjusted Calories']:.0f}"
            )

        with col5:
            st.metric(
                "Protein",
                f"{meal['Adjusted Protein']:.1f} g"
            )

        st.write("Dietary Type:", meal["Dietary Type"])

        st.write("Cooking Instructions:")

        st.write(meal["Cooking Instructions"])


        # ALTERNATIVE MEALS

        show_alternatives = st.checkbox(
            "Show more meal options",
            key=f"show_alternatives_{index}"
        )

        if show_alternatives:

            other_meals = filtered_meals[
                ~filtered_meals["Meal Name"].isin(
                    meal_plan["Meal Name"]
                )
            ]

            if other_meals.empty:

                st.info(
                    "No additional matching meals are available."
                )

            else:

                alternative_names = (
                    other_meals["Meal Name"].tolist()
                )

                selected_alternative = st.selectbox(
                    "Choose an alternative meal:",
                    alternative_names,
                    key=f"alternative_{index}"
                )

                if st.button(
                    "Use This Meal",
                    key=f"use_alternative_{index}"
                ):

                    new_meal = other_meals[
                        other_meals["Meal Name"]
                        == selected_alternative
                    ].iloc[0]

                    st.session_state.meal_plan.loc[
                        index
                    ] = new_meal

                    st.rerun()


# MEAL PLAN SUMMARY

st.divider()

st.subheader("💰 Meal Plan Summary")

total_cost = meal_plan["Adjusted Cost"].sum()

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "Total Estimated Cost",
        f"${total_cost:.2f}"
    )

with col2:
    st.metric(
        "Planned Meals",
        plan_days
    )

if use_weekly_budget:

    if total_cost <= weekly_budget:

        st.success(
            f"Your meal plan is within your "
            f"${weekly_budget:.2f} weekly budget."
        )

    else:

        st.warning(
            f"Your meal plan exceeds your weekly budget "
            f"by ${total_cost - weekly_budget:.2f}."
        )

st.caption(
    "Estimated costs reflect the ingredients used "
    "for your selected serving sizes."
)
