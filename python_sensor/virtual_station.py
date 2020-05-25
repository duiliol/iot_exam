import datetime
import json
import random

class Station:
    id: str
    time: datetime
    temperature: int
    humidity: int
    wind_direction: int
    wind_intensity: int
    rain_height: int


    def __init__(self, id):
        self.id = id
        self.update_sensors_values()
        print("Created virtual station with ID: "+self.id)

    def update_sensors_values(self):
        self.time = datetime.datetime.now()
        self.temperature = random.randint(-50,50)
        self.humidity = random.randint(0,100)
        self.wind_direction = random.randint(0,360)
        self.wind_intensity = random.randint(0,100)
        self.rain_height = random.randint(0,50)

    def get_sensors_values(self):
        sensor_values = {"id":self.id,
                         "time":self.time.isoformat(),
                         "temperature":self.temperature,
                         "humidity":self.humidity,
                         "wind_direction":self.wind_direction,
                         "wind_intensity":self.wind_intensity,
                         "rain_height":self.rain_height}
        return json.dumps(sensor_values)

    def get_station_id(self):
        return self.id

    def get_last_update_time(self):
        return self.time;

    def get_temperature(self):
        return self.temperature

    def get_humidity(self):
        return self.humidity

    def get_wind_direction(self):
        return self.wind_direction

    def get_wind_intensity(self):
        return self.wind_intensity

    def get_rain_height(self):
        return self.rain_height


