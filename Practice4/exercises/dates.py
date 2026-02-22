import datetime as dt

#1
cur_date = dt.datetime.now()
new_date = cur_date - dt.timedelta(days=5)

print(f"The date five day before: {new_date.date()}")

#2
today = dt.datetime.now()
yesterday = today - dt.timedelta(days=1)
tomorrow = today + dt.timedelta(days=1)
print(f"Yesterday: {yesterday.date()}")
print(f"Today: {today.date()}")
print(f"Tomorrow: {tomorrow.date()}")

#3
no_micro = dt.datetime.now().replace(microsecond=0)
print(f"Without microseconds: {no_micro}")

#4
date1 = dt.datetime(2026, 2, 25, 12, 0, 0)
date2 = dt.datetime(2026, 2, 20, 18, 0, 0)
diff = (date1 - date2).total_seconds()
print(f"Difference in seconds: {diff}")