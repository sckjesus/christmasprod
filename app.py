from flask import Flask, render_template, request, jsonify
import uuid

app = Flask(__name__)

# Dictionary to store room data
rooms = {}

# Predefined template
tasks_template = {
    "Sam": [("1 - Strike", "Table"), ("2 - Set Up", "Table")],
    "Mila": [("1 - Strike", "Table")],
    "Danny": [("1 - Set Up", "Table")],
    "Allison": [("1 - Set Up", "Wall")],
    "Messi": [("1 - Set Up", "Plants")],
}

# Dictionary to store person's color
person_colors = {
    "Sam": "#FF6347",  # Red
    "Mila": "#4682B4",  # Blue
    "Danny": "#32CD32",  # Green
    "Allison": "#FFD700",  # Yellow
    "Messi": "#8A2BE2",  # Blue Violet
}


# Route: Home
@app.route("/")
def home():
    return render_template("index.html")


# API: Create a Room
@app.route("/create_room", methods=["POST"])
def create_room():
    room_code = str(uuid.uuid4())[:8]  # Generate unique room code
    rooms[room_code] = {"tasks": {}}
    return jsonify({"message": f"Room created! Your code is: {room_code}", "room_code": room_code})


# API: Add Template Tasks
@app.route("/add_template_tasks", methods=["POST"])
def add_template_tasks():
    data = request.json
    room_code = data.get("room_code")

    if room_code in rooms:
        rooms[room_code]["tasks"] = {}
        for person, task_list in tasks_template.items():
            for scene, task in task_list:
                scene_parts = scene.split(" - ")
                if len(scene_parts) > 1:
                    scene_number = scene_parts[0].strip()
                    scene_name = scene_parts[1].strip()
                else:
                    scene_number = "0"
                    scene_name = scene.strip()

                if scene_number not in rooms[room_code]["tasks"]:
                    rooms[room_code]["tasks"][scene_number] = {}

                if person not in rooms[room_code]["tasks"][scene_number]:
                    rooms[room_code]["tasks"][scene_number][person] = []

                rooms[room_code]["tasks"][scene_number][person].append(task)
        return jsonify({"message": "Template tasks added successfully!"})
    else:
        return jsonify({"message": "Invalid room code. Please create a room first."})


# API: View Tasks
@app.route("/view_tasks/<room_code>")
def view_tasks(room_code):
    if room_code not in rooms:
        return jsonify({"message": "Invalid room code. Please create a room first."})

    return jsonify({"tasks": rooms[room_code]["tasks"]})

@app.route("/join_room", methods=["GET", "POST"])
def join_room():
    if request.method == "POST":
        room_code = request.form.get("room_code")
        if room_code in rooms:
            return render_template("room.html", room_code=room_code, tasks=rooms[room_code]["tasks"])
        else:
            return render_template("join_room.html", error="Invalid room code. Please try again.")
    
    return render_template("join_room.html")

# API: Update Tasks
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
