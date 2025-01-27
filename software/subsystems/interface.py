import kivy
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.button import Button
from kivy.clock import Clock
import multiprocessing as mp

from subsystems.subsystem import Subsystem

class Interfacer(Subsystem):

     def __init__(self, sensor_data_in: mp.connection.PipeConnection = None,
                 sensor_data_out: mp.connection.PipeConnection = None,
                 set_points_in: mp.connection.PipeConnection = None,
                 set_points_out: mp.connection.PipeConnection = None,
                 status_in: mp.connection.PipeConnection = None,
                 status_out: mp.connection.PipeConnection = None) -> 'Interfacer':
          """
          Initialize the subsystem with one-way Pipes to communicate with the data bus.

          @param sensor_data_in: multiprocessing one-way Pipe to receive sensor data in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param sensor_data_out: multiprocessing one-way Pipe to send sensor data in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param set_points_in: multiprocessing one-way Pipe to receive set points in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param set_points_out: multiprocessing one-way Pipe to send set points in the following format:
               {"CO2": %.1f, "temperature": %.1f, "humidity": %.0f}
          @param status_in: multiprocessing one-way Pipe to receive status in the following format:
               {"status": "on" or "off"}
          @param status_out: multiprocessing one-way Pipe to send status in the following format:
               {"status": "on" or "off"}
          @rtype: Subsystem
          @return: Initialized subsystem with necessary Pipes for communication
          """

          # initialize the subsystem parent class with data pipes
          super().__init__(sensor_data_in, sensor_data_out, set_points_in, set_points_out, status_in, status_out)

          # create any necessary custom classes for functionality
          self.kivyapp = KivyApp()

     def start(self) -> None:
          # override the parent start() function
          # this is where you begin looping your process for implmenting functionality
          # pipes can be assessed like the following: self.pipe_sensor_data_in.send(<data_here>)
          # data packets can be created like the following: data_dict = {"CO2": 5.1, "temperature": 37.0, "humidity": 90.0}
          pass

# custom class
class KivyApp(App):
    def __init__(self, pipe_recv, pipe_send, **kwargs):
        super().__init__(**kwargs)
        self.pipe_recv = pipe_recv
        self.pipe_send = pipe_send
        self.co2_setpoint = 0
        self.temp_setpoint = 0
        self.humidity_setpoint = 0

    def build(self):
        layout = GridLayout(cols=2, row_force_default=True, row_default_height=40)

        # Labels to show current sensor values
        self.co2_label = Label(text="CO2 Concentration: 0 %")
        self.temp_label = Label(text="Temperature: 0 °C")
        self.humidity_label = Label(text="Humidity: 0 %")

        # Sliders for setpoints
        self.co2_slider = Slider(min=0, max=30, value=0)
        self.temp_slider = Slider(min=0, max=40, value=0)
        self.humidity_slider = Slider(min=0, max=100, value=0)

        # Labels to display current setpoints
        self.co2_setpoint_label = Label(text=f"CO2 Setpoint: {self.co2_setpoint} %")
        self.temp_setpoint_label = Label(text=f"Temperature Setpoint: {self.temp_setpoint} °C")
        self.humidity_setpoint_label = Label(text=f"Humidity Setpoint: {self.humidity_setpoint} %")

        # Buttons for setting and resetting values
        set_button = Button(text="Set Setpoints")
        reset_button = Button(text="Reset Setpoints")

        # Bind buttons to methods
        set_button.bind(on_press=self.send_setpoints)
        reset_button.bind(on_press=self.reset_setpoints)

        # Add widgets to layout
        layout.add_widget(self.co2_label)
        layout.add_widget(self.co2_slider)
        layout.add_widget(self.co2_setpoint_label)

        layout.add_widget(self.temp_label)
        layout.add_widget(self.temp_slider)
        layout.add_widget(self.temp_setpoint_label)

        layout.add_widget(self.humidity_label)
        layout.add_widget(self.humidity_slider)
        layout.add_widget(self.humidity_setpoint_label)

        layout.add_widget(set_button)
        layout.add_widget(reset_button)

        # Update current values from sensor data every second
        Clock.schedule_interval(self.update_sensor_data, 1)
        Clock.schedule_interval(self.update_setpoint_labels, 0.1)

        return layout

    def update_sensor_data(self, dt):
        if self.pipe_recv.poll():
            sensor_data = self.pipe_recv.recv()
            co2, temp, humidity = sensor_data
            self.co2_label.text = f"CO2 Concentration: {co2} %"
            self.temp_label.text = f"Temperature: {temp} °C"
            self.humidity_label.text = f"Humidity: {humidity} %"

    def send_setpoints(self, instance):
        # Get setpoint values from sliders
        self.co2_setpoint = self.co2_slider.value
        self.temp_setpoint = self.temp_slider.value
        self.humidity_setpoint = self.humidity_slider.value
        setpoints = (self.co2_setpoint, self.temp_setpoint, self.humidity_setpoint)
        self.pipe_send.send(setpoints)

    def update_setpoint_labels(self, dt):
        # Update the labels that display the current setpoints
        self.co2_setpoint_label.text = f"CO2 Setpoint: {self.co2_slider.value} %"
        self.temp_setpoint_label.text = f"Temperature Setpoint: {self.temp_slider.value} °C"
        self.humidity_setpoint_label.text = f"Humidity Setpoint: {self.humidity_slider.value} %"

    def reset_setpoints(self, instance):
        self.co2_slider.value = 0
        self.temp_slider.value = 0
        self.humidity_slider.value = 0

def run_gui(pipe_recv, pipe_send):
    app = EnvControlApp(pipe_recv, pipe_send)
    app.run()

