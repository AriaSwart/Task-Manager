#=====Importing libraries===========
from datetime import datetime


#=====File checking functions===========
def user_password(user_name):
    with open('user.txt', 'r') as file:
        for line in file:
            if user_name == line.split(", ")[0]:
                return (line.split(", ")[1].strip('\n'))
    return (False)

def user_exists(user_name):
    if user_password(user_name):
        return (True)
    else:
        return (False)


#=====Formatted outputs===========
def format_task(task_line, task_num: int = -1):
    name, title, descript, due, date, completion = task_line.split(', ')
    completion = completion.strip('\n')
    task = f'''Task: \t\t\t{title}
Assigned to:   \t\t{name}
Date assigned: \t\t{date}
Due date:      \t\t{due}
Task Complete? \t\t{completion}
Task description:
 {descript}
---------------------------------------------------------'''
    if (task_num >= 0):
        task = f'Task [{task_num}]\n' + task
    return (task)


def reg_user(user_name):
    # Take input from user and check for already existing entry in file
    if user_exists(user_name):
        print(f"Error: User '{user_name}' already exists.")

    else:
        # Check password - add to file if matches, display message otherwise
        password = input("Enter password: ")
        if password == input("Confirm password: "):
            print("Password confirmed - Creating user")
            with open('user.txt', 'a') as user_file:
                user_file.write(f"\n{user_name}, {password}")   
 
        else:
            print("Error: Password does not match.")


#=====File interactions===========
# # This code block will allow a user to add a new task to task.txt file
def add_task():
    name = input("Assign task to: ")
    if not user_exists(name):
        print("Error: User not found")
    else:
        # Prompt user for information on task to be added and store it
        title = input("Assign a title: ")
        descript = input("Assign description: ")
        due = input("Assign Due Date: ")
        due = datetime.strftime(datetime.strptime(due, "%d %b %Y").date(), "%d %b %Y")
        
        # Get current date and format it for addition to file
        date = datetime.strftime(datetime.today().date(), '%d %b %Y')
        submit = f"\n{name}, {title}, {descript}, {due}, {date}, No"
        
        # Add the data to the file task.txt
        with open('tasks.txt', 'a') as file:
            file.write(submit)



# This code block will allow a user to edit a task in the task.txt file
def edit_task(task_index: int):
    # Pulls data from file and cleans lines
    with open('tasks.txt', 'r') as file:
        tasks = [line.replace("\n", '') for line in file.readlines()]
        print(tasks)


    # Confirms current task to user and breaks line down for working
    print(f"Current Task Details:\n")
    line = tasks[task_index]
    print(format_task(line))
    line = line.split(', ')

    # Checks completion state and lets you change completion state
    if line[5] == 'Yes':
        user_input = input('Mark Task as incomplete? (Yes/No)\n: ').lower()
        if user_input == 'yes':
            line[5] = 'No'
    elif line[5] == 'No':
        user_input = input('Mark Task as complete? (Yes/No/Edit)\n: ').lower()
        if user_input == 'yes':
            line[5] = 'Yes'

        # Checks previous prompt for edit confirmation
        elif user_input == 'edit':
            print('Editing task - leave blank to keep old data')
            name = input("Assign task to: ")

            if (name == '') or (user_exists(name)):
                # Prompt user for information on task to be edited - store if valid or ignore if blank
                if name != '':
                    line[0] =  name
                title = input("Assign a title: ")
                if title != '':
                    line[1] =  title
                descript = input("Assign description: ")
                if descript != '':
                    line[2] =  descript
                due = input("Assign Due Date: ")
                if due != '':
                    line[3] = datetime.strftime(datetime.strptime(due, "%d %b %Y").date(), "%d %b %Y")
                
            # Prints error if username is invalid
            else:
                print("Error: User not found - Cannot edit")

        # Recondense lines for writing to file
        line = ', '.join(line)
        tasks[task_index] = line
        tasks = '\n'.join(tasks)

        # Write the data to the file task.txt
        with open('tasks.txt', 'w') as file:
            file.write(tasks)
            


#=====Data Processing===========
# Generates a list of task numbers based on username
def task_numbers(username: str, include_complete: bool):
    num_list = []
    num = 0
    with open('tasks.txt', 'r') as file:
        for line in file:
            line = line.replace('\n', '')
            line = line.split(', ')
            if (username == "") or (username == line[0]):
                if (include_complete == True) or (line[5] == 'No'):
                    num_list.append(num)
            num += 1
    return (num_list)


