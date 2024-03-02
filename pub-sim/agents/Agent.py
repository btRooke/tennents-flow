"""
Agent.py
- Superclass "Person" is to be inherited by all agents in the system.
"""

global time

class Agent:
  def __init__(self):
    self.archetype = None
    self.balance = None
    self.coordinates = None
    self.preferences = None
    self.activity = None
    self.bedtime = None
    self.drink_intake = None
    self.drink_capacity = None

  def is_occupied(self):
    return self.activity is not None

  def is_drunk(self):
    return self.drink_intake > self.drink_capacity

  def is_asleep(self):
      self.bedtime > time

