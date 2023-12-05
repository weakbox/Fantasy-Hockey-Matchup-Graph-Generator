import json
import jsbeautifier as jb
import os
import glob as gb
import matplotlib.pyplot as plt
import numpy as np

FILE_PATH = 'C:\\Users\\conno\\Desktop\\Matchup Graphs\\'   # Location to save generated graphs.
BAR_GRAPH_WIDTH = 0.30                                      # Constant for bar graph width.

def input_list():
    """
    Takes user input for a list of game-day data.

    Returns:
    list: A list containing data for each game-day.
    """
    new_list = []
    n = int(input('Enter the number of game-days in this week: '))
    for i in range(n):
        new_data = float(input(f'Enter data for day {i+1}: '))
        new_list.append(new_data)
    return new_list

def create_new_team():
    """
    Creates a new team with user input for team details.

    Returns:
    dict: A dictionary containing team details.
    """
    new_team = {}
    new_team['name'] = input("Enter the team's full name -> ")
    new_team['abbreviation'] = input("Enter the team's abbreviation -> ").lower()
    new_team['owner'] = input("Enter the team's owner -> ")
    new_team['color'] = input("Enter the team's color -> ")
    json_save(new_team, f"{new_team['abbreviation']}.json")

def team_view_info():
    """
    Displays information about a team.

    Parameters:
    team (dict): A dictionary containing team details.
    """
    team_id = input("Enter the team's abbreviation -> ").lower()
    team_dict = json_open(f"{team_id}.json")
    print(f"Displaying data for {team_dict['abbreviation']}:")
    print(f"\tName: {team_dict['name']} ({team_dict['abbreviation']})")
    print(f"\tOwner: {team_dict['owner']}")
    print(f"\tColor: {team_dict['color']}")

def team_add_data():
    """
    Adds data for a specific week to a team's record.

    Parameters:
    team (dict): A dictionary containing team details.
    """
    team_id = input("Enter the team's abbreviation -> ").lower()
    team_dict = json_open(f"{team_id}.json")
    week = input('Enter the week you would like to enter data for -> ')
    data = input_list()
    team_dict[f'{week}'] = data
    json_save(team_dict, f"{team_dict['abbreviation']}.json")
    print(f"Added new data to {team_dict['name']} for week {week}!")

def team_process_data(team):
    """
    Takes a team dictionary and plots the data for a specified week.

    Parameters:
    team (dict): A dictionary containing team details and data for different weeks.

    Returns:
    None
    """
    week = input('Enter week you would like to plot: ')

    if f'{week}' in team:
        data = team[f'{week}']
        # Use list comprehension to convert the data into floats from strings.
        data_floats = [float(x) for x in data]
        plt.plot(data_floats)
        plt.title('Processed Data')
        plt.xlabel('Day')
        plt.ylabel('Points')
        plt.show()
    else:
        print(f'ERROR: Data for week {week} does not exist.')

def json_open(path):
    """
    Opens and reads a JSON file, returning the parsed content as a dictionary.

    Parameters:
    path (str): The path to the JSON file.

    Returns:
    dict: The parsed JSON content.

    Raises:
    FileNotFoundError: If the specified file is not found.
    """
    if os.path.exists(path):
        with open(path, 'r') as file:
            team = json.loads(file.read())
            return team
    else:
        raise FileNotFoundError(f"The file {path} is missing!")
    

def json_save(team, path):
    """
    Saves a team's data to a JSON file.

    Parameters:
    team (dict): A dictionary containing team details.
    path (str): The path to the JSON file.
    """
    jb_options = jb.default_options()
    jb_options.indent_size = 2

    with open(path, 'w') as file:
        file.write(jb.beautify(json.dumps(team), jb_options))
        print('Your changes were saved successfully.')

def generate_matchup_plots(away_team_id, home_team_id, week):
    away_team = json_open(f'{away_team_id}.json')
    home_team = json_open(f'{home_team_id}.json')
    print(f"Plotting {away_team['name']} vs. {home_team['name']} using week {week}'s data set...")
    plot_matchup_bar(home_team, away_team, week)
    plot_matchup_scatter(home_team, away_team, week)

def team_modifier():
    while True:
        print('Choose an action:')
        print('\t1: Create New Team')
        print('\t2: View Existing Team')
        print('\t3: Add New Data')
        print('\t0: Return to Main Menu')

        action = int(input('Your input -> '))
        match action:
            case 1:
                print('Chose action: Create New Team')
                create_new_team()
            case 2:
                print('Chose action: View Existing Team')
                team_view_info()
            case 3:
                print('Chose action: Add New Data')
                team_add_data()
            case _:
                print('Chose action: Return to Main Menu')
                break
        action = 0

