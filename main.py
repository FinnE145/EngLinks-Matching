"""
Main script to set up the algorithm and run it, as well as initialize and run the API and UI.
"""

"""
Excel file format:

    Tutor | course1 | course2 | ... | course10 | Availability1 | Availability2 | ... | Availability7


tutor_data format:

 *Tutor ID*
    ↓
{
    0: {
        "Name": "Tutor Name",
        "courses": [course1, ..., course10],
        "availability": [Availability1, ..., Availability7],
        "students": 10
    },
    1: {
        "Name": "Tutor Name",
        "courses": [course1, ..., course10],
        "availability": [Availability1, ..., Availability7],
        "students": 5
    },
    ...
}

student_data format:

 *Student ID*
    ↓
{
    0: {
        "name": "Student Name",
        "courses": [course1, ..., course10],
        "availability": [Availability1, ..., Availability7],
        "tutor": 0
    },
    1: {
        "name": "Student Name",
        "courses": [course1, ..., course10],
        "availability": [Availability1, ..., Availability7],
        "tutor": 1
    },
}
"""

from UI.app import create_app
from CoreAlg.matching import best_tutor, match
from data_utilities import load_excel, shelve_data, load_shelve, next_id
from iformat import iprint
import pandas as pd

# Load tutor data from excel and create/update the persistent shelve file with any new tutors or changed data, while preserving the number of students assigned to each tutor
# Assumes that there are no blank rows, tutors have not been removed or reordered (without the respective changes already made to the shelved data), and new tutors are added to the end of the Excel file.

excel_data = load_excel("Data/tutor_data.xlsx")             # Load the Excel file containing tutor data into a DataFrame
tutor_data = load_shelve("Data/tutor_data.shelve")          # Load the existing shelve data into a dictionary

if excel_data is not None:                                  # Check if the Excel file was loaded successfully
    for i, row in excel_data.iterrows():
        if not row.isnull().all():                              # Check if the row is not completely blank (to avoid creating empty tutor entries from blank rows)
            if i >= len(tutor_data.keys()):                         # Check if the current row index exceeds the number of existing tutors in the shelve data
                tutor_id = next_id(tutor_data)                          # ...if so, generate a new tutor ID using the next_id function
            else:
                tutor_id = tuple(tutor_data.keys())[i]                  # ...if not, use the existing tutor ID to update the existing tutor entry

            tutor_name = row["Tutor"]                               # Use the "Tutor" column value as the tutor name
            courses = row[1:10]                                    # Extract the course columns (assuming they are in columns 1-10)
            availability = row[11:18]                               # Extract the availability columns (assuming they are in columns 11-17)

            if tutor_data is not None and tutor_id in tutor_data:   # Check if the tutor already exists in the shelve data, and shelve data could be retrieved...
                students = tutor_data[tutor_id]["students"]             # ...if so, get the existing number of students for this tutor
            else:
                students = 0                                            # ...if not, initialize the number of students to 0

            tutor_data[tutor_id] = {                                # Add the new/updated tutor data to the shelve data dictionary
                "name": tutor_name,
                "courses": list(filter(lambda x: not pd.isna(x), courses)),
                "availability": list(filter(lambda x: not pd.isna(x), availability)),
                "students": students
            }

shelve_data(tutor_data, "Data/tutor_data.shelve")           # Save the updated tutor data back to the shelve file

#iprint(tutor_data)                                          # Print the tutor data to verify that it was loaded and shelved correctly

student_data = {
    0: {
        "name": "Test Student",
        "courses": ["MREN 178"],
        "availability": ["Monday", "Wednesday"],
        "tutor": 1
    },
    1: {
        "name": "Test Student 2",
        "courses": ["APSC 293", "APSC 174"],
        "availability": ["Tuesday", "Thursday"],
        "tutor": None
    }
}

matched_tutor_id = match(student_data[1], tutor_data)     # Test the matching algorithm with a sample student data dictionary
student_data[1]["tutor"] = matched_tutor_id                     # Update the sample student data with the matched tutor ID
iprint(f"Matched Tutor ID: {matched_tutor_id}, Matched Tutor Data: {tutor_data.get(matched_tutor_id)}")             # Print the ID of the matched tutor

if __name__ == "__main__":
    app = create_app(tutor_data=tutor_data, student_data=student_data)
    app.run(debug=True)
