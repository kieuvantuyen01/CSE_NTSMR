from pysat.formula import CNF
from pysat.solvers import Solver

def encode_problem_es2(tasks, resources):
    cnf = CNF()

    # Get the maximum time from the tasks' deadlines
    time = max(task[2] for task in tasks)

    # Variables y[i][j][t] for task i starts accessing resource j at time t
    y = [[[t + j * time + i * time * resources + 1 for t in range(time)] for j in range(resources)] for i in range(len(tasks))]

    # Constraint B1: Task i should not access two resources at the same time
    for i in range(len(tasks)):
        for j in range(resources):
            for jp in range(j + 1, resources):
                for t1 in range(time):
                    for t2 in range(time):
                        cnf.append([-y[i][j][t1], -y[i][jp][t2]])

    # Constraint B2: Each task must get some resource within its time window
    for i in range(len(tasks)):
        clause = []
        for j in range(resources):
            for t in range(tasks[i][0], tasks[i][2]):  # Time window from ri to di-1
                clause.append(y[i][j][t])
        cnf.append(clause)

    # Constraint B3: A resource can only be held by one task at a time
    for i in range(len(tasks)):
        for ip in range(i + 1, len(tasks)):
            for j in range(resources):
                for t1 in range(tasks[i][0], tasks[i][2]):  # Time window from ri to di-1
                    for t2 in range(t1, min(t1 + tasks[i][1], time)):  # Ensure t2 respects the execution time of task i
                        if t2 < time:  # Boundary check
                            cnf.append([-y[i][j][t1], -y[ip][j][t2]])

    # Constraint B4: Non-preemptive resource access by a task
    for i in range(len(tasks)):
        for j in range(resources):
            for t1 in range(tasks[i][0], tasks[i][2] - tasks[i][1] + 1):  # Ensure t1 respects the task's window
                for t2 in range(t1 + 1, min(t1 + tasks[i][1], time)):  # Ensure t2 respects the execution time of task i
                    cnf.append([-y[i][j][t1], -y[i][j][t2]])

    return cnf, time, y

# Example usage of the encoding function with a SAT solver
tasks = [(0, 2, 2), (0, 2, 3)]  # Each task is a tuple (ri, ei, di)
resources = 2
cnf, time, y = encode_problem_es2(tasks, resources)

with Solver(name="glucose4") as solver:
    solver.append_formula(cnf.clauses)
    result = solver.solve()
    if result:
        model = solver.get_model()
        for i in range(len(tasks)):
            for j in range(resources):
                for t in range(time):
                    if model[y[i][j][t] - 1] > 0:
                        print(f"Task {i} starts accessing resource {j} at time {t}")
    else:
        print("No solution found")