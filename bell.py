import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import requests
from playsound import playsound
import schedule
import time
from threading import Thread

kivy.require('2.0.0')  # Make sure Kivy is installed


# Function to fetch prayer times
def get_prayer_times():
    latitude = 33.712090  # Example: New York latitude
    longitude = -84.105782  # Example: New York longitude
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'method': 2,  # ISNA method
        'school': 1,  # Adjust school if needed
        'format': 'json'
    }
    url = 'http://api.aladhan.com/v1/timings/today'
    response = requests.get(url, params=params)
    data = response.json()
    return data['data']['timings']


# Function to notify for a prayer
def prayer_reminder(prayer_name):
    print(f"🔔 It's time for {prayer_name} prayer!")
    playsound('prayer_sound.mp3')  # Ensure the sound file is in the same folder


# Schedule prayer reminders
def schedule_prayers(prayer_times):
    for prayer, prayer_time in prayer_times.items():
        schedule.every().day.at(prayer_time).do(prayer_reminder, prayer)


# Running the schedule in a separate thread to avoid blocking the Kivy UI
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


# Kivy GUI Class
class PrayerReminderApp(App):

    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Add a label to display prayer times
        self.prayer_label = Label(text="Prayer Times will appear here...", size_hint=(1, None), height=44)
        self.layout.add_widget(self.prayer_label)

        # Button to refresh prayer times
        self.refresh_button = Button(text="Refresh Prayer Times", on_press=self.refresh_prayer_times)
        self.layout.add_widget(self.refresh_button)

        # Scrollable view for prayer times
        self.scroll_view = ScrollView()
        self.scroll_label = Label(text="", size_hint=(1, None), height=200)
        self.scroll_view.add_widget(self.scroll_label)
        self.layout.add_widget(self.scroll_view)

        # Start prayer reminder scheduling in a background thread
        thread = Thread(target=run_schedule, daemon=True)
        thread.start()

        return self.layout

    def refresh_prayer_times(self, instance):
        # Fetch prayer times and display them
        prayer_times = get_prayer_times()
        prayer_times_text = "\n".join([f"{prayer}: {time}" for prayer, time in prayer_times.items()])
        self.scroll_label.text = prayer_times_text
        self.prayer_label.text = "Prayer times updated!"

        # Schedule prayers
        schedule_prayers(prayer_times)


# Run the Kivy app
if __name__ == '__main__':
    PrayerReminderApp().run()
