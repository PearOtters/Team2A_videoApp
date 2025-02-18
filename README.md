Team 2A video app project

## Prerequisites

- **Python** 3.11
- **Django** 2.2.28

## Installation

Begin by cloning the repository to your local machine:

```bash
git clone https://github.com/PearOtters/Team2A_videoApp.git
```


Create a virtual environment for dependencies:

Linux:
```bash
virtualenv <path-to-venv>
```
Windows:
```bash
py 3.11 -m venv <path-to-venv>
```

```Anaconda prompt
conda create -n <path-to-venv> python=3.11
```

Activate the virtual environment using the commands for your OS and CLI of choice:

| Platform | Shell | Command to activate virtual environment |
| :-: | :-: | :-: |
| POSIX | bash/zsh | source \<venv-path>/bin/activate |
| | fish | source \<venv-path>/bin/activate.fish |
| | csh/tsch | source \<venv-path>/bin/activate.csh |
| | Powershell | \<venv-path>/bin/Activate.ps1 |
| Windows | cmd.exe | \<venv-path>\Scripts\activate.bat |
| | Powershell | \<venv-path>\Scripts\Activate.ps1 |
| Anaconda Prompt || conda activate <path-to-venv>

Dependencies are then installed using `pip`:

```bash
pip install -r requirements.txt
```

Dependencies are now installed.

To complete the initial Django setup, the following needs to be run:

```bash
python manage.py makemigrations
``` 
and then,

```bash 
python manage.py migrate
```

This "imports" the changes made to the models throughout development.

To run the Django web app, run the following:

```bash
python manage.py runserver
```