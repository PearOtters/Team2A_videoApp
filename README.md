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

Anaconda prompt:
```bash
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
| Anaconda Prompt || conda activate <venv-path> |

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

## Creating and using branches

If creating branch in terminal:

```bash
  git checkout -b branch-name
```
This will also move you within your terminal into the branch. If this is done you can then do the normal git add * etc to commit.

If creating branch on webclient:

Click on branches and then select create new branch and follow instructions. Once done in terminal do command:

```bash
  git checkout branch-name
```

Once you have done this you can now commit your code to your branch in the usual way with git add * etc.


## Keeping your branch up to date with main by pulling main into your branch

WHEN MERGING ALWAYS ENSURE IT IS TO 'ORIGIN MAIN' NOT JUST 'MAIN'

Firstly make sure you are on your branch

```bash
git checkout <branch-name>
```

Fetch changes from the remote respository

```bash
git fetch origin
```

Merge main into your branch
```bash
git merge origin/main
```

If there are conflicts it will say in the terminal, after resolving these through vscode's built in
merge conflict resolver or through your preferred method
```bash
git add *
git commit -m "your message"
```

## Merging with main

Ensure your branch is up to date with main
```bash
git checkout <your-branch>
git fetch origin
git merge origin/main
```

Switch to main
```bash
git checkout main
```

Merge your branch into main
```bash
git merge <your-branch>
```

If there are conflicts it will say in the terminal, after resolving these through vscode's built in
merge conflict resolver or through your preferred method
```bash
git add *
git commit -m "your message"
```

Push the updated main branch to the remote repository
```bash
git push origin main
```
