part1 = False

with open("day2.in", "r") as f:
  count = 0
  line = f.readline()

  while line:
    left, pw = line.split(":")
    pw = pw.strip()
    b, l = left.strip().split()
    low, upp = map(int, b.split("-"))

    # Part 1
    if part1:
      x = pw.count(l)
      if low <= x <= upp:
        count += 1

    # Part 2
    else:
      # 1 indexed, inclusive bounds; assume len(pw) > upp
      if bool(pw[low-1] == l) != bool(pw[upp-1] == l):
        count += 1

    line = f.readline()
  print(count)
