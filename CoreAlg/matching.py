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

    if tutor1["students"] < tutor2["students"]:
        score1 += 1
    
    if tutor2["students"] < tutor1["students"]:
        score2 += 1

    if score1 > score2:
        return tutor1_id

    if score2 > score1:
        return tutor2_id    
    
    return tutor1_id

def match(student_data: dict, tutors: dict) -> int | None:
    """
    Match a student to the best available tutor based on their courses, availability, and additional criteria in the event of a tie. Updates the tutor's student count if a match is found.

    Args:
        student_data: A dictionary containing the student's desired courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.
    Returns:
        The ID of the matched tutor, or ``None`` if no suitable tutor is found.
    """
    # Note: this function should filter the tutors, and if there is a tie, call `best_tutor` to break the tie. Then it should return the ID of the best tutor (as a number)
    
    # Extract student's courses and availability
    student_courses = set(student_data.get("courses", []))
    student_availability = set(student_data.get("availability", []))
    
    # Filter tutors that match student's courses and availability
    matching_tutors = {}
    
    for tutor_id, tutor_info in tutors.items():
        tutor_courses = set(tutor_info.get("courses", []))
        tutor_availability = set(tutor_info.get("availability", []))
        
        # Check if tutor has at least one matching course and one matching availability slot
        if student_courses & tutor_courses and student_availability & tutor_availability:
            matching_tutors[tutor_id] = tutor_info
    
    # If no matching tutors found, return None
    if not matching_tutors:
        return None
    
    # If only one match, return that tutor
    if len(matching_tutors) == 1:
        matched_id = list(matching_tutors.keys())[0]
    else:
        # Multiple matches - use best_tutor to break the tie
        matched_id = best_tutor(student_data, matching_tutors)
    
    # Update the matched tutor's student count
    if matched_id is not None:
        tutors[matched_id]["students"] += 1
    
    return matched_id
