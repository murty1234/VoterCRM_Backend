from Backend.app.__init__ import application, db
from Backend.app.Models.States import *
from Backend.app.Authentication.jwtservice import JWTService
from Backend.app.Authentication.middleware import Middleware
from flask import request, Blueprint
import uuid

jwt_secret = "secret"

jwt_service = JWTService(jwt_secret)
middleware = Middleware(jwt_service)

# application.before_request(lambda: middleware.auth(request))

States_API_blueprint = Blueprint("States_API", __name__)


@States_API_blueprint.route("/api/states")
def get_all_states():
    print(f"url accessed")
    states = States.query.all()
    if states:
        state_list = []
        for state in states:
            print(f"State Name: {state.State_Name}")
            state_dict = {}
            state_dict["State_Id"] = state.State_Id
            state_dict["State_Name"] = state.State_Name
            state_dict["State_No"] = state.State_No
            state_list.append(state_dict)
        return {"states": state_list}
    else:
        return {"message": "No states Available"}


@States_API_blueprint.route("/api/add_state", methods=["POST"])
def add_state():
    body = request.json
    state = States(body["State_Id"], body["State_Name"], body["State_No"])
    db.session.add(state)
    db.session.commit()
    return {"message": "New state added successfully"}
