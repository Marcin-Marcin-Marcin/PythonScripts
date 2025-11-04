class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        return str(self.feet) + " feet, " + str(self.inches) + " inches"

    def __lt__(self, other):
        return (self.feet * 12 + self.inches) < (other.feet * 12 + other.inches)

    def __le__(self, other):
        return (self.feet * 12 + self.inches) <= (other.feet * 12 + other.inches)

    def __eq__(self, other):
        return (self.feet * 12 + self.inches) == (other.feet * 12 + other.inches)

    def __gt__(self, other):
        return (self.feet * 12 + self.inches) > (other.feet * 12 + other.inches)

    def __ge__(self, other):
        return (self.feet * 12 + self.inches) >= (other.feet * 12 + other.inches)

    def __ne__(self, other):
        return (self.feet * 12 + self.inches) != (other.feet * 12 + other.inches)


print(Height(4, 6) > Height(4, 5))
print(Height(4, 5) >= Height(4, 5))
print(Height(5, 9) != Height(5, 10))