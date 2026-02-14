#--------------------------------------------
class Student:
    count = 0   # class variable

    def __init__(self, name):
        self.name = name
        Student.count += 1

s1 = Student("Ali")
s2 = Student("Dani")

print(Student.count)
#--------------------------------------------
class Student:
    school = "KBTU"   # class variable

s1 = Student()
s2 = Student()

print(s1.school)
print(s2.school)

#--------------------------------------------
class Product:
    tax = 0.2   # class variable

    def __init__(self, price):
        self.price = price

    def total_price(self):
        return self.price + self.price * Product.tax

p = Product(100)
print(p.total_price())

#--------------------------------------------
class Game:
    level = 1   # class variable

player1 = Game()
player2 = Game()

Game.level = 2

print(player1.level)
print(player2.level)

#--------------------------------------------
