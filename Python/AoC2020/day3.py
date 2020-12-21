def prod(l):
  res = 1
  for i in l:
    res *= i
  return res

with open("day3.in", "r") as f:
  cols = [0] * 5
  incr = [1, 3, 5, 7, 1]
  trees = [0] * 5
  line = f.readline().strip()
  l = len(line)
  line_num = 0
  while line:
    for i in range(len(cols)):
      if i == len(cols) - 1 and line_num % 2 != 0:
        continue
      if line[cols[i] % l] == "#":
        trees[i] += 1
      cols[i] += incr[i]
    line = f.readline().strip()
    line_num += 1
  print(trees, prod(trees))
