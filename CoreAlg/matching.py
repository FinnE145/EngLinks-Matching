from data_utilities import load_excel, shelve_data, load_shelve

def best_tutor(student_data: dict, tutor1_id:int, tutor1: dict, tutor2_id: int, tutor2: dict) -> str | None:
    """
    Break a tie between multiple tutors with a scoring algorithm

    Args:
        student_data: A dictionary containing the student's courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.

    Returns:
        The ID of the best tutor, or ``None`` if no suitable tutor is found.
    """
    score1 = 0
    score2 = 0

    student_availability = student_data["availability"]

    for day in student_availability:
        if day in tutor1["availability"]:
            score1 += 1
    
    for day in student_availability:
        if day in tutor2["availability"]:
            score2 += 1

    if score1 > score2:
        return tutor1_id

    if score2 > score1:
        return tutor2_id    
    
    if tutor1["students"] < tutor2["students"]:
        return tutor1_id
    
    if tutor2["students"] < tutor1["students"]:
        return tutor2_id
    
    return None

def match(student_data: dict, tutors: dict) -> str | None:
    """
    Match a student to the best available tutor based on their courses, availability, and additional criteria in the event of a tie. Updates the tutor's student count if a match is found.

    Args:
        student_data: A dictionary containing the student's desired courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.
    Returns:
        The ID of the matched tutor, or ``None`` if no suitable tutor is found.
    """
    """L"""
    pass
