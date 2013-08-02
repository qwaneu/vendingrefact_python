#
# (c) Quality Without A Name 2011
#     Refactoring Course material
#
class Chipknip:
    def __init__(self, initial_value):
        self.credits = initial_value

    def reduce(self, amount):
        self.credits -= amount

    def has_value(self, value):
        return self.credits >= value

