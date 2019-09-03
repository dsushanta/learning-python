
# Strings are immutable in Python

s1 = "Hello World"

print(s1[1:3])  # range
print(s1[0])
print(s1[:4])   # start from begining
print(s1[1:])

print("a" in s1)
print("e" in s1)
print("a" not in s1)
print("l" not in s1)
print("index of W in the string : %d" % s1.index("W"))
print("hey\nhello")
print("hey\thello")
print(r"hey\nhello")
print(r"hey\thello")
print(r"heyhello")

print("how you doing "*2)

s2 = "hello chandler"
s2 = s2.replace("chandler", "joey")
print(s2)
print("No of occurences of character l : %d" % s2.count("l"))

s2 = s2.upper()
print(s2)

s2 = s2.lower()
print(s2)

s3 = "hello"
s3 = "".join(reversed(s3))    # one way to reverse a string
print(s3)
s3 = s3[::-1]       # another way to reverse a string
print(s3)

print(s3.startswith("h"))
print(s3.endswith("o"))

s4 = "hello,world"
s5 = s4.split(",")  # this returns a list
for s6 in s5:
    print(s6)