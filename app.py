import streamlit as st
from utils import get_llama_response, calculate_population_growth, generate_3d_city_model, analyze_sustainability, optimize_traffic_flow
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(layout="wide")
st.title("Advanced Urban Planner Bot")

# Input section
st.header("Input Information")
col1, col2 = st.columns(2)

with col1:
    land_area = st.number_input("Land Area (sq km)")
    current_population = st.number_input("Current Population")
    zoning = st.selectbox("Zoning", ["Residential", "Commercial", "Industrial", "Mixed-Use"])

with col2:
    existing_infrastructure = st.text_area("Existing Infrastructure")
    sustainability_goals = st.multiselect("Sustainability Goals", 
        ["Reduce carbon emissions", "Increase green spaces", "Improve public transport", "Enhance energy efficiency"])
    budget = st.number_input("Development Budget (millions $)")

# Generate comprehensive plan
if st.button("Generate Comprehensive Urban Plan"):
    prompt = f"""
    As an advanced urban planning AI, create a comprehensive development plan with the following characteristics:
    - Land Area: {land_area} sq km
    - Current Population: {current_population}
    - Zoning: {zoning}
    - Existing Infrastructure: {existing_infrastructure}
    - Sustainability Goals: {', '.join(sustainability_goals)}
    - Development Budget: ${budget} million

    Provide detailed recommendations on:
    1. Land use optimization
    2. Infrastructure development
    3. Sustainability implementation
    4. Community engagement strategies
    5. Economic development opportunities
    6. Smart city technologies integration
    7. Climate resilience measures
    8. Public space design
    9. Transportation network improvements
    10. Affordable housing initiatives
    """

    response = get_llama_response(prompt)

    st.markdown("## Comprehensive Urban Plan")
    st.markdown(response)

    # Generate and display 3D city model
    city_model = generate_3d_city_model(land_area, zoning, existing_infrastructure)
    st.plotly_chart(city_model, use_container_width=True)

    # Sustainability Analysis
    sustainability_score, sustainability_breakdown = analyze_sustainability(response, sustainability_goals)
    st.markdown(f"## Sustainability Score: {sustainability_score}/100")
    st.bar_chart(sustainability_breakdown.set_index('Goal'))

    # Traffic Flow Optimization
    traffic_flow = optimize_traffic_flow(response)
    st.markdown("## Optimized Traffic Flow")
    st.plotly_chart(traffic_flow, use_container_width=True)

# Calculations section
st.header("Urban Planning Calculations")

calc_type = st.selectbox("Select Calculation", ["Population Growth", "Land Use Distribution", "Infrastructure Cost Estimation"])

if calc_type == "Population Growth":
    initial_pop = st.number_input("Initial Population")
    growth_rate = st.number_input("Annual Growth Rate (as decimal)", min_value=0.0, max_value=1.0, step=0.01)
    years = st.number_input("Number of Years", min_value=1, step=1)

    if st.button("Calculate Population Growth"):
        future_population = calculate_population_growth(initial_pop, growth_rate, years)
        st.markdown(f"## Projected Population after {years} years")
        st.markdown(f"**{future_population:.0f}**")

        # Population growth chart
        years_range = list(range(years + 1))
        pop_values = [initial_pop * (1 + growth_rate) ** year for year in years_range]
        
        fig = go.Figure(data=go.Scatter(x=years_range, y=pop_values, mode='lines+markers'))
        fig.update_layout(title='Population Growth Projection', xaxis_title='Years', yaxis_title='Population')
        st.plotly_chart(fig)

elif calc_type == "Land Use Distribution":
    st.markdown("Enter the percentage distribution for each land use type:")
    residential = st.slider("Residential", 0, 100, 30)
    commercial = st.slider("Commercial", 0, 100, 20)
    industrial = st.slider("Industrial", 0, 100, 15)
    green_space = st.slider("Green Space", 0, 100, 15)
    infrastructure = st.slider("Infrastructure", 0, 100, 20)

    total = residential + commercial + industrial + green_space + infrastructure
    if total != 100:
        st.warning(f"Total distribution should equal 100%. Current total: {total}%")
    else:
        fig = go.Figure(data=[go.Pie(labels=['Residential', 'Commercial', 'Industrial', 'Green Space', 'Infrastructure'],
                                     values=[residential, commercial, industrial, green_space, infrastructure])])
        fig.update_layout(title='Land Use Distribution')
        st.plotly_chart(fig)

elif calc_type == "Infrastructure Cost Estimation":
    road_length = st.number_input("Road Network Length (km)")
    utility_coverage = st.number_input("Utility Network Coverage (sq km)")
    public_buildings = st.number_input("Number of Public Buildings")

    if st.button("Estimate Infrastructure Cost"):
        road_cost = road_length * 2  # Assuming $2 million per km
        utility_cost = utility_coverage * 1.5  # Assuming $1.5 million per sq km
        building_cost = public_buildings * 5  # Assuming $5 million per building
        total_cost = road_cost + utility_cost + building_cost

        st.markdown(f"## Estimated Infrastructure Cost")
        st.markdown(f"Road Network: ${road_cost:.2f} million")
        st.markdown(f"Utility Network: ${utility_cost:.2f} million")
        st.markdown(f"Public Buildings: ${building_cost:.2f} million")
        st.markdown(f"**Total Estimated Cost: ${total_cost:.2f} million**")

        # Cost breakdown chart
        fig = go.Figure(data=[go.Bar(x=['Road Network', 'Utility Network', 'Public Buildings'],
                                     y=[road_cost, utility_cost, building_cost])])
        fig.update_layout(title='Infrastructure Cost Breakdown', yaxis_title='Cost (millions $)')
        st.plotly_chart(fig)