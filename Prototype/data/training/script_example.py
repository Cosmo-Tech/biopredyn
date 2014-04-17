from biopredyn import resources, workflow

rm = resources.ResourceManager() # Mandatory resource manager
wf = workflow.WorkFlow('training_3_3.xml', rm)

for m in wf.get_models():
  m.apply_changes()
  m.write_sbml(m.get_id() + "_changed.xml")
  m.init_tree() # Model reset

# Work flow execution
wf.run_tasks()
wf.process_outputs()