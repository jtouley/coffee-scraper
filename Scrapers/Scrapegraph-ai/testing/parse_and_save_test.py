import os
import json
import datetime

def parse_and_save_data(result, roaster):
    today = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    data_dir = "data"
    filename = f"{data_dir}/{roaster}_{today}.json"
    
    # Create the data directory if it doesn't exist
    os.makedirs(data_dir, exist_ok=True)
    
    # Write JSON data to file
    with open(filename, 'w') as file:
        json.dump(result, file, indent=4)  # Write JSON data to file with indentation

    print(f"Data saved to {filename}")
