import random
import json

def load_json(filepath):
    """Loads a JSON file into a python dictionary
    Params:
        - filepath (str): plaintext path from root directory to the JSON file"""
    try:
        with open(filepath, 'r') as file:
            dictionary = json.load(file)
            return dictionary
    except FileNotFoundError:
        print(f"The file at {filepath} was not found.")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file at {filepath}.")
    except Exception as e:
        print(f"An error occurred: {e}")


def timestep_to_time(step):
    """Program goes from step 0 to step 540, this converts a timestep value to
    its equivalent time between 18:00-03:00

    Params:
        - step (int): value between 0 to 540"""

    # Base start time in hours (18:00)
    base_hour = 18

    # Convert input minutes to hours and minutes
    hours_added = step // 60
    minutes_added = step % 60

    # Calculate the new hour and minute
    final_hour = base_hour + hours_added
    final_minute = minutes_added

    # Format the time string
    time_str = f"{final_hour:02d}:{final_minute:02d}"

    return time_str