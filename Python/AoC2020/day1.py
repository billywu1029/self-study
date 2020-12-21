with open("day1.in", "r") as f:
  nums = list(map(int, f.read().strip().split("\n")))
  numset = set(nums)
  
  # Two-sum
  for i in nums:
    if 2020-i in numset:
      print(i, 2020-i, i * (2020-i))
      break
  
  # Three-sum
  for i in range(len(nums)):
    for j in range(i + 1, len(nums)):
      x = 2020 - nums[i] - nums[j]
      if x in numset: 
        print(nums[i], nums[j], x, nums[i] * nums[j] * x)
        exit()

