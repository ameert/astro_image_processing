#++++++++++++++++++++++++++
#
# TITLE: settings.py
#
# PURPOSE: Holds the configuration settings
#          for run_batch.py 
#          It is imported by run_batch.py at run-time
#
# INPUTS: NONE
#
# OUTPUTS: NONE
#
# PROGRAM CALLS: NONE
#
# BY: Alan Meert
#     Department of Physics and Astronomy
#     University of Pennsylvania
#
# FOR: Folio Cluster 
#      Department of Physics and Astronomy
#      University of Pennsylvania
#
# DATE: 10 OCT 2012
#
#-----------------------------------

username='ameert'
band = 'i'
models = ['dev','ser','devexp','serexp']
job_prefix = ''
email_address = 'alan.meert@gmail.com'
pickle_path = '/data2/home/ameert/grid_scripts/pickled_backup'
jobs_to_run = range(1,5)

# if part of the submission has already run, set to 1
restart = 0

# set the parameters for job submission to the cluster
minnumqueuedtorun= 5 
maxnumqueuedtorun= 80
maxwaiting = 1
minnumqueuedholding = 5
