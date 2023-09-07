# Modular Robotic End-effector for Microsurgery

This repository contains all the scripts created for the Modular Robotic End-effector for microsurgery developed from scratch as part of my dissertation at the Department of BioEngineering at Imperial College London.

## Installation

1. Create an environment with Python `>= 3.9.6` and install the dependencies listed in `requirements.txt`
```
python3 -m venv effector
source env/bin/activate
pip install -f requirements.txt
```

2. Install the Kortex Python API either by installing the [wheel included in this repository](kortex_api-2.6.0.post3-py3-none-any.whl) or by following the instructions in [their github](https://github.com/Kinovarobotics/kortex/blob/master/linked_md/python_quick_start.md)
3. You may also want to install [Arduino IDE](https://www.arduino.cc/en/software) to load the Arduino's code into a brand-new Arduino. 

## Usage

### Xbox Controller

The Xbox controller can be used to communicate both with the end effector and the Kinova arm, simultaneously. To start it, run:

`python XboxController\xboxController2.py`

### Arduino Nano

To interact with the Arduino directly through Arduino IDE:

1. Start Arduino IDE
2. Load the file `XboxController\instrument_test.ino` into Arduino.
3. Use the Serial Monitor to send commands following the programmed interface. More details on the dissertation's report.

## Structure

The repository is structured as below:

1. [Data](Data): contains the data collected from task 1
2. [Force_data](Force_data): contains the total raw data collected from task 2
3. [task2_results](task2_results): contains the processed results from task 2
4. [XboxController](XboxController):
    1. [xboxController2.py](XboxController\xboxController2.py): code to receive commands from Xbox controller and execute them calling Arduino or Kinova robotic arm
    2. [move_angular_and_cartesian.py](XboxController\move_angular_and_cartesian.py) and [utilities.py](XboxController\utilities.py): used to perform movements with the Kinova Robotic arm
    3. [instrument_test.ino](XboxController\instrument_test.ino): microcontroller (Arduino code) of the end-effector
5. [force_test_plots.ipynb](force_test_plots.ipynb): processing of results and graph for the Force tests with each instrument
6. [Frequency.ipynb](Frequency.ipynb): processing frequency of the signal while performing Task 2
7. [FSR_calibration.ipynb](FSR_calibration.ipynb): FSR calibration results and graph of weights vs voltage
8. [kinematics.ipynb](kinematics.ipynb): kinematics calculations and experiment results
9. [results_questionnaire_task1.ipynb](results_questionnaire_task1.ipynb): analysis of Task 1 results for time and plots of the questionnaire answers
10. [Task2_experimental_results.ipynb](Task2_experimental_results.ipynb): analysis and plots for Task 2 (all data)
11. [Task2_mean_trial.ipynb](Task2_mean_trial.ipynb): analysis and plots for Task 2 (mean trial)
12. [trigger_mapping.ipynb](trigger_mapping.ipynb): mapping of pressed trigger vs. the distance between the jaws
13. [wrist_twist.ipynb](wrist_twist.ipynb): graph of the force vs angle per instrument
14. [kortex_api-2.6.0.post3-py3-none-any.whl](kortex_api-2.6.0.post3-py3-none-any.whl): copy of the Kortex API's wheel. You may also get it from [their repository]((https://github.com/Kinovarobotics/kortex/tree/master).
15. [Results.xlsx](Results.xlsx): results of the questionnaire, the time spent on task 1 and time for changing instrument
16. [twist_test.xlsx](twist_test.xlsx): results of force vs angle of rotation while holding the three instruments when they are completely close and completely open
