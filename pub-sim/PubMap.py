"""
PubMap.py
- Contains the class required to instantiate the world maps
"""

from utils import utils
from agents import Agent
from venues import Venue
class PubMap:

    def __init__(self, num_agents, venue_path, distribution_path, seed):
        """
        Central class for storing a state of the simulation at timestep t

        Parameters:
            num_agents:
            venues: list of venue objects for a given town maps
            seed: seeds random number generation for simulation
        """

        # Static Map Attributes
        self.total_agents = num_agents
        self.seed = seed

        # Dynamic Map Attributes
        self.venues = self.generate_venues(venue_path)
        self.agents = self.generate_agents(num_agents,distribution_path)
        self.timestep = 0

    # Read a JSON file of the venues in the region and store the contents as an attribute
    def generate_venues(self, venue_path):
        """Generates the initialized venue objects"""
        venues = {}
        venue_data = utils.load_json(venue_path)

        for data in venue_data:  # Use enumerate to get both index and data
            venues[data["name"]] = Venue(data["name"], data["classification"], data["average_stay"], data["location"], data["closing_time"], data["capacity"], data["attendence"], data["popularity"], data["drink_cost"], data["wait_time"])

        return venues


    # Generate N agents in the environment, store as a dictionary with id key, Agent object value.
    def generate_agents(self):
        """ Take a dictionary of agent behavior archetype distributions. Initializes agents. """

        agents = {}

        for id in range(self.total_agents):

            agent = Agent()

            agents[id] = agent

        return agents



