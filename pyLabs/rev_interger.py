n = int(input("Enter the number: "))
rev =0
print("Actual number: ", n)
while n > 0:
    print(n)
    rev = rev* 10 + n% 10
    n = n //10
    print(rev)

print("Reversed number: ", rev)