import pickle
import random
import time

CHECKPOINT_FILE = "checkpointexample.pkl"

def save_checkpoint(state):
  """Save the current state to a checkpoint file."""
  with open(CHECKPOINT_FILE, "wb") as f:
    pickle.dump(state, f)
    print(f"Checkpoint saved: {state}")

def load_checkpoint():
  """Load the last saved checkpoint."""
  try:
    with open(CHECKPOINT_FILE, "rb") as f:
      state = pickle.load(f)
      print(f"Restored from checkpoint: {state}")
    return state
  except FileNotFoundError:
    print("No checkpoint found. Starting fresh.")
    return {"task_count": 0}

# Simulate a process performing a task
state = load_checkpoint()
for i in range(state["task_count"], 10):
  if random.random() < 0.2: # 20% chance of failure
    print("Process crashed!")
    state = load_checkpoint()
    continue # Restart from checkpoint
  state["task_count"] = i + 1
  save_checkpoint(state)
  time.sleep(1)