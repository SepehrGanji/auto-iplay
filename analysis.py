import json
import matplotlib.pyplot as plt

def read_bandwidth_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        time = []
        bandwidth = []
        for item in data['bandwidth_estimate']:
            if item['bandwidth'] <= 10000:
                time.append(item['time'])
                bandwidth.append(item['bandwidth']/8/1000)
        return time, bandwidth

def plot_data(time1, bandwidth1, time2, bandwidth2):
    plt.figure(figsize=(10, 6))
    plt.plot(time1, bandwidth1, label='Segment-based')
    plt.plot(time2, bandwidth2, label='Instantaneous')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Bandwidth (Kbps)')
    plt.title('Delay Network')
    plt.legend()
    plt.grid(True)
    plt.show()

# Read data from JSON files
time1, bandwidth1 = read_bandwidth_data('Results/delay200-C1/data-1.json')
time2, bandwidth2 = read_bandwidth_data('Results/delay200-C2/data-1.json')

# Plot the data
plot_data(time1, bandwidth1, time2, bandwidth2)
