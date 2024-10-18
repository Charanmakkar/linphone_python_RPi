import json

def read_and_update_json(file_path, new_data):
    # Step 1: Read the existing JSON file
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            print(data)
    except FileNotFoundError:
        print(f"{file_path} not found!")
        return

    # Step 2: Update the JSON data (here, assuming new_data is a dictionary)
    data.update(new_data)

    # Step 3: Write the updated data back to the same file
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)  # indent=4 makes the JSON readable

    print("File updated successfully.")

# Usage example
file_path = 'data.json'
new_data = {"i was saying that": "fullOK"}  # New data to be added/updated in the JSON

read_and_update_json(file_path, new_data)
