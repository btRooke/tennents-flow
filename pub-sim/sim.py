"""
py-sim.py:
- Main program containing simulation execution loop.
"""

# System library imports
import sys

import pandas as pd

# Program class imports
from PubMap import PubMap
from utils import utils

# Individual class imports
from argparse import ArgumentParser

# Global Variables:
DURATION = 200

def sim_cmd():
    """
       Command-line interface for the pub simulation.
       Parameters:
       -n, --num_agents : int
            Number of agents to be simulated. Default is 1000.
       -v, --venue_path : str
            List of venues to be included. This refers to a file of pickled objects.
       -m, --maps : str
    """
    # PARSE FOR ALL ARGUMENTS AT COMMAND LINE
    arg_parser = ArgumentParser()
    arg_parser.add_argument("-n", "--num_agents", type=int, default=1000, help="Number of Agents")
    arg_parser.add_argument("-v", "--venue_path", type = str, default = "example/StA_venue_data.json", help="Path to venues file")
    arg_parser.add_argument("-d", "--distribution_path", type = str, default="example/StA_venue_distribution.json", help="Path to start venue probability distribution")
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
    num_agents = args.num_agents
    venue_path = args.venue_path
    venue_distribution_path = args.distribution_path

    # Construct the simulation map
    pub_map = PubMap(num_agents = num_agents, venue_path= venue_path, venue_distribution_path = venue_distribution_path, seed= args.seed)

    # Run the simulation
    for i in range(DURATION):
        transition_matrix, revenues = pub_map.step()
        # send these to tim
        # Transition matrix is a pandas dataframe
        # transition_matrix["Aikmans","Whey Pat"] has how many transitions
        # from aikmans to whey pat in this iteration
        # revenues is a list of dictionaries of the form
        # [{"Aikmans": 472}, {"Union": 3484},...
        # This is the culmulative totals each pub has made on the evening.
