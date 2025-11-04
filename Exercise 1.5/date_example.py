class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year


first_moon_landing = Date(20, 7, 1969)
print(first_moon_landing.day)
print(first_moon_landing.month)
print(first_moon_landing.year)
