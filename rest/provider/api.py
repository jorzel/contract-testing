from flask import Flask, abort, jsonify

fakedb = {
    "UserA": {
        "name": "A",
        "username": "a",
        "id": "'8d36c5fe-ba82-4db3-9373-2de4325c7efa'",
        "created_on": "2016-12-15T20:16:01",
        "ip_address": "192.0.0.1",
        "admin": False,
    }
}  # Use a simple dict to represent a database

app = Flask(__name__)


@app.route("/users/<name>")
def get_user_by_name(name: str):
    """Handle requests to retrieve a single user from the simulated database.
    :param name: Name of the user to "search for"
    :return: The user data if found, None (HTTP 404) if not
    """
    user_data = fakedb.get(name)
    if not user_data:
        app.logger.debug(f"GET user for: '{name}', HTTP 404 not found")
        abort(404)
    response = jsonify(**user_data)
    app.logger.debug(f"GET user for: '{name}', returning: {response.data}")
    return response


if __name__ == "__main__":
    app.run(debug=True, port=5000)
