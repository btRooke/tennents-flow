"""
Map.py
- Contains the class required to instantiate the world map
"""

import random
from agents import Agent

class Map:

    def __init__(self, num_agents, venues, seed):
        """
        Central class for storing a state of the simulation at timestep t

        Parameters:
            num_agents:
            venues: list of venue objects for a given town map
            seed: seeds random number generation for simulation
        """

        # Static Map Attributes
        self.total_agents = num_agents
        self.venues = venues
        self.seed = seed

        # Dynamic Map Attributes
        self.agents = {}
        self.venues = {}
        self.time = 0
        self.arrival_index = 0


    def generate_agents(self, archetype_distribution):
        """ Take a dictionary of agent behavior archetype distributions. Initializes agents. """

        if sum(archetype_distribution.values()) != 100:
            raise AssertionError("The percent of behavior archetypes does not add up to 100%")

        total_agents = self.total_agents
        for agent_id in range(total_agents):
            random.seed(self.random_seed + agent_id)
            exp_ability = random.uniform(0,1) < exp_ability_pct

            agent = Agent(random_seed=self.random_seed)
            agent.initialize_agent(
                agent_id=agent_id,
                behavior_archetype_distribution=behavior_archetype_distribution,
                exp_ability=exp_ability,
                exp_wait_threshold=exp_wait_threshold,
                exp_limit=exp_limit,
                attraction_names=[attraction["name"] for attraction in self.attraction_list],
                activity_names=[activity["name"] for activity in self.activity_list],
            )
            self.agents.update({agent_id: agent})

