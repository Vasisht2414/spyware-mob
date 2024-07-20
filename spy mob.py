import os
import datetime
import platform
import sqlite3
import threading
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from plyer import notification, uniqueid

# Global variables
running = False
screenshot_timer = None

# Ensure the mainspymob directory exists
folder_name = "mainspymob"
os.makedirs(folder_name, exist_ok=True)

# Function to get system information
def get_system_info(folder_path):
    try:
        date = datetime.date.today()
        processor = platform.processor()
        system = platform.system()
        release = platform.release()
        host_name = uniqueid.id  # Use unique device ID

        system_info = (
            f"Date: {date}\n"
            f"Processor: {processor}\n"
            f"System: {system}\n"
            f"Release: {release}\n"
            f"Host Name: {host_name}\n"
        )

        with open(os.path.join(folder_path, 'system.txt'), 'w') as file:
            file.write(system_info)
    except Exception as e:
        print(f"Error getting system information: {e}")

# Function to take a screenshot
def take_screenshot(folder_path):
    global screenshot_timer
    try:
        # Placeholder for screenshot functionality
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = os.path.join(folder_path, f"screenshot_{timestamp}.png")
        print(f"Screenshot saved: {screenshot_path}")
        notification.notify(title="Screenshot taken", message=f"Screenshot saved at {screenshot_path}")
    except Exception as e:
        print(f"Error occurred while taking screenshot: {e}")

    # Schedule the next screenshot in 5 seconds if running
    if running:
        screenshot_timer = threading.Timer(5, take_screenshot, args=[folder_path])
        screenshot_timer.start()

# Main function to execute all components
def main_program():
    global running
    try:
        # Get system information
        get_system_info(folder_name)

        # Start taking screenshots
        running = True
        take_screenshot(folder_name)
    except Exception as e:
        print(f"An error occurred: {e}")

def start_monitoring(instance):
    global running
    if not running:
        running = True
        main_program()
    notification.notify(title="Monitoring", message="Monitoring started")

def stop_monitoring(instance):
    global running, screenshot_timer
    running = False
    if screenshot_timer:
        screenshot_timer.cancel()
    notification.notify(title="Monitoring", message="Monitoring stopped")

class MonitoringApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')
        start_button = Button(text='Start Monitoring', on_press=start_monitoring)
        stop_button = Button(text='Stop Monitoring', on_press=stop_monitoring)
        layout.add_widget(start_button)
        layout.add_widget(stop_button)
        return layout

if __name__ == '__main__':
    MonitoringApp().run()
