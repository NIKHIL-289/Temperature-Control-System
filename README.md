# Temperature-Control-System
This will help in controlling the temperature of the House easily and parallelly reducing the energy consumption

Overview
This project is a Temperature Control System built using Kivy that automatically adjusts the temperature in a room or environment. It first scrapes the current temperature from a weather website and then compares it to the user-defined set temperature. If the current temperature deviates from the required value, it triggers a system to adjust the temperature to the desired level.

Features
Web Scraping: Scrapes real-time temperature data from a weather website using BeautifulSoup.
User Interface: Built using Kivy, allowing users to set a desired temperature for their environment.
Temperature Monitoring: Continuously compares the current temperature with the set value and displays it on the interface.
Automatic Adjustment: Triggers actions (e.g., turn on heater or cooler) based on the comparison between current and set temperature.
Real-Time Updates: The temperature is updated periodically, and actions are taken to maintain the set temperature.

Technologies Used
Python
Kivy (for the user interface)
BeautifulSoup (for web scraping the current temperature)
Requests (to make HTTP requests for web scraping)
Threading (to fetch temperature data periodically and update UI in real time)

Sample Output
Kivy GUI: A simple user interface will show the current temperature and allow you to set a target temperature.
The system will alert you when the current temperature is too high or low compared to the set temperature, and a visual indicator will show whether the system is adjusting the temperature.

Future Improvements
Integration with smart devices: Control physical heaters, air conditioners, or fans via IoT APIs based on the temperature difference.
Error Handling: Add better error handling for failed web scraping or network issues.
Multiple Location Support: Allow users to monitor temperatures from multiple locations and control environments accordingly.
User Preferences: Enable users to customize the behavior of the system, such as setting temperature thresholds for notifications or automatic adjustments.
