class Date(object):
    def __init__(self, day, month, year):
        self.day = day
        self.month = month
        self.year = year

    def get_date(self):
        output = str(self.day) + "/" + str(self.month) + "/" + str(self.year)
        return output

    def is_leap_year(self):
        return self.year % 4 == 0

    def is_valid_date(self):
        if not (type(self.day) == int and type(self.month) == int and type(self.year) == int):
            return False
        if self.year < 0:
            return False
        if self.month < 1 or self.month > 12:
            return False

        last_dates = {
            1: 31,
            2: 29 if self.is_leap_year() else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }

        if self.day < 1 or self.day > last_dates.get(self.month):
            return False

        return True


date1 = Date(29, 2, 2000)           # Valid
date2 = Date(29, 2, 2001)           # Invalid
date3 = Date('abc', 'def', 'ghi')   # Invalid

print(str(date1.get_date()) + ": " + str(date1.is_valid_date()))
print(str(date2.get_date()) + ": " + str(date2.is_valid_date()))
print(str(date3.get_date()) + ": " + str(date3.is_valid_date()))
