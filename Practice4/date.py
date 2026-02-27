from datetime import datetime, timedelta

#-----------------------------------
# Subtract Five Days from Current Date
#-----------------------------------

current_date = datetime.now()
five_days_ago = current_date - timedelta(days=5)

print("Current date:", current_date)
print("Date after subtracting 5 days:", five_days_ago)


#-----------------------------------
# Print Yesterday, Today, Tomorrow
#-----------------------------------

today = datetime.now().date()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("\nYesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)


#-----------------------------------
# Drop Microseconds from Datetime
#-----------------------------------

now = datetime.now()
without_microseconds = now.replace(microsecond=0)

print("\nOriginal datetime:", now)
print("Without microseconds:", without_microseconds)


#-----------------------------------
#  Calculate Difference Between Two Dates in Seconds
#-----------------------------------

print("\nEnter two dates to calculate difference in seconds")

date1 = input("Enter first date (YYYY-MM-DD HH:MM:SS): ")
date2 = input("Enter second date (YYYY-MM-DD HH:MM:SS): ")

dt1 = datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
dt2 = datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

difference_seconds = abs((dt2 - dt1).total_seconds())

print("Difference in seconds:", int(difference_seconds))

#-----------------------------------