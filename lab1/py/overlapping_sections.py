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
                    slot1['start_hr'] * 60 + slot1['start_min'],
                    slot1['end_hr'] * 60 + slot1['end_min']
    )
    start2, end2 = (
                    slot2['start_hr'] * 60 + slot2['start_min'],
                    slot2['end_hr'] * 60 + slot2['end_min']
    )
    
    if end1 >= start2 and end2 >= start1:
        # compute the overlap window
        overlap_start = max(start1, start2)
        overlap_end = min(end1, end2)

        # convert back to hours
        start_hr, start_min = int(overlap_start // 60), int(overlap_start % 60)
        end_hr, end_min = int(overlap_end // 60), int(overlap_end % 60)
        # print(type(overlap_start), type(overlap_end), type(start_hr), type(start_min))
        return (
            f"{start_hr:02d}:{start_min:02d}",
            f"{end_hr:02d}:{end_min:02d}",
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
            ORDER BY
            CASE t.day WHEN 'M' THEN 1 WHEN 'T' THEN 2 WHEN 'W' THEN 3
            WHEN 'R' THEN 4 WHEN 'F' THEN 5 ELSE 6 END,
            s.semester, s.year, t.start_hr, t.start_min;
        """
        )
        schedules = cursor.fetchall()
        # TODO 2: map the schedules into a list of TimeSlotInfo objects
        timeslots = []
        for row in schedules:
            course_id, sec_id, day, semester, year, start_hr, start_min, end_hr, end_min = row
            timeslots.append(TimeSlotInfo(
                course_id=course_id,
                sec_id=sec_id,
                day=day,
                semester=semester,
                year=int(year),
                start_hr=int(start_hr),
                start_min=int(start_min),
                end_hr=int(end_hr),
                end_min=int(end_min),
            ))

        # TODO 3: find overlapping sections            
        i = 0
        n = len(timeslots)
        while i < n:
            # compare only within the same (day, semester, year) bucket
            day_i = timeslots[i]['day']
            sem_i = timeslots[i]['semester']
            year_i = timeslots[i]['year']
            end_i = timeslots[i]['end_hr'] * 60 + timeslots[i]['end_min']

            j = i + 1
            while j < n:
                # stop when we move to a new bucket (next day/term/year)
                if (timeslots[j]['day'] != day_i or
                    timeslots[j]['semester'] != sem_i or
                    timeslots[j]['year'] != year_i):
                    break

                # since rows are ordered by start time, once next starts at/after current end, no more overlaps for i
                start_j = timeslots[j]['start_hr'] * 60 + timeslots[j]['start_min']
                if start_j >= end_i:
                    break

                over = is_overlap(timeslots[i], timeslots[j])
                if over is not None:
                    start, end = over
                    overlaps.append((timeslots[i], timeslots[j], start, end))
                j += 1

            i += 1

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
    for ts1, ts2, start, end in overlaps:
        print(f"({ts1['course_id']}, {ts1['sec_id']}, {ts1['semester']}, {ts1['year']}) "
            f"({ts2['course_id']}, {ts2['sec_id']}, {ts2['semester']}, {ts2['year']})")


if __name__ == "__main__":
    overlapping_sections = get_overlapping_sections()
    print_overlapping_sections(overlapping_sections)
