class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def get_date(self):
        output = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        return output

    def set_date(self):
        self.day = int(input("Enter the day of the month: "))
        self.month = int(input("Enter the month: "))
        self.year = int(input("Enter the year: "))


first_moon_landing = Date(20, 7, 1969)

print(first_moon_landing.get_date())
first_moon_landing.set_date()
print(first_moon_landing.get_date())
