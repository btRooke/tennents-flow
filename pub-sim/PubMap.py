"""
PubMap.py
- Contains the class required to instantiate the world maps
"""

from utils import utils
from Agent import Agent
from Venue import Venue


class PubMap:

    def __init__(self, num_agents, venue_path, venue_distribution_path, seed):
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
        self.agents = self.generate_agents(venue_distribution_path)
        self.timestep = 0

    # Read a JSON file of the venues in the region and store the contents as an attribute
    def generate_venues(self, venue_path):
        """Generates the initialized venue objects"""
        venues = {}
        venue_data = utils.load_json(venue_path)

        for data in venue_data:  # Use enumerate to get both index and data
            venues[data["name"]] = Venue(data["name"], data["classification"], data["average_stay"], data["location"],
                                         data["closing_time"], data["capacity"], data["popularity"],
                                         data["drink_cost"], data["average_wait"])

        return venues

    # Generate N agents in the environment, store as a dictionary with id key, Agent object value.
    def generate_agents(self, venue_distribution_path):
        """ Take a dictionary of agent behavior archetype distributions. Initializes agents. """

        agents = {}

        for id in range(self.total_agents):
            agent = Agent(id, self.venues, venue_distribution_path, self.seed)
            agents[id] = agent

        return agents

    def __str__(self):
     # Starting with the map's general information
        map_info = f"PubMap State at Timestep {self.timestep}\n"
        map_info += f"Total Agents: {self.total_agents}, Seed: {self.seed}\n"

        # Adding venue information
        map_info += "\nVenues:\n"
        for venue in self.venues.values():
            map_info += str(venue) + "\n"

        # Adding agent information
        map_info += "\nAgents:\n"
        for agent in self.agents.values():
            map_info += str(agent) + "\n"

        return map_info