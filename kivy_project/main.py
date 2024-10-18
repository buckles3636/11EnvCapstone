
from multiprocessing import Process, Pipe
import kivy_app
import sensor_reader
import controller

if __name__ == "__main__":
    # Create pipes for communication
    sensor_recv_pipe, sensor_send_pipe = Pipe()
    setpoint_recv_pipe, setpoint_send_pipe = Pipe()

    # Create processes
    gui_process = Process(target=kivy_app.run_gui, args=(sensor_recv_pipe, setpoint_send_pipe))
    sensor_process = Process(target=sensor_reader.read_sensors, args=(sensor_send_pipe,))
    control_process = Process(target=controller.control_system, args=(setpoint_recv_pipe,))

    # Start processes
    gui_process.start()
    sensor_process.start()
    control_process.start()

    # Join processes
    gui_process.join()
    sensor_process.join()
    control_process.join()
