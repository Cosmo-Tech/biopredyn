from biopredyn import workflow, resources as rm
wf = workflow.WorkFlow('wf_1.xml', rm.ResourceManager())
for m in wf.get_models():
  m.apply_changes() # Apply changes to current model
  m.write_sbml(m.get_id() + "_changed.xml") # Write it
  m.init_tree() # Reset model
wf.run_tasks() # Execute work flow
wf.process_outputs()
