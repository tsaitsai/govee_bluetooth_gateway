# govee_bluetooth_gateway
**Bluetooth to MQTT gateway for Govee brand bluetooth sensors.**

<img src="https://raw.githubusercontent.com/tsaitsai/govee_bluetooth_gateway/main/images/chest_freezer_test.jpg" width="359" height="300">

I got a chest freezer recently, and planned to put it in the basement.  Since it's not used frequently, I wanted to keep track of the temperature and send myself a notification in case the freezer breaks down and I need to save the food.

I have zigbee temperature sensors that are small and use CR2032 coin cells.  They'll work for a little while, but freezing temperatures may not be best for coin cell battery performance and might necessitate frequent battery changes.  I came across these [Govee brand](https://www.amazon.com/Govee-Temperature-Notification-Hygrometer-Thermometer/dp/B0872X4H4J) Bluetooth temperature sensors that use a pair of AAA batteries.

If I swap the alkaline AAA batteries out with Energizer Lithium AAA batteries, the sensor should work better in a chest freezer.  The lithium-iron disulfide chemistry in these Energizer AAA batteries perform better in freezing conditions than the Lithium Manganese dioxide chemistry used in typical CR2032 coin cells.  The added capacity should also reduce battery changes.

<img src="https://raw.githubusercontent.com/tsaitsai/govee_bluetooth_gateway/main/images/chest_freezer_temp_sensor.jpg" width="302" height="403"> <img src="https://raw.githubusercontent.com/tsaitsai/govee_bluetooth_gateway/main/images/battery.jpg" width="403" height="302">


Like a lot of these gateway projects, I wanted to use a Raspberry Pi to read the bluetooth sensor data and act as a dedicated gateway.  I came across this [github project](https://github.com/Thrilleratplay/GoveeWatcher/issues/2) that explains the how the Govee bluetooth advertisement formats the temperature, humidity, and battery level.  The sensor data is encoded in the advertisement, so no GATT connections needed.  The manufacturer provides mobile apps for typical usage, but it's got creepy permissions and it's not useful for my purpose.  I used Bluepy library to read the BLE advertisement and parse it out per the description from GoveeWatcher project.  As I'm already using MQTT, Influx, Grafana, and telegraph, it was convenient to publish the sensor data as MQTT messages and visualize it in Grafana.  Then send email notifications using Node-Red.

<img src="https://raw.githubusercontent.com/tsaitsai/govee_bluetooth_gateway/main/images/chest_freezer-cooldown_warmup.jpg" width="472" height="480">

I'm also interested in how the freezer behaves.  How the temperature fluctuates, how many watts it consumes, etc.  It's interesting how long it takes for it to go from -13F back put up to 32F when the power is shut off.  To monitor energy consumption, I used a [wifi outlet](https://www.amazon.com/BN-LINK-Monitoring-Function-Compatible-Assistant/dp/B07VDGM6QR) with built-in current sensor and flashed it with Tasmota via [Tuya Convert](https://github.com/ct-Open-Source/tuya-convert).  This 7 cu-ft Hisense chest freezer uses about 0.7 kWh per day when the unit is totally empty and door kept closed.

<img src="https://raw.githubusercontent.com/tsaitsai/govee_bluetooth_gateway/main/images/energy_consumption_monitoring.jpg" width="317" height="423">

  I'll update the energy usage once the freezer is more fully filled.  I'll also update when I get battery life data.  The Govee bluetooth sensor unfortunately sends out updates too often (every couple of seconds).  So the added battery capacity from the AAA batteries may not be a huge advantage at the end of the day.
