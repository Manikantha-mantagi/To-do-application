# To Do List Application Project by Teem 5, (Dileep, Deepak and Manikantha.

import os
from datetime import datetime

class TaskManager:
    # Manages tasks by date
    def __init__(self, base_file_name="tasks"):
        # Initialize
        self.__base_file_name = base_file_name
        self.date = None  # Init date
        self.__tasks = self.__load_tasks()  # Load tasks

    def __get_file_name(self):
        # Get file name
        if self.date:
            return f"{self.date.replace('/', '_')}_{self.__base_file_name}.txt"
        else:
            return f"temp_{self.__base_file_name}.txt"  # Temp file if no date

    def __load_tasks(self):
        # Load tasks from file
        file_name = self.__get_file_name()  # Get file name
        if not os.path.exists(file_name):
            return []  # Empty list if no file
        try:
            with open(file_name, "r") as file:
                return [line.strip() for line in file.readlines()]  # Read tasks
        except Exception as e:
            print(f"Error loading: {file_name}: {e}")
            return []  # Empty list on error

    def __save_tasks(self):
        # Save tasks to file
        file_name = self.__get_file_name()  # Get file name
        try:
            with open(file_name, "w") as file:
                for task in self.__tasks:
                    file.write(task + "\n")  # Write each task
        except Exception as e:
            print(f"Error saving: {file_name}: {e}")

    def set_date(self, date_str):
        # Set date
        try:
            self.date = datetime.strptime(date_str, "%d/%m/%Y").strftime("%d/%m/%Y")
            self.__tasks = self.__load_tasks()  # Load tasks for date
            print(f"Date set: {self.date}")
        except ValueError:
            print("Invalid date format. Use DD/MM/YYYY.")
            self.date = None
            self.__tasks = []  # Clear tasks if invalid

    def add_task(self, task):
        # Add task
        if self.date:
            self.__tasks.append(task)
            self.__save_tasks()
            print(f"Task '{task}' added to '{self.date}'.")
        else:
            print("Set date first.")

    def view_tasks(self):
        # View tasks
        if self.date:
            if not self.__tasks:
                print(f"'{self.date}' is empty.")
            else:
                print(f"Plan for '{self.date}':")
                for i, task in enumerate(self.__tasks, 1):
                    print(f"{i}. {task}")
        else:
            print("Set date first to view.")

    def remove_task(self, position):
        # Remove task
        if self.date:
            try:
                if 1 <= position <= len(self.__tasks):
                    removed = self.__tasks.pop(position - 1)
                    self.__save_tasks()
                    print(f"Task '{removed}' removed from '{self.date}'.")
                else:
                    print("Invalid position.")
            except ValueError:
                print("Enter valid number.")
            except IndexError:
                print("Invalid position.")
        else:
            print("Set date first to remove.")

    def update_task(self, position, new_task):
        # Update task
        if self.date:
            try:
                if 1 <= position <= len(self.__tasks):
                    self.__tasks[position - 1] = new_task
                    self.__save_tasks()
                    print(f"Task at {position} updated to '{new_task}' for '{self.date}'.")
                else:
                    print("Invalid position.")
            except ValueError:
                print("Enter valid number.")
            except IndexError:
                print("Invalid position.")
        else:
            print("Set date first to update.")

    def move_task_to_another_date(self, task_position, new_date):
        # Move a single task to another date and switch to that date
        try:
            new_date = datetime.strptime(new_date, "%d/%m/%Y").strftime("%d/%m/%Y")
            if 1 <= task_position <= len(self.__tasks):
                task_to_move = self.__tasks.pop(task_position - 1)
                self.__save_tasks()

                # Save task to the new date file
                new_manager = TaskManager()
                new_manager.set_date(new_date)
                new_manager.add_task(task_to_move)

                # Switch current manager to new date (open operated file)
                self.set_date(new_date)

                print(f"Task '{task_to_move}' has been moved and you're now working on {new_date}.")
            else:
                print("Invalid task position.")
        except ValueError:
            print("Invalid date format. Use DD/MM/YYYY.")
        except IndexError:
            print("Invalid task position.")

    def change_date_of_plan(self, new_date):
        # Change the date of the current plan (move all tasks to new date)
        try:
            new_date = datetime.strptime(new_date, "%d/%m/%Y").strftime("%d/%m/%Y")

            # Save current tasks to the new date file
            new_manager = TaskManager()
            new_manager.set_date(new_date)
            new_manager.__tasks = self.__tasks[:]  # Copy tasks
            new_manager.__save_tasks()

            # Delete old file silently
            old_file = self.__get_file_name()
            if os.path.exists(old_file):
                os.remove(old_file)

            # Update current object to point to new date
            self.set_date(new_date)

            print(f"All tasks have been moved. You're now working on {new_date}.")
        except ValueError:
            print("Invalid date format. Use DD/MM/YYYY.")

    def navigate_between_plans(self):
        # Let user pick a date-based plan from available files
        plan_files = [f for f in os.listdir() if f.endswith(f"_{self._TaskManager__base_file_name}.txt")]

        if not plan_files:
            print("No saved plans found.")
            return

        # Display available plans
        print("\nAvailable Plans:")
        date_map = {}
        for idx, file in enumerate(plan_files, 1):
            date_part = file.replace(f"_{self._TaskManager__base_file_name}.txt", "").replace("_", "/")
            date_map[idx] = date_part
            print(f"{idx}. {date_part}")

        try:
            choice = int(input("Enter the number of the plan to switch to: ").strip())
            if choice in date_map:
                self.set_date(date_map[choice])
            else:
                print("Invalid selection.")
        except ValueError:
            print("Enter a valid number.")
            
