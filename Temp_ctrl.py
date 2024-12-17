import requests
from bs4 import BeautifulSoup
import time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.clock import Clock

class TemperatureControlUnit(BoxLayout):
    current_temp = NumericProperty(0.0)
    adjusted_temp = NumericProperty(0.0)
    city = StringProperty("sehore")
    target_temp = NumericProperty(25.0)
    kp = NumericProperty(0.5)
    status = StringProperty("")

    def fetch_temperature(self):
        """Fetch the current temperature from a weather website."""
        try:
            url = f"https://www.timeanddate.com/weather/india/{self.city.lower().replace(' ', '-')}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            temp_div = soup.find("div", {"id": "qlook"})
            temp_string = temp_div.find("div", {"class": "h2"}).text.strip()
            self.current_temp = float(temp_string.split("°")[0])  # Extract temperature
            self.status = f"Current temperature: {self.current_temp}°C"
        except Exception as e:
            self.status = f"Error fetching temperature: {e}"
            self.current_temp = self.target_temp  # Fallback

    def transition_to_emodet(self, *args):
        # If exiting is necessary, do it gracefully
        App.get_running_app().stop()  # Stops the Kivy app gracefully

    def adjust_temperature(self):
        """Adjust the temperature using proportional control."""
        error = self.target_temp - self.current_temp
        adjustment = error

        if adjustment > 0:
            appliance = "HEATER"
        elif adjustment < 0:
            appliance = "AC"
        else:
            self.status = "Temperature is already at target. No adjustment needed."
            return

        runtime = adjustment
        Status = f"{appliance} running for {runtime:.2f} seconds..."  # This will print to the console
        print(Status)
        time.sleep(runtime)
        self.current_temp += adjustment
        self.adjusted_temp = self.current_temp
        if adjustment > 0:
            self.status = f"Adjusted temperature: {self.current_temp:.2f}°C || HEATER WAS ACTIVATED "
            Clock.schedule_once(self.transition_to_emodet, 7)
        elif adjustment < 0:
            self.status = f"Adjusted temperature: {self.current_temp:.2f}°C || AC WAS ACTIVATED "
            Clock.schedule_once(self.transition_to_emodet, 7)
        else:
            self.status = "Temperature is already at target. No adjustment needed."
            Clock.schedule_once(self.transition_to_emodet, 7)
            

    def on_button_press(self):
        """Handle button press to fetch and adjust temperature."""
        self.status = "Fetching temperature..."
        self.fetch_temperature()
        if self.current_temp:
            self.adjust_temperature()


class TemperatureApp(App):
    def build(self):
        layout = BoxLayout(orientation="vertical", padding=20, spacing=20)

        # Title
        title_label = Label(
            text="Temperature Control Unit",
            font_size=27,
            bold=True,
            color=(0.2, 0.6, 0.8, 1),  # Title color
            size_hint=(1, 0.1),  # Adjust size_hint for better proportioning
        )

        # Fixed city (Sehore)
        city_label = Label(
            text="City: Sehore",
            font_size=27,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.1),  # Adjust size_hint for better proportioning
        )

        # Slider to control target temperature
        self.temp_slider = Slider(min=16, max=30, value=22)
        self.temp_slider.bind(value=self.on_slider_value_change)
        self.temp_slider_label = Label(
            text=f"Target Temperature: {self.temp_slider.value}°C",
            font_size=27,
            color=(0.5, 0.5, 0.5, 1),
            size_hint=(1, 0.1),  # Adjust size_hint for better proportioning
        )

        # Fetch and Adjust Button
        fetch_button = Button(
            text="Fetch & Adjust Temperature",
            size_hint=(1, 0.15),  # Adjust size_hint for better proportioning
            background_color=(0.2, 0.8, 0.2, 1),
            font_size=27,  # Set font size to 30
            on_press=self.on_fetch_button_press,
        )

        # Status display
        self.status_label = Label(
            text="",
            font_size=27,  # Set font size to 30
            color=(0.5, 0.5, 0.5, 1),  # Status text color
            size_hint=(1, 0.15),  # Adjust size_hint for better proportioning
        )

        # Add widgets to layout
        layout.add_widget(title_label)
        layout.add_widget(city_label)
        layout.add_widget(self.temp_slider_label)
        layout.add_widget(self.temp_slider)
        layout.add_widget(fetch_button)
        layout.add_widget(self.status_label)

        return layout

    def on_slider_value_change(self, instance, value):
        """Update target temperature based on slider value."""
        self.temp_slider_label.text = f"Target Temperature: {value}°C"

    def on_fetch_button_press(self, instance):
        # Fixed city is "Sehore", so we don't need user input for it
        city = "sehore"
        target_temp = self.temp_slider.value

        tcu = TemperatureControlUnit(city=city, target_temp=target_temp)
        tcu.fetch_temperature()
        self.status_label.text = tcu.status
        Clock.schedule_once(lambda dt: self.update_status(tcu), 1)

    def update_status(self, tcu):
        tcu.adjust_temperature()
        self.status_label.text = tcu.status


def run():
    TemperatureApp().run()
