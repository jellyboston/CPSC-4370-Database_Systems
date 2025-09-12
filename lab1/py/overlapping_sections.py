"""
Find overlapping sections

This task joins the section and time_slot tables to get the section and time slot details for each section. We will then
compute the overlapping sections based on the time slots.

E.g., the following two sections overlap on Monday from 10:00 to 10:15:
    CPSC-437-001, Monday, 2017, fall, 09:00-10:15
    CPSC-237-002, Monday, 2017, fall, 10:00-10:45

The above example was used for illustration purposes only and is not necessarily the
shape of the data you will be working with.

Author: Rami Pellumbi
"""
# feel free to add any imports you need here that do not require a package
# outside of requirements.txt or the standard library
from typing import TypedDict

from database_connection import DatabaseConnection


# utility type for time slots
TimeSlotInfo = TypedDict(
    "TimeSlotInfo",
    {
        "course_id": str,
        "sec_id": str,
        "day": str,
        "semester": str,
        "year": int,
        "start_hr": int,
        "start_min": int,
        "end_hr": int,
        "end_min": int,
    },
)


def is_overlap(slot1: TimeSlotInfo, slot2: TimeSlotInfo) -> None | tuple[str, str]:
    """
    Given two time slots, return None if they do not overlap, or a tuple of the
    start and end time of the overlap if they do.

    - The start and end time should be formatted as HH:MM

    NOTE: This function should be implemented with respect to the type definition `TimeSlotInfo`.
    """
    # TODO: implement this function
    start1, end1 = (
                    slot1.start_hr * 60 + slot1.start_min,
                    slot1.end_hr * 60 + end1.end_min
    )
    start2, end2 = (
                    slot2.start_hr * 60 + slot2.start_min,
                    slot2.end_hr * 60 + slot2.end_min
    )
    
    if end1 >= start2 and end2 >= start1:
        # compute the overlap window
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        # convert back to hours
        start_hr, start_min = overlap_start // 60, overlap_start % 60
        end_hr, end_min = overlap_end // 60, overlap_end % 60
        return (
            f"{overlap_start // 60:02d}:{overlap_start % 60:02d}",
            f"{overlap_end // 60:02d}:{overlap_end % 60:02d}"
        )
    return None

def get_overlapping_sections() -> list[tuple[TimeSlotInfo, TimeSlotInfo, str, str]]:
    """
    Implement this function to complete the task. It should return a list of tuples where each tuple contains:
    """
    overlaps = []

    with DatabaseConnection() as cursor:
        # TODO 1: write a SELECT sql query to get the section and time slot details for each section
        cursor.execute(
            """
            SELECT s.course_id, s.sec_id, t.day, s.semester, s.year, t.start_hr, t.start_min, t.end_hr, t.end_min
            FROM section s JOIN time_slot t
            USING (time_slot_id)
        """
        )
        schedules = cursor.fetchall()
        # TODO 2: map the schedules into a list of TimeSlotInfo objects
        timeslots = []
        for row in schedules:
            course_id, sec_id, day, semester, year, start_hr, start_min, end_hr, end_min = row
            timeslots.append(TimeSlotInfo(
                course_id, sec_id, day, semester, year, start_hr, start_min, end_hr, end_min
            ))

        # TODO 3: find overlapping sections
        for i in range(len(schedules) - 2):
            start, end = is_overlap(timeslots(i, i+1))
            if start and end:
                overlaps.append(timeslots[i], timeslots[i+1], start, end)

        # TODO 4: return the overlapping sections as a list of tuples. If A and B overlap, do not return both (A,B) and (B,A)
        return overlaps 


def print_overlapping_sections(overlaps: list[tuple[TimeSlotInfo, TimeSlotInfo, str, str]]) -> None:

    if not overlaps:
        print("No overlapping sections.")
        return

    # TODO 5: for each overlapping pair of sections A and B
    # print (A,B) followed by a new line.
    # Your output should look like:
    # (A,B)
    # (M,W)
    # (S,P)

    # Note that A, B etc. reperesent an attribute or set of attributes that uniquely identifies a section.
    # Hint: look at the schema of the section table using the command "\d section" in a psql shell.

if __name__ == "__main__":
    overlapping_sections = get_overlapping_sections()
    print_overlapping_sections(overlapping_sections())
