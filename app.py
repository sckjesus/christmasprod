# Full Flask application (app.py)
from flask import Flask, render_template, request, jsonify, redirect, url_for
import uuid
import logging
import re

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Dictionary to store room data
rooms = {}

# Predefined template for tasks
tasks_template = {
    "Selected crowd members": [
        ("Pre Play", "Hand out candles")
    ],
    "Allison": [
        ("Pre Play", "Verify props are ready and in place"),
        ("Pre Play", "Verify Stage is clean and in ready order"),
        ("1 - Song 'It Came Upon A Midnight Clear'", "Release the Kubuki Drop"),
        ("1 - Song 'It Came Upon A Midnight Clear'", "Mailboxes"),
        ("4 - Lobby Scene Standard", "Confirm Dry Ice Machines are ready"),
        ("5 - Song 'All Is Well'", "Verify football, bandana, and VR headsets are present and accessible"),
        ("6 - College Guy Apartment Standard", "Prep spinning platform to come on during next song"),
        ("12 - Lobby Scene Standard", "Prep spinner platform with lowest stair facing forward and lock the rotation pegs"),
        ("12 - Lobby Scene Standard", "Open middle slide wall"),
        ("13 - Song 'Yuletide'", "Double Check Prop Arrangement on Desk"),
        ("16 - Song 'Midwinter'", "Moving Boxes"),
        ("Post Play", "Charge radios for the next show")
    ],
    "Per adult on special effects": [
        ("Pre Play", "Verify Special effects machines and mechanisms are prepared")
    ],
    "Sarah": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Pull Kubuki Drop off the stage smoothly after the drop"),
        ("1 - Song 'It Came Upon A Midnight Clear'", "Cushion on Floor"),
        ("2 - Lobby Scene Standard + Move Into Apartment Props", "Hold wall while Kyle crashes through it"),
        ("5 - Song 'All Is Well'", "Dry ice"),
        ("5 - Song 'All Is Well'", "Slide college guy wall into place when set is ready"),
        ("6 - College Guy Apartment Standard", "Prep spinning platform to come on during next song"),
        ("6 - College Guy Apartment Standard", "Push out the spinning platform"),
        ("12 - Lobby Scene Standard", "Prep extra steps for behind it"),
        ("12 - Lobby Scene Standard", "Quickly clear scene to sides"),
        ("13 - Song 'Yuletide'", "Vintage Chair"),
        ("16 - Song 'Midwinter'", "Blanket & Toys")
    ],
    "Maddie": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Pull Kubuki Drop off the stage smoothly after the drop"),
        ("1 - Song 'It Came Upon A Midnight Clear'", "Crib Pieces"),
        ("6 - College Guy Apartment Standard", "Open the middle wall"),
        ("12 - Lobby Scene Standard", "Quickly clear scene to sides"),
        ("13 - Song 'Yuletide'", "Desk"),
        ("13 - Song 'Yuletide'", "Shut middle with Lobby Door"),
    ],
    "Samuel": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "The Two Plants"),
        ("2 - Lobby Scene Standard + Move Into Apartment Props", "Repair the wall"),
        ("5 - Song 'All Is Well'", "Recliner #2"),
        ("6 - College Guy Apartment Standard", "Push out the spinning platform"),
        ("7 - Song 'He Is Born'", "Pull back the spinning platform"),
        ("7 - Song 'He Is Born'", "Keep cables clear of wheels"),
        ("12 - Lobby Scene Standard", "Push out the spinner platform"),
        ("12 - Lobby Scene Standard", "Stairs behind spinner"),
        ("13 - Song 'Yuletide'", "Pull back the platform"),
        ("16 - Song 'Midwinter'", "Moving Boxes")
    ],
    "Adrianna": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "The Two Plants"),
        ("6 - College Guy Apartment Standard", "Curtain Holders on sides"),
        ("9 - Song 'Christmas Hits Different'", "Left Side Table"),
        ("13 - Song 'Yuletide'", "Desk"),
        ("16 - Song 'Midwinter'", "Left Side Table")
    ],
    "Mila": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Table"),
        ("6 - College Guy Apartment Standard", "Curtain Holders on sides"),
        ("9 - Song 'Christmas Hits Different'", "Right Side Table"),
        ("13 - Song 'Yuletide'", "Waste Basket"),
        ("16 - Song 'Midwinter'", "Right Side Table")
    ],
    "Rebecca": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Sofa"),
        ("2 - Lobby Scene Standard + Move Into Apartment Props", "Unlatch breakaway hole in the wall"),
        ("6 - College Guy Apartment Standard", "Open the middle wall"),
        ("13 - Song 'Yuletide'", "Paper Box")
    ],
    "Grace": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Chair"),
        ("5 - Song 'All Is Well'", "Slide college guy wall into place when set is ready"),
        ("7 - Song 'He Is Born'", "Prepare to spin"),
        ("7 - Song 'He Is Born'", "Begin the slow spin"),
        ("7 - Song 'He Is Born'", "Pull back the spinning platform"),
        ("12 - Lobby Scene Standard", "Push out the spinner platform"),
        ("12 - Lobby Scene Standard", "Stairs behind spinner"),
        ("16 - Song 'Midwinter'", "Sofa")
    ],
    "Jacelynn": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Table"),
        ("2 - Lobby Scene Standard + Move Into Apartment Props", "Hold wall while Kyle crashes through it"),
        ("6 - College Guy Apartment Standard", "Quickly clear of the scene"),
        ("9 - Song 'Christmas Hits Different'", "Diaper Boxes"),
        ("12 - Lobby Scene Standard", "Quickly clear scene to sides")
    ],
    "Daniel": [
        ("1 - Song 'It Came Upon A Midnight Clear'", "Sofa"),
        ("5 - Song 'All Is Well'", "Clothes Pile"),
        ("6 - College Guy Apartment Standard", "Quickly clear of the scene"),
        ("12 - Lobby Scene Standard", "Open middle slide wall"),
        ("13 - Song 'Yuletide'", "Desk Chair"),
        ("16 - Song 'Midwinter'", "High Chair")
    ]
}




