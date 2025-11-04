class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        return f"{self.feet} feet, {self.inches} inches"

    def __lt__(self, other):
        return (self.feet * 12 + self.inches) < (other.feet * 12 + other.inches)

height_1 = Height(4, 10)
height_2 = Height(5, 6)
height_3 = Height(7, 1)
height_4 = Height(5, 5)
height_5 = Height(6, 7)
height_6 = Height(5, 6)

heights = [height_1, height_2, height_3, height_4, height_5, height_6]

heights = sorted(heights)
for height in heights:
    print(height)
