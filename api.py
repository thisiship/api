from flask import Flask
from flask_jwt_extended import JWTManager

from events.events import events_bp
from auth.auth import auth_bp
from utils import create_event_helper, generate_event_id

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'WOWomgIAMsecRET'
jwt = JWTManager(app)

# events routes
app.register_blueprint(events_bp, url_prefix='/events')
# auth routes
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def hello():
    return 'Hello from the thisiship API'
