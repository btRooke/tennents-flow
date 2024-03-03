"""
Agent.py
- Superclass "Person" is to be inherited by all agents in the system.
"""

global time
import numpy as np
import random
from utils import utils

def __init__(self, id, venues, start_venue_distribution_path, seed):
  self.id = id                      # Used to index an agent in the PubMap 'agents' dictionary
  self.budget = self.init_budget()  # Each agent has a budget for the night out, when it runs out an agent goes home.
  self.current_venue = self.init_current_venue(venues, start_venue_distribution_path) # Store where the agent is at any time.
  self.coordinates = self.init_coordinates(venues)  # Match the latitude and longitude to the starting location.
  self.preference_distribution = self.init_preference_distribution(venues) # This dictates what the Agent will choose next
  self.busy = self.init_busy()  # True or False, documents if the agent is in a venue at this time.
  self.bedtime = self.init_bedtime() # Set the time that the agent will go home.
  self.balktime = self.init_balktime() # Set the maximum amount of time the agent is willing to wait for a full venue
  self.seed = seed


def init_budget():
  # Set budget via a normal distribution
  return int(round(max(np.random.normal(30, 20), 0)))

def init_current_venue(self, venues, start_venue_distribution_path):
  # Set the current venue by sampling from a predefined distribution heavily weighted towards "HOME"
  starting_location_distribution = utils.load_json(start_venue_distribution_path)
  # Extract the venue names and the starting probabilities
  venue_names = list(starting_location_distribution[0].keys())
  probabilities = list(starting_location_distribution[0].values())

  while True:
    # Sample from the distribution
    sampled_venue = random.choices(venue_names, weights=probabilities, k=1)[0]

    # If "HOME" is sampled, set the current venue to "HOME"
    if sampled_venue == "HOME":
      return "HOME"

    # If the sampled venue is not full, assign the agent to the venue and increment its attendance
    elif not venues[sampled_venue].is_full():
      agent_start_venue = venues[sampled_venue]
      agent_start_venue.add_customer()
      return sampled_venue

    # Continue if a full venue has been sampled.


# Match the Agent's coordiniates to its initialized venue location
def init_coordinates(self, venues):
  if self.current_venue == "HOME":
    return None
  else:
    current_coordinates = venues[self.current_venue].get_location()
    return current_coordinates


# Initialize the starting distribution as tending towards home, uniform on all other choices
def init_preference_distribution(self, venues):
  venue_names = list(venues.keys())
  preference_distribution = {venue: (1 - 0.3) / len(venue_names) for venue in venue_names}
  preference_distribution["HOME"] = 0.5
  print(preference_distribution)


# Set an Agent's bedtime (no longer going out) as normal around 12:30
def init_bedtime(self):
  return int(round(max(np.random.normal(390, 100), 0)))


# Set the amount of time an agent is willing to spend waiting for a venue.
def init_balktime(self):
  return int(round(max(np.random.normal(10, 8), 0)))

