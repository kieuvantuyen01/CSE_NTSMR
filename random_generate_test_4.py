import random
import os

def generate_task():
    return (
        random.randint(0, 7),    # release time
        random.randint(3, 7),     # execution time
        random.randint(15, 35)  # deadline time
    )

# Create the input folder if it doesn't exist
input_folder = "input/medium"
os.makedirs(input_folder, exist_ok=True)

for i in range(1, 101):
    filename = os.path.join(input_folder, f"medium_{i}.txt")
    num_tasks = random.randint(25, 50)  # Assuming 50-100 tasks per file
    
    tasks = [generate_task() for _ in range(num_tasks)]
    
    with open(filename, 'w') as f:
        f.write(f"{num_tasks}\n")
        f.write(str(tasks))

print("Generated 100 test cases in the 'input' folder.")
