![logo](res/logo3.png)


# Sleep Apnea Guardian - natHACKS 2022

Sleep Apnea Guardian is an affordable and non-invasive solution to detect sleep apnea using EEG brain signal. We use a comfortable and discreet wearable headband during sleep. When a person stops breathing, their brain responds by sending a certain pattern of signals which our software can detect and provide instant feedback. We also record all the apnea events throughout the night to create a detailed sleep quality report in the morning. With accessibility in mind, we developed a voice assistant using speech recognition to enable full voice control and customization. Affordable, non-invasive, and user-friendly, Sleep Apnea Guardian has great potential to serve high risk populations, relieve stress on the healthcare system, and help everyone get better sleep.

### Index
main.py - GUI, flow control and starting point

sim_graph_window.py - active sleep monitoring flow control and data preprocessing

SleepApneaDetect.py - detect apnea and plot live/simulated data

voice_assistant.py - voice recognition and audio instructions


### Requirements
- [Python](https://www.python.org/downloads/) 3.9 or above
- [virtualenv](https://docs.python.org/3/library/venv.html)
- All requirements within requirements.txt (refer to above for installation)

## Installation
```sh
git clone https://github.com/dreambigzhang/Sleep-Apnea-Guardian.git
cd Sleep-Apnea-Guardian
python3 main.py
```



Create a virtual environment to install the dependencies:
```sh
python -m venv <Environment-Name>  # For example  $ python -m venv python_boiler
```

Activate the virtual environment and install the dependencies (Platform-Specific):
#### Linux 
```sh
./<Environment-Name>/Scripts/activate  # ./python_boiler/Scripts/activate
pip install -r requirements.txt
```
#### MacOS 
```sh
./<Environment-Name>/bin/activate  # ./python_boiler/Scripts/activate
pip install -r requirements.txt
```
#### Windows (Powershell)
```sh
./<Environment-Name>/Scripts/Activate.ps1
pip install -r requirements.txt
```
