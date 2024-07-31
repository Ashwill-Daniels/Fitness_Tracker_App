"""This program allows the user to:
    Add new workout categories to the database.
    Update a workout category.
    Delete a workout category from the database.
    Add a workout goal.
    Add goal categories.
    Delete a goal category from the database.
    The program should be able to calculate the user's fitness goal
    progress based on the workouts and goals that they have provided.
"""

# Import the sqlite3 and datetime modules.
import sqlite3
import datetime 

# Holds all the names of the exercises in the table.
exercise_name_list = []

# Holds cardio workouts.
cardio_workouts = []

# Holds resistance trainings.
resistance_trainings = []


class Workout():
    """A class to handle all workout category processes."""
    
    def add_exercise(self):
        """Add a new workout category to the database."""

        # Request a name for the workout.
        exercise_name = (input("Please enter the name of the exercise \
category: ")).capitalize()
        
        while True:
            # Inquire what type of workout it is.
            exercise_type = (input("Is it a resistance or cardio exercise? \
")).lower()
            if exercise_type == "resistance" or exercise_type == "cardio":
                break

            else:
                print("Please enter either 'resistance' or 'cardio'")

        # Call different methods based on what the user selected.
        if exercise_type == "resistance":
            self.resistance_exercise(exercise_name)
        
        else:
            self.cardio_exercise(exercise_name)
        
    def resistance_exercise(self, exercise_name):
        """Adds a resistance type exercise to the database table."""

        while True:           
            try:
                # The number of sets, specifically for resistance 
                # training.
                num_of_sets = int(input("How many sets will the exercise \
be? "))           
                if num_of_sets < 1:
                    print("Please enter an appropriate number.")
                    continue
                
                break
            
            # Catch value errors.
            except ValueError:               
                print("Please enter a number value.")

        try:
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Count the records in the table.
            cursor.execute("""SELECT COUNT(*) FROM workout_category""")

            table_count = cursor.fetchone()

            # Check if the table is empty and if it is, set the ID to 1.
            if table_count[0] > 0:
                cursor.execute("""SELECT id FROM workout_category 
                                        ORDER BY id DESC LIMIT 1""")
                
                last_id = cursor.fetchone()
                last_id = last_id[0] + 1

            else: 
                last_id = 1

            # Add a record to the table.
            cursor.execute("""INSERT INTO workout_category(id, exercise_name, 
                        exercise_type, duration, num_of_sets)
                        VALUES(?, ?, ?, ?, ?)""", (last_id, exercise_name, 
                                                    "resistance", "N/A", 
                                                    num_of_sets))
            
            # Provide feedback to the user.
            print("The exercise has been added successfully.")

            database.commit()
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def cardio_exercise(self, exercise_name):
        """Adds a cardio type exercise to the database table."""

        while True:           
            try:
                # Get the duration of the cardio workout.
                exercise_duration = int(input("In minutes, what is the \
duration of the exercise? "))
                
                if exercise_duration < 1:
                    print("Please enter an appropriate number.")
                    continue
                
                break
            
            except ValueError:                
                print("Please enter a number value.")
        try:

            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Count the records in the table.
            cursor.execute("""SELECT COUNT(*) FROM workout_category""")

            table_count = cursor.fetchone()

            # Check if the table is empty and if it is, set the ID to 1.
            if table_count[0] > 0:
                cursor.execute("""SELECT id FROM workout_category 
                                        ORDER BY id DESC LIMIT 1""")
                
                last_id = cursor.fetchone()
                last_id = last_id[0] + 1

            else: 
                last_id = 1

            # Add a record to the table.
            cursor.execute("""INSERT INTO workout_category(id, exercise_name, 
                        exercise_type, duration, num_of_sets)
                        VALUES(?, ?, ?, ?, ?)""", (last_id, exercise_name, 
                                                    "cardio", 
                                                    exercise_duration, 
                                                    "N/A"))
            
            # Provide feedback to the user.
            print("The exercise has been added successfully.")

            database.commit()
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def sort_categories(self):
        """Obtain the table contents and add it to the cardio and
           resistance workout lists.
        """

        try:
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Select all data from the table.
            cursor.execute("""SELECT * from workout_category""")

            table_contents = cursor.fetchall()
            
            # Append to data to the appropriate list.
            for index in range (0, len(table_contents)):
                if table_contents[index][2] == "cardio":
                    cardio_workouts.append(table_contents[index])

                elif table_contents[index][2] == "resistance":
                    resistance_trainings.append(table_contents[index])

        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def show_exercise_names(self):
        """Print the names of all exercises and save it in a list."""

        print("---------------------------------------------------")
        for index in range (0, len(resistance_trainings)):
            print(resistance_trainings[index][1])
            exercise_name_list.append(resistance_trainings[index][1])

        for index in range (0, len(cardio_workouts)):
            print(cardio_workouts[index][1])
            exercise_name_list.append(cardio_workouts[index][1])

        print("---------------------------------------------------")

    def show_resistance_exercises(self):
        """Print resistance workouts stored in the database table."""
        
        print("Resistance workouts:")

        print("---------------------------------------------------")
        for index in range (0, len(resistance_trainings)):
            print(f"Name of exercise: {resistance_trainings[index][1]}\t \
Number of sets: {resistance_trainings[index][4]} sets")
            
    def show_cardio_exercises(self):
        """Print cardio workouts stored in the database table."""

        print("Cardio workouts:")

        print("---------------------------------------------------")
        for index in range (0, len(cardio_workouts)):
            print(f"Name of exercise: {cardio_workouts[index][1]}\t \
Duration of workout: {cardio_workouts[index][3]} minutes")
            
    def delete_exercise(self):
        """Delete an existing record in the table."""

        # Prompt the user for a category.
        while True:
            user_input = (input("Which category will you delete from? \
")).lower()
            if user_input == "resistance" or user_input == "cardio":
                break

            else:
                print("Please enter either 'resistance' or 'cardio'.")

        name_found = False

        # Show the selected category's entries and prompt for a specific 
        # entry to delete.
        if user_input == "resistance":

            self.show_resistance_exercises()           
            
            while name_found == False:
                user_input = input("Please enter the name of the exercise you\
 wish to delete: ")
                
                for index in range(0, len(resistance_trainings)):
                    
                    if user_input == resistance_trainings[index][1]:
                        name_found = True
                        break

                if name_found:
                    break

                else:
                    print("Please enter an existing workout name.")

        else:
            self.show_cardio_exercises()
            
            while name_found == False:
                user_input = input("Please enter the name of the exercise you\
 wish to delete: ")
                
                for index in range(0, len(cardio_workouts)):
                    
                    if user_input == cardio_workouts[index][1]:
                        name_found = True
                        break

                if name_found:
                    break
                
                else:
                    print("Please enter an existing workout name.")

        try:
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Create the DELETE FROM SQL statement.
            cursor.execute("""DELETE FROM workout_category 
                           WHERE exercise_name = ?""",
                           (user_input, ))
            
            # Give feedback to the user.
            print("Exercise removed successfully.")

            database.commit()

        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()  
        
        
