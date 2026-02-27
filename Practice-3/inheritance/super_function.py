#--------------------------------------------
class Animal:
    def __init__(self):
        print("Animal created")

class Dog(Animal):
    def __init__(self):
        super().__init__()
        print("Dog created")

Dog()

#--------------------------------------------
class Person:
    def greet(self):
        print("Hello")

class Student(Person):
    def greet(self):
        super().greet()
        print("I am a student")

Student().greet()

#--------------------------------------------
class Vehicle:
    def start(self):
        print("Vehicle starting")

class Car(Vehicle):
    def start(self):
        super().start()
        print("Car ready")

Car().start()

#--------------------------------------------
class Shape:
    def draw(self):
        print("Drawing shape")

class Square(Shape):
    def draw(self):
        super().draw()
        print("Drawing square")

Square().draw()


#--------------------------------------------
