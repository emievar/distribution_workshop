import multiprocessing
import time

class SharedCounterWithLock:
  def __init__(self):
    self.count = multiprocessing.Value("i", 0) # Shared integer
    self.lock = multiprocessing.Lock() # Mutex lock
  
  def increment(self):
    with self.lock: # Ensures only one process at a time (comment out to test lock)
      local_count = self.count.value
      time.sleep(0.01) # Simulate processing time
      local_count += 1
      self.count.value = local_count
      
class SharedCounterWithoutLock:
  def __init__(self):
    self.count = multiprocessing.Value("i", 0) # Shared integer
  
  def increment(self):
    local_count = self.count.value
    time.sleep(0.01) # Simulate processing time
    local_count += 1
    self.count.value = local_count

def worker(counter, num_increments):
    for _ in range(num_increments):
      counter.increment()

if __name__ == "__main__":
    amount_of_processes = 5
    incrementing = 100
    multi_trials = 8
    
    #with lock
    print("trials 'with' lock")
    with_lock_results = []
    for _ in range(multi_trials):
      counter = SharedCounterWithLock()
      processes = [multiprocessing.Process(target=worker, args=(counter, incrementing)) for _ in range(amount_of_processes)]
      
      for p in processes:
        p.start()
        
      for p in processes:
        p.join()
        
      with_lock_results.append(counter.count.value)
    print("With lock results:", with_lock_results)
    
    #without lock
    print("trials 'without' lock")
    with_lockout_results = []
    for _ in range(multi_trials):
      counter = SharedCounterWithoutLock()
      processes = [multiprocessing.Process(target=worker, args=(counter, incrementing)) for _ in range(amount_of_processes)]
      
      for p in processes:
        p.start()
        
      for p in processes:
        p.join()
        
      with_lockout_results.append(counter.count.value)
    print("With lock results:", with_lockout_results)
    
    # the results show that without a lock, processes race to increment the counter causing errors which return a value that is always less than the expected of 500