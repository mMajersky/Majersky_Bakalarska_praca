import json
import os

LEVEL_STATE_PATH = "lvls/level_status.json"

def load_level_state():
    if os.path.exists(LEVEL_STATE_PATH):
        with open(LEVEL_STATE_PATH, "r") as f:
            return json.load(f)
    return {}

def save_level_state(state):
    with open(LEVEL_STATE_PATH, "w") as f:
        json.dump(state, f, indent=4)

def mark_level_completed(mode, level_label, file_name=None):
    state = load_level_state()
    if mode not in state:
        state[mode] = {}
    if level_label not in state[mode]:
        state[mode][level_label] = {"completed": False}
    state[mode][level_label]["completed"] = True
    if file_name:
        state[mode][level_label]["file"] = file_name
    save_level_state(state)

def is_level_unlocked(mode, level_label, index):
    if index == 0:
        return True  # Prvý level je vždy odomknutý
    prev_label = f"Level {index}"  # napr. pred Level 2 je Level 1
    state = load_level_state()
    return state.get(mode, {}).get(prev_label, {}).get("completed", False)

def reset_progress():
    state = load_level_state()
    for mode in state:
        for lvl in state[mode]:
            state[mode][lvl]["completed"] = False
    save_level_state(state)
    print("🔄 Level progress reset.")