class Workout_routine(Workout):
    """Handles all workout routine processes."""

    def workout_routine_list(self):
        """Create a workout routine list, then return it as a string."""

         # A list to store the workout routine.
        routine_list = []

        # Keep track of the entries in the workout routine.
        index = 0
        
        # Keep running until the user is finished with the workout 
        # routine list (minimum 2 entries).
        while True:
            workout_name = input("Please enter a name from the list to add to \
the workout routine: ")
            
            valid_name = False

            for name in exercise_name_list:
                if workout_name == name:
                    valid_name = True
                    routine_list.append(name)
                    index += 1
                    
            if valid_name:
                if index > 1:
                    keep_adding = (input("Do you want to add another name? \
Type 'Y' or 'N'. ")).upper()
                    
                    if keep_adding == "Y":
                        continue

                    elif keep_adding == "N":
                        break

                    else:
                        break

            else:
                print("Please enter a name from the saved workouts.")
        
        # Convert the list into a string.
        routine_list_str = ",".join(routine_list)

        return routine_list_str

    def add_workout_routine(self):
        """Create a workout routine."""

        # Prompt the user for a name for the workout routine.
        routine_name = input("Please enter a name for the workout routine: ")
        
        print("These are the saved exercises:")

        # Show the user the existing workouts.
        self.show_exercise_names()

        # Create the list.
        saved_routine = self.workout_routine_list()

        # Prompt the user for a date and check the validity of the 
        # input.
        while True:
            start_date = input("Please enter a start date for the workout \
routine(format - YYYY-MM-DD): ")

            if len(start_date) == 10:
                break

            else:
                print("Please enter an appropriate date and format.")

        try:
            
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Count the records in the table.
            cursor.execute("""SELECT COUNT(*) FROM workout_routine""")

            table_count = cursor.fetchone()

            # Check if the table is empty and if it is, set the ID to 1.
            if table_count[0] > 0:
                cursor.execute("""SELECT id FROM workout_routine 
                                        ORDER BY id DESC LIMIT 1""")
                
                last_id = cursor.fetchone()
                last_id = last_id[0] + 1

            else: 
                last_id = 1

            # Add a record to the table.
            cursor.execute("""INSERT INTO workout_routine(id, routine_name, 
                        routine_list, start_date)
                        VALUES(?, ?, ?, ?)""", (last_id, routine_name, 
                                                    saved_routine, 
                                                    start_date))
            
            # Provide feedback to the user.
            print("Workout routine created successfully.")

            database.commit()
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def view_routines(self):
        """Print all workout routines stored in the database table."""

        try:           
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

            # Select all records from the table.
            cursor.execute("""SELECT * FROM workout_routine""")

            routines = cursor.fetchall()

            # Format and print the details in the database table.
            print("-----------------------------------------------")
            for index in range (0, len(routines)):
                print(f"Routine name: {routines[index][1]}\nWorkout list: \
{routines[index][2]}\nStart data: {routines[index][3]}")
                print("-----------------------------------------------")
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def exercise_progress(self):
        """Checks if the workout routine has started."""

        try:           
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()
 
            # Select only the routine_name field from the table.
            cursor.execute("""SELECT routine_name FROM workout_routine""")

            routine_names = cursor.fetchall()
            workout_routines = []

            # Add all the names to the new list.
            for index in range (0, len(routine_names)):
                workout_routines.append(routine_names[index][0])

            while True:
                user_input = input("Please enter a name of a workout \
routine: ")
                if user_input in workout_routines:
                    break

                else:
                    print("Incorrect input.")

            # Get the specific start_date field from the table.
            cursor.execute("""SELECT start_date FROM workout_routine 
                           WHERE routine_name = ?""",
                           (user_input,))
            
            start_date = cursor.fetchone()
            start_date = start_date[0]

            # Get the current date and cast it into string.
            current_date = str(datetime.date.today())
            
            # Turn the variables into lists.
            start_date = start_date.split("-")
            current_date = current_date.split("-")

            # Convert the string dates into datetime objects.
            # Format: YYYY, MM, DD
            # Reference - https://www.geeksforgeeks.org/comparing-dates-
            # python/
            start_date = datetime.datetime(int(start_date[0]), 
                                           int(start_date[1]), 
                                           int(start_date[2]))
            
            current_date = datetime.datetime(int(current_date[0]), 
                                             int(current_date[1]), 
                                             int(current_date[2]))

            if current_date > start_date:
                # Prints when the start date is in the past.

                # Cast the datetime object, format the strings and print
                # how many days until the workout routine starts.
                days_since = str(current_date - start_date)
                days_since = days_since.split(", ")
                days_since = days_since[0]

                print(f"Good job starting the new routine! It has been \
{days_since} since you started.")
                
            elif current_date < start_date:
                # Prints when the start date is in the future.

                # Cast the datetime object, format the strings and print
                # how many days until the workout routine starts.
                days_left = str(start_date - current_date)
                days_left = days_left.split(", ")
                days_left = days_left[0]

                print(f"You have {days_left} left until \
the routine starts!")
            
            else:
                # Prints when the current date and the start date is 
                # the same date.
                print("Your workout routine starts today. Good luck!")

        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()


