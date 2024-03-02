"""
py-sim.py:
- Main program containing simulation execution loop.
"""

# System library imports
import os
import sys
import datetime

# Program class imports
from map import Map
from utils import utils

# Individual class imports
from argparse import ArgumentParser

# System Global Variables.
# Distribution of the proportion of agents that will be "active" each hour.
HOURLY_AGENT_PERCENT = {
    "6:00 PM": 11,
    "7:00 PM": 20,
    "8:00 PM": 33,
    "9:00 PM": 50,
    "10:00 PM": 55,
    "11:00 PM": 50,
    "12:00 PM": 50,
    "00:00 AM": 20,
    "01:00 AM": 11,
    "02:00 AM": 9
}

# Distribution of the proportion of archetypes that agents take in the population.
AGENT_ARCHETYPE_DISTRIBUTION = {
    "Antisocial": 10,
    "CrowdAvoider": 5,
    "CrowdFollower": 20,
    "Devotee": 10,
    "UpForAnything": 50,
    "UpperClass": 5,
}

def sim_cmd():
    """
       Command-line interface for the pub simulation.
       Parameters:
       -n, --num-agents : int
            Number of agents to be simulated. Default is 1000.
       -v, --venues : str
            List of venues to be included. This refers to a file of pickled objects.
       -m, --map : str
    """
    # PARSE FOR ALL ARGUMENTS AT COMMAND LINE
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-n", "--num-agents", type=int, default=1000, help="Number of Agents")
    arg_parser.add_argument("-v", "--venues", type = str, default = "data\example\st-a-venues.csv", help="Path to venues file")
    arg_parser.add_argument("-m", "--map", type = str, default="data\example\map.csv", help="Path to map")
    arg_parser.add_argument("-s", "--seed", type=int, default= 144, help="Random generation seed")

    try:
        args = arg_parser.parse_args()
        return args
    except ValueError as e:
        arg_parser.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    # Parse the command line args
    args = sim_cmd()
    n = args.num_agents
    venues = utils.load_venue_data(args.venues)
    # Construct the simulation map
    map = Map(num_agents = n, venue_list= venues, random_seed= args.seed)

    # Run the simulation
    for i in range(60*9):
        map.step()
        map.send_to_tim()

    # Save the final simulation output paramters.
    map.out(data=map.get_parameters(), output_path=f"output\{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}\parameters", output_format="json")

    print("pub-sim.py!")