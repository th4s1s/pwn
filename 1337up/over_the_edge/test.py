import numpy as np
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

def process_input(input_value):
    num1 = np.array([0], dtype=np.uint64)
    num2 = np.array([0], dtype=np.uint64)
    num2[0] = 0
    a = input_value
    if a < 0:
        return "Exiting..."
    num1[0] = (a + 65)
    num1[0] = num2[0] - 1337 - 65
    print(num1[0]) # the number we're looking for
    if (num2[0] - num1[0]) == 1337:
        return 'You won!\n'
    return 'Try again.\n'

print(process_input(int(input('>> '))))