class Fitness_goals(Workout):
    """Handles all fitness goal processes."""

    def set_fitness_goal(self):
        """Create a fitness goal entry."""

        lose_weight = False
        build_muscle = False

        goal_name = input("Please enter a name for your fitness goal: ")

        # Prompt the user to pick between the two types of fitness 
        # goals and call the appropriate method.
        while True:
            goal_type = (input("Please choose either 'lose weight' or \
'build muscle' as your fitness goal. ").lower())
                     
            if goal_type == "lose weight" or goal_type == "build muscle":
                break

            else:
                print("Incorrect input.")

        if goal_type == 'build muscle':
            self.build_muscle_goal()
            build_muscle = True

        else:
            self.lose_weight_goal()
            lose_weight = True

        # Prompt for the current and target weight of the user.
        while True:
            try:
                current_kg = float(input("Please enter your current weight in \
kilograms: "))
                if current_kg < 25:
                    print("Please enter an appropriate amount.")
                    continue

                else:
                    break
                
            except ValueError:
                print("Please enter an appropriate amount.")
        
        
        while True:
            try:
                target_kg = float(input("Please enter the target weight in \
kilograms: "))
                if target_kg < 25:
                    print("Please enter an appropriate amount.")
                    continue

                elif build_muscle:
                    if target_kg <= current_kg:
                        print("The target weight must be more than the \
current weight.")
                        continue

                    else:
                        break

                elif lose_weight:
                    if target_kg >= current_kg:
                        print("The target weight must be less than the \
current weight.")
                        continue

                    else:
                        break

                else:
                    break
                
            except ValueError:
                print("Please enter an appropriate amount.")

        print("You're all set. Good luck and have fun!")

        try:           
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

             # Count the records in the table.
            cursor.execute("""SELECT COUNT(*) FROM fitness_goal""")

            table_count = cursor.fetchone()

            # Check if the table is empty and if it is, set the ID to 1.
            if table_count[0] > 0:
                cursor.execute("""SELECT id FROM workout_category 
                                        ORDER BY id DESC LIMIT 1""")
                
                last_id = cursor.fetchone()
                last_id = last_id[0] + 1

            else: 
                last_id = 1

            # Add a new record to the table.
            cursor.execute("""INSERT INTO fitness_goal (id, goal_name, 
                           type_of_goal, current_kg, target_kg)
                           VALUES (?, ?, ?, ?, ?)""", (last_id, goal_name, 
                                                    goal_type, current_kg, 
                                                    target_kg))

            database.commit()
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

    def build_muscle_goal(self):
        """Create a fitness goal for building muscle."""
        
        print("""For building muscle, we recommend creating a workout \
routine that includes resistance training. 
Here is a list of resistance trainings in the exercise category: """)
            
        self.show_resistance_exercises()

        print("We will measure the amount of muscle weight you gain \
during this fitness goal.")
        
        
    def lose_weight_goal(self):
        """Create a fitness goal for losing weight."""

        print("""For weight loss, we recommend creating a workout \
routine that includes cardio exercises. 
Here is a list of cardio exercise categories: """)
            
        self.show_cardio_exercises()       

        print("We will measure the amount of weight you lose during this\
 fitness goal.")
        
    def fitness_goal_progress(self):
        """Check the user's fitness goal progress based on their current 
        weight.
        """
        try:           
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

             # Count the records in the table.
            cursor.execute("""SELECT goal_name FROM fitness_goal""")

            names = cursor.fetchall()
            name_list = []

            # Add all names to the new list.
            for index in range (0, len(names)):
                name_list.append(names[index][0])
        
        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

        while True:
            fitness_goal_name = input("Please enter the name of your saved \
fitness goal: ")
            
            if fitness_goal_name in name_list:
                break

            else:
                print("Name not found.")

        current_weight = float(input("Please enter your current weight: "))

        try:           
            database = sqlite3.connect("fitness_tracker_db.db")

            cursor = database.cursor()

             # Get the details of a specific record in the table.
            cursor.execute("""SELECT target_kg, type_of_goal 
                           FROM fitness_goal 
                           WHERE goal_name = ?""", (fitness_goal_name,))

            goal_details = cursor.fetchone()
            
            target_kg = goal_details[0]
            type_of_goal = goal_details[1]

        except sqlite3.Error as error:
            # Revert any changes.
            database.rollback()

            raise error
        
        finally:
            database.close()

        # Compare the user's current weight with the target weight and 
        # print an appropriate message.
        if type_of_goal == "lose weight":
            if current_weight == target_kg:
                print("Wow! You reached your goal!")

            elif current_weight < target_kg:
                print("Wow! You beat your target and you're still going!")

            else:
                print("You're not at your target weight yet. Good luck!")

        elif type_of_goal == "build muscle":
            if current_weight == target_kg:
                print("Wow! You reached your goal!")

            elif current_weight > target_kg:
                print("Wow! You beat your target and you're still going!")

            else:
                print("You're not at your target weight yet. Good luck!")


