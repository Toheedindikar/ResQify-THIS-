from datetime import datetime, timedelta

# Mechanic booked time
current_time = datetime.now()   
booked_time = datetime.strptime(current_time.strftime('%H:%M:%S'), '%H:%M:%S')
print(booked_time)
duration = (2799 // 60)

# Time taken to reach the customer (50 minutes)
reach_time = booked_time + timedelta(minutes=50)
cust_time = booked_time + timedelta(minutes=10)
print(reach_time)
current_time = datetime.now()

# Customer opens the site time
customer_open_time = cust_time
print(customer_open_time)
# Calculate time differences
time_to_reach = reach_time - booked_time
time_until_open = customer_open_time - reach_time

# Display the results
print(f"Time taken to reach the customer: {time_to_reach}")
print(f"Time until the customer opens the site: {time_until_open}")

# timer_to_display = duration - datetime.strptime(time_until_open, '%M')
print(datetime.strptime(time_until_open, '%M'))
