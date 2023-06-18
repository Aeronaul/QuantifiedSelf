# Quantified Self (Python)
A web app to track your habits.

## Quantified Self Screenshot
![Tic-tac-toe screenshot](screenshot.jpg?raw=true)

## Features
- User Authentication:
  - Login page with username and password fields.
  - Register page with additional field for confirming the password.
  - Users can directly sign in from the login page after registering.
- Main Dashboard:
  - Displays a list of trackers and the time of the last entry in each tracker.
  - Actions available: editing and deleting trackers.
- Adding New Trackers:
  - Large button on the main dashboard for adding new trackers.
  - Takes the user to a new page to specify the name and type of the tracker (numeric, yes/no, or MCQ).
  - The input presentation changes based on the chosen tracker type.
- Accessing Previous Logs and Graphs:
  - Trackers' names on the dashboard are hyperlinks that take the user to the respective tracker page.
  - Tracker page displays a graph plotting the user's entered values over time (dates).
- Data Retrieval and Graph Generation:
  - The app retrieves stored data from the database.
  - Passes the data to a function from the Matplotlib library to create a graph.
  - The graph is stored in the 'static' folder along with other image resources.
- Tracker Page:
  - Below the graph, there is a table of records made by the user.
  - Provides options to edit or delete records on the right column.
- Tracker Editing and New Entry:
  - Tracker page includes buttons for editing the tracker and making a new entry.

## Getting Started
To get a local copy of the project up and running on your machine, follow these steps:

### Prerequisites
- Python3
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

