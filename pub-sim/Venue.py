
class Venue:
  def __init__(self, name, classification, average_stay, location, closing_time, capacity, popularity, drink_cost, wait_time):
    self.name = name
    self.classification = classification # What type of venue it is ("Small", "Medium", "Large"). Helps Billy
    self.average_stay = average_stay # When an agent enters a venue, it should stay idle buying drinks for some amount
                                     # of time. This period should be determined by a normal dist centred at average_stay
    self.location = location         # Dictionary of latitude and longitude values. Sourced from Google API hopefully.
    self.closing_time = closing_time # When the pub closes and thereby accepts no customers (set capacity to zero).
    self.capacity = capacity         # How many agents can be in a pub at any given time
    self.attendance = 0              # How many agents are currently in the pub. Initialize as zero.
    self.popularity = popularity     # Score out of 10, should influence the probability decision for an agents next choice
    self.drink_cost = drink_cost     # When an agent buys a drink in a pub, decrement its balance by this amount
    self.revenue = 0

  def __str__(self):
      """Print statement override in case needed for testing."""
      return (f"Venue(Name: {self.name}, Classification: {self.classification}, Average Stay: {self.average_stay}, "
                f"Location: {self.location}, Closing Time: {self.closing_time}, Capacity: {self.capacity}, "
                f"Attendance: {self.attendance}, Popularity: {self.popularity}, Drink Cost: {self.drink_cost}")


# GET / SET METHODS.
  def get_location(self):
      return self.location

  def is_full(self):
      return self.attendance >= self.capacity

  def add_customer(self):
    self.attendance += 1

  def remove_customer(self):
      self.attendance -= 1

  def add_purchase(self):
      self.revenue += self.drink_cost

  def get_price(self):
      return self.drink_cost

  def get_average_time_spent(self):
      return self.average_stay

  def get_revenue(self):
      return self.revenue


