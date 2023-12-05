import os
import json

def process_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
        avg_br = data['avg_bitrate']
        dur_stall = data['dur_stall']
        return avg_br, dur_stall

def process_results_directory(directory):
    results = []
    for root, dirs, files in os.walk(directory):
        dirs.sort()  # Sort the directories
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                result = process_json_file(file_path)
                results.append((file_path, result))

    return results

results_directory = 'Results'
processed_results = process_results_directory(results_directory)

for file_path, result in processed_results:
    print(f"File: {file_path}, Data: {result}")
