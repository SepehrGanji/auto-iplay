import subprocess
import os

# iplay -i http://server/final.mpd --mod_analyzer data_collector --mod_abr 360_hm:data=./hm_data.json
gethm = ["docker", "exec", "client", "wget", "-P", "/hmdata", "http://server/hm_data.json"]
client = ["docker", "exec", "client", "iplay", "-i", "http://server/final.mpd", 
              "--mod_analyzer", "data_collector", "--config", "/config.json",
              "--mod_abr", "360_hm:data=/hmdata/hm_data.json", "--run_dir"]

subprocess.call(["docker", "compose", "up", "-d"])
subprocess.call(gethm)
limit = ["docker", "exec", "server", "tc", "qdisc", 
         "add", "dev", "eth0", "root", "netem",
         "rate", "100Kbps",
         "delay", "100ms",
         "loss", "5%"]
subprocess.call(limit)

current_directory = os.path.dirname(os.path.realpath(__file__))
config_directory = os.path.join(current_directory, 'Config')
for config in os.listdir(config_directory):
    if os.path.isfile(os.path.join(config_directory, config)):
        print(f"Running {config}")
        subprocess.call(["docker", "cp", f"./Config/{config}", "client:/config.json"])
        final = client + ["/Results/" + config]
        subprocess.call(["docker", "exec", "client", "mkdir", "-p", "/Results/" + config])
        subprocess.call(final)
        
subprocess.call(["docker", "compose", "down"])

