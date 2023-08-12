import datetime

person_id = input("Enter person identification number: ")
experiment_num = input("Enter experiment number: ")
trial_num = input("Enter trial number: ")


with open(f"person_{person_id}_exp_{experiment_num}_trial_{trial_num}_time_manual.csv", "w") as streamer:
    try:
        while True:
            input("Press Enter to save the date and time:")
            current_datetime = f'{datetime.datetime.now()}\n'
            print(current_datetime)
            streamer.write(current_datetime)
    except KeyboardInterrupt:
        print("\nExiting....")
