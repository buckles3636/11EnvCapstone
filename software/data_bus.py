import multiprocessing
from multiprocessing import Process, Pipe
import logging

from subsystems.sense import Sensor
#from subsystems.interface import Interfacer
from subsystems.control import Controller
from subsystems.log import Logger
from subsystems.notify import Notifier

if __name__ == "__main__":
#-- Create logger
    #logger = multiprocessing.log_to_stderr()
    #logger.info("DATA BUS")

#-- Create pipes for communication
    # sensor subsystem
    sensor_receive_sensor_data, sensor_send_sensor_data = Pipe(duplex=False)
    # user interface subsystem
    interfacer_receive_sensor_data, interfacer_send_sensor_data = Pipe(duplex=False)
    interfacer_receive_set_points, interfacer_send_set_points = Pipe(duplex=False)
    interfacer_receive_status, interfacer_send_status = Pipe(duplex=False)
    # control subsystem
    controller_receive_sensor_data, controller_send_sensor_data = Pipe(duplex=False)
    controller_receive_set_points, controller_send_set_points = Pipe(duplex=False)
    controller_receive_status, controller_send_status = Pipe(duplex=False)
    # logging subsystem
    logger_receive_sensor_data, logger_send_sensor_data = Pipe(duplex=False)
    logger_receive_set_points, logger_send_set_points = Pipe(duplex=False)
    # notifier subsystem
    notifier_receive_sensor_data, notifier_send_sensor_data = Pipe(duplex=False)
    notifier_receive_set_points, notifier_send_set_points = Pipe(duplex=False)
    notifier_receive_status, notifier_send_status = Pipe(duplex=False)
    print("DATA BUS:\tPipes created")

#-- Instantiate subsystems
    the_sensor = Sensor(sensor_data_out=sensor_send_sensor_data)
    #the_interfacer = Interfacer(sensor_data_in=interfacer_receive_sensor_data, set_points_out=interfacer_send_set_points, status_out=interfacer_send_status)
    the_controller = Controller(sensor_data_in=controller_receive_sensor_data, set_points_in=controller_receive_set_points, status_in=controller_receive_status)
    the_logger = Logger(sensor_data_in=logger_receive_sensor_data, set_points_in=logger_receive_set_points)
    the_notifier = Notifier(sensor_data_in=notifier_receive_sensor_data, set_points_in=notifier_receive_set_points, status_in=notifier_receive_status)
    print("DATA BUS:\tSubsystems instantiated")

#-- Create processes
    the_sensor_process = Process(target=the_sensor.start, name="Sensor")
    #the_interface_process = Process(target=the_interfacer.start, name=Interfacer)
    the_controller_process = Process(target=the_controller.start, name="Controller")
    the_logger_process = Process(target=the_logger.start, name="Logger")
    the_notifier_process = Process(target=the_notifier.start, name="Notifier")
    print("DATA BUS:\tProcesses created for subsystem start() functions")

#-- Start processes
    the_sensor_process.start()
    #the_interface_process.start()
    the_controller_process.start()
    the_logger_process.start()
    the_notifier_process.start()
    print("DATA BUS:\tProcesses started")

#-- Join processes: this says bring them all together when they finish executing
    #the_sensor_process.join(timeout=1)
    #the_interface_process.join()
    #the_controller_process.join()
    #the_logger_process.join()
    #the_notifier_process.join()

#-- Poll pipes and distrubute data
    while True:
        # poll, receive, and distribute sensor data
        if sensor_receive_sensor_data.poll():
            sensor_data = sensor_receive_sensor_data.recv()
            interfacer_send_sensor_data.send(sensor_data)
            controller_send_sensor_data.send(sensor_data)
            notifier_send_sensor_data.send(sensor_data)
            logger_send_sensor_data.send(sensor_data)
            print("DATA BUS:\tSensor data RX/TX complete")

        
        # poll, receive, and distribute set points
        if interfacer_receive_set_points.poll():
            set_points = interfacer_receive_set_points.recv()
            controller_send_set_points.send(set_points)
            notifier_send_set_points.send(set_points)
            logger_send_set_points.send(set_points)
            print("DATA BUS:\tSet points RX/TX complete")


        # poll, receive, and distribute status
        if interfacer_receive_status.poll():
            status = interfacer_receive_status.recv()
            controller_send_status.send(status)
            notifier_send_status.send(status)
            print("DATA BUS:\tStatus RX/TX complete")

