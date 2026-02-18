A=[[1,2,3],[4,5,6],[7,8,9]]

B = [[9, 8, 7],   
     [6, 5, 4],   
     [3, 2, 1]]

# print(len(A))
# arr = [2, 3, 4]

c = []

for i in range(len(A)):
    c_row = []
    for j in range(len(A[i])):
        print(A[i][j], end=" ")
        print(B[i][j], end=" ")
        c_row.append(A[i][j] + B[i][j])
    c.append(c_row)
    print("\n")

# print("Print mat c: ")
for i in range(len(c)):
    for j in range(len(c[i])):
        print(c[i][j], end=" ")
    print("\n")

