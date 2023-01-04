class Parent:
    def func1(self):
        self.func2()
    
    def func2(self):
        print('I am func2 from the parent')

class Child(Parent):
    def func2(self):
        print('I am func2 from the child')

# Create an instance of the Child class
child = Child()

# Call the func1 function on the Child instance
child.func1()
