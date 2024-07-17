import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('EV_API_KEY')
BASE_URL = "http://localhost:8000/"

def fetch_ev_data(params):
    headers = {"Authorization": f"Bearer {API_KEY}"}
    response = requests.get(BASE_URL, params=params, headers=headers)
    response.raise_for_status()
    return response.json()

def promptResponse(prompt: str) -> str:
    prompt = prompt.strip().lower()
    
    if not prompt:
        return "Please provide more details about your preferences."

    params = {}

    if "range" in prompt:
        if "300" in prompt or "three hundred" in prompt:
            params['range_min'] = 300
        elif "400" in prompt or "four hundred" in prompt:
            params['range_min'] = 400
        else:
            return "Please specify the range you're looking for (e.g., 300 miles, 400 miles)."

    if "price" in prompt:
        if "affordable" in prompt or "cheap" in prompt:
            params['price_max'] = 30000
        elif "luxury" in prompt or "expensive" in prompt:
            params['price_min'] = 60000
        else:
            return "Please specify your budget range (e.g., affordable, luxury)."

    if "type" in prompt:
        if "suv" in prompt:
            params['type'] = 'SUV'
        elif "sedan" in prompt:
            params['type'] = 'Sedan'
        elif "compact" in prompt or "small" in prompt:
            params['type'] = 'Compact'
        else:
            return "Please specify the type of vehicle you're interested in (e.g., SUV, sedan, compact)."

    if "manufacturer" in prompt:
        if "tesla" in prompt:
            params['manufacturer'] = 'Tesla'
        elif "nissan" in prompt:
            params['manufacturer'] = 'Nissan'
        elif "porsche" in prompt:
            params['manufacturer'] = 'Porsche'
        else:
            return "Please specify the manufacturer you're interested in (e.g., Tesla, Nissan, Porsche)."

    if "charging time" in prompt or "charge time" in prompt:
        return "Charging times vary by vehicle and charger type. For example, the Tesla Supercharger can charge a Tesla Model 3 to 80% in about 30 minutes."

    if not params:
        return "Please provide more specific details about your preferences so we can better assist you."

    try:
        data = fetch_ev_data(params)
        if not data:
            return "No recommendations available based on your preferences."
        
        # need to create a response based on the data
        vehicle = data[0]
        return (f"We recommend the {vehicle['make']} {vehicle['model']} which has a range of {vehicle['range']} miles, "
                f"costs around ${vehicle['price']}.")
    except requests.exceptions.RequestException as e:
        return f"An error occurred while fetching recommendations: {e}"

    return "Please provide more specific details about your preferences so we can better assist you."