# Generates reports for specific user
def user_report(user_name):
    # Get basic information while protecting agains division by 0
    total_tasks = len(task_numbers(user_name, True))
    assigned = (total_tasks / len(task_numbers('', True))) * 100
    if total_tasks > 0:
        incomplete = (len(task_numbers(user_name, False)) / total_tasks) * 100
    else:
        incomplete = 0

    # Compare due dates to current date and tally overdue taks
    overdue = 0
    pending = task_numbers(user_name, False)
    date = datetime.today().date()
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()
        for num in pending:
            due = datetime.strptime(tasks[num].split(', ')[3], "%d %b %Y").date()
            if due < date:
                overdue += 1
    
    # Protect against division by 0
    if total_tasks > 0:
        overdue = (overdue / len(task_numbers(user_name, False))) * 100
    else:
        overdue = 0

    # Build output
    out = f'''User:  \t\t\t{user_name}
Total Tasks:   \t\t{total_tasks}
Assigned (%):  \t\t{assigned}%
Completed (%): \t\t{100 - incomplete}%
Incomplete (%):\t\t{incomplete}%
Overdue (%):   \t\t{overdue}%'''
    return (out)

def user_overview():
    # Establish basic numbers and header statistics
    with open('user.txt', 'r') as file:
        total_users = len(file.readlines())
    overview = f'''Total Users:   \t\t{total_users}
Total Tasks:   \t\t{len(task_numbers('', True))}\n\n'''
    
    # Add per user report
    with open('user.txt', 'r') as file:
        users = file.readlines()
        for line in users:
            user = line.split(', ')[0]
            overview = overview + user_report(user) + '\n\n'
    return (overview[:-2])


# Generates general task overview
def task_overview():
    total_tasks = len(task_numbers('', True))
    incomplete = len(task_numbers('', False))

    # Compare due dates to current date and tally overdue taks
    overdue = 0
    pending = task_numbers('', False)
    date = datetime.today().date()
    with open('tasks.txt', 'r') as file:
        tasks = file.readlines()
        for num in pending:
            due = datetime.strptime(tasks[num].split(', ')[3], "%d %b %Y").date()
            if due < date:
                overdue += 1
    overdue_percent = (overdue / len(task_numbers('', False))) * 100
    pending = (len(pending) / total_tasks) * 100

    # Build output
    overview = f'''Total Tasks:  \t\t{total_tasks}
Completed:  \t\t{total_tasks - incomplete}
Uncompleted:\t\t{incomplete}
Overdue:    \t\t{overdue}
Pending (%):\t\t{pending}%
Overdue (%):\t\t{overdue_percent}%'''
    return (overview)


# Generates a summary from the overall task list based on task_numbers
def task_summary(task_numbers: list):
    track = 0
    summary = '---------------------------------------------------------\n'
    with open('tasks.txt', 'r') as file:
        for line in file:
            complete = line.split(', ')[5]
            complete = complete.replace('\n', '')
            if (track in task_numbers) and (complete == 'No'):
                summary = summary + f'{format_task(line, task_numbers.index(track))}\n'
            track += 1
    return (summary[:-1])


# This function will selectively get tasks and display them before allowing editing
def view_mine(user_name: str, show_complete: bool = True):
    numbers = task_numbers(user_name, show_complete)
    summary = task_summary(numbers)
    prompt = "Select a task (-1 to exit): "
    print(summary)
    num = int(input(prompt))
    tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            tasks.append(line)
        while num != -1:
            edit_task((numbers[num]))
            num = int(input(prompt))

# This function exists because the document says it must
def view_all():
    view_mine("")

def generate_reports():
    with open('user_overview.txt', 'w') as file:
        file.write(user_overview())
    with open('task_overview.txt', 'w') as file:
        file.write(task_overview())


#====Login Section====
def login():
    login = False
    while not login:
        username = input("Please enter your username: ")
        if user_exists(username):
            if user_password(username) == input("Please enter your password: "):
                login = True
            else:
                print("Password incorrect, please try again.")
        else:
            print("Username incorrect, please try again.")
    print(f'Welcome, {username}.')
    return (username)

#====Interface Section=========
print('''Welcome to Task Manager!
    Please Log in to continue
    -----------------------------''')

username = login()
while True:
    # Present the menu to the user and 
    # make sure that the user input is converted to lower case.
    print("Select one of the following options:")
    if username == 'admin':
        print('''r - register a user
gr - generate report
ds - display statistics''')
    menu = input('''a - add task
va - view all tasks
vm - view my tasks
u - change user
e - exit
: ''').lower()


    if (menu == 'r') and (username == 'admin'):
        reg_user(input("Enter new username: "))

    elif (menu == 'gr') and (username == 'admin'):
        generate_reports()

    elif (menu == 'ds') and (username == 'admin'):
        generate_reports()
        print('Task Overview\n--------------------------')
        with open('task_overview.txt', 'r') as file:
            task_report = ''.join(file.readlines())
            print(task_report)
        print('\n\nUser Overview\n--------------------------')
        with open('user_overview.txt', 'r') as file:
            users_overview = ''.join(file.readlines())
            print(users_overview)
        print('\n')


    elif menu == 'a':
        add_task()

    # This code block will read all the tasks from task.txt file and display them
    elif menu == 'va':
        view_all()

    # This code block will read the user's tasks from task.txt file and display them
    elif menu == 'vm':
        show_complete = input('Show completed tasks? (Yes/No)\n: ').lower
        if show_complete == "yes":
            show_complete = True
        view_mine(username, show_complete)

    elif menu == 'u':
        login()

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made entered an invalid input. Please try again")