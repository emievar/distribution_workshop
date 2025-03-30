import pickle
import random
import time
import multiprocessing
import os
from multiprocessing import Process, Lock
from datetime import datetime

CHECKPOINT_FILE = "checkpoint.pkl"

log_lock = Lock() #lock for logging

def log_message(worker_id, message): #logging function
    """logging with timestamp and worker ID."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    with log_lock:
        print(f"[{timestamp}] Worker {worker_id}: {message}")

def worker(worker_id, checkpoint_lock): #worker function
    """Worker process with checkpointing and crash recovery."""
    state = load_checkpoint(worker_id, checkpoint_lock)
    if state is None:
        state = {"worker_id": worker_id, "task_count": 0, "completed": False}
        log_message(worker_id, f"Starting fresh (task_count: 0)")
    else:
        log_message(worker_id, f"Recovered from checkpoint (task_count={state['task_count']})")
    
    while state["task_count"] < 10 and not state["completed"]:
        try:
            if random.random() < 0.2: # 20% chance of failure
                raise RuntimeError("Crashed")
            
            time.sleep(0.5 + random.random())
            
            state["task_count"] += 1
            log_message(worker_id, f"Completed task {state['task_count']}")
            
            if state["task_count"] % 3 == 0 or state["task_count"] == 10: #saves checkpoint every 3 tasks or at the end
                checkpoint(worker_id, state, checkpoint_lock)
                
        except Exception as e:
            log_message(worker_id, f"{e}")
            old_task = state["task_count"]
            state = load_checkpoint(worker_id, checkpoint_lock)
            if state is None:
                log_message(worker_id, "No checkpoint found, restarting from 0") #restarting message if no checkpoint is found
                state = {"worker_id": worker_id, "task_count": 0, "completed": False}
            else:
                log_message(worker_id, f"Restored progress (lost tasks {old_task} → {state['task_count']})") #restoring message
            time.sleep(1)  # Small delay before retry
    
    if not state["completed"]:
        state["completed"] = True
        checkpoint(worker_id, state, checkpoint_lock)
        log_message(worker_id, "finished")

def checkpoint(worker_id, state, lock): #checkpoint function
    """Save state to checkpoint file."""
    with lock:
        try:
            all_states = {}
            if os.path.exists(CHECKPOINT_FILE):
                with open(CHECKPOINT_FILE, "rb") as f:
                    all_states = pickle.load(f)
            
            all_states[worker_id] = state
            
            with open(CHECKPOINT_FILE, "wb") as f:
                pickle.dump(all_states, f)
            
            log_message(worker_id, f"Checkpoint saved at task: {state['task_count']}")
        except Exception as e:
            log_message(worker_id, f"Failed to save checkpoint: {e}")

def load_checkpoint(worker_id, lock): #load checkpoint function
    """Load state from checkpoint file."""
    with lock:
        try:
            if os.path.exists(CHECKPOINT_FILE):
                with open(CHECKPOINT_FILE, "rb") as f:
                    all_states = pickle.load(f)
                return all_states.get(worker_id)
        except Exception as e:
            log_message(worker_id, f"Failed to load checkpoint: {e}")
        return None

def cleanup_checkpoint(): #cleanup function
    """Remove old checkpoint file if it exists."""
    try:
        if os.path.exists(CHECKPOINT_FILE):
            os.remove(CHECKPOINT_FILE)
    except Exception as e:
        print(f"Error cleaning up checkpoint: {e}")

if __name__ == "__main__": #main function
    cleanup_checkpoint()  #cleans up old checkpoint file 
    checkpoint_lock = Lock()
    

    workers = []
    for i in range(3): #changes how may workers are created
        p = Process(target=worker, args=(i, checkpoint_lock))
        workers.append(p)
        p.start()
    
    for p in workers:
        p.join()
    
    print("\n All work done")