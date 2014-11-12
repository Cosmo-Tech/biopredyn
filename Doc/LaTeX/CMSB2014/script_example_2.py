from biopredyn import resources, workflow
from COPASI import CCopasiMethod
# required inputs
simulation_file = "febs_workflow.xml"
calibration_file = "calibration_data.txt"
validation_file = "validation_data.txt"
observables = ["sp_C"]
unknowns = ["k1", "k2", "k3"] # parameters to be estimated
min_unknown_values = [0.0, 0.0, 0.0] # lower bound for unknowns
max_unknown_values = [10.0, 10.0, 10.0] # upper bound for unknowns
algo = CCopasiMethod.LevenbergMarquardt 
# uses BioPreDyn API to estimate parameters
rm = resources.ResourceManager()
wf = workflow.WorkFlow(simulation_file, rm)
sim = wf.get_simulations()[0]
model_result = sim.run_as_parameter_estimation(
  wf.get_models()[0], calibration_file, validation_file,
  observables, unknowns, min_unknown_values, max_unknown_values, algo, rm)
