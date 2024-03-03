"""
PubMap.py
- Contains the class required to instantiate the world maps
"""

from pubsim.utils import utils
from pubsim.Agent import Agent
from pubsim.Venue import Venue

import numpy as np
import pandas as pd


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
        self.total_venues = len(self.venues)

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

    def step(self):

        venue_names = list(self.venues.keys()) + ["HOME"]
        transition_matrix =pd.DataFrame(0, index=venue_names, columns= venue_names)

        for id in range(self.total_agents):

            # Run the simulation step for each agent
            agent = self.agents[id]

            # Do nothing with retired agents
            if agent.is_retired():
                continue

            # If an agent is at a venue, test if it wants to buy a drink, decrement it's wait counters
            if agent.is_busy():
                # Determine if agent wants to buy a drink, if so invoke that action.
                agent.thirsty(self.venues)

                if agent.get_idletime() == 0:
                    agent.set_busy(False)
                else:
                    # Decrement count until the agent will leave the venue
                    agent.decrement_idletime()

            # If an agent is not at a venue, probabilistically roll to inform the next decision.
            else:
                transition = agent.make_decision(self.timestep, self.venues)
                if transition:
                    old_place = transition[0]
                    new_place = transition[1]
                    transition_matrix.loc[old_place, new_place] += 1

        self.timestep += 1

        revenues = [{name: obj.get_revenue()} for name, obj in self.venues.items()]

        return transition_matrix, revenues

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
