def draw_calendar_day(day, month, year, startHour, startMinute, endHour, endMinute, display, index):
    xIndex = (678 - (index*85))
    display.line((xIndex, 0, xIndex, 378), fill = 0)