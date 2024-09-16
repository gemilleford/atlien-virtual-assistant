import json

def load_restaurants(knowledge_base):    
    with open('data/restaurants.json', 'r') as f:
        restaurants = json.load(f)
        for restaurant in restaurants:
            knowledge_base["restaurants"][restaurant["name"]] = restaurant

    return knowledge_base

def present(restaurants, query):
    response = ""
    types = []
    for restaurant in restaurants.values():
        type = restaurant['type']
        types += type
        if any(word in query for word in type):
            response += f"\n - {restaurant['description']}. \nIt can be found at {restaurant['address']}.\n"

    if not response:
        response = f"I can help you with these types of restaurants: {list(set(types))}"
    return response