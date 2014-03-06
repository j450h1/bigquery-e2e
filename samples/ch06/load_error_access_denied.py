import json
import os
import time

from apiclient.discovery import build
import httplib2
# Sample code authorization support.
import auth

# Set this to your sample project id.
PROJECT_ID = 317752944021
JOB_ID = 'ch06_%d' % int(time.time())
body = {
    'jobReference': {
        'jobId': JOB_ID
        },
    'configuration': {
        'load': {
            'destinationTable': {
                'projectId': 'publicdata',
                'datasetId': 'samples',
                'tableId': 'mypersonaltable'
                }
            }
        }
    }
loadConfig = body['configuration']['load']
# Setup the job here.
# load[property] = value
loadConfig['sourceUris'] = [
    'gs://bigquery-e2e/chapters/06/sample.csv',
    ]
# End of job configuration.

bq = build('bigquery', 'v2',
           http=auth.get_creds().authorize(httplib2.Http()))
jobs = bq.jobs()

start = time.time()
# Create the job.
result = jobs.insert(projectId=PROJECT_ID,
                     body=body).execute()
print json.dumps(result, indent=2)
# Wait for completion.
done = False
while not done:
    time.sleep(5)
    result = jobs.get(projectId=PROJECT_ID, jobId=JOB_ID).execute()
    print "%s %ds" % (result['status']['state'], time.time() - start)
    done = result['status']['state'] == 'DONE'
# Print all errors and warnings.
for err in result['status'].get('errors', []):
    print json.dumps(err, indent=2)
# Check for failure.
if 'errorResult' in result['status']:
    print 'FAILED'
    print json.dumps(result['status']['errorResult'], indent=2)
else:
    print 'SUCCESS'
