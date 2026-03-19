from data_utilities import load_excel, shelve_data, load_shelve
#Comment
def best_tutor(student_data: dict, tutors: dict) -> int | None:
    """
    Break a tie between multiple tutors with a scoring algorithm

    Args:
        student_data: A dictionary containing the student's courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.

    Returns:
        The ID of the best tutor, or ``None`` if no suitable tutor is found.
    """
    # Note: this function should use the ranking criteria to return the best tutor's ID (as a number)
    
    best_id = None
    best_score = float('inf')
    
    for tutor_id, tutor_info in tutors.items():
        # Calculate a score for this tutor (lower is better)
        # Primary criteria: fewer students (load balancing)
        score = tutor_info.get("students", 0)
        
        if best_id is None or score < best_score:
            best_id = tutor_id
            best_score = score
    
    return best_id

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