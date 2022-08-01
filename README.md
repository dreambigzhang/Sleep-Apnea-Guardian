![logo](res/logo3.png)


# Sleep Apnea Guardian - natHACKS 2022

Our solution is to detect sleep apnea by analyzing the brain waves of sleeping patients. We use a comfortable and discreet wearable headband worn during sleep and software to analyze the data. When a person stops breathing, their brain responds by sending a certain pattern of signals which our software can detect. We can then wake the person out of their deep sleep by playing a gentle sound so they can resume breathing, without waking them up completely. 


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
