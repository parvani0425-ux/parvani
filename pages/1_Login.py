import json
import datetime

# Load history
def load_history():
    try:
        with open("login_history.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_history(username):
    history = load_history()
    history.append({
        "user": username,
        "time": str(datetime.datetime.now())
    })
    with open("login_history.json", "w") as f:
        json.dump(history, f, indent=4)

# After successful login:
if login_success:
    save_history(username)
