from datetime import timedelta

def calculate_overtime(attendance_records, standard_hours_per_day=8):
    """
    Calculates the total overtime hours from a list of attendance records.

    Args:
        attendance_records (list): A list of Attendance objects for a single user.
        standard_hours_per_day (int): The number of standard work hours per day.

    Returns:
        float: The total number of overtime hours.
    """
    daily_hours = {}
    for record in attendance_records:
        if record.clock_in_time and record.clock_out_time:
            day = record.clock_in_time.date()
            if day not in daily_hours:
                daily_hours[day] = timedelta(0)

            duration = record.clock_out_time - record.clock_in_time
            daily_hours[day] += duration

    total_overtime = timedelta(0)
    standard_workday = timedelta(hours=standard_hours_per_day)

    for day, total_duration in daily_hours.items():
        if total_duration > standard_workday:
            overtime_for_day = total_duration - standard_workday
            total_overtime += overtime_for_day

    return total_overtime.total_seconds() / 3600  # Return overtime in hours