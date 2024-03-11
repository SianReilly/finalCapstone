#######################   TASK 17: CAPSTONE PROJECT   #############################################################
# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

#===== Importing Libraries===========
import os
from datetime import datetime, date

# Date and time format used throughout the program
DATETIME_STRING_FORMAT = "%Y-%m-%d"


## FIRST CREATING ALL THE FUNCTIONS REQUIRED:

# Function to register a new user
def reg_user(username_password):
    while True:
        # Prompt user to enter a new username and password
        new_username = input("New Username: ")
        # Check if the username already exists
        if new_username in username_password:
            print("Username already exists. Please choose a different username.")
            continue
        new_password = input("New Password: ")
        confirm_password = input("Confirm Password: ")
        # Confirm passwords match
        if new_password == confirm_password:
            print("New user added")
            # Add new user to the dictionary and write to file
            username_password[new_username] = new_password
            with open("user.txt", "w") as out_file:
                user_data = [f"{k};{username_password[k]}" for k in username_password]
                out_file.write("\n".join(user_data))
            break
        else:
            print("Sorry, Passwords do not match. Please try again.")


# Function to add a new task
def add_task(task_list, username_password):
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User doesn't exist, please can you enter a valid username")
        return
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            # Use the provided logic to ensure the due date is in the right format
            our_date = task_due_date.split("-")
            our_date = list(map(lambda x: int(x), our_date))
            due_date_time = date(our_date[0], our_date[1], our_date[2])
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    curr_date = date.today()
    # Create a new task dictionary
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }
    # Append new task to the task list
    task_list.append(new_task)
    # Update tasts.txt file with the new task
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    # Display all tasks with corresponding index
    for idx, task in enumerate(task_list, start=1):
        disp_str = f"Task {idx}:\n"
        disp_str += f"Title: {task['title']}\n"
        disp_str += f"Assigned to: {task['username']}\n"
        disp_str += f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\n{task['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(task_list, curr_user):
    print("Your Tasks:")
    # Filter tasks assigned to the current user
    user_tasks = [(idx, task) for idx, task in enumerate(task_list, start=1) if task['username'] == curr_user]
    for idx, task in user_tasks:
        disp_str = f"Task {idx}:\n"
        disp_str += f"Title: {task['title']}\n"
        disp_str += f"Assigned to: {task['username']}\n"
        disp_str += f"Date Assigned: {task['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: {task['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description:\n{task['description']}\n"
        print(disp_str)
    # Prompt user to select a task to edit
    task_idx = int(input("Enter the number of the task to edit, or -1 to return to the main menu: "))
    if task_idx == -1:
        return
    selected_task = user_tasks[task_idx - 1][1]
    if selected_task['completed']:
        print("You cannot edit a completed task.")
        return
    action = input("Enter 'm' to mark the task as complete, 'e' to edit: ")
    if action == 'm':
        selected_task['completed'] = True
        print("Task marked as complete.")
    elif action == 'e':
        field_to_edit = input("Enter 'username' to edit assigned username, 'due_date' to edit due date: ")
        if field_to_edit == 'username':
            new_username = input("Enter new username: ")
            selected_task['username'] = new_username
            print("Username updated.")
        elif field_to_edit == 'due_date':
            while True:
                try:
                    new_due_date = input("Enter new due date (YYYY-MM-DD): ")
                    our_date = new_due_date.split("-")
                    our_date = list(map(lambda x: int(x), our_date))
                    selected_task['due_date'] = date(our_date[0], our_date[1], our_date[2])
                    print("Due date updated.")
                    break
                except ValueError:
                    print("Invalid datetime format. Please use the format specified")
        else:
            print("Invalid option.")
# Function to generate reports
def generate_reports(task_list, username_password):
    # Task Overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    today_date = date.today()  # Get today's date

    # Calculate overdue tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < today_date)

    # Calculate percentages
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview:\n")
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Incomplete tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage:.2f}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage:.2f}%\n")

    # User Overview
    total_users = len(username_password)
    user_task_counts = {username: sum(1 for task in task_list if task['username'] == username) for username in
                        username_password}

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview:\n")
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")
        for username, task_count in user_task_counts.items():
            completed_count = sum(1 for task in task_list if task['username'] == username and task['completed'])
            incomplete_count = task_count - completed_count
            overdue_count = sum(1 for task in task_list if task['username'] == username and
                                not task['completed'] and task['due_date'].date() < today_date)
            percentage_assigned = (task_count / total_tasks) * 100 if total_tasks != 0 else 0
            percentage_completed = (completed_count / task_count) * 100 if task_count != 0 else 0
            percentage_incomplete = (incomplete_count / task_count) * 100 if task_count != 0 else 0
            percentage_overdue = (overdue_count / task_count) * 100 if task_count != 0 else 0

            user_overview_file.write(f"\n{username}:\n")
            user_overview_file.write(f"Total tasks assigned: {task_count}\n")
            user_overview_file.write(f"Percentage of total tasks assigned: {percentage_assigned:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks completed: {percentage_completed:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks incomplete: {percentage_incomplete:.2f}%\n")
            user_overview_file.write(f"Percentage of tasks overdue: {percentage_overdue:.2f}%\n")


# Function to display the statistics
def display_statistics(task_list, username_password):
    # Check if reports exist, if not, generate them
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        print("Generating reports...")
        generate_reports(task_list, username_password)
    
    # Display the task overview report
    with open("task_overview.txt", "r") as task_overview_file:
        print(task_overview_file.read())

    # Display the user overview report
    with open("user_overview.txt", "r") as user_overview_file:
        print(user_overview_file.read())
    

# Main function
def main():
    # Check and create files if they don't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass
    
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Read user data from file
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Parse user data
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # Login
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password:
            print("This user does not exist.")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login was successful!")
            logged_in = True

    # Read task data from file
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]
    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)


    # Main menu loop
    while True:
        print()
        # Display main menu
        menu = input('''Please select one of the following options:
        r - Register user
        a - Add task
        va - View all tasks
        vm - View my tasks
        gr - Generate reports
        ds - Display statistics
        e - Exit                
        : ''').lower()
        if menu == 'r':
            reg_user(username_password) # Call the function to register a user
        elif menu == 'a':
            add_task(task_list, username_password) # Call the function to add a task
        elif menu == 'va':
            view_all(task_list) # Call the function to view all tasks
        elif menu =='vm':
            view_mine(task_list, curr_user) # Call the function to view tasks assigned to the current user
        elif menu == 'gr':
            generate_reports(task_list, username_password)  # Call function to generate reports
            print("Reports generated successfully.")
        elif menu == 'ds' and curr_user == 'admin':
            display_statistics(task_list, username_password)  # Call function to display statistics
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")


if __name__ == "__main__":
    main()
