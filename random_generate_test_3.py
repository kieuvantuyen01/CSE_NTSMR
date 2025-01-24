import random
import os

def generate_task():
    return (
        random.randint(0, 10),    # release time
        # random.randint(5, 10),     # execution time
        random.randint(40, 70),     # execution time
        random.randint(100, 120)  # deadline time
    )

# Create the input folder if it doesn't exist
input_folder = "input/long_duration"
os.makedirs(input_folder, exist_ok=True)

for i in range(1, 101):
    filename = os.path.join(input_folder, f"long_duration_{i}.txt")
    # num_tasks = random.randint(50, 100)  # Assuming 50-100 tasks per file
    num_tasks = 200

    tasks = [generate_task() for _ in range(num_tasks)]
    
    with open(filename, 'w') as f:
        f.write(f"{num_tasks}\n")
        f.write(str(tasks))

print("Generated 100 test cases in the 'input' folder.")
