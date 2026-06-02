from datetime import datetime


def time_to_minutes(time_str: str) -> int:
    dt = datetime.strptime(time_str, "%H:%M")
    return dt.hour * 60 + dt.minute


def minutes_to_time(minutes: int) -> str:
    hours = (minutes // 60) % 24
    mins = minutes % 60
    return f"{hours:02d}:{mins:02d}"