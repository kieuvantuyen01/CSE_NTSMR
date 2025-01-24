import gurobipy as gp
from gurobipy import GRB

try:
    # Create empty model to access Gurobi
    m = gp.Model()
    
    # Get version info
    print(f"Gurobi version: {gp.gurobi.version()}")
    print(f"Gurobipy interface version: {gp.__version__}")
    
    # Optional: Get more detailed version info
    print("\nDetailed version info:")
    print(f"Platform: {gp.platform}")
    print(f"License info: {m.getParamInfo('LicenseID')}")
    
    # Clean up
    m.dispose()
    
except gp.GurobiError as e:
    print(f"Error: {e}")