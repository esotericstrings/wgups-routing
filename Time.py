# STUDENT: Jamie Huang 001195694
import datetime
from datetime import time
import re


# O(1)
def convert_time(string):
    try:
        # Convert Standard times to Military time for time object
        if 'AM' or 'PM' in string:
            check_time = re.sub('[A-Z]+', '', string)
            split_time = check_time.split(':')
            hour = int(split_time[0])
            minute = int(split_time[1].split(' ')[0])
            # Convert 12AM to 0 hours for time object
            if hour == 12 and ('AM' in string):
                hour = 0
            # Convert 12-24 hours to corresponding PM times
            if ('PM' in string) and hour < 12 and hour != 12:
                hour += 12
        else:
            # Parse Military times
            split_time = string.split(':')
            hour = int(split_time[0])
            minute = int(split_time[1].split(' ')[0])
        time_object = time(hour=hour, minute=minute)
        return time_object
    except IndexError as error:
        return False
    except ValueError as error:
        return False
    except AttributeError as error:
        return False


# O(1)
def display_time(time_object):
    ampm = 'AM'
    hour = time_object.hour
    minute = time_object.minute
    # Convert 0 and 12 hours to 12AM and 12PM
    if time_object.hour == 0:
        hour = '12'
    if time_object.hour == 12:
        ampm = 'PM'
    # Convert 12-24 hours to PM times
    if time_object.hour > 12:
        hour = hour - 12
        ampm = 'PM'
    # add leading 0 to single digit minutes
    if time_object.minute < 10:
        minute = '0'+str(time_object.minute)

    time_string = str(hour) + ':' + str(minute) + ' ' + ampm
    return time_string


# O(1)
def add_minutes(time_object, minutes):
    added_time = (datetime.datetime.combine(datetime.date(1, 1, 1), time_object) + datetime.timedelta(minutes=minutes)).time()
    return added_time
