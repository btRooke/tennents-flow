import math
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

    # Adjust final_hour to wrap around after 24 (to handle times past midnight correctly)
    if final_hour >= 24:
        final_hour -= 24

    final_minute = minutes_added

    # Format the time string
    time_str = f"{final_hour:02d}:{final_minute:02d}"

    return time_str



def time_to_timestep(time_str):
    """Converts a time string in the format "HH:MM" to the corresponding
    timestep between 18:00 and 03:00.

    Params:
        - time_str (str): Time in the format "HH:MM"

    Returns:
        - int: Corresponding timestep value
    """
    # Extract hours and minutes from the input time string
    hours, minutes = map(int, time_str.split(':'))

    # Initial base hour for the simulation start
    base_hour = 18

    # Adjust hours for times after midnight (00:00 to 03:00)
    if hours < base_hour:
        hours += 24

    # Calculate the total minutes elapsed since 18:00
    elapsed_hours = hours - base_hour
    elapsed_minutes = elapsed_hours * 60 + minutes

    return elapsed_minutes


def calculate_distance(agent, venue):

    if agent.get_current_venue() == "HOME":
        return 1

    agent_lat = agent.get_location()["lat"]
    agent_lon = agent.get_location()["lng"]
    venue_lat = venue.get_location()["lat"]
    venue_lon = agent.get_location()["lng"]
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(agent_lat)
    lon1_rad = math.radians(agent_lon)
    lat2_rad = math.radians(venue_lat)
    lon2_rad = math.radians(venue_lon)

    # Difference in coordinates
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c

    return distance


def agent_venue_score(agent, venue):
    distance = abs(calculate_distance(agent, venue))

    return venue.popularity * (1 / (distance+ 0.1))
