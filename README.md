# robotic_tool

1. [Data](Data): contains the data collected from task 1
2. [Force_data](Force_data): contains the total raw data collected from task 2
3. [task2_results](task2_results): contains the proccessed results from task 2
4. [XboxController](XboxController):
    1. [xboxController2.py](XboxController\xboxController2.py): code to received commands from xbox controller and excecute them calling arduino or kinova robotic arm
    2. [move_angular_and_cartesian.py](XboxController\move_angular_and_cartesian.py) and [utilities.py](XboxController\utilities.py): used to perform movements with the Kinova Robotic arm
    3. [instrument_test.ino](XboxController\instrument_test.ino): microcontroller (Arduino code) of the end-effector
5. [force_test_plots.ipynb](force_test_plots.ipynb): processing of results and graph for the Force tests with each instrument
6. [Frequency.ipynb](Frequency.ipynb): processing frequency of the signal while performing Task 2
7. [FSR_calibration.ipynb](FSR_calibration.ipynb): FSR calibration results and graph of weights vs voltage
8. [kinematics.ipynb](kinematics.ipynb): kinematics calculations and experiment results
9. [results_questionnaire_task1.ipynb](results_questionnaire_task1.ipynb): analysis of Task 1 results for time and plots of the questionnaire answers
10. [Task2_experimental_results.ipynb](Task2_experimental_results.ipynb): analysis and plots for Task 2 (all data)
11. [Task2_mean_trial.ipynb](Task2_mean_trial.ipynb): analysis and plots for Task 2 (mean trial)
12. [trigger_mapping.ipynb](trigger_mapping.ipynb): mapping of pressed trigger vs the distance between the jaws
13. [wrist_twist.ipynb](wrist_twist.ipynb): graph of the force vs angle per isntrument
14. [kortex_api-2.6.0.post3-py3-none-any.whl](https://github.com/Kinovarobotics/kortex/tree/master): link with instructons to install Kortex API 
15. [Results.xlsx](Results.xlsx): results of the questionnaire, the time spent of task 1 and time for changing instrument
16. [twist_test.xlsx](twist_test.xlsx): results of force vs angle of rotation while holding the three instruments when they are completely close and completely open
