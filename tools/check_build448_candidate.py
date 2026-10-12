import os,json,urllib.request,time
base='https://api.github.com/repos/Nnentx/Ngelx/actions/workflows/NgelX-BUILD-448-CANDIDATE.yml/runs?branch=work/build-448-device-live-fixes&per_page=1'
for i in range(60):
 req=urllib.request.Request(base,headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'})
 with urllib.request.urlopen(req,timeout=30)as response:r=json.load(response)['workflow_runs']
 if r and r[0]['status']=='completed':
  if r[0]['conclusion']!='success':raise RuntimeError('App candidate failed; backend deployment blocked')
  print('Build448 app checks passed:',r[0]['id'],r[0]['head_sha']);break
 time.sleep(30)
else:raise RuntimeError('Candidate checks not completed; deployment blocked')
