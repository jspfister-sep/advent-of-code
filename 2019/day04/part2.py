import sys

def split_into_digits(n):
    return [int(c) for c in str(n)]

def digits_are_non_decreasing(digits):
    for i in range(len(digits) - 1):
        if digits[i] > digits[i + 1]:
            return False
    return True

def has_a_pair_of_equal_digits(digits):
    for i in range(len(digits) - 1):
        if (digits[i] == digits[i + 1] and 
                (i == 0 or digits[i - 1] != digits[i]) and
                (i == len(digits) - 2 or digits[i + 1] != digits[i + 2])):
            return True
    return False

min_val = int(sys.argv[1])
max_val = int(sys.argv[2])

num_valid_passwords = 0

for n in range(min_val, max_val + 1):
    digits = split_into_digits(n)
    if (digits_are_non_decreasing(digits) and has_a_pair_of_equal_digits(digits)):
        num_valid_passwords += 1

print(f'There are {num_valid_passwords} valid passwords'
        f'in the range [{min_val}, {max_val}]')
