# RPi-Adafruit-RGB-Matrix-Weather-Station

This is a simple weather station project using Raspberry pi 3b+, adafruit rgb 32x32 matrices, adafruit mcp9808 and a PIR sensor.

Links for the components are below:
1. https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/
2. https://www.adafruit.com/product/607
3. https://www.adafruit.com/product/1782
4. https://www.adafruit.com/product/189
5. https://www.adafruit.com/product/3211
6. https://www.adafruit.com/product/1466 

Actual power supply used is 5v 6Amps.

Weather data is obtained from https://openweathermap.org/ every 5 minutes.

PIR detects the human presense and turns on the matrix for around a minute. This time and sensitivity can be incrased/decreased using the onboard potentiometers. The matrix shows time, date, outside temp, outside humidity, inside temperature, sunrise and sunset times etc.

I designed and 3d printed a few bridges to attach two matrices together. Also a 3d printed part was designed to attach the PIR sensor.
