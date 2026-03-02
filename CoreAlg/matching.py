from data_utilities import load_excel, shelve_data, load_shelve

def best_tutor(student_data: dict, tutors: dict) -> int | None:
    """
    Break a tie between multiple tutors with a scoring algorithm

    Args:
        student_data: A dictionary containing the student's courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.

    Returns:
        The ID of the best tutor, or ``None`` if no suitable tutor is found.
    """
    pass
    # Note: this function should use the ranking criteria to return the best tutor's ID (as a number)

def match(student_data: dict, tutors: dict) -> int | None:
    """
    Match a student to the best available tutor based on their courses, availability, and additional criteria in the event of a tie. Updates the tutor's student count if a match is found.

    Args:
        student_data: A dictionary containing the student's desired courses and availability.
        tutors: A dictionary of tutors with their courses, availability, and current student count.
    Returns:
        The ID of the matched tutor, or ``None`` if no suitable tutor is found.
    """
    pass
    # Note: this function should filter the tutors, and if there is a tie, call `best_tutor` to break the tie. Then it should return the ID of the best tutor (as a number)