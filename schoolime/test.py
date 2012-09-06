from os import path

f = open("/Users/Stephen/Desktop/b.txt", "r")
lines = f.readlines()

for line in lines:
    print line

