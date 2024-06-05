import datetime


def get_current_quarter():
    current_month = datetime.datetime.now().month
    return (current_month - 1) // 3 + 1


if __name__ == "__main__":
    current_quarter = get_current_quarter()
    print(f"We are in Q{current_quarter} of the year.")
