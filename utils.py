import random

def generate_event_id(min=0, max=10000):
    return random.randint(min, max)

def create_event_helper(request_data):
    new_event = {
        "id": generate_event_id()
    }
    for (k,v) in request_data.items():
        new_event[k] = v
    return new_event

