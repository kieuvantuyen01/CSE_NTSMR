import random
import os

def generate_task():
    return (
        random.randint(0, 5),    # release time
        random.randint(1, 5),     # execution time
        random.randint(10, 20)  # deadline time
    )

# Create the input folder if it doesn't exist
input_folder = "input/small"
os.makedirs(input_folder, exist_ok=True)

for i in range(1, 101):
    filename = os.path.join(input_folder, f"small_{i}.txt")
    num_tasks = random.randint(5, 10)  # Assuming 5-10 tasks per file
    
    tasks = [generate_task() for _ in range(num_tasks)]
    
    with open(filename, 'w') as f:
        f.write(f"{num_tasks}\n")
        f.write(str(tasks))

print("Generated 100 test cases in the 'input' folder.")
