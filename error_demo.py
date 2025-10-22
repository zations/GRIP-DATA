# error_demo.py
def divide(a, b):
    return a / b  # division by zero error will happen

def main():
    nums = [10, 0, 5]
    result = divide(nums[0], nums[1])  # ZeroDivisionError
    print("Result:", result)

if __name__ == "__main__":
    main()
