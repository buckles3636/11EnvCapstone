import multiprocessing as mp

from subsystems.subsystem import Subsystem

class Controller(Subsystem):

     def __init__(self, sensor_data_in: mp.connection.Connection = None,
                    sensor_data_out: mp.connection.Connection = None,
                    set_points_in: mp.connection.Connection = None,
                    set_points_out: mp.connection.Connection = None,
                    status_in: mp.connection.Connection = None,
                    status_out: mp.connection.Connection = None) -> 'Controller':
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
          @rtype: Controller
          @return: Initialized Controller subsystem with necessary Pipes for communication
          """

          # initialize the subsystem parent class with data pipes
          super().__init__(sensor_data_in, sensor_data_out, set_points_in, set_points_out, status_in, status_out)

          # initialize the logger
          self.logger = mp.log_to_stderr()

          # create any necessary custom classes for functionality
          # self.pid = PID()

     def start(self) -> None:
          # override the parent start() function
          # this is where you begin looping your process for implmenting functionality
          # pipes can be assessed like the following: self.pipe_sensor_data_in.send(<data_here>)
          # data packets can be created like the following: data_dict = {"CO2": 5.1, "temperature": 37.0, "humidity": 90.0}
          pass

class PID:
     
     # KP: float                 # proportional gain
     # KI: float                 # integral gain
     # KD: float                 # derivative gain
     # TAU: float                # derivative low-pass filter time constant
     # OUTMIN: float             # output limit min
     # OUTMAX: float             # output limit max
     # T: float                  # sample time in seconds
     # _integrator: float        # integrator "memory"
     # _differentiator: float    # differentiator "memory"
     # _prev_error: float        # previous error value
     # _prev_pt: float           # previous measurement data point value
     # _set_point: float         # PID controller setpoint
     # _output: float            # PID controller output
     # _status: bool             # enable/disable controller

     def __init__(self, kp: float, ki: float, kd: float, tau: float, outmin: float, outmax: float, t: float) -> 'PID':
        """
        Initialize PID controller object and set attributes for gains and time characteristics.
        The setpoint is uninitialized and the controller is disabled on initialization.

        @param kp: proportional gain
        @param ki: integral gain
        @param kd: derivative gain
        @param tau: derivative low-pass filter time constant
        @param outmin: output limit min
        @param outmax: output limit max
        @param t: sample time in seconds

        @rtype: PID
        @return PID that initializes constants and previous values as empty arrays
        """
        self.KP = kp
        self.KI = ki
        self.KD = kd
        self.TAU = tau
        self.OUTMIN = outmin
        self.OUTMAX = outmax
        self.T = t
        self._integrator = []
        self._differentiator = []
        self._prev_error = []
        self._prev_pt = []
        self._set_point = None
        self._status = False

     def output(self, pt: float) -> float:
          """
          Update PID stored values and return the output.
          output based on digitized standard PID form + some practicle considerations (anti-windup and HF noise rejection)

          @param setpoint: setpoint from user

          @rtype float
          @return PID output value
          """
          # check for uninitialized set point
          if self._set_point == None:
               print("Set point not initialized")
               return 0
          
          # disable if controller is not active
          if not self._status:
               print("Controller inactive")
               return 0

          _error = self._setpoint - pt

          # compute proportional term
          _proportional = self.KP*_error

          # comput integral term
          self._integrator = self._integrator + 0.5*self.KI*self.T*(_error + self._prev_error)


          # anti-windup via dynamic integrator clamping

          # finding integrator limits based on output limits
          if self.OUTMAX > _proportional :
               _integrator_max = self.OUTMAX - _proportional
          else:
               _integrator_max = 0

          if self.OUTMIN < _proportional :
               _integrator_min = self.OUTMIN - _proportional
          else:
               _integrator_min = 0
          
          # clamping integrator
          if self._integrator > _integrator_max :
               self._integrator = _integrator_max
          elif self._integrator < _integrator_min:
               self._integrator = _integrator_min
     
          # compute derivative term
          # differentiator with HF rejection (band-limitted differetiation)
          # derivative on measurement to prevent derivative kick
          self._differentiator = (2 * self.KD * (pt - self._prev_pt) + (2 * self.TAU - self.T) * self._differentiator) / (2 * self.TAU + self.T)

          # calculate output
          output = _proportional + self._integrator + self._differentiator

          if output > self.OUTMAX:
               output = self.OUTMAX
          elif output < self.OUTMIN:
               output = self.OUTMIN
          
          # store current error and data point for next update
          self._prev_error = _error
          self._prev_pt = pt

          return output

     def setpoint(self, setpoint: float) -> None:
          """
          Update the setpoint.

          @param setpoint: setpoint from user

          @rtype None
          """
          self._set_point = setpoint
          return
     
     def status(self, status: bool) -> None:
          """
          Update the status.

          @param status: status from user [True, False]

          @rtype None
          """
          self._status = status
          return

class TunableBangBang:

     # DUTY_CYCLE: float        # duty cycle for actuator: [0,1]
     # INIT_THRESH: float       # threshold where control switches from 100% duty cycle to self.DUTY_CYCLE
     # T: float                 # sample time in seconds
     # _set_point: float        # the set point to control to
     # _status: bool            # enable/disable controller

     def __init__(self, t: float, duty_cycle: float, init_thresh: float) -> 'TunableBangBang':
          """
          Initialize the controller with provided values. Status is False (disabled) and the set point is uninitialized on initialization.

          @param t: sample time in seconds
          @param duty_cycle: duty cycle for actuator: [0,1]
          @param init_thresh: threshold where control switches from 100% duty cycle to self.DUTY_CYCLE

          @rtype TunableBangBang
          @return initialized controller
          """
          self.DUTY_CYCLE = duty_cycle
          self.INIT_THRESH = init_thresh
          self.T = t
          self._set_point = None
          self._status = False

     def output(self, pt: float) -> float:
          """
          Update controller output and stored values.

          @param pt: the most recent data point

          @rtype float
          @return time in seconds that the actuator should be turned on
          """

          # check for uninitialized set point
          if self._set_point == None:
               print("Set point not initialized")
               return 0 # actuator off

          # disable if controller is not active
          if not self._status:
               print("Controller inactive")
               return 0 # actuator off

          if pt < self._set_point:
               if pt < self.INIT_THRESH:
                    return self.T # actuator on for complete period
               else:
                    return self.T * self.DUTY_CYCLE # actuator on for duty cycle
          else:
               return 0 # actuator off
     
     def setpoint(self, setpoint: float) -> None:
          """
          Update the setpoint.

          @param setpoint: setpoint from user

          @rtype None
          """
          self._set_point = setpoint
          return
     
     def status(self, status: bool) -> None:
          """
          Update the status.

          @param status: status from user [True, False]

          @rtype None
          """
          self._status = status
          return
