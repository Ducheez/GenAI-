from utils import get_llama_response
import json

def generate_city_layout(land_area, population, zoning, infrastructure, sustainability_goals, budget):
    prompt = f"""
    As an AI urban planner, generate a detailed city layout based on the following parameters:
    - Land Area: {land_area} sq km
    - Population: {population}
    - Zoning: {zoning}
    - Existing Infrastructure: {infrastructure}
    - Sustainability Goals: {', '.join(sustainability_goals)}
    - Budget: ${budget} million

    Provide a JSON output with the following structure:
    {{
        "residential_areas": [
            {{"name": "Area name", "size": "Size in sq km", "population": "Estimated population"}}
        ],
        "commercial_areas": [
            {{"name": "Area name", "size": "Size in sq km", "type": "Type of commercial activity"}}
        ],
        "industrial_areas": [
            {{"name": "Area name", "size": "Size in sq km", "type": "Type of industry"}}
        ],
        "green_spaces": [
            {{"name": "Area name", "size": "Size in sq km", "type": "Type of green space"}}
        ],
        "infrastructure": [
            {{"name": "Infrastructure name", "type": "Type of infrastructure", "coverage": "Coverage area or length"}}
        ]
    }}
    """

    response = get_llama_response(prompt)
    
    try:
        layout = json.loads(response)
        return layout
    except json.JSONDecodeError:
        print("Error: AI generated an invalid JSON response")
        return None

def analyze_layout(layout):
    total_residential = sum(float(area['size'].split()[0]) for area in layout['residential_areas'])
    total_commercial = sum(float(area['size'].split()[0]) for area in layout['commercial_areas'])
    total_industrial = sum(float(area['size'].split()[0]) for area in layout['industrial_areas'])
    total_green = sum(float(area['size'].split()[0]) for area in layout['green_spaces'])
    
    total_area = total_residential + total_commercial + total_industrial + total_green
    
    analysis = {
        "Residential": (total_residential / total_area) * 100,
        "Commercial": (total_commercial / total_area) * 100,
        "Industrial": (total_industrial / total_area) * 100,
        "Green Space": (total_green / total_area) * 100
    }
    
    return analysis

def suggest_improvements(layout, sustainability_goals):
    prompt = f"""
    Analyze the following city layout and suggest improvements based on the sustainability goals:
    
    City Layout: {json.dumps(layout, indent=2)}
    
    Sustainability Goals: {', '.join(sustainability_goals)}
    
    Provide suggestions for improving the layout to better meet the sustainability goals.
    Focus on practical and innovative solutions.
    """

    response = get_llama_response(prompt)
    return response