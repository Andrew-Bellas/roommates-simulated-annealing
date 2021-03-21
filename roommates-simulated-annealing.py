import argparse
import random
import math
import time

parser = argparse.ArgumentParser()
parser.add_argument('-f', '--file', nargs='?', default='roommates.txt',
                    help='Specify the input file. Defaults to roommates.txt')
parser.add_argument('-T', '--temperature', nargs='?', type=int,
                    default=1000, help='The initial temperature, defaults to 1000')
parser.add_argument('-s', '--student-count', nargs='?', type=int, default=200,
                    help='The number of students being placed into rooms, defaults to 200')
parser.add_argument('-c', '--room-capacity', nargs='?', type=int,
                    default=4, help='The number of students per room, defaults to 4')
parser.add_argument('-a', '--cooling-factor', nargs='?', type=int, default=.95,
                    help='The cooling factor for the temperature, defaults to 0.95')
args = parser.parse_args()

INPUT_FILE = args.file
INITIAL_TEMPERATURE = args.temperature
COOLING_FACTOR = args.cooling_factor
STUDENT_COUNT = args.student_count
ROOM_CAPACITY = args.room_capacity
NUMBER_OF_ROOMS = STUDENT_COUNT / ROOM_CAPACITY


class Room:
    def __init__(self, room_number, students):
        self.room_number = room_number
        self.students = students

    def calculate_compatibility_score(self):
        result = 0
        for i in range(len(self.students) - 1):
            for j in range(i + 1, len(self.students)):
                result = result + \
                    self.students[i].ratings[self.students[j].student_number]
        return result


class Student:
    def __init__(self, student_number, ratings):
        self.student_number = student_number
        self.ratings = ratings


class Rooms:
    def __init__(self, student_list):
        self.rooms = self.assign_random_rooms(student_list)

    def average_room_score(self):
        score = 0
        for room in self.rooms:
            score = score + room.calculate_compatibility_score()
        return score / NUMBER_OF_ROOMS

    def best_room_score(self):
        lowest = self.rooms[0].calculate_compatibility_score()
        for room in self.rooms:
            score = room.calculate_compatibility_score()
            if score < lowest:
                lowest = score
        return lowest

    def worst_room_score(self):
        highest = self.rooms[0].calculate_compatibility_score()
        for room in self.rooms:
            score = room.calculate_compatibility_score()
            if score > highest:
                highest = score
        return highest

    def assign_random_rooms(self, student_list):
        room_count = int(STUDENT_COUNT / ROOM_CAPACITY)
        rooms = []

        for i in range(room_count):
            first_student = i * ROOM_CAPACITY
            last_student = first_student + ROOM_CAPACITY
            rooms.append(Room(i, student_list[first_student:last_student]))
        return rooms

    def print_rooms(self):
        print('Room Assignments: ')
        for room in self.rooms:
            print('  Room Number: ' + str(room.room_number))
            students = []
            for student in room.students:
                students.append(student.student_number)
            print("    Students: " + str(sorted(students)))
            print("    Score: " + str(room.calculate_compatibility_score()))
        print()

    def optimize_rooms(self):
        def swap_students(students_one, students_two, student_one_index, student_two_index):
            students_one[student_one_index], students_two[student_two_index] = students_two[student_two_index], students_one[student_one_index]

        def is_change_accepted(old_score, new_score):
            if old_score > new_score:
                return True
            if old_score == new_score:
                return False

            acceptance_probability = math.exp((old_score - new_score) / T)
            if random.random() < acceptance_probability:
                return True
            return False

        T = INITIAL_TEMPERATURE
        total_attempted_change_counter = 0
        accepted_change_counter = 0
        attempted_change_counter = 0
        current_compatibility_score = self.average_room_score()
        while(accepted_change_counter != 0 or attempted_change_counter < 20000):
            room_one = random.choice(self.rooms)
            room_two = random.choice(self.rooms)
            swap_strategy = random.getrandbits(1)

            if(swap_strategy):
                # Select 2 rooms at random, and 1 student at random from each room; exchange them
                student_one_index = random.randrange(ROOM_CAPACITY - 1)
                student_two_index = random.randrange(ROOM_CAPACITY - 1)

                swap_students(room_one.students, room_two.students,
                              student_one_index, student_two_index)
            else:
                # Swap the first 2 students in one room with the last 2 students in the other.
                swap_students(room_one.students,
                              room_two.students, 0, ROOM_CAPACITY - 2)
                swap_students(room_one.students,
                              room_two.students, 1,  ROOM_CAPACITY - 1)

            swapped_compatibility_score = self.average_room_score()

            if(is_change_accepted(current_compatibility_score, swapped_compatibility_score)):
                # Accept change
                accepted_change_counter = accepted_change_counter + 1
                current_compatibility_score = swapped_compatibility_score
            else:
                # Revert change
                if(swap_strategy):
                    swap_students(room_one.students, room_two.students,
                                  student_one_index, student_two_index)
                else:
                    swap_students(room_one.students,
                                  room_two.students, 0, ROOM_CAPACITY - 2)
                    swap_students(room_one.students,
                                  room_two.students, 1,  ROOM_CAPACITY - 1)
            attempted_change_counter = attempted_change_counter + 1
            total_attempted_change_counter = total_attempted_change_counter + 1
            # Reset counters and reduce T every so often
            if (attempted_change_counter > 20000 or accepted_change_counter >= 2000):
                T = T * COOLING_FACTOR
                attempted_change_counter = 0
                accepted_change_counter = 0
        return 0


def parse_input_file_into_student_list():
    file = open(INPUT_FILE, 'r')
    lines = file.readlines()

    students = []
    for i in range(STUDENT_COUNT):
        students.append(Student(i, list(map(int, lines[i].split()))))
    return students


def print_output(rooms):
    print('Parameters:')
    print('  Initial Temperature: ' + str(INITIAL_TEMPERATURE))
    print('  Cooling Factor: ' + str(COOLING_FACTOR))
    print('  Execution time: ' + str(time.perf_counter()) + 'sec')
    print('Results:')
    print('  Average Room Score: ' + str(rooms.average_room_score()))
    print('  Best Room Score: ' + str(rooms.best_room_score()))
    print('  Worst Room Score: ' + str(rooms.worst_room_score()))
    rooms.print_rooms()


rooms = Rooms(parse_input_file_into_student_list())
rooms.optimize_rooms()
print_output(rooms)
