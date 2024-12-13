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

    "Allison": [
        ("Pre Play", "Props ready, in place"),
        ("Pre Play", "Stage ready, clean"),
        ("1 - 'Midnight Clear'", "Release Kubuki	"),
        ("1 - END of 'Midnight Clear'", "Mailboxes"),
        ("2 - AFTER Lobby + Moving", "Clear sofa"),
("3 - 'Behold Him'", "Nothing to do"),

        ("4 - Lobby", "Dry Ice Machines ready"),
        ("4 - AFTER Lobby", "Clear Mailboxes"),

        ("5 - 'All Is Well'", "Verify football, bandana, and VR headsets are present and accessible"),
        ("5 - END of 'All Is Well'", "Verify football, bandana, and VR headsets are present and accessible"),
        ("6 - College Apartment", "Prep spinning platform to come on during next song"),
        ("6 - AFTER College Apartment", "Prep spinning platform to come on during next song"),
        ("7 - 'He Is Born'", "Prepare to spin"),
        ("7 - AFTER 'He Is Born'", "Prepare to spin"),
        ("8 - Lobby", "Prepare to spin"),
("8 - AFTER Lobby", "Prepare to spin"),
        ("9 - END 'Hits Different'", "Left Side Table"),
        ("9 - AFTER 'Hits Different'", "Left Side Table"),
        ("10 - AFTER Young Couples", "Left Side Table"),
        ("11 - END 'Wait Is Over'", "Left Side Table"),

        ("12 - Lobby", "Prep spinner platform with lowest stair facing forward and lock the rotation pegs"),
        ("12 - Lobby", "Open middle slide wall"),
        ("12 - AFTER Lobby", "Prep spinner platform with lowest stair facing forward and lock the rotation pegs"),
        ("13 - 'Yuletide'", "Double Check Prop Arrangement on Desk"),
        ("13 - AFTER 'Yuletide'", "Double Check Prop Arrangement on Desk"),
        ("14 - AFTER George’s Apartment", "Double Check Prop Arrangement on Desk"),
        ("15 - 'Heard the Bells'", "Double Check Prop Arrangement on Desk"),
        ("Message", "Double Check Prop Arrangement on Desk"),

        ("16 - 'Midwinter'", "Moving Boxes"),
        ("16 - END of 'Midwinter'", "Moving Boxes"),
        ("17 - Young Couples", "Moving Boxes"),

        ("Post Play", "Charge radios for the next show"),
        ("AFTER Post Play", "Charge radios for the next show")
    ],
    "Sarah": [
        ("1 - 'Midnight Clear'", "Pull Kubuki"),
        ("1 - END of 'Midnight Clear'", "Cushion on floor"),
("9 - END 'Hits Different'", "Toys, and diaper box"),
        ("10 - AFTER Young Couples", "Penelope"),
        ("10 - AFTER Young Couples", "Toys and diaper box"),
        ("13 - 'Yuletide'", "Vintage chair"),
        ("14 - AFTER George’s Apartment", "Clear vintage chair"),
        ("15 - AFTER 'Heard the Bells'", "Prepare smoke"),
        ("15 - AFTER 'Heard the Bells'", "Prepare snow"),
        ("16 - END 'Midwinter'", "Snow"),
        ("17 - Young Couples", "Smoke machine"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ],
    "Samuel": [
        ("1 - 'Midnight Clear'", "Move Recliner 2"),
        ("1 - END 'Midnight Clear'", "Chair"),
        ("2 - AFTER Lobby + Moving", "Repair wall"),
        ("4 - AFTER Lobby", "Clear Plants"),
        ("5 - END 'All Is Well'", "Recliner 2"),
        ("6 - College Apartment", "Prep spinner platform"),
        ("6 - AFTER College Apartment", "Push spinner platform"),
        ("7 - END 'He Is Born'", "Clear spinner platform"),
        ("7 - AFTER 'He Is Born'", "Plants"),
        ("8 - AFTER Lobby", "Clear plants"),
        ("9 - END 'Hits Different'", "Moving boxes"),
        ("9 - END 'Hits Different'", " Young couples wall"),
        ("10 - AFTER Young Couples", "Clear Moving Boxes"),
        ("11 - END 'Wait Is Over'", "Plants"),
        ("12 - AFTER Lobby", "Push spinner platform"),
        ("12 - AFTER Lobby", "Push spinner stairs"),
        ("13 - AFTER 'Yuletide'", "Clear spinner stairs"),
        ("13 - AFTER 'Yuletide'", "Georges Wall"),
        ("16 - END 'Midwinter'", "Moving Boxes"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ],
    "Adriana": [
        ("1 - END 'Midnight Clear'", "Plants"),
        ("4 - AFTER Lobby", "Clear Plants"),
        ("5 - END 'All Is Well'", "Both side tables"),
        ("6 - AFTER College Apartment", "Clear both side tables"),
        ("7 - AFTER 'He Is Born'", "Plants"),
        ("8 - AFTER Lobby", "Plants"),
        ("9 - 'Hits Different'", "Side tables"),
        ("10 - AFTER Young Couples", "Clear side tables"),
        ("11 - END 'Wait Is Over'", "Plants"),
        ("12 - AFTER Lobby", "Clear plants"),
        ("13 - 'Yuletide'", "Lights with Daniel"),
        ("13 - END 'Yuletide'", "Lights with Daniel"),
        ("14 - AFTER George’s Apartment", "Clear desk"),
        ("16 - 'Midwinter'", "Side tables")
    ],
    "Mila": [
        ("1 - END 'Midnight Clear'", "Crib Peices"),
        ("2 - AFTER Lobby + Moving", "Repair wall"),
        ("4 - AFTER Lobby", "Clear whatever"),
        ("5 - END 'All Is Well'", "Rolling chair"),
        ("6 - AFTER College Apartment", "Rolling chair and headsets"),
        ("7 - AFTER 'He Is Born'", "Plants"),
        ("8 - AFTER Lobby", "Plants"),
        ("9 - END 'Christmas Hits Different'", "Boxes"),
        ("10 - AFTER Young Couples", "Boxes"),
        ("11 - END 'Wait Is Over'", "Plants"),
        ("12 - AFTER Lobby", "Plants"),
        ("13 - AFTER 'Yuletide'", "Desk chair"),
        ("16 - END 'Midwinter'", "Boxes"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ],
    "Rebecca": [
        ("1 - END 'Midnight Clear'", "Sofa"),
        ("2 - Lobby + Moving", "Unlatch crash wall"),
        ("2 - Lobby + Moving", "Hold crash wall"),
        ("4 - AFTER Lobby", "Clear chair"),
        ("7 - AFTER 'He Is Born'", "Chair"),
        ("8 - AFTER Lobby", "Clear chair"),
        ("9 - END 'Hits Different'", "Sofa"),
        ("10 - AFTER Young Couples", "Clear sofa"),
        ("11 - END 'Wait Is Over'", "Chair"),
        ("12 - AFTER Lobby", "Clear chair"),
        ("13 - AFTER 'Yuletide'", "Desk"),
        ("16 - END 'Midwinter'", "Sofa"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ],
    "GraceK": [
        ("1 - END 'Midnight Clear'", "Crib peices vertical"),
        ("2 - AFTER Lobby + Moving", "Clear crib peices"),
        ("4 - AFTER Lobby", "Clear Chair"),
        ("6 - AFTER College Apartment", "Clear laundry"),
        ("9 - END 'Hits Different'", "Baby box"),
        ("10 - AFTER Young Couples", "Clear baby box"),
        ("13 - 'Yuletide'", "Lights"),
        ("13 - After 'Yuletide'", "Clear lights"),
        ("14 - AFTER George’s Apartment", "Clear desk"),
    ],
    "GraceB": [
        ("1 - END 'Midnight Clear'", "Curtain"),
        ("2 - AFTER Lobby + Moving", "Curtain"),
        ("4 - AFTER Lobby", "Curtain"),

        ("5 - 'All Is Well'", "Curtain"),
         ("6 - College Apartment", "Prep spinner platform"),
        ("6 - AFTER College Apartment", "Push spinner platform"),
        ("7 - END 'He Is Born'", "Clear spinner platform"),
  ("12 - AFTER Lobby", "Push spinner platform"),
        ("13 - AFTER 'Yuletide'", "Clear spinner platform"),
        ("16 - 'Midwinter'", "Sofa"),
        ("16 - END 'Midwinter'", "Snow"),

    ],
    "Jacelynn": [
        ("1 - END 'Midnight Clear'", "Table"),
        ("2 - Lobby + Moving", "Unlatch crash wall"),
        ("2 - Lobby + Moving", "Hold crash wall"),
        ("4 - AFTER Lobby", "Clear table"), 
("5 - AFTER 'All Is Well'", "Recliner 2"),
        ("6 - AFTER College Apartment", "Clear recliner 2"),
        ("7 - AFTER 'He Is Born'", "Table"),
("8 - AFTER Lobby", "Clear table"),
        ("11 - END 'Wait Is Over'", "Table"),
        ("12 - AFTER Lobby", "Clear table"),
        ("13 - 'Yuletide'", "Lights with "),
        ("13 - After 'Yuletide'", "Clear lights"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ],
    "Daniel": [
        ("1 - END 'Midnight Clear'", "Sofa"),
        ("2 - AFTER Lobby + Moving", "Repair wall"),

        ("5 - END 'All Is Well'", "Clothes pile"),
        ("6 - AFTER College Apartment", "Clear clothes pile"),
        ("7 - AFTER 'He Is Born'", "Plants"),
("8 - AFTER Lobby", "Clear plants"),
        ("9 - END 'Hits Different'", "High chair"),
        ("10 - AFTER Young Couples", "High chair"),

        ("12 - AFTER Lobby", "Lights with Adriana"),
        ("13 - AFTER 'Yuletide'", "Clear Lights"),
        ("13 - AFTER 'Yuletide'", "Desk chair"),
        ("14 - AFTER George’s Apartment", "Clear desk chair"),

        ("16 - END 'Midwinter'", "High Chair"),
        ("Post Play", "Come for thanks"),
        ("AFTER Post Play", "Reset props")
    ]
}










def initialize_room(room_code):
    if room_code not in rooms:
        rooms[room_code] = {"tasks": {}, "scene_order": [], "scene_selected": None}


logging.basicConfig(level=logging.DEBUG)

@app.route("/add_template_tasks/<room_code>", methods=["POST"])
def add_template_tasks_to_room(room_code):
    # Ensure room is initialized
    initialize_room(room_code)

    # Predefined scene order with responsibilities
    scene_order_with_responsibilities = [
    'Pre Play',
 "1 - 'Midnight Clear'",
 "1 - END 'Midnight Clear'",
 '2 - AFTER Lobby + Moving',
 "3 - 'Behold Him'",
 '4 - Lobby',
 '4 - AFTER Lobby',
 "5 - 'All Is Well'",
 "5 - END 'All Is Well'",
 '6 - College Apartment',
 '6 - AFTER College Apartment',
 "7 - 'He Is Born'",
 "7 - AFTER 'He Is Born'",
 '8 - Lobby',
 '8 - AFTER Lobby',
 "9 - AFTER 'Hits Different'",
 "9 - END 'Hits Different'",
 '10 - AFTER Young Couples',
 "11 - END 'Wait Is Over'",
 '12 - Lobby',
 '12 - AFTER Lobby',
 "13 - 'Yuletide'",
 "13 - AFTER 'Yuletide'",
 '14 - AFTER George’s Apartment',
 "15 - 'Heard the Bells'",
 "15 - AFTER 'Heard the Bells'",
  'Message',
 "16 - 'Midwinter'",
 "16 - END 'Midwinter'",
 '17 - Young Couples',
 'Post Play',
 'AFTER Post Play'
]


    # Replace or initialize the room's scene_order
    rooms[room_code]["scene_order"] = scene_order_with_responsibilities

    # Add tasks for each person based on the template
    for person, task_list in tasks_template.items():
        for task_data in task_list:
            scene, task = task_data  # Unpack the tuple containing scene and task

            # Ensure the scene is present in the room's tasks
            if scene not in rooms[room_code]["tasks"]:
                rooms[room_code]["tasks"][scene] = {}

            # Ensure the person exists within the scene's tasks
            if person not in rooms[room_code]["tasks"][scene]:
                rooms[room_code]["tasks"][scene][person] = []

            # Debugging Log
            logging.debug(f"Adding task: {task} for person: {person} in scene: {scene}")

            # Add the task to the person's task list for the scene
            rooms[room_code]["tasks"][scene][person].append(task)

    # Set the first scene as the selected scene if not already set
    if not rooms[room_code]["scene_selected"] and rooms[room_code]["scene_order"]:
        rooms[room_code]["scene_selected"] = rooms[room_code]["scene_order"][0]

    return jsonify({"message": "Template tasks and scene order added successfully!", "rooms": rooms})




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
    
@app.route("/contact", methods=["GET"])
def contact():
    return render_template("contact.html")

@app.route("/about", methods=["GET"])
def about():
    return render_template("about.html")


    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
