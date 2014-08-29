#!/usr/bin/env python
# coding=utf-8

from biopredyn import resources, workflow

# input values required for data generation
data_file = 'artificial_data.txt'
simulation_file = 'generate_data.xml'
noise = 'heteroscedastic'
std = 0.1 # experimental data standard deviation

rm = resources.ResourceManager()
wf = workflow.WorkFlow(simulation_file, rm)

task = wf.get_task_by_id('task_1')
task.set_tool('copasi') # choosing COPASI as simulation engine
task.run(True) # running the simulation and applying changes

report = wf.get_output_by_id('report_1') # processing output with noise
report.write_as_csv(data_file, artificial=True, noise_type=noise, std_dev=std)
