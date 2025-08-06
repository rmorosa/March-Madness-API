import datetime

# Define log file path
log_file = "C:/Dev/Python/task_log.txt"

# Get current timestamp
now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Write new entry to the log file
with open(log_file, "a") as file:
    file.write(f"[{now}] Task Scheduler ran this script.\n")

print(f"Logged at {now}")  # For debugging if running manually