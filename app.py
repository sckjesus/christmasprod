# Full Flask application (app.py)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Dictionary to store room data
rooms = {}

# Predefined template for tasks
tasks_template = {
    "Sam": [("1 - Strike", "Table"), ("2 - Set Up", "Table")],
    "Mila": [("1 - Strike", "Table")],
    "Danny": [("1 - Set Up", "Table")],
    "Allison": [("1 - Set Up", "Wall")],
    "Messi": [("1 - Set Up", "Plants")],
}

def initialize_room(room_code):
    if room_code not in rooms:
        rooms[room_code] = {"tasks": {}, "scene_order": [], "scene_selected": None}


logging.basicConfig(level=logging.DEBUG)

@app.route("/add_template_tasks/<room_code>", methods=["POST"])
def add_template_tasks_to_room(room_code):
    initialize_room(room_code)  # Ensure room is initialized

    for person, task_list in tasks_template.items():
        for scene, task in task_list:
            # Add scene to scene_order if it's not already there
            if scene not in rooms[room_code]["scene_order"]:
                rooms[room_code]["scene_order"].append(scene)

            if scene not in rooms[room_code]["tasks"]:
                rooms[room_code]["tasks"][scene] = {}

            if person not in rooms[room_code]["tasks"][scene]:
                rooms[room_code]["tasks"][scene][person] = []

            # Debugging Log
            logging.debug(f"Adding task: {task} for person: {person} in scene: {scene}")

            rooms[room_code]["tasks"][scene][person].append(task)
    if not rooms[room_code]["scene_selected"] and rooms[room_code]["scene_order"]:
        rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][0]


    return jsonify({"message": "Template tasks added successfully!", "rooms": rooms})



@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        room_code = str(uuid.uuid4())[:8]  # Generate a unique room code
        rooms[room_code] = {"tasks": {}, "scene_order": [], "scene_selected": None}
        return redirect(url_for('creator_view', room_code=room_code))

    return render_template("index.html")

@app.route("/create_room", methods=["GET", "POST"])
def create_room():
    logging.debug("Create room route accessed.")
    if request.method == "POST":
        room_code = str(uuid.uuid4())[:8]  # Generate a unique room code
        rooms[room_code] = {"tasks": {}, "scene_order": []}
        logging.debug(f"Generated room code: {room_code}")
        return render_template("create_room.html", room_code=room_code)
    return render_template("create_room.html")

@app.route("/join_room", methods=["GET", "POST"])
def join_room():
    if request.method == "POST":
        room_code = request.form.get("room_code")
        if room_code in rooms:
            return redirect(url_for("viewer_view", room_code=room_code))
        else:
            return render_template("join_room.html", error="Invalid room code. Please try again.")

    return render_template("join_room.html")

@app.route("/creator_view/<room_code>", methods=["GET", "POST"])
def creator_view(room_code):
    if room_code in rooms:
        if request.method == "POST":
            data = request.json
            action = data.get("action")

            if action == "add_task":
                scene_number = data.get("scene_number")
                person = data.get("person")
                task = data.get("task")

                if scene_number not in rooms[room_code]["tasks"]:
                    rooms[room_code]["tasks"][scene_number] = {}

                if person not in rooms[room_code]["tasks"][scene_number]:
                    rooms[room_code]["tasks"][scene_number][person] = []

                rooms[room_code]["tasks"][scene_number][person].append(task)
                return jsonify({"message": "Task added successfully!", "rooms":rooms})

            elif action == "delete_task":
                scene_number = data.get("scene_number")
                person = data.get("person")
                task_to_delete = data.get("task")

                if scene_number in rooms[room_code]["tasks"]:
                    if person in rooms[room_code]["tasks"][scene_number]:
                        try:
                            rooms[room_code]["tasks"][scene_number][person].remove(task_to_delete)
                            if not rooms[room_code]["tasks"][scene_number][person]:
                                del rooms[room_code]["tasks"][scene_number][person]
                            if not rooms[room_code]["tasks"][scene_number]:
                                del rooms[room_code]["tasks"][scene_number]
                            return jsonify({"message": "Task deleted successfully!", "rooms":rooms})
                        except ValueError:
                            return jsonify({"message": "Task not found."})
                    else:
                        return jsonify({"message": "Person not found in this scene."})
                else:
                    return jsonify({"message": "Scene number not found."})

        return render_template("creator_view.html", room_code=room_code, rooms=rooms)
    else:
        return "Invalid room code.", 404

