with open("day1.in", "r") as f:
  nums = set(map(int, f.read().strip().split("\n")))
  for i in nums:
    if 2020-i in nums:
      print(i, 2020-i, i * (2020-i))
      break
  
