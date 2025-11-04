class Animal(object):
    def __init__(self, age):
        self.age = age
        self.name = None

    def set_name(self, name):
        self.name = name

    def __str__(self):
        return f"\nClass: Animal\nName: {self.name}\nAge: {self.age}"


class Human(Animal):
    def __init__(self, name, age):
        Animal.__init__(self, age)

        self.set_name(name)
        self.friends = []

    def add_friend(self, friend_name):
        self.friends.append(friend_name)

    def show_friends(self):
        for friend in self.friends:
            print(friend)

    def speak(self):
        print(f"Hello, my name's {self.name}!")

    def __str__(self):
        output = f"\nClass: Human\nName: {self.name}\nAge: {self.age}\nFriends list:\n"
        for friend in self.friends:
            output += friend + "\n"
        return output


human = Human("Tobias", 35)
human.add_friend("Robert")
human.add_friend("Élise")
human.add_friend("Abdullah")
human.add_friend("Asha")
human.add_friend("Lupita")
human.add_friend("Saito")

human.speak()
print(human)