# Instances of all classes.
workout_obj = Workout()
workout_routine_obj = Workout_routine()
fitness_goal_obj = Fitness_goals()

while True:
    # Clear and update the lists that hold the table contents.
    resistance_trainings = []
    cardio_workouts = []
    workout_obj.sort_categories()

    user_input = input("""--------------FITNESS TRACKER APP-----------------
Welcome to The Fitness Tracker App, please select an option:
1. Add exercise category
2. View exercise by category
3. Delete exercise by category
4. Create Workout Routine
5. View Workout Routine
6. View Exercise Progress
7. Set Fitness Goals
8. View Progress towards Fitness Goals
9. Quit
Type your number selection here: """)
    
    if user_input == "1":
        workout_obj.add_exercise()
    
    elif user_input == "2":
        workout_obj.show_resistance_exercises()
        workout_obj.show_cardio_exercises()

    elif user_input == "3":
        workout_obj.delete_exercise()

    elif user_input == "4":
        workout_routine_obj.add_workout_routine()

    elif user_input == "5":
        workout_routine_obj.view_routines()

    elif user_input == "6":
        workout_routine_obj.exercise_progress()

    elif user_input == "7":
        fitness_goal_obj.set_fitness_goal()

    elif user_input == "8":
        fitness_goal_obj.fitness_goal_progress()

    elif user_input == "9":
        print("Thank you for using our services, goodbye!")
        break

    else:
        print("Sorry, that's an incorrect selection.")