@app.route("/viewer_view/<room_code>")
def viewer_view(room_code):
    if room_code in rooms:
        room_data = rooms[room_code]
        return render_template("viewer_view.html", room_code=room_code, tasks=room_data["tasks"], scene_order=room_data["scene_order"], scene_selected=room_data["scene_selected"], rooms=rooms)
    else:
        return "Invalid room code.", 404
@app.route("/update_tasks", methods=["POST"])
def update_tasks():
    data = request.json
    room_code = data.get("room_code")
    updated_tasks = data.get("updated_tasks")

    if room_code not in rooms:
        return jsonify({"message": "Invalid room code. Please create a room first."})

    updated_rooms = {}
    for person, tasks in updated_tasks.items():
        for full_task in tasks:
            if ": " in full_task:
                scene, task = full_task.split(": ", 1)
                if scene not in updated_rooms:
                    updated_rooms[scene] = {}
                if person not in updated_rooms[scene]:
                    updated_rooms[scene][person] = []
                updated_rooms[scene][person].append(task)

    rooms[room_code]["tasks"] = updated_rooms
    return jsonify({"message": "Tasks updated successfully!", "rooms":rooms})

@app.route("/delete_task", methods=["POST"])
def delete_task():
    data = request.json
    room_code = data.get("room_code")
    scene_number = data.get("scene_number")
    person = data.get("person")
    task_to_delete = data.get("task")

    if room_code in rooms and scene_number in rooms[room_code]["tasks"]:
        if person in rooms[room_code]["tasks"][scene_number]:
            try:
                rooms[room_code]["tasks"][scene_number][person].remove(task_to_delete)
                if not rooms[room_code]["tasks"][scene_number][person]:
                    del rooms[room_code]["tasks"][scene_number][person]
                if not rooms[room_code]["tasks"][scene_number]:
                    del rooms[room_code]["tasks"][scene_number]
                return jsonify({"message": "Task deleted successfully!", "rooms":rooms})
            except ValueError:
                return jsonify({"message": "Task not found."})
        else:
            return jsonify({"message": "Person not found in this scene."})
    else:
        return jsonify({"message": "Invalid room code or scene number."})

@app.route("/add_task", methods=["POST"])
def add_task():
    data = request.json
    room_code = data.get("room_code")
    scene_name = data.get("scene_name")
    person = data.get("person")
    task_detail = data.get("task_detail")

    if room_code in rooms:
        if "scene_order" not in rooms[room_code]:
            rooms[room_code]["scene_order"] = []

        # Add to scene_order if the scene is new
        if scene_name not in rooms[room_code]["scene_order"]:
            rooms[room_code]["scene_order"].append(scene_name)

        # Add task
        if scene_name not in rooms[room_code]["tasks"]:
            rooms[room_code]["tasks"][scene_name] = {}
        if person not in rooms[room_code]["tasks"][scene_name]:
            rooms[room_code]["tasks"][scene_name][person] = []

        # Append the new task
        rooms[room_code]["tasks"][scene_name][person].append(task_detail)
        # Set the first scene as selected if no scene is currently selected
        if not rooms[room_code]["scene_selected"] and rooms[room_code]["scene_order"]:
            rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][0]

        # Return the updated rooms dictionary to the frontend
        return jsonify({"message": "Task added successfully!", "rooms": rooms})
    else:
        return jsonify({"message": "Invalid room code."}), 404


