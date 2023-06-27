import string
import random


def generate_verify_code():
    nums = ','.join(string.digits[1:]).split(',')
    random.shuffle(nums)
    result = ','.join(nums).replace(',', '')[0:4]
    return result
