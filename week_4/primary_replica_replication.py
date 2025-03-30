print('python is running')

# Primary node
primary_data = {}

# Replica nodes
replica1_data = {}
replica2_data = {}

# Replication log
replication_log = set()

# Primary Node status
primary_node = True

def write_to_primary(key, value):
  """Add or update a key-value pair in the primary."""
  if not primary_node:
    return "Primary node error"
  primary_data[key] = value
  # Log the operation
  replication_log.add(key)
  # Return success message
  return f"Value '{value}' written to key '{key}' in primary"

def replicate_to_replicas():
  """Propagate all changes from primary to replicas."""
  if not primary_node:
    return "Primary node error"
  #task 3
  for key in replication_log:
    if key in replication_log:
      replica1_data[key] = primary_data[key]
      replica2_data[key] = primary_data[key]
      
  replication_log.clear()
  return "Replication completed"

def read_from_primary(key):
  """Read a value from the primary."""
  if not primary_node:
    return "Primary node error"
  return primary_data.get(key, f"Key '{key}' not found")

def read_from_replica(replica_num, key):
  """Read a value from a specific replica."""
  if replica_num == 1:
    return replica1_data.get(key, f"Key '{key}' not found in replica 1")
  elif replica_num == 2:
    return replica2_data.get(key, f"Key '{key}' not found in replica 2")
  else:
    return "Invalid replica number"
  
def detect_primary_node():
  """Detect if the primary node is available"""
  return primary_node

def simulate_failure():
  """Simulate a failed primary node"""
  global primary_node
  primary_node = False
  print("\nPrimary node is not working")
  
def promote_replica_to_primary(replica_num):
  global primary_data, primary_node
  if replica_num == 1:
    primary_data = replica1_data.copy()
  elif replica_num == 2:
    primary_data = replica2_data.copy()
  else:
    return "Invalid replica number"
  primary_node = True
  return f"Replica {replica_num} promoted"
  
def test_basic_replication():
  """Test basic write and replication functionality."""
  print("\n=== BASIC WRITE AND REPLICATION ===")
  # Clear all data
  primary_data.clear()
  replica1_data.clear()
  replica2_data.clear()
  replication_log.clear()
  # Add data to primary
  print("Writing data to primary...")
  print(write_to_primary("student1", "Alice"))
  print(write_to_primary("student2", "Bob"))
  print(write_to_primary("student3", "Charlie"))
  # Check data in primary
  print("\nReading from primary:")
  print(f"student1: {read_from_primary('student1')}")
  print(f"student2: {read_from_primary('student2')}")
  print(f"student3: {read_from_primary('student3')}")
  # Check data in replicas before replication
  print("\nReading from replicas before replication:")
  print(f"Replica 1 - student1: {read_from_replica(1, 'student1')}")
  print(f"Replica 2 - student2: {read_from_replica(2, 'student2')}")
  # Perform replication
  print("\nPerforming replication...")
  print(replicate_to_replicas())
  # Check data in replicas after replication
  print("\nReading from replicas after replication:")
  print(f"Replica 1 - student1: {read_from_replica(1, 'student1')}")
  print(f"Replica 1 - student2: {read_from_replica(1, 'student2')}")
  print(f"Replica 2 - student1: {read_from_replica(2, 'student1')}")
  print(f"Replica 2 - student3: {read_from_replica(2, 'student3')}")
  
  #test for task 3
  print("\nUpdating data in primary...")
  print(write_to_primary("student1", "Alicia"))
  print(write_to_primary("student4", "Dan"))
  print(f"student1: {read_from_primary('student1')}")
  print(f"student4: {read_from_primary('student4')}")
  print("\nDAta in replicas before replication")
  print(f"Replica 1 - student1: {read_from_replica(1, 'student1')}")
  print(f"Replica 2 - student4: {read_from_replica(2, 'student4')}")
  print("\nPerforming replication...")
  print(replicate_to_replicas())
  print("\nData in replicas after replication...")
  print(f"Replica 1 - student1: {read_from_replica(1, 'student1')}")
  print(f"Replica 1 - student4: {read_from_replica(1, 'student4')}")
  print(f"Replica 2 - student1: {read_from_replica(2, 'student1')}")
  print(f"Replica 2 - student4: {read_from_replica(2, 'student4')}")
  print("\nReplication log after replication...")
  print(f"Replication log: {replication_log}")
  
  #test for task 4
  print("\nWriting data to primary...")
  print(write_to_primary("student1", "Alice"))
  print(write_to_primary("student2", "Bob"))
  print(write_to_primary("student3", "Charlie"))
  print("\nPerforming replication...")
  print(replicate_to_replicas())
  print("\nSimulating primary failure...")
  simulate_failure()
  print("\nAttempting to write to primary after failure...")
  print(write_to_primary("student4", "Dan"))
  print("\nPromoting replica 1 to primary...")
  print(promote_replica_to_primary(1))
  print("\nWriting to the new primary...")
  print(write_to_primary("student4", "Dan"))
  print("\nPerforming replication...")
  print(replicate_to_replicas())
  print("\nReading from replicas...")
  print(f"Replica 1 - student4: {read_from_replica(1, 'student4')}")
  print(f"Replica 2 - student4: {read_from_replica(2, 'student4')}")
  print("\nReading current primary")
  print(f"student1: {read_from_primary('student1')}")
  print(f"student2: {read_from_primary('student2')}")
  print(f"student3: {read_from_primary('student3')}")
  print(f"student4: {read_from_primary('student4')}")

  
if __name__ == "__main__":
  test_basic_replication()