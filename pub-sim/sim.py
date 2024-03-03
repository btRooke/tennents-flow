"""
py-sim.py:
- Main program containing simulation execution loop.
"""

# System library imports
import sys
import datetime

# Program class imports
import PubMap

# Individual class imports
from argparse import ArgumentParser

# Global Variables:
DURATION = 540

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
    arg_parser.add_argument("-v", "--venue_path", type = str, default = "example\st_andrews_distribution.json", help="Path to venues file")
    arg_parser.add_argument("-d", "--distribution_path", type = str, default="example\st_andrews_venues.json", help="Path to archetype probability distribution")
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
    distribution_path = args.distribution_path

    # Construct the simulation map
    pub_map = PubMap(num_agents = num_agents, venue_path= venue_path, distribution_path= distribution_path, random_seed= args.seed)

    # Run the simulation
    for i in range(DURATION):
        pub_map.step()
        pub_map.send_to_tim()

    # Save the final simulation output parameters.
    pub_map.out(data=pub_map.get_parameters(), output_path=f"output\{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}\parameters", output_format="json")

    print("sim.py!")