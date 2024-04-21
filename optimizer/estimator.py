import json
from gurobipy import *

# Get the parameter values passed from the command
if len(sys.argv) < 2:
    raise 'no argument given'
elif sys.argv[1] == 'contig':
    FORCE_CONTIGUOUS_FORWARD = True
elif sys.argv[1] == 'noncontig':
    FORCE_CONTIGUOUS_FORWARD = False
else:
    raise 'argument should be contig/noncontig'

# Load input
graph = json.load(sys.stdin)  # operator graph in JSON format
nodes = {}

# Init solver
model = Model("minimize_maxload")
model.setParam("LogToConsole", 0)
model.setParam("LogFile", "gurobi.log")
model.setParam("MIPGap", 0.01)
model.setParam("TimeLimit", 1200)
model.setParam("MIPFocus", 1)

# if this is too large, then the reformulated
# ex-quadratic constraints can behave funky
model.setParam("IntFeasTol", 1e-6)

# Define variables
x = {}  # key will be (node_id, machine_id), value will be 1 or 0
d = {}  # key will be (node_id_1, node_id_2), value will be 1 or 0
for node in graph.getNodes():
    for machine_id in range(deviceNum):
        x[node.id, machine_id] = model.addVar(vtype=GRB.BINARY)
for edge in graph.getEdges():
    d[edge.sourceID, edge.destID] = model.addVar(vtype=GRB.BINARY)

# TotalLatency that we are minimizing
TotalLatency = model.addVar(vtype = GRB.CONTINUOUS, lb=0.0)
for node_id, node in nodes.items():
    model.addConstr(TotalLatency >= latency[node_id])

# Add constraints
# schedule every node on exactly one machine
for node_id, node in nodes.items():
    times_scheduled = LinExpr()
    for machine_id in range(1 + maxSubgraphs):
        times_scheduled += x[node_id, machine_id]
    model.addConstr(times_scheduled == 1)

# Set the target of solver
model.setObjective(TotalLatency, GRB.MINIMIZE)

# Run the solver
sys.stdout.flush()
model.optimize()

if model.Status == GRB.Status.INFEASIBLE:
    raise "infeasible"
elif model.Status == GRB.Status.OPTIMAL:
    print("Value is:", TotalLatency.X)
else:
    raise "Wrong status code"

print('Runtime = ', "%.2f" % model.Runtime, 's', sep='')

result = {}

del model
disposeDefaultEnv()
print(json.dumps(result))