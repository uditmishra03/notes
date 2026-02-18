A = [[1, 2, 5], [1, 3, 223]]
# A = [[1, 2, 3]]

ans = []
for i in range(len(A)):
    # print(A[i])
    max = 0
    for j in range(len(A[i])):
        print("i:", i, "j:", j , "value: ", A[i][j])
        if max < A[i][j]:
            max = A[i][j]
    ans.append(max)

print(ans)
               