import subprocess

scenarios = ["bw", "delay", "loss"]
values = {"bw": [50, 100, 200, 1000],
          "delay": [100, 250, 500],
          "loss": [10, 15, 25]}

baseClient = ["docker", "exec", "client", "scripts/dash-emulator.py", "--abr"]
clients = [
  baseClient + ["buffer-based", "--dump-results"],
  baseClient + ["bandwidth-based", "--dump-results"],
  baseClient + ["hybrid", "--dump-results"],
]
repCount = 3

for scenario in scenarios:
  callArray = ["docker", "exec", "server", "tc", "qdisc", "add", "dev", "eth0", "root", "netem"]
  suffix = ""
  if scenario == "bw":
    callArray.append("rate")
    suffix = "Kbps"
  elif scenario == "delay":
    callArray.append("delay")
    suffix = "ms"
  elif scenario == "loss":
    callArray.append("loss")
    suffix = "%"
  
  for value in values[scenario]:
    subprocess.call(["docker", "compose", "up", "-d"])
    callArray.append(str(value) + suffix)
    print(callArray)
    subprocess.call(callArray)
    callArray.pop()
    clientCounter = 0;
    for client in clients:
      clientCounter += 1
      for i in range(repCount):
        final = client + ["/Results/" + scenario + str(value) + "-C" + str(clientCounter) + "/data", "http://server/output.mpd"]
        subprocess.call(["docker", "exec", "client", "mkdir", "-p", "/Results/" + scenario + str(value) + "-C" + str(clientCounter)])
        print(final)
        subprocess.call(final)
    subprocess.call(["docker", "exec", "server", "ping", "-c" , "1", "client"])
    subprocess.call(["docker", "compose" ,"stop", "server"])
    subprocess.call(["docker", "compose", "rm", "-f"])
    
