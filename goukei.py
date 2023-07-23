list_m = [3, 4, 1, 2, 2, 5, 2, 3, 2, 2, 2, 3]
list_s = [50, 45, 34, 11, 58, 25, 12, 19, 52, 54, 47, 58, 55]
ans = sum(list_m)
sum_s = sum(list_s)

ans += sum_s//60 + 1
print(ans)