import pickle
import random
import time
import os
from multiprocessing import Process, Lock
from datetime import datetime

CHECKPOINT_FILE = "checkpoint.pkl"

log_lock = Lock() #lock for logging

def log_message(worker_num, message): #logging function
    """logging with timestamp and worker ID."""
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    with log_lock:
        print(f"[{timestamp}] Worker {worker_num}: {message}")

def worker(worker_num, checkpoint_lock): #worker function
    """Worker process with checkpointing and crash recovery."""
    state = load_checkpoint(worker_num, checkpoint_lock)
    if state is None:
        state = {"worker_num": worker_num, "task_count": 0, "completed": False}
        log_message(worker_num, f"Starting fresh (task_count: 0)")
    else:
        log_message(worker_num, f"Recovered from checkpoint (task_count={state['task_count']})")
    
    while state["task_count"] < 10 and not state["completed"]: #changes how many tasks are done by each worker
        try:
            if random.random() < 0.2: # 20% chance of failure
                raise RuntimeError("Process crashed!")
            
            time.sleep(0.5 + random.random())
            
            state["task_count"] += 1
            log_message(worker_num, f"Completed task {state['task_count']}")
            
            if state["task_count"] % 2 == 0: #saves checkpoint every 3 tasks or at the end (can be changed)
                checkpoint(worker_num, state, checkpoint_lock)
                
        except Exception as e:
            log_message(worker_num, f"{e}")
            old_task = state["task_count"]
            state = load_checkpoint(worker_num, checkpoint_lock)
            if state is None:
                log_message(worker_num, "No checkpoint found. Starting fresh.") #restarting message if no checkpoint is found
                state = {"worker_id": worker_num, "task_count": 0, "completed": False}
            else:
                log_message(worker_num, f"Restored progress (lost tasks {old_task} → {state['task_count']})") #restoring message
            time.sleep(1)  # Small delay before retry
    
    if not state["completed"]:
        state["completed"] = True
        checkpoint(worker_num, state, checkpoint_lock)
        log_message(worker_num, "finished")

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
  try:
    for i in range(1,4): #changes how may workers are created
          p = Process(target=worker, args=(i, checkpoint_lock))
          workers.append(p)
          p.start()
      
    for p in workers:
          p.join()
          
  finally: 
    checkpoint_lock.acquire()
    checkpoint_lock.release()
      
    print("\n All work done")