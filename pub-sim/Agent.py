"""
Agent.py
- Superclass "Person" is to be inherited by all agents in the system.
"""

global time
import numpy as np
import random
from utils import utils

class Agent:
    def __init__(self, id, venues, start_venue_distribution_path, seed):
        self.id = id  # Used to index an agent in the PubMap 'agents' dictionary
        self.budget = self.init_budget()  # Each agent has a budget for the night out, when it runs out an agent goes home.
        self.current_venue = self.init_current_venue(venues, start_venue_distribution_path)  # Store where the agent is at any time.
        self.location = self.init_location(venues)  # Match the latitude and longitude to the starting location.
        self.busy = self.init_busy()  # True or False, documents if the agent is in a venue at this time.
        self.bedtime = self.init_bedtime()  # Set the time that the agent will go home.
        self.idletime = self.init_idletime()  # Set the initial amount of time that the agent will wait in its start state
        self.thirst_level = self.init_thirst_level()
        self.thirst = self.thirst_level
        self.retired = False
        self.seed = seed

    def __str__(self):
        return f"Agent {self.id}: Budget: {self.budget}, Current Venue: {self.current_venue}, Coordinates: {self.location}, Busy: {self.busy}, Thirst: {self.thirst}, Bedtime: {self.bedtime}, Idle-Time: {self.idletime}, Retired = {self.retired}"

    def make_decision(self, time, venue_df):

        if self.is_retired():
            return

        # If the player needs to retire, then set this in motion
        if time >= utils.time_to_timestep(self.bedtime) or self.budget <= 2:
            self.retire()
            return

        # Determine the probability that the Agent is to retire
        retire_probability = 0.75 * (1 * (time / 540))
        remaining_probability = 1 - retire_probability

        # Exclude the agent's current venue from the list of venues to consider
        venues_to_consider = {name: venue for name, venue in venue_df.items() if name != self.current_venue}

        # Calculate scores for the remaining venues
        total_score = sum(utils.agent_venue_score(self, venue) for venue in venues_to_consider.values())
        # Avoid division by zero in case all venues are excluded or have zero scores
        if total_score == 0:
            normalized_scores = [0 for _ in venues_to_consider.values()]
        else:
            normalized_scores = [utils.agent_venue_score(self, venue) / total_score for venue in
                                 venues_to_consider.values()]
        adjusted_scores = [score * remaining_probability for score in normalized_scores]

        # Sample a place to move to using the probability distribution over venues and retire
        probabilities = {'RETIRE': retire_probability}
        probabilities.update({venue_name: prob for venue_name, prob in zip(venues_to_consider.keys(), adjusted_scores)})
        sampled_venue = random.choices(list(probabilities.keys()), weights=list(probabilities.values()), k=1)[0]

        # If sample has been randomly drawn, then set retirement in motion
        if sampled_venue == "RETIRE":
            self.retire()
        # Otherwise, move from current venue to a new one.
        else:
            # If the agent tries to move to a full venue, reroll.
            if venue_df[sampled_venue].is_full():
                self.make_decision(time, venue_df)
            else:
                return self.transition(sampled_venue, venue_df)

    def transition(self, destination, venues):
        past_venue_name = self.current_venue
        past_venue = venues[past_venue_name]
        past_venue.remove_customer()

        self.current_venue = destination
        current_venue = venues[self.current_venue]
        current_venue.add_customer()

        self.location = current_venue.get_location()
        self.idletime = int(round(max(np.random.normal(current_venue.get_average_time_spent(), 20), 0)))
        self.busy = True

        transition = [past_venue_name, destination]
        return transition


    def thirsty(self, venues):
        # Buy a drink at the current venue if thirst = 0.
        if self.thirst == 0:
            current_venue_name = self.current_venue
            current_venue = venues[current_venue_name]
            price = current_venue.get_price()

            if self.budget >= price:
                self.budget -= price
                venues[current_venue_name].add_purchase()
                self.thirst = self.thirst_level
                return
            # Can't afford a drink, enter dice roll.
            else:
                self.busy = False
                return
        else:
            self.thirst -= 1

    def init_budget(self):
        # Set budget via a normal distribution
        return int(round(max(np.random.normal(15, 20), 0)))

    def init_current_venue(self, venues, start_venue_distribution_path):
        # Set the current venue by sampling from a predefined distribution heavily weighted towards "HOME"
        starting_location_distribution = utils.load_json(start_venue_distribution_path)
        # Extract the venue names and the starting probabilities
        venue_names = list(starting_location_distribution[0].keys())
        probabilities = list(starting_location_distribution[0].values())

        while True:
            # Sample from the distribution
            sampled_venue = random.choices(venue_names, weights=probabilities, k=1)[0]

            # If the sampled venue is not full, assign the agent to the venue and increment its attendance
            if not venues[sampled_venue].is_full():
                agent_start_venue = venues[sampled_venue]
                agent_start_venue.add_customer()
                return sampled_venue

            # Continue if a full venue has been sampled.

    # Match the Agent's coordiniates to its initialized venue location
    def init_location(self, venues):
        if self.current_venue == "HOME":
            return None
        else:
            current_coordinates = venues[self.current_venue].get_location()
            return current_coordinates

    # Initialize the starting distribution as tending towards home, uniform on all other choices

    # Set an Agent's bedtime (no longer going out) as normal around 12:30
    def init_bedtime(self):
        return utils.timestep_to_time(int(round(max(np.random.normal(390, 100), 0))))

    def init_idletime(self):
        return int(round(max(np.random.normal(60, 20), 0)))

    def init_busy(self):
        if self.current_venue == "HOME":
            return False
        else:
            return True

    def init_thirst_level(self):
        return int(round(max(np.random.normal(45, 20), 0)))

    def is_busy(self):
        return self.busy

    def is_retired(self):
        return self.retired

    def retire(self):
        self.retired = True
        self.idletime = 540
        transition = [self.current_venue, "HOME"]
        self.current_venue = "HOME"

    def decrement_idletime(self):
        self.idletime -= 1

    def get_idletime(self):
        return self.idletime

    def get_location(self):
        return self.location

    def get_current_venue(self):
        return self.current_venue

    def set_busy(self,b):
        self.busy = b
