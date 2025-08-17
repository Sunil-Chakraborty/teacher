# (teacher_env) D:\JU\Python_tricks>
# https://drive.google.com/file/d/1-7kxCMK11eFD9qMrN87v8Uw8V0qZ7Z6a/view?usp=sharing
# from DOS Python prompt (the >>> interactive interpreter)

import os

#>>>os.system('cls')
#>>>exit()
"""
#Assert in Python
def apply_discount(product, discount):
	price = int(product['price'] * (1.0 - discount))
	assert 0 <= price <= product['price']
	return price

# >>> exec(open('tricks1.py').read())  Use exec() with open()

"""

#String Conversion (Every Class Needs a __repr__)
class Car:
    def __init__(self, color, mileage):
        self.color = color
        self.mileage = mileage
    
    def __str__(self):
        return '__str__ for Car'
    def __repr__(self):
        return f'Car({self.color!r}, {self.mileage!r})' 
        
    def __repr__(self):
        return (f'{self.__class__.__name__}('
                f'{self.color!r}, {self.mileage!r})')


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"{self.name}, {self.age} years old"

    def __repr__(self):
        return f"Person(name='{self.name}', age={self.age})"
        
