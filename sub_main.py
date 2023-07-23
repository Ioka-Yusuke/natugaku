import numpy as np

toku = []

toku = sorted(toku)[::-1]
print(toku)
ans = []
k = len(toku)

for i in range(k):
    if i == 0:
        ans.append(abs(toku[0]-toku[1]))
    elif i == k-1:
        ans.append(abs(toku[k-1]-toku[k-2]))
    else:
        s = (abs(toku[i]-toku[i-1]) + abs(toku[i]-toku[i+1]))/2
        ans.append(s)

ans_a = []
for i in range(k):
    ans_a.append(1/ans[i])

min_value = min(ans_a)
cnt = 0

while True:
    if min_value * 10 < 1:
        min_value *= 10
        cnt += 1
    else:
        cnt += 1
        break

ans_a = np.array(ans_a)
ans_b = ans_a*pow(10, cnt)
ans_r = []

for num in ans_b:
    ans_r.append(round(num, 1))

print(ans_r)