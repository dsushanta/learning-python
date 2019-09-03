l1 = [10,20,30,40,50]

for ll in l1 :
    print(ll)

print("------------------------------------------")

for x in range(5,8) :
    print(x)

print("------------------------------------------")

for x in range(3,18,3) :
    print(x)

print("------------------------------------------")

c = 0
while(c < 5) :
    print(c)
    c += 1
else :
    print("Else part in while loop")

print("------------------------------------------")

for x in range(5) :
    print(x)
else :
    print("Else part in for loop")

print("------------------------------------------")

for x in range(5) :
    if x==2 :
        print(x)
        break
else :
    print("Else part in for loop") # this wont get printed because of the break statement

print("------------------------------------------")

for x in range(5) :
    if x==2 :
        print(x)
        continue
else :
    print("Else part in for loop") # this will still get printed even if we have continue