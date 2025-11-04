class Car(object):
    id = 0

    def __init__(self, name, model, year):
        self.name = name
        self.model = model
        self.year = year
        self.id = Car.id
        Car.id += 1

    def __str__(self):
        output = "\nID: " + str(self.id) + \
                 "\nName: " + self.name + \
                 "\nModel: " + self.model + \
                 "\nYear: " + self.year
        return output


c0 = Car("Ford", "Shelby GT500", "2015")
c1 = Car("Toyota", "Corolla", "2012")
c2 = Car("BMW", "Z3", "2001")
c3 = Car("Audi", "A6", "2020")

print(c0)
print(c1)
print(c2)
print(c3)
