from flask import Flask, request, jsonify
from utils import get_llama_response, analyze_sustainability

app = Flask(__name__)

@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    data = request.json
    prompt = f"""
    As an advanced urban planning AI, create a comprehensive development plan with the following characteristics:
    - Land Area: {data['land_area']} sq km
    - Current Population: {data['current_population']}
    - Zoning: {data['zoning']}
    - Existing Infrastructure: {data['existing_infrastructure']}
    - Sustainability Goals: {', '.join(data['sustainability_goals'])}
    - Development Budget: ${data['budget']} million

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
    sustainability_score, sustainability_breakdown = analyze_sustainability(response, data['sustainability_goals'])

    return jsonify({
        'plan': response,
        'sustainability_score': sustainability_score,
        'sustainability_breakdown': sustainability_breakdown.to_dict(orient='records')
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)