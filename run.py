import subprocess

scenarios = ["bw", "delay", "loss"]
values = {"bw": [10, 20, 100],
          "delay": [100, 200, 500],
          "loss": [10, 20, 30]}

baseClient = ["docker", "exec", "client", "iplay", "-i", "http://server/output.mpd", "--mod_analyzer", "data_collector", "--mod_abr"]
clients = [
  baseClient + ["bandwidth", "--run_dir"],
  baseClient + ["buffer", "--run_dir"],
  baseClient + ["hybrid", "--run_dir"],
]
repCount = 1

for scenario in scenarios:
  callArray = ["docker", "exec", "server", "tc", "qdisc", "add", "dev", "eth0", "root", "netem"]
  suffix = ""
  if scenario == "bw":
    callArray.append("rate")
    suffix = "kbit"
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
        final = client + ["/Results/" + scenario + str(value) + "-C" + str(clientCounter)]
        subprocess.call(["docker", "exec", "client", "mkdir", "-p", "/Results/" + scenario + str(value) + "-C" + str(clientCounter)])
        print(final)
        subprocess.call(final)
    subprocess.call(["docker", "exec", "server", "ping", "-c" , "1", "client"])
    subprocess.call(["docker", "compose" ,"stop", "server"])
    subprocess.call(["docker", "compose", "rm", "-f"])
    
