#--------------------------------------------
class Animal:
    def speak(self):
        print("Animal sound")

class Dog(Animal):
    pass

d = Dog()
d.speak()

#--------------------------------------------
class Person:
    def walk(self):
        print("Walking")

class Student(Person):
    pass

s = Student()
s.walk()

#--------------------------------------------
class Vehicle:
    def move(self):
        print("Moving")

class Car(Vehicle):
    pass

c = Car()
c.move()

#--------------------------------------------
class Fruit:
    def color(self):
        print("Colorful")

class Apple(Fruit):
    pass

a = Apple()
a.color()

#--------------------------------------------

