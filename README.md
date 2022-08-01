![logo](res/logo3.png)


# Sleep Apnea Guardian - natHACKS 2022
Sleep apnea is a serious disorder in which breathing stops during sleep, which causes fatigue, heart disease, cognitive impairment, or even death. Shockingly, 80% of all people with sleep apnea are left undiagnosed. In response, we developed Sleep Apnea Guardian to offer an affordable and non-invasive solution to detect sleep apnea. We used **Brainflow** to obtain EEG signals from the Muse 2 BCI headset, **numpy** to preprocess the data, **matplotlib** to graph the data, and **PyQt5** to create an intuitive GUI. To detect sleep apnea in a patient’s brain signals, we convert the EEG signal into the frequency domain using **Fast Fourier Transformation**, and use a bandstop filter around 60Hz to remove interference from power lines. We then split it into 5 bands: delta (0.5 - 4Hz), theta (4 - 8Hz), alpha (8 - 13Hz) and beta ( > 13Hz).
The most significant indicator for sleep apnea is the rapid decrease in the ratio between the delta and beta bands, denoted ∂-β. Sleep Apnea Guardian can monitor ∂-β ratio changes during sleep and provide instant feedback. We also record all the apnea events throughout the night to create a detailed sleep quality report in the morning.
With accessibility in mind, we developed a voice assistant using **speech_recognition** to enable full voice control and customization.
Affordable, non-invasive, and user-friendly, Sleep Apnea Guardian has great potential to serve high risk populations, relieve stress on the healthcare system, and help everyone get better sleep.


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
