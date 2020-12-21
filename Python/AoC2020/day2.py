with open("day2.in", "r") as f:
  count = 0
  line = f.readline()

  while line:
    left, pw = line.split(":")
    pw = pw.strip()
    b, l = left.strip().split()
    low, upp = map(int, b.split("-"))

    x = pw.count(l)
    if low <= x <= upp:
      count += 1

    line = f.readline()
  print(count)
