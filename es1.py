from pysat.formula import CNF
from pysat.solvers import Solver

def encode_problem_es1(tasks, resources):
    cnf = CNF()
    max_time = max(task[2] for task in tasks)

    # Variables x[i][j][t] for task i accessing resource j at time t
    x = [[[i * resources * max_time + j * max_time + t + 1 
           for t in range(max_time)] 
           for j in range(resources)] 
           for i in range(len(tasks))]

    # Variables A[i][j][t] for task i starting non-preemptive access of resource j at time t
    A = [[[len(tasks) * resources * max_time + i * resources * max_time + j * max_time + t + 1 
           for t in range(max_time)] 
           for j in range(resources)] 
           for i in range(len(tasks))]

    # A1: Task i should not access two resources at the same time
    for i in range(len(tasks)):
        for j in range(resources):
            for jp in range(j + 1, resources):
                for t1 in range(tasks[i][0], tasks[i][2]):
                    for t2 in range(tasks[i][0], tasks[i][2]):
                        cnf.append([-x[i][j][t1], -x[i][jp][t2]])
                        print(f"Added clause A1: -x{i+1}{j+1}{t1} -x{i+1}{jp+1}{t2}")

    # A2: Each task must get some resource
    for i in range(len(tasks)):
        clause = []
        clause_str = []
        for j in range(resources):
            for t in range(tasks[i][0], tasks[i][2]):
                clause.append(x[i][j][t])
                clause_str.append(f"x{i+1}{j+1}{t}")
        cnf.append(clause)
        print(f"Added clause A2: {clause_str}")

    # A3: A resource can only be held by one task at a time
    for j in range(resources):
        for t in range(max_time):
            for i in range(len(tasks)):
                for ip in range(i + 1, len(tasks)):
                    if tasks[i][0] <= t < tasks[i][2] and tasks[ip][0] <= t < tasks[ip][2]:
                        cnf.append([-x[i][j][t], -x[ip][j][t]])
                        print(f"Added clause A3: -x{i+1}{j+1}{t} -x{ip+1}{j+1}{t}")
    # A4: Each task must have exactly one start time for accessing a resource non-preemptively
    for i in range(len(tasks)):
        clause = []
        clause_str = []
        for j in range(resources):
            for t in range(tasks[i][0], tasks[i][2] - tasks[i][1] + 1):
                clause.append(A[i][j][t])
                clause_str.append(f"A{i+1}{j+1}{t}")
        cnf.append(clause)
        print(f"Added clause A4: {clause_str}")

    # A5: Linking start variable to x variables
    for i in range(len(tasks)):
        for j in range(resources):
            for t in range(tasks[i][0], tasks[i][2] - tasks[i][1] + 1):
                # Reverse implication
                clause = [A[i][j][t]]
                clause_str = []
                clause_str.append(f"A{i+1}{j+1}{t}")

                # If A[i][j][t] is true, the task must hold the resource for its entire duration
                for k in range(tasks[i][1]):
                    if t + k < max_time:
                        cnf.append([-A[i][j][t], x[i][j][t+k]])
                        clause.append(-x[i][j][t+k])
                        clause_str.append(f"-x{i+1}{j+1}{t+k}")
                        print(f"Added clause A5: -A{i+1}{j+1}{t} x{i+1}{j+1}{t+k}")
                # If A[i][j][t] is true, the task must not hold the resource before t
                for tp in range(tasks[i][0], t):
                    cnf.append([-A[i][j][t], -x[i][j][tp]])
                    clause.append(x[i][j][tp])
                    clause_str.append(f"x{i+1}{j+1}{tp}")
                    print(f"Added clause A5: -A{i+1}{j+1}{t} -x{i+1}{j+1}{tp}")
                # If A[i][j][t] is true, the task must not hold the resource after t + e_i - 1
                for tp in range(t + tasks[i][1], tasks[i][2]):
                    if tp < max_time:
                        cnf.append([-A[i][j][t], -x[i][j][tp]])
                        clause.append(x[i][j][tp])
                        clause_str.append(f"x{i+1}{j+1}{tp}")
                        print(f"Added clause A5: -A{i+1}{j+1}{t} -x{i+1}{j+1}{tp}")

                cnf.append(clause)
                print(f"Added clause A5: {clause_str}")

    return cnf, max_time, x, A

# Example usage
tasks = [(0, 2, 2), (0, 2, 3)]  # Each task is a tuple (ri, ei, di)
resources = 2
cnf, max_time, x, A = encode_problem_es1(tasks, resources)

with Solver(name="glucose4") as solver:
    solver.append_formula(cnf.clauses)
    result = solver.solve()
    if result:
        model = solver.get_model()
        print("Satisfiable")
        for i in range(len(tasks)):
            for j in range(resources):
                for t in range(max_time):
                    if model[x[i][j][t] - 1] > 0:
                        print(f"Task {i} is accessing resource {j} at time {t}")
            for j in range(resources):
                for t in range(tasks[i][0], tasks[i][2] - tasks[i][1] + 1):
                    if model[A[i][j][t] - 1] > 0:
                        print(f"Task {i} starts non-preemptive access of resource {j} at time {t}")
    else:
        print("No solution found")