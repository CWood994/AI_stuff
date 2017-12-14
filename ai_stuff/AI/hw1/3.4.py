import random
def run():
	money = 10
	count = 0
	while money >= 1:
		money -=1
		count += 1
		machine = [random.choice(["bar", "bell", "orange", "lemon", "cherry"]) for i in range(3)]
        same = 1
		if machine[0] == machine[1]:
			if machine[1] == machine[2]:
				same = 3
			else:
				same = 2
		if machine[0] == "cherry":
			money += same
		elif same == 3:
			if machine[0] == "bar":
				money += 25
			elif machine[0] == "bell":
				money += 10
			elif machine[0] == "orange":
				money += 5
			else:
				money += 4
	return count

def main(num):
	ans = [run() for i in xrange(num)]
	mean = sum(ans) / float(num)
	median = sorted(ans)[num/2]
	print "%s trials: mean=%s, median=%s" % (num, mean, median)

main(100000)
