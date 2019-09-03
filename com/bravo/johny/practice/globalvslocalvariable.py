x = 10
print(x)


def g():
    global x
    print(x)
    x = 12


g()

print(x)
