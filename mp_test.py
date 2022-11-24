from subprocess import Popen, PIPE
import json

# from utils import PersonData
commands = [r"python utils\utils.py 0000-0003-1706-0205",r"python utils\utils.py 0000-0002-7851-4330",r"python utils\utils.py 0000-0001-7387-9210"]
# out = check_output(["python", r"utils\utils.py",'0000-0003-1706-0205'])

procs = [ Popen(i,text=True, stdout=PIPE) for i in commands  ]
for p in procs:
   p.wait()
for p in procs:
    print(p.communicate()[0])
# res = procs[0].communicate()[0]
# res = json.loads(res)
# print(res)