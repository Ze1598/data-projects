import pandas as pd

df = pd.read_csv("https://kustodetectiveagency.blob.core.windows.net/prime-numbers/prime-numbers.csv.gz", header=None)
numbers = df[0].tolist()
# Sort numbers in descending order
numbers = sorted(numbers, reverse=True)

# Flag to break the outer forLoop
c = 0
for i in range(len(numbers)):
	print(f"Testing index {i}, number {numbers[i]}")
	
	# Loop through the remaining smaller primes
	for j in range(i + 1, len(numbers)):
		# Test the sum of each consecutive prime pair plus 1
		# Ensure the code does not look outside the list range
		# If verified then found the answer
		if (j+1 < len(numbers)) and ((numbers[j] + numbers[j + 1] + 1) == numbers[i]):
			print(f"{numbers[i]} was the solution with values {numbers[j]} + {numbers[j + 1]} + 1")
			c += 1
			break
	if c > 0:
		break


# 99999517 was the solution with values 49999759 + 49999757 + 1
# https://aka.ms/99999517