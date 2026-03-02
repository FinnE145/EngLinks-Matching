from data_utilities import load_excel, shelve_data, load_shelve

def best_tutor(student_data: dict, tutors: dict) -> str | None:
    """
    Break a tie between multiple tutors with a scoring algorithm

    Args:
        student_data: A dictionary containing the student's courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.

    Returns:
        The ID of the best tutor, or ``None`` if no suitable tutor is found.
    """
    pass

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
