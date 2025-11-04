class Height(object):
    def __init__(self, feet, inches):
        self.feet = feet
        self.inches = inches

    def __str__(self):
        output = str(self.feet) + " feet, " + str(self.inches) + " inches"
        return output

    def __sub__(self, other):
        height_A_inches = self.feet * 12 + self.inches
        height_B_inches = other.feet * 12 + other.inches

        diff_inches = height_A_inches - height_B_inches

        if diff_inches < 0:
            diff_inches = abs(diff_inches)
            print("Note: Result converted to positive difference")

        output_feet = diff_inches // 12
        output_inches = diff_inches % 12

        return Height(output_feet, output_inches)


person_A_height = Height(5, 10)
person_B_height = Height(3, 9)

height_difference = person_A_height - person_B_height

print("Height difference:", height_difference)
