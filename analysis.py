import json
import matplotlib.pyplot as plt

def read_bandwidth_data(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        time = []
        buff = []
        for item in data['buffer_level']:
            if item['level'] > 0:
                time.append(item['time'])
                buff.append(item['level'])
        return time, buff

def plot_data(time1, buff1, time2, buff2, time3, buff3):
    plt.figure(figsize=(10, 6))
    plt.plot(time1, buff1, label='2')
    plt.plot(time2, buff2, label='4')
    plt.plot(time3, buff3, label='6')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Buffer Level')
    plt.title('Panic Level')
    plt.legend()
    plt.grid(True)
    plt.show()

# Read data from JSON files
time1, buff1 = read_bandwidth_data('Results/panic2.json/data-1.json')
time2, buff2 = read_bandwidth_data('Results/panic4.json/data-1.json')
time3, buff3 = read_bandwidth_data('Results/panic6.json/data-1.json')

# Plot the data
plot_data(time1, buff1, time2, buff2, time3, buff3)
