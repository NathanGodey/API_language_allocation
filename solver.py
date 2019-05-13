from pymprog import *
from random_data import *
import random as rd
from time import time


#Generating data
COURSES = generate_random_course_list(30)
VOWS, WEIGHTS= generate_random_vow_matrix_and_weight_matrix(300, 10, COURSES)
NB_STUDENTS=len(VOWS)
NB_VOWS=len(VOWS[0])

#indexing the set of students
S=range(NB_STUDENTS)

#indexing the set of courses
C=range(len(COURSES))

#indexation of wishes for cartesian product
V=range(NB_VOWS)

#cartesian product of S and W
SxV=iprod(S, V)


##solving linear problem
deb = time()

assignment_model = model("assign")

# Variables
course_is_open = assignment_model.var('course is open', C, kind=bool)
course_headcount = assignment_model.var('course headcount', C)
student_gets_vow = assignment_model.var('student gets wish', SxV, kind=bool)


# Objective function
assignment_model.min(sum(
    WEIGHTS[s, v] * student_gets_vow[s, v]
    for s, v in SxV
))

# Constraints
for student in S:
    sum(student_gets_vow[student, v] for v in V) == 1
for course in C:
    course_is_open[course]<=1
    sum(student_gets_vow[s, v] * int(VOWS[s, v, course]) for s, v in SxV) == course_headcount[course]
    COURSES[course].min_students*course_is_open[course] <= course_headcount[course]
    COURSES[course].max_students*course_is_open[course] >= course_headcount[course]

# Solve

assignment_model.solve()
fin = time()

print("temps : ",fin-deb)

## building results

result=[0 for student in S]
open_courses=[course_is_open[course].primal for course in C]

for student, vow in SxV:
    if student_gets_vow[student, vow].primal!=0:
        result[student]=vow

#for student, vow in SxV:
#    if student_gets_vow[student, vow].primal!=0 and student_gets_vow[student, vow].primal!=1:
#        print(student, vow, student_gets_vow[student, vow].primal)

## results display
print('open courses:')
print(open_courses)
print('result:')
print(result)
print("Total cost = ", assignment_model.vobj())