def initialize_room(room_code):
    if room_code not in rooms:
        rooms[room_code] = {"tasks": {}, "scene_order": [], "scene_selected": None}


logging.basicConfig(level=logging.DEBUG)

@app.route("/add_template_tasks/<room_code>", methods=["POST"])
def add_template_tasks_to_room(room_code):
    initialize_room(room_code)  # Ensure room is initialized

    for person, task_list in tasks_template.items():
        for task_data in task_list:
            scene, task = task_data  # Unpack the tuple containing scene and task
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
        completed_tasks = room_data.get("completed_tasks", [])
        return render_template(
            "viewer_view.html",
            room_code=room_code,
            tasks=room_data["tasks"],
            scene_order=room_data["scene_order"],
            scene_selected=room_data["scene_selected"],
            completed_tasks=completed_tasks,
            rooms=rooms
        )
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

def sanitize_name(name):
    return re.sub(r'[^a-zA-Z0-9]', '_', name)
def resolve_original_name(sanitized_name, original_dict):
    """Find the original name from a dictionary key or subkey that matches the sanitized name."""
    for original_name in original_dict:
        if sanitize_name(original_name) == sanitized_name:
            return original_name
    return None

@app.route("/mark_task_completed/<room_code>", methods=["POST"])
def mark_task_completed(room_code):
    try:
        if room_code not in rooms:
            logging.error(f"Room code '{room_code}' not found.")
            return jsonify({"success": False, "message": "Invalid room code."}), 404

        data = request.get_json()
        if not data:
            logging.error("No data received in request.")
            return jsonify({"success": False, "message": "No data received."})

        # Extract and sanitize data
        raw_scene = data.get("scene")
        raw_person = data.get("person")
        

        if not raw_scene or not raw_person:
            logging.error(f"Missing scene or person in request data. Scene: {raw_scene}, Person: {raw_person}")
            return jsonify({"success": False, "message": "Missing scene or person in request data."})

        sanitized_scene = sanitize_name(raw_scene)
        sanitized_person = sanitize_name(raw_person)
        logging.debug(f"Received sanitized inputs - Scene: {sanitized_scene}, Person: {sanitized_person}")

        # Resolve original names from the dictionary
        room = rooms[room_code]
        tasks = room.get("tasks", {})
        actual_scene = resolve_original_name(sanitized_scene, tasks)
        if actual_scene is None:
            logging.error(f"Scene not found: {sanitized_scene}")
            return jsonify({"success": False, "message": "Scene not found in tasks."})

        actual_person = resolve_original_name(sanitized_person, tasks.get(actual_scene, {}))
        if actual_person is None:
            logging.error(f"Person not found: {sanitized_person}")
            return jsonify({"success": False, "message": "Person not found in tasks."})

        logging.debug(f"Resolved actual names - Scene: {actual_scene}, Person: {actual_person}")

        # Mark the task as completed
        completed_task = {"scene": actual_scene, "person": actual_person}
        if "completed_tasks" not in room:
            room["completed_tasks"] = []

        if completed_task not in room["completed_tasks"]:
            room["completed_tasks"].append(completed_task)
            logging.debug(f"Task marked as completed: {completed_task}")
            return jsonify({"success": True, "message": "Task marked as completed!", "rooms": rooms})

        logging.debug(f"Task already marked as completed: {completed_task}")
        return jsonify({"success": True, "message": "Task already marked as completed.", "rooms": rooms})
    except Exception as e:
        logging.error(f"Error in mark_task_completed: {e}")
        return jsonify({"success": False, "message": "An error occurred."})

