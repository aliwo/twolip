class Foo:
    def __eq__(self, other):
        return True


print(Foo() == 1)
print(Foo() == [1,2,3])
print(Foo() == dict())
print(Foo() == False)
print(Foo() == True)


