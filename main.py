import schedule
import time


# Function to notify for a prayer
def prayer_reminder(prayer_name):
    print(f"🔔 It's time for {prayer_name} prayer!")


# Define prayer times (adjust times as per your location)
prayer_times = {
    "Fajr": "05:30",  # Example time
    "Dhuhr": "12:30",  # Example time
    "Asr": "15:45",  # Example time
    "Maghrib": "17:30",  # Example time
    "Isha": "19:45"  # Example time
}

# Schedule the prayers
for prayer, time in prayer_times.items():
    schedule.every().day.at(time).do(prayer_reminder, prayer)

print("📿 Prayer reminder system is running...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