@app.route("/unmark_task_completed/<room_code>", methods=["POST"])
def unmark_task_completed(room_code):
    try:
        if room_code not in rooms:
            logging.error(f"Room code '{room_code}' not found. Available rooms: {list(rooms.keys())}")
            return jsonify({"success": False, "message": "Invalid room code."}), 404

        data = request.get_json()
        if not data:
            logging.error("No data received in request.")
            return jsonify({"success": False, "message": "No data received."})

        # Extract and sanitize data
        raw_scene = data.get("scene")
        raw_person = data.get("person")

        if not raw_scene or not raw_person:
            logging.error(f"Missing scene or person in request data. Scene: {raw_scene}, Person: {raw_person}")
            return jsonify({"success": False, "message": "Missing scene or person in request data."})

        sanitized_scene = sanitize_name(raw_scene)
        sanitized_person = sanitize_name(raw_person)
        logging.debug(f"Received sanitized inputs - Scene: {sanitized_scene}, Person: {sanitized_person}")

        # Resolve original names from the dictionary
        room = rooms[room_code]
        tasks = room.get("tasks", {})
        actual_scene = resolve_original_name(sanitized_scene, tasks)
        if actual_scene is None:
            logging.error(f"Scene not found: {sanitized_scene}")
            return jsonify({"success": False, "message": "Scene not found in tasks."})

        actual_person = resolve_original_name(sanitized_person, tasks.get(actual_scene, {}))
        if actual_person is None:
            logging.error(f"Person not found: {sanitized_person}")
            return jsonify({"success": False, "message": "Person not found in tasks."})

        logging.debug(f"Resolved actual names - Scene: {actual_scene}, Person: {actual_person}")

        # Ensure completed_tasks is initialized
        if "completed_tasks" not in room:
            logging.debug("No completed tasks to unmark.")
            return jsonify({"success": False, "message": "No completed tasks to unmark."})

        completed_tasks = room["completed_tasks"]

        # Check if the task is in completed_tasks and remove it
        task_to_remove = {"scene": actual_scene, "person": actual_person}
        if task_to_remove in completed_tasks:
            completed_tasks.remove(task_to_remove)
            logging.debug(f"Task for scene '{actual_scene}' and person '{actual_person}' unmarked as completed.")
            return jsonify({"success": True, "message": "Task unmarked as completed!", "rooms": rooms})
        
        logging.debug(f"Task for scene '{actual_scene}' and person '{actual_person}' was not marked as completed.")
        return jsonify({"success": False, "message": "Task was not marked as completed.", "rooms": rooms})

    except Exception as e:
        logging.error(f"Error in unmark_task_completed: {e}")
        return jsonify({"success": False, "message": "An error occurred while unmarking the task as completed."})

    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
