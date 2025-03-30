import multiprocessing
import time
import random

class Producer(multiprocessing.Process):
  def __init__(self, q):
    super().__init__()
    self.q = q
  
  def run(self):
    for i in range(10):
      item = random.randint(1,100) #rng
      self.q.put(item) #puts the item into q
      print(f"Produced: {item}")
      time.sleep(random.uniform(0.1, 0.5)) # Simulate work  
    self.q.join() #waits for all items to be processed

class Consumer(multiprocessing.Process):
  def __init__(self, q, name):
    super().__init__()
    self.q = q
    self.name = name

  def run(self):
    while True:
      try:
        item = self.q.get(timeout = 1) #fetch items
        
        print(f"{self.name} consumed: {item}")
        time.sleep(random.uniform(0.1, 0.5))
        self.q.task_done()
      except:
        print(f"{self.name} exiting")
        break

if __name__ == "__main__":
  queue_buffer = multiprocessing.JoinableQueue()
  
  #new producer and consumers
  producer = Producer(queue_buffer)
  consumer1 = Consumer(queue_buffer, "Consumer 1")
  consumer2 = Consumer(queue_buffer, "Consumer 2")
  
  #run process
  producer.start()
  consumer1.start()
  consumer2.start()  
  
  producer.join()
  queue_buffer.join() # Wait for all tasks to finish
  
  # Consumers are in infinite loops, so we need to terminate them
  consumer1.join(timeout=0.1)
  consumer2.join(timeout=0.1)
  
  if consumer1.is_alive():
    consumer1.terminate()
  if consumer2.is_alive():
    consumer2.terminate()