#--------------------------------------------
class Fly:
    def fly(self):
        print("Flying")

class Swim:
    def swim(self):
        print("Swimming")

class Duck(Fly, Swim):
    pass

d = Duck()
d.fly()
d.swim()
#--------------------------------------------

class Read:
    def read(self):
        print("Reading")

class Write:
    def write(self):
        print("Writing")

class Student(Read, Write):
    pass

s = Student()
s.read()
s.write()
#--------------------------------------------
class A:
    def a(self):
        print("A")

class B:
    def b(self):
        print("B")

class C(A, B):
    pass

c = C()
c.a()
c.b()

#--------------------------------------------
class Music:
    def play(self):
        print("Playing music")

class Call:
    def call(self):
        print("Calling")

class Smartphone(Music, Call):
    pass

phone = Smartphone()
phone.play()
phone.call()

#--------------------------------------------