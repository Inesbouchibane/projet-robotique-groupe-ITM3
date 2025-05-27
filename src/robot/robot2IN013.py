# src/robot/robot2IN013.py
import time, threading, math, numpy as np
from collections import deque  # Added missing import
from easygopigo3 import EasyGoPiGo3, Servo
from di_sensors import distance_sensor as ds_sensor
from di_sensors import inertial_measurement_unit as imu
import picamera

class Robot2IN013:
    WHEEL_BASE_WIDTH = 117
    WHEEL_DIAMETER = 66.5
    WHEEL_CIRCUMFERENCE = WHEEL_DIAMETER * math.pi
    WHEEL_BASE_CIRCUMFERENCE = WHEEL_BASE_WIDTH * math.pi

    _DEFAULT_RES = (640, 480)
    _DEFAULT_FPS = 24

    def __init__(self, nb_img=10, fps=25, resolution=None, servoPort="SERVO1", motionPort="AD1"):
        self._gpg = EasyGoPiGo3()

        # Video setup
        self.resolution = resolution or self._DEFAULT_RES
        self.fps_camera = fps or self._DEFAULT_FPS
        self.nb_img = nb_img
        self._img_queue = None
        self._recording = False
        self._thread = None

        try:
            self.camera = picamera.PiCamera()
            self.camera.resolution = self.resolution
            self.camera.framerate = self.fps_camera
            print("Camera initialized successfully")
        except Exception as e:
            print(f"Camera initialization failed: {e}. Ensure camera is enabled (raspi-config) and picamera is installed.")
            self.camera = None

        # Servo setup
        try:
            self.servo = Servo(servoPort, self._gpg)
        except Exception as e:
            print(f"Servo not found: {e}")
            self.servo = None

        # Sensors
        # ─── Capteur de distance ──────────────────────────────────────────────
        try:
            self.distanceSensor = ds_sensor.DistanceSensor()
            print("✅ Capteur de distance initialisé avec succès")
        except Exception as e:
            print(f"❌ Erreur initialisation capteur de distance : {e}")
            self.distanceSensor = None          # important : on garde l’attribut


        try:
            self.imu = imu.inertial_measurement_unit()
        except Exception as e:
            print(f"IMU sensor not found: {e}")
            self.imu = None

        # Motors and LEDs
        self._gpg.set_motor_limits(self._gpg.MOTOR_LEFT + self._gpg.MOTOR_RIGHT, 0)

        if self.camera:
            self.start_recording()

    def set_motor_dps(self, port, dps):
        self._gpg.set_motor_dps(port, dps)
        self._gpg.set_motor_limits(port, dps)

    def get_motor_position(self):
        return self._gpg.read_encoders()

    def offset_motor_encoder(self, port, offset):
        self._gpg.offset_motor_encoder(port, offset)

    def get_distance(self):
        """
        Renvoie la distance (mm) ou None.
        Si la lecture I²C échoue (Errno 5), on tente de recréer
        l'instance DistanceSensor jusqu’à 3 fois.
        """
        if self.distanceSensor is None:
            return None

        for _ in range(3):                       # 3 tentatives maxi
            try:
                d = self.distanceSensor.read_range_single(False)
                return d if 5 <= d <= 3000 else None
            except OSError as e:                 # Errno 5 / entrée-sortie
                if getattr(e, 'errno', None) == 5:
                    # tentative de ré-initialisation du capteur
                    try:
                        from di_sensors import distance_sensor
                        self.distanceSensor = distance_sensor.DistanceSensor()
                        continue                 # on ré-essaie
                    except Exception:
                        self.distanceSensor = None
                        return None
                else:
                    return None
            except Exception:
                return None
        return None




    def start_recording(self):
        if not self.camera:
            print("No camera available, cannot start recording")
            return
        if self._recording:
            return
        self._recording = True
        self._img_queue = deque(maxlen=self.nb_img)
        self._thread = threading.Thread(target=self._grab_loop, daemon=True)
        self._thread.start()
        print("Camera recording started")

    def stop_recording(self):
        if not self._recording:
            return
        self._recording = False
        if self._thread:
            self._thread.join()
            self._thread = None
        print("Camera recording stopped")

    def _grab_loop(self):
        try:
            with self.camera as cam:
                cam.framerate = self.fps_camera
                while self._recording:
                    time.sleep(1 / self.fps_camera)
                    frame = np.empty((self.resolution[1], self.resolution[0], 3), dtype=np.uint8)
                    cam.capture(frame, 'rgb', use_video_port=True)
                    self._img_queue.append((frame, time.time()))
        except Exception as e:
            print(f"Error in camera grab loop: {e}")
            self._recording = False

    def get_image(self):
        return self._img_queue[-1][0] if self._img_queue else None

    def get_images(self):
        return list(reversed(self._img_queue)) if self._img_queue else []

    def stop(self):
        self.set_motor_dps(self._gpg.MOTOR_LEFT + self._gpg.MOTOR_RIGHT, 0)
        self._gpg.set_led(self._gpg.LED_LEFT_BLINKER + self._gpg.LED_RIGHT_BLINKER +
                          self._gpg.LED_LEFT_EYE + self._gpg.LED_RIGHT_EYE + self._gpg.LED_WIFI, 0, 0, 0)

    def __getattr__(self, name):
        return getattr(self._gpg, name)
