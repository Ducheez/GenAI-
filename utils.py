import boto3
from botocore.config import Config
import json
import os
from dotenv import load_dotenv
import plotly.graph_objects as go
import numpy as np
import pandas as pd

load_dotenv()

# Setup Amazon Bedrock client
bedrock = boto3.client(
    service_name='bedrock',
    region_name=os.getenv('AWS_REGION'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    config=Config(
        retries={'max_attempts': 10, 'mode': 'standard'}
    )
)

def get_llama_response(prompt):
    try:
        body = json.dumps({
            "prompt": prompt,
            "max_tokens": 1024,
            "temperature": 0.7,
            "top_p": 0.9,
        })
        
        response = bedrock.invoke_model(
            body=body,
            modelId=os.getenv('LLAMA_MODEL_ID'),
            accept="application/json",
            contentType="application/json"
        )
        
        response_body = json.loads(response.get("body").read())
        return response_body.get("generation")
    except Exception as e:
        print(f"Error calling Bedrock: {str(e)}")
        # Fallback to mock response for testing
        return "Error: Unable to generate response. Please try again."

def calculate_population_growth(initial_population, growth_rate, years):
    return initial_population * (1 + growth_rate) ** years

def generate_3d_city_model(land_area, zoning, existing_infrastructure):
    # This is a simplified 3D city model generation
    # In a real application, this would be much more complex and data-driven
    
    # Generate random building heights
    num_buildings = int(land_area * 10)  # Assume 10 buildings per sq km
    building_heights = np.random.randint(10, 100, num_buildings)
    
    # Generate random x, y coordinates for buildings
    x = np.random.rand(num_buildings) * np.sqrt(land_area)
    y = np.random.rand(num_buildings) * np.sqrt(land_area)
    
    # Create 3D scatter plot
    trace = go.Scatter3d(
        x=x, y=y, z=building_heights,
        mode='markers',
        marker=dict(
            size=5,
            color=building_heights,
            colorscale='Viridis',
            opacity=0.8
        )
    )
    
    # Create layout
    layout = go.Layout(
        scene=dict(
            xaxis_title='X (km)',
            yaxis_title='Y (km)',
            zaxis_title='Height (m)',
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=0.5)
        ),
        title=f'3D City Model - {zoning} Zone'
    )
    
    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig

def analyze_sustainability(plan, goals):
    score = 0
    breakdown = {}

    for goal in goals:
        if goal.lower() in plan.lower():
            score += 25
            breakdown[goal] = 25
        else:
            breakdown[goal] = 0

    return score, pd.DataFrame(list(breakdown.items()), columns=['Goal', 'Score'])

def optimize_traffic_flow(plan):
    # This is a simplified traffic flow optimization
    # In a real application, this would involve complex simulations and algorithms
    
    # Generate random traffic flow data
    hours = list(range(24))
    traffic_volume = np.random.randint(100, 1000, 24)
    
    # Create line plot
    trace = go.Scatter(x=hours, y=traffic_volume, mode='lines+markers')
    
    # Create layout
    layout = go.Layout(
        title='24-Hour Traffic Flow Projection',
        xaxis_title='Hour of Day',
        yaxis_title='Traffic Volume'
    )
    
    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    
    return fig