# Bar graph: shows how many points each team scored on each day.
def plot_matchup_bar(away_team, home_team, week):
    plt.figure(1)

    away_team_data = away_team[f"{week}"]
    away_team_data_floats = [float(x) for x in away_team_data]

    home_team_data = home_team[f"{week}"]
    home_team_data_floats = [float(x) for x in home_team_data]

    x = np.arange(len(home_team_data))

    plt.bar(x - BAR_GRAPH_WIDTH/2, away_team_data_floats, width=BAR_GRAPH_WIDTH, label=away_team['name'], color=away_team['color'])
    plt.bar(x + BAR_GRAPH_WIDTH/2, home_team_data_floats, width=BAR_GRAPH_WIDTH, label=home_team['name'], color=home_team['color'])

    plt.xlabel('Day')
    plt.ylabel('Points')
    plt.title(f"{away_team['name']} vs. {home_team['name']} Points-Per-Day")
    plt.legend()
    plt.grid(True)

# Scatter plot: shows the accumulation of team points throughout the week.
def plot_matchup_scatter(away_team, home_team, week):
    plt.figure(2)  # Use the 'figure' parameter for specifying the figure number.

    away_team_data = away_team[f"{week}"]
    away_team_data_floats = [float(x) for x in away_team_data]

    home_team_data = home_team[f"{week}"]
    home_team_data_floats = [float(x) for x in home_team_data]

    x = np.arange(len(home_team_data) + 1)

    # Insert a zero into the first index of the data array for a more readable graph.
    # Performs a shallow copy to avoid modifying the original data set.
    away_data_copy = away_team_data_floats.copy()
    away_data_copy.insert(0,0)
    home_data_copy = home_team_data_floats.copy()
    home_data_copy.insert(0,0)

    plt.plot(x, np.cumsum(away_data_copy), label=away_team['name'], linewidth = 3, color=away_team['color'])
    plt.plot(x, np.cumsum(home_data_copy), label=home_team['name'], linewidth = 3, color=home_team['color'])

    plt.xlabel('Day')
    plt.ylabel('Points')
    plt.title(f"{away_team['name']} vs. {home_team['name']} Points Trend")
    plt.legend()
    plt.grid(True)

# League-wide scatter plot: Shows the race for the President's Trophy.
def plot_presidents_trophy_race(week):
    plt.figure(3)
    
    # Iterate through all json files in directory and extract data.
    for team_json in gb.glob('*.json'):
        print(f'Parsing file: {team_json}')
        team = json_open(team_json)
        team_data = []

        for i in range(week):
            # Use a default value if the key is not present!
            team_data.append(team.get(str(i + 1), 0))
        
        team_cumsum = []
        team_cumsum = np.insert(np.cumsum(team_data), 0, 0).flatten()
        
        x = np.arange(len(team_cumsum))

        plt.plot(x, team_cumsum, label=team['name'], linewidth = 3, color=team['color'])   

    plt.xlabel("Day")
    plt.ylabel('Fantasy Points')
    plt.title(f"The Race for the President's Trophy (Week {week})")
    plt.legend()
    plt.grid(True)

# ------------------------------------------------------------
#                           MAIN
# ------------------------------------------------------------

print('FHMGG: Fantasy Hockey Matchup Graph Generator')
print('Weakbox Industries 2023')
print(f'Looking for team data in: {os.getcwd()}')

while True:
    print('Choose an action:')
    print('\t1: Modify Team Data')
    print('\t2: Generate Matchup Plots')
    print('\t3: Generate Leaguewide Plots')
    print('\t4: Show Plots')
    print('\t0: Exit the Program')

    action = int(input('Your input -> '))

    match action:
        case 1:
            print('Chose action: Modify Team Data')
            team_modifier()
        case 2:
            print('Chose action: Generate Matchup Plots')
            away_team = input('Enter the away team abbreviation for this matchup -> ').lower()
            home_team = input('Enter the home team abbreviation for this matchup -> ').lower()
            week = int(input('Enter the week you would like to pull data from -> '))
            generate_matchup_plots(away_team, home_team, week)
        case 3:
            print('Chose action: Generate Leaguewide Plots')
            week = int(input('Enter the week you would like to plot until -> '))
            plot_presidents_trophy_race(week)
        case 4:
            print('Chose action: Show Plots')
            print('Please close all plots to continue using FHMGG...')
            plt.show()
        case _:
            print('Chose action: Exit the Program')
            break
    action = 0