def show_menu(current_date):
    print(f"\nOptions for {current_date}:")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Remove Task")
    print("4. Update Task")
    print("5. Move Task to Another Date")
    print("6. Make New Plan")
    print("7. Change Date")
    print("8. Exit")
    print("n. Navigate Between Plans")

def main():
    # Main function
    manager = TaskManager()  # Create manager
    print('Hello,')  # Greeting
    user = input("Please enter your name: ").strip()  # Get name
    print("Welcome", user, "to your Date-Based To-Do List Application!")  # Welcome
    print("We're happy to assist you in tracking your daily routine.")  # Info
    print("Let's get started!")  # Start

    while True:
        date_input = input("Enter date (DD/MM/YYYY, or type 'today' or 'exit'): ").strip().lower()  # Get date input
        if date_input == 'exit':
            print("Thank you for using To do list application. Have a great day!")
            break
        elif date_input == 'today':
            today = datetime.now().strftime("%d/%m/%Y")
            manager.set_date(today)  # Set today's date
        else:
            manager.set_date(date_input)  # Set date

        if manager.date:
            while True:
                show_menu(manager.date)  # show menu every time

                choice = input("Enter choice: ").strip()

                if choice == "1":
                    task = input("Enter task: ").strip()
                    manager.add_task(task)
                elif choice == "2":
                    manager.view_tasks()
                elif choice == "3":
                    try:
                        position = int(input("Enter position to remove: ").strip())
                        manager.remove_task(position)
                    except ValueError:
                        print("Enter valid number.")
                elif choice == "4":
                    try:
                        position = int(input("Enter position to update: ").strip())
                        new_task = input("Enter new task: ").strip()
                        manager.update_task(position, new_task)
                    except ValueError:
                        print("Enter valid number.")
                elif choice == "5":
                    try:
                        task_position = int(input("Enter position of task to move: ").strip())
                        new_date = input("Enter new date (DD/MM/YYYY): ").strip()
                        manager.move_task_to_another_date(task_position, new_date)
                    except ValueError:
                        print("Enter valid number.")
                elif choice == "6":
                    break  # Make new plan
                elif choice == "7":
                    new_date = input("Enter the new date (DD/MM/YYYY) to change the plan: ").strip()
                    manager.change_date_of_plan(new_date)
                elif choice == "8":
                    print("Thank you for using To do list application. Have a great day!")
                    return
                elif choice.lower() == "n":
                    manager.navigate_between_plans()
                else:
                    print("Invalid choice.")
                    
if __name__ == "__main__":
    main()  # Run main
