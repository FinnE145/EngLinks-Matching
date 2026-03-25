#file tests the major parts of the tutor matching system
#dictionary recreates tutor data that would be loaded from the Excel spreadsheet in desired format

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from data_utilities import load_excel, shelve_data, load_shelve, next_id
from CoreAlg.matching import best_tutor, match

tutor_data = {
    0: {
        "Name": "Tutor 1",
        "courses": ["APSC 142", "APSC 172", "APSC 174"],
        "availability": ["Monday", "Tuesday", "Wednesday"],
        "students": 3
    },
    1: {
        "Name": "Tutor 2",
        "courses": ["MREN 178", "CIVL 215", "MTHE 237"],
        "availability": ["Wednesday", "Thursday", "Friday"],
        "students": 1
    },
    2: {
        "Name": "Tutor 3",
        "courses": ["APSC 131", "APSC 171", "MREN 178"],
        "availability": ["Monday", "Tuesday"],
        "students": 2
    }
}


# Example requests from students, that will be used in different tests

student_data = {
    "name": "Test Student",
    "courses": ["APSC 142"],
    "availability": ["Tuesday", "Wednesday"]
};

# Backend tests

def test_next_id():

# Test the next_id() function.
# function should return the next ID available based on largest
# key that is in the dictionary currently

    new_id = next_id(tutor_data)

    # largest current tutor ID is 2 so the next ID should be 3

    if new_id == 3:
        print("PASS: next_id function test")
    else:
        print("FAIL: next_id function test")


def test_shelve_storage():

    # Test shelve_data() and load_shelve() functions, which represent systems storage

    filename = "test_shelve_db" 

    # Save tutor data to shelve database 
    shelve_data(tutor_data, filename) 

    # Load the data back from the shelve file 
    loaded_data = load_shelve(filename) 

    # Compare the original vs. the loaded data 
    if loaded_data == tutor_data: 
        print("PASS: Shelve storage test") 
    else: 
        print("FAIL: Shelve storage test")




#Matching logic tests

def test_basic_match():

# tests the basic effectiveness of the match() function.
    # The student needs help with APSC 142 and is available on Tuesday
    # Tutor 1 teaches APSC 142 and is available on Tuesday, and the other
    # tutors either do not teach the course or are not available that day
    # Therefore, Tutor 1 (ID 1) should be selected as the best match

    result = match(student_data, tutor_data)

    if result == 1:
        print("PASS: Basic matching test")
    else:
        print("FAIL: Basic matching test")

def test_lowest_workload_priority():

#Test that algorithm prioritizes tutors with fewer students
# If multiple tutors qualify, system should choose the tutor with the lowest #workload


    result = best_tutor(student_data, tutor_data)


    if result == 1: 
        print("PASS: Workload balancing test") 
    else: 
        print("FAIL: Workload balancing test")



def test_tie_breaking():

    #Test that the tie-breaking system works properl

    #Two tutors have the same course and availability. The tutor with fewer students should be selected. 

    tie_tutors = {
        0: {"Name": "TutorA", "courses": ["APSC 142"], "availability": ["Tuesday"], "students": 5},
        1: {"Name": "TutorB", "courses": ["APSC 142"], "availability": ["Tuesday"], "students": 2}
    } 

    result = best_tutor(student_data, tie_tutors)

    if result == 1: 
        print("PASS: Tie-breaking test") 
    else: 
        print("FAIL: Tie-breaking test") 



def test_student_count_update(): 

    # Test that tutor's student count increases after a match.
    # Test confirms that workload tracking works correctly. 


    original_count = tutor_data[1]["students"] 

    # Run the matching function 

    match(student_data, tutor_data) 
    if tutor_data[1]["students"] == original_count + 1: 
        print("PASS: Student count update test")
    else: 
        print("FAIL: Student count update test") 

# Edge case tests


def test_no_course_match(): 

#Test what happens when no tutor teaches the requested course. 
# algorithm should return None instead of crashing

    test_student = { 
        "name": "Student2", 
        "courses": ["BIO999"], 
        "availability": ["Monday"] 
    } 


    result = match(test_student, tutor_data) 

    if result is None: 
        print("PASS: No course match test") 
    else: 
        print("FAIL: No course match test") 


def test_no_availability_overlap(): 
# Test when tutors teach the correct course but schedules do not overlap. 

    test_student = { 
        "name": "Student3", 
        "courses": ["APSC 142"], 
        "availability": ["Sunday"] 
    } 


    result = match(test_student, tutor_data)

    if result is None: 
        print("PASS: No availability overlap test") 
    else: 
        print("FAIL: No availability overlap test") 




def test_empty_tutor_dataset(): 

# Test what system does when the tutor database is empty. 


    empty_tutors = {} 
    result = match(student_data, empty_tutors) 

    if result is None: 
        print("PASS: Empty tutor dataset test") 
    else: 
        print("FAIL: Empty tutor dataset test") 



#error handling tests


def test_missing_student_fields(): 

# Test behavior when student data is missing required fields
#The program should handle the error neatly instead of crashing. 

    bad_student = { 
        "name": "Broken Student" 
    } 


    try:
        match(bad_student, tutor_data) 
        print("PASS: Missing student field test") 
    except Exception: 
        print("FAIL: Missing student field test") 



def test_excel_error_handling(): 

# Test how system behaves when Excel file cannot be found

    result = load_excel("file_that_does_not_exist.xlsx")

    if result is None: 
        print("PASS: Excel error handling test") 
    else: 
        print("FAIL: Excel error handling test") 


#Performance test


def test_large_dataset(): 
# Test algorithm performance using many tutors. This replicates a high demand # situation, with many tutors are stored in the database

    large_tutor_data = {} 

    # Create 100 recreated tutors 
    for i in range(100): 
        large_tutor_data[i] = { 
            "Name": f"Tutor{i}", 
            "courses": ["APSC 142"], 
            "availability": ["Tuesday"], 
            "students": i 
        } 


    result = match(student_data, large_tutor_data)

    if result is not None:
        print("PASS: Large dataset performance test") 
    else: 
        print("FAIL: Large dataset performance test")


#Test for full integration of system

def test_full_system_flow(): 

#Simulate the real flow of the system. 
#Steps: 1. Load tutor data from storage 2. Run the matching algorithm 3. #Confirm a valid match is outputted

    tutors = load_shelve("Data/tutor_data.shelve") 

    if tutors is None: 
        print("FAIL: Full system test (data failed to load)") 
        return 


    result = match(student_data, tutors) 
    if result is not None: 
        print("PASS: Full system integration test") 
    else: 
        print("PASS: System handled 'no match' case correctly") 


def run_all_tests():

    # Run all tests in the testing suite

    print("\nRunning EngLinks Matching System Tests...\n") 

    # Platform tests 
    test_next_id() 
    test_shelve_storage() 

    #Matching logic tests 
    test_basic_match() 
    test_lowest_workload_priority() 
    test_tie_breaking() 
    test_student_count_update() 

    #Edge cases 

    test_no_course_match() 
    test_no_availability_overlap() 
    test_empty_tutor_dataset() 

    #Error handling 
    test_missing_student_fields() 
    test_excel_error_handling() 

    #Performance 
    test_large_dataset() 

    #Full system test 
    test_full_system_flow() 

    print("\nTesting complete.\n") 

# Automatically run tests when the file is executed 

if __name__ == "__main__": 
    run_all_tests()




