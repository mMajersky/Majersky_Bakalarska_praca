import json
import os
from scripts.utils import resource_path
from scripts.utils import get_levels


LEVEL_STATE_FILE = "level_status.json"
LEVEL_STATE_FOLDER = "lvls"
LEVEL_STATE_READ_PATH = resource_path(os.path.join(LEVEL_STATE_FOLDER, LEVEL_STATE_FILE))
LEVEL_STATE_WRITE_PATH = os.path.join(os.getcwd(), LEVEL_STATE_FOLDER, LEVEL_STATE_FILE)

def load_level_state():
    if os.path.exists(LEVEL_STATE_WRITE_PATH):  # Čítame z write path
        with open(LEVEL_STATE_WRITE_PATH) as f:
            return json.load(f)
    return {}


def save_level_state(state):
    os.makedirs(os.path.dirname(LEVEL_STATE_WRITE_PATH), exist_ok=True)
    with open(LEVEL_STATE_WRITE_PATH, "w") as f:
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
    levels = get_levels()
    new_state = {}

    for mode in levels:
        new_state[mode] = {}
        for i, lvl in enumerate(levels[mode]):
            label = f"Level {i+1}"
            new_state[mode][label] = {
                "completed": False,
                "file": lvl if mode != "Sokoban" else None
            }

    save_level_state(new_state)
    print("🔄 Level progress reset.")

