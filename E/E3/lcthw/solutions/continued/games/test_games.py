import subprocess
cases=[("",["Hall."]),("w\nq\n",["blocked"]),("n\ne\nn\ne\nq\n",["Throne.","Kitchen.","Garden.","Tower."]),("n\nw\n"+"a\n"*10+"q\n",["Arena.","dead","empty"])]
for data,parts in cases:
 p=subprocess.run(["valgrind","--error-exitcode=99","--leak-check=full","./adventure"],input=data,text=True,capture_output=True);assert p.returncode==0,(p.stdout,p.stderr)
 assert all(x in p.stdout for x in parts);assert "ERROR SUMMARY: 0 errors" in p.stderr and "in use at exit: 0 bytes" in p.stderr
p=subprocess.run(["valgrind","--error-exitcode=99","--leak-check=full","./walk"],text=True,capture_output=True);assert p.returncode==0 and "Entry.\nBridge.\nTreasure.\ntreasure reached" in p.stdout and "ERROR SUMMARY: 0 errors" in p.stderr
print("PASS two games, five scenarios, clean ownership")
