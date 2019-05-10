from flask import jsonify, request, Blueprint
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity

from utils import create_event_helper, generate_event_id

events_bp = Blueprint('events', __name__)

event_owner = 'tonisbones'
events_list = [
    {
        'title': 'Root Shock wsg Forest Dwellers @ Montage',
        'venue': 'Montage',
        'description': 'A kinky reggae party!',
        'price': 10,
        'date': datetime.now().isoformat(),
        'id': 1234,
        'creator': event_owner
    },
    {
        'title': 'Forest Dwellers @ Huber Hoedown',
        'venue': 'G Lodge',
        'description': 'Come check out the FD at huber hoedown. It\'s going to be a family affair.',
        'price': 10,
        'date': datetime.now().isoformat(),
        'id': 7890,
        'creator': 'SomeOtherUser'
    }
]


@events_bp.route('/', methods=['GET'])
def all_events_list():
    """ Get all events """
    return jsonify(events_list)


@events_bp.route('/<int:event_id>')    
def event_details(event_id):
    """ Get the details of a single event\n
        Parameters:\n
        <event_id> - the id of the event
    """
    requested_event = list(filter(lambda ev: ev['id'] == event_id, events_list))
    if not requested_event or len(requested_event) <= 0:
        return jsonify(message=f'Event with id {event_id} not found.'), 404
    return jsonify(event=requested_event[0])


@events_bp.route('/create', methods=['POST'])
def create_event():
    req_data = request.get_json()
    new_event = create_event_helper(req_data)
    events_list.append(new_event)
    return jsonify(id=new_event['id']), 200
    

@events_bp.route('/edit', methods=['PUT'])
@jwt_required
def update_event():
    current_user = get_jwt_identity()
    req_data = request.get_json()
    event_id = int(req_data['id'])
    if not event_id:
        return jsonify(message="Invalid request: Missing event id."), 400
     
    # event = list(filter(lambda ev: ev['id'] == event_id, events_list))[0]
    event_index = -1
    try:
        found_event = [events_list.index(ev) for ev in events_list if ev['id'] == event_id]
        if len(found_event) > 0:
            event_index = found_event[0]
    except ValueError as e:
        # this will be handled below - the event_index will be -1 still 
        pass

    if event_index == -1:
        message = f"Invalid request: Event doesn't exist with id: {event_id}"
        print(message)
        return jsonify(message=message), 404

    if current_user != events_list[event_index]['creator']:
        return jsonify(message="Unauthorized!"), 403
    # if we've reached here, we have a valid event_index and we can safely update
    req_data['creator'] = current_user
    events_list[event_index] = create_event_helper(req_data)
    
    return jsonify(events_list[event_index]), 200

