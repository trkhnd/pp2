#--------------------------------------------
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    def speak(self):
        print("Bark")

Dog().speak()

#--------------------------------------------
class Person:
    def job(self):
        print("Working")

class Teacher(Person):
    def job(self):
        print("Teaching")

Teacher().job()

#--------------------------------------------
class Shape:
    def draw(self):
        print("Drawing shape")

class Circle(Shape):
    def draw(self):
        print("Drawing circle")

Circle().draw()

#--------------------------------------------
class Phone:
    def brand(self):
        print("Generic phone")

class iPhone(Phone):
    def brand(self):
        print("Apple")

iPhone().brand()




