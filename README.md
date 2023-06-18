# Quantified-Self (Python)
A web app to track your habits.

## Quantified-Self Screenshot
![Tic-tac-toe screenshot](screenshot.jpg?raw=true)

## Features
- Play against the computer: Challenge the computer and test your Tic-Tac-Toe skills.
- Play against another human player: Enjoy the game with a friend or family member.
- Watch the computer play against itself: Observe the computer playing both X and O positions.
- Easy-to-use graphical interface: The game board and controls are displayed using Java Swing components.

## Getting Started
To get a local copy of the project up and running on your machine, follow these steps:

### Prerequisites
- Python3
- Flask
- Flask-SQLAlchemy
- Jinja2
- SQLAlchemy
- matplotlib
- Git

### Installation
1. Clone the repository:
```
git clone https://github.com/Aeronaul/QuantifiedSelf_Python.git
```
```
cd QuantifiedSelf_Python
```
2. Optionally create a virutal environment:
```
python -m venv venv
```
```
source ./venv/bin/activate
```
3. Install requirements:
```
pip install -r requirements.txt
```
4. Run the application:
```
python run.py
```
5. Go to: http://127.0.0.1:5000/

## Usage
- The login page has a username and password field, while the register page has another field for confirming the password. Once registered, the user can directly sign in from the login page.
- On the main dashboard there is a list of trackers and the time of last entry in each tracker. There are also a few actions available like editing and deleting trackers.
- Below there is a large button for adding new trackers which takes to a new page for specifying the name and type of tracker (numeric, yes/no or MCQ.)
- Depending on which type you choose for the trackers, it will change the type of input presented when making the logs.
- To access the previous logs and graphs, the user has to click on the name of the trackers on the dashboard (they are hyperlinks.) This takes the user to the tracker page.
- On the tracker page, the user is presented with a graph plotting the values entered by the user over time (ie. dates).
- The app retrieves the stored data from the database and passes it to a function from the matplotlib library to create a graph. This graph is stored inside the 'static' folder alongside other image resources.
- Below the graph, there is a table of records made by the user. There is also the option of editing or deleting said records on the right column.
- On the tracker page, the user can also scroll down to find two buttons for editing the tracker and making a new entry.

## Acknowledgements
The Python programming language and Flask module.

## Contact
For any questions or inquiries, please contact me at: aeronaul@proton.me.

