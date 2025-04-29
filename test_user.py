import requests
SERVER_URL = "https://cse198.pythonanywhere.com/"
#SERVER_URL = "http://127.0.0.1:5000/"
user_id = None

#
def create_user(name):
    global user_id
    response = requests.post(f"{SERVER_URL}/create_user", json={"name": name})
    if response.status_code == 200:
        user_id = response.json()["user_id"]
        print(f"User created! Your ID is: {user_id}")
    else:
        print("Failed to create user:", response.json())

def submit_solution(problem_number, solution_text):
    if not user_id:
        print("Error: You must create a user first!")
        return
    
    payload = {
        "user_id": user_id,
        "problem_number": problem_number,
        "solution": solution_text
    }
    response = requests.post(f"{SERVER_URL}/submit_solution", json=payload)
    
    if response.status_code == 200:
        print(f"Success! Your new score is {response.json()['new_score']}")
    else:
        print("Failed to submit solution:", response.json())

def check_user_id():
    print(f"Your saved user ID is: {user_id}")

create_user('alice')
submit_solution(1, 'asdf')
submit_solution(1, 'sad')
submit_solution(1, 'letmein')
submit_solution(2, 'shrug')
submit_solution(2, 'freepass')