@app.route("/update_scene_order", methods=["POST"])
def update_scene_order():
    data = request.json
    room_code = data.get("room_code")
    new_order = data.get("new_order")

    if room_code in rooms:
        rooms[room_code]["scene_order"] = new_order
        # Update scene_selected only if the selected scene is no longer in the new scene_order
        if rooms[room_code]["scene_selected"] not in new_order and new_order:
            rooms[room_code]["scene_selected"] = new_order[0]
        return jsonify({"message": "Scene order updated successfully!", "rooms":rooms})
    else:
        return jsonify({"message": "Invalid room code."}), 404

        
@app.route("/next_scene/<room_code>", methods=["POST"])
def next_scene(room_code):
    if room_code in rooms:
        current_index = 0
        if rooms[room_code]["scene_selected"]:
            current_index = rooms[room_code]["scene_order"].index(rooms[room_code]["scene_selected"])
        if current_index < len(rooms[room_code]["scene_order"]) - 1:
            rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][current_index + 1]
        else:
            rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][0]  # Loop back to the first scene
        return jsonify({"success": True, "scene_selected": rooms[room_code]["scene_selected"]})
    return jsonify({"success": False, "message": "Invalid room code."})

@app.route("/previous_scene/<room_code>", methods=["POST"])
def previous_scene(room_code):
    if room_code in rooms:
        current_index = 0
        if rooms[room_code]["scene_selected"]:
            current_index = rooms[room_code]["scene_order"].index(rooms[room_code]["scene_selected"])
        if current_index > 0:
            rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][current_index - 1]
        else:
            rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][-1]  # Loop back to the last scene
        return jsonify({"success": True, "scene_selected": rooms[room_code]["scene_selected"]})
    return jsonify({"success": False, "message": "Invalid room code."})

@app.route("/mark_task_completed/<room_code>", methods=["POST"])
def mark_task_completed(room_code):
    try:
        if room_code not in rooms:
            logging.error(f"Room code '{room_code}' not found. Available rooms: {list(rooms.keys())}")
            return jsonify({"success": False, "message": "Invalid room code."}), 404

        data = request.get_json()
        if not data:
            logging.error("No data received in request.")
            return jsonify({"success": False, "message": "No data received."})

        scene = data.get("scene")
        person = data.get("person")

        # Check if required fields are present
        if not scene or not person:
            logging.error(f"Missing scene or person in request data. Scene: {scene}, Person: {person}")
            return jsonify({"success": False, "message": "Missing scene or person in request data."})

        # Logging to verify data received
        logging.debug(f"Received request to mark task as completed in room '{room_code}' for scene '{scene}' and person '{person}'")

        room = rooms[room_code]

        # Ensure completed_tasks is initialized
        if "completed_tasks" not in room:
            room["completed_tasks"] = []

        tasks = room.get("tasks", {})

        # Check if scene exists in tasks
        if scene in tasks:
            scene_tasks = tasks[scene]

            # Check if person exists in the scene
            if person in scene_tasks:
                # Avoid marking the same task as completed multiple times
                if {"scene": scene, "person": person} not in room["completed_tasks"]:
                    room["completed_tasks"].append({"scene": scene, "person": person})
                    logging.debug(f"Task for scene '{scene}' and person '{person}' marked as completed.")
                    return jsonify({"success": True, "message": "Task marked as completed!", "rooms": rooms})

                logging.debug(f"Task for scene '{scene}' and person '{person}' is already marked as completed.")
                return jsonify({"success": True, "message": "Task already marked as completed.", "rooms": rooms})
            else:
                logging.error(f"Person '{person}' not found in scene '{scene}'. Available persons: {list(scene_tasks.keys())}")
                return jsonify({"success": False, "message": "Person not found in this scene."})
        else:
            logging.error(f"Scene '{scene}' not found in tasks. Available scenes: {list(tasks.keys())}")
            return jsonify({"success": False, "message": "Scene not found."})

    except Exception as e:
        logging.error(f"Error in mark_task_completed: {e}")
        return jsonify({"success": False, "message": "An error occurred while marking the task as completed."})

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
