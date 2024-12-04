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

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        room_code = str(uuid.uuid4())[:8]  # Generate a unique room code
        rooms[room_code] = {"tasks": {}}
        return redirect(url_for('creator_view', room_code=room_code))

    return render_template("index.html")


@app.route("/create_room", methods=["GET", "POST"])
def create_room():
    logging.debug("Create room route accessed.")
    if request.method == "POST":
        room_code = str(uuid.uuid4())[:8]  # Generate a unique room code
        rooms[room_code] = {"tasks": {}}
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

# @app.route("/creator_view/<room_code>")
# def creator_view(room_code):
#     if room_code in rooms:
#         return render_template("creator_view.html", room_code=room_code, tasks=rooms[room_code]["tasks"])
#     else:
#         return "Invalid room code.", 404
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
                return jsonify({"message": "Task added successfully!"})

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
                            return jsonify({"message": "Task deleted successfully!"})
                        except ValueError:
                            return jsonify({"message": "Task not found."})
                    else:
                        return jsonify({"message": "Person not found in this scene."})
                else:
                    return jsonify({"message": "Scene number not found."})

        return render_template("creator_view.html", room_code=room_code, tasks=rooms[room_code]["tasks"])
    else:
        return "Invalid room code.", 404


@app.route("/viewer_view/<room_code>")
def viewer_view(room_code):
    if room_code in rooms:
        return render_template("viewer_view.html", room_code=room_code, tasks=rooms[room_code]["tasks"])
    else:
        return "Invalid room code.", 404

@app.route("/add_template_tasks", methods=["POST"])
def add_template_tasks():
    data = request.json
    room_code = data.get("room_code")
    if room_code in rooms:
        rooms[room_code]["tasks"] = {}
        for person, task_list in tasks_template.items():
            for scene, task in task_list:
                scene_parts = scene.split(" - ")
                scene_number = scene_parts[0].strip() if len(scene_parts) > 1 else "0"
                scene_name = scene_parts[1].strip() if len(scene_parts) > 1 else scene_parts[0].strip()

                if scene_number not in rooms[room_code]["tasks"]:
                    rooms[room_code]["tasks"][scene_number] = {}

                if person not in rooms[room_code]["tasks"][scene_number]:
                    rooms[room_code]["tasks"][scene_number][person] = []

                rooms[room_code]["tasks"][scene_number][person].append(task)
        return jsonify({"message": "Template tasks added successfully!"})
    else:
        return jsonify({"message": "Invalid room code. Please create a room first."})

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
    return jsonify({"message": "Tasks updated successfully!"})

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
                return jsonify({"message": "Task deleted successfully!"})
            except ValueError:
                return jsonify({"message": "Task not found."})
        else:
            return jsonify({"message": "Person not found in this scene."})
    else:
        return jsonify({"message": "Invalid room code or scene number."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

