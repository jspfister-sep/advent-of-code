import sys

def is_valid_password(n):
    last_digit = n % 10
    left_digits = int(n / 10)
    has_adjacent_repeat = False

    while left_digits != 0:
        next_to_last_digit = left_digits % 10
        if last_digit < next_to_last_digit:
            return False
        if last_digit == next_to_last_digit:
            has_adjacent_repeat = True
        last_digit = next_to_last_digit
        left_digits = int(left_digits / 10)
    return has_adjacent_repeat

min_val = int(sys.argv[1])
max_val = int(sys.argv[2])

num_valid_passwords = 0

for n in range(min_val, max_val + 1):
    if is_valid_password(n):
        num_valid_passwords += 1

print(f'There are {num_valid_passwords} valid passwords'
        f'in the range [{min_val}, {max_val}]')
