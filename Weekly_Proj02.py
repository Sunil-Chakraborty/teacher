#!/usr/bin/env python
# coding: utf-8

# # **1. Addition**

# In[ ]:


def add_num(a,b):
  return a+b


# # **2.Substruction**

# In[ ]:


def sub_num(a,b):
  return a-b


# # **3.Multiplication**

# In[ ]:


def mul_num(a,b):
  return a*b


# # **4.Divide**

# In[ ]:


def div_num(a,b):
  if b == 0:
        return "Error: Division by zero is undefined."

  return a/b


# # **Calculator**
def calculator():

     print("Welcome to the Simple Calculator!")
     exit_calculator = False

     while not exit_calculator:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice (1/2/3/4/5): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 5:
            print("Exiting the calculator. Goodbye!")
            exit_calculator = True
            continue

        if choice not in [1, 2, 3, 4]:
            print("Invalid choice. Please select 1, 2, 3, 4, or 5.")
            continue

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input. Please enter numeric values.")
            continue

        if choice == 1:
            print(f"The result of addition: {add_num(num1, num2)}")
        elif choice == 2:
            print(f"The result of subtraction: {sub_num(num1, num2)}")
        elif choice == 3:
            print(f"The result of multiplication: {mul_num(num1, num2)}")
        elif choice == 4:
            print(f"The result of division: {div_num(num1, num2)}")
