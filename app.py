from flask import Flask, request, redirect, url_for, render_template, jsonify
import uuid
import random

app = Flask(__name__)

users = {}

emojis = [
    '🐱', '🐶', '🐵', '🐸', '🐧', '🦄', '🐝', '🦊', '🐼', '🐢',
    '🐙', '🐬', '🐳', '🦋', '🐞', '🐍', '🦕', '🦖', '🦐', '🦑',
    '🦞', '🦦', '🦔', '🦇', '🦉', '🐺', '🐴', '🐮', '🐷', '🐰',
    '🐤', '🐥', '🦢', '🦚', '🦜', '🦩', '🦦'
]
assigned_emojis = []

def pick_unique_emoji():
    global assigned_emojis
    available = list(set(emojis) - set(assigned_emojis))
    if not available:
        assigned_emojis.clear()
        available = emojis.copy()
    emoji = random.choice(available)
    assigned_emojis.append(emoji)
    return emoji

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        action = request.form.get("action")
        user_id = request.form.get("user_id")

        if action == "clear_all":
            users.clear()
        elif action == "remove" and user_id in users:
            del users[user_id]
        elif action == "increase" and user_id in users:
            users[user_id]['score'] += 100
        elif action == "decrease" and user_id in users:
            users[user_id]['score'] -= 100

        return redirect(url_for('admin'))

    return render_template("admin.html")

@app.route("/create_user", methods=['POST'])
def create_user():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return {"error": "Name is required"}, 400

    user_id = str(uuid.uuid4())
    emoji = pick_unique_emoji()

    users[user_id] = {
        "id": user_id,
        "name": name,
        "score": 0,
        "icon": emoji,
        "solved_problems": set()
    }
    return {"user_id": user_id}

@app.route("/submit_solution", methods=["POST"])
def submit_solution():
    data = request.get_json()
    user_id = data.get("user_id")
    problem_number = data.get("problem_number")
    solution = data.get("solution")

    if not user_id or not problem_number or not solution:
        return {"error": "Missing fields"}, 400
    if user_id not in users:
        return {"error": "Invalid user ID"}, 404

    problem_number = int(problem_number)

    correct_answers = {
        1: "letmein",
        2: "freepass",
        3: "rainbow",
        4: "l",
        5: "ava",
        6: "ch1kn"
    }

    if problem_number in users[user_id]['solved_problems']:
        return {"message": "Problem already solved."}, 400

    awarded_score = 0
    correct_answer = correct_answers.get(problem_number)

    if correct_answer and solution.strip().lower() == correct_answer:
        awarded_score = 100

    users[user_id]['score'] += awarded_score
    users[user_id]['solved_problems'].add(problem_number)

    return {"new_score": users[user_id]['score']}

@app.route("/api/leaderboard")
def api_leaderboard():
    sorted_users = sorted(users.values(), key=lambda x: x['score'], reverse=True)

    # Convert each user's 'solved_problems' set into a list
    serializable_users = []
    for user in sorted_users:
        user_copy = user.copy()
        user_copy['solved_problems'] = list(user_copy['solved_problems'])
        serializable_users.append(user_copy)

    return jsonify(serializable_users)

if __name__ == "__main__":
    app.run(debug=True)
