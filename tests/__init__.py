"""check for speed test"""
def user_choice():
    """User choice for speed test"""
    speed = input("Would you like run speed test Y/N?. This will take approx 3 min \nNOTE: Large temporary file(100MB) will be generated and deleted.")
    if speed in ('y', 'YES', 'yes', 'ye', 'Yes', 'Y'):
        choice = True
    else:
        choice = False
    return choice

SPEED_TEST = user_choice()