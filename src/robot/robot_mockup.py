from logging import getLogger
from math import pi

class MockupRobot:
    """Classe de simulation complète du robot réel pour les tests"""
    
    def __init__(self):
        # Configuration physique
        self.WHEEL_BASE_WIDTH = 117  # Distance entre les roues (mm)
        self.WHEEL_DIAMETER = 66.5   # Diamètre des roues (mm)
        self.WHEEL_BASE_CIRCUMFERENCE = self.WHEEL_BASE_WIDTH * pi
        self.WHEEL_CIRCUMFERENCE = self.WHEEL_DIAMETER * pi
        
        # Ports moteurs
        self.MOTOR_LEFT = 1
        self.MOTOR_RIGHT = 2
        self.MOTOR_BOTH = 3
        
        # États
        self.dpsg = 0  # Degrés par seconde (roue gauche)
        self.dpsd = 0  # Degrés par seconde (roue droite)
        self.angleg = 0  # Angle cumulé gauche (degrés)
        self.angled = 0  # Angle cumulé droite (degrés)
        self.estCrash = False
        self.logger = getLogger(self.__class__.__name__)

    # --- Méthodes Moteurs ---
    def set_motor_dps(self, port, dps):
        """Définit la vitesse angulaire des moteurs en degrés/seconde"""
        if port in [self.MOTOR_LEFT, self.MOTOR_BOTH]:
            self.dpsg = dps
        if port in [self.MOTOR_RIGHT, self.MOTOR_BOTH]:
            self.dpsd = dps
        self.logger.debug(f"Moteurs: G={self.dpsg}°/s, D={self.dpsd}°/s")

    def get_motor_position(self):
        """Retourne les positions angulaires cumulées des moteurs"""
        self.angleg += self.dpsg / 10  # Simulation du mouvement
        self.angled += self.dpsd / 10
        return (self.angleg, self.angled)

    def offset_motor_encoder(self, port, offset):
        """Réinitialise les encodeurs moteurs"""
        if port in [self.MOTOR_LEFT, self.MOTOR_BOTH]:
            self.angleg = offset
        if port in [self.MOTOR_RIGHT, self.MOTOR_BOTH]:
            self.angled = offset
        self.logger.debug(f"Encodeurs réinitialisés: port={port}, offset={offset}")

    # --- Méthodes de Contrôle ---
    def stop(self):
        """Arrête immédiatement tous les moteurs"""
        self.dpsg = 0
        self.dpsd = 0
        self.logger.info("Moteurs arrêtés")

    def avancer(self, vitesse):
        """Avance à vitesse linéaire donnée (mm/s)"""
        dps = vitesse / (self.WHEEL_DIAMETER * pi) * 360
        self.set_motor_dps(self.MOTOR_BOTH, dps)

    def tourner(self, angle):
        """Tourne d'un angle spécifié (degrés)"""
        dps = 50  # Vitesse angulaire constante
        if angle > 0:  # Droite
            self.set_motor_dps(self.MOTOR_LEFT, dps)
            self.set_motor_dps(self.MOTOR_RIGHT, -dps)
        else:  # Gauche
            self.set_motor_dps(self.MOTOR_LEFT, -dps)
            self.set_motor_dps(self.MOTOR_RIGHT, dps)

    # --- Capteurs ---
    def get_distance(self):
        """Simule la lecture du capteur de distance (mm)"""
        dist = 150 + (self.angleg % 360)  # Valeur variant pour les tests
        self.logger.debug(f"Distance mesurée: {dist}mm")
        return dist

    # --- Caméra ---
    def get_image(self):
        """Retourne une image simulée"""
        self.logger.debug("Capture d'image simulée")
        return bytearray([0]*640*480*3)  # Image noire 640x480 RGB

    def get_images(self):
        """Retourne un flux d'images"""
        return [self.get_image()]

    def servo_rotate(self, position):
        """Contrôle le servo de la caméra"""
        self.logger.debug(f"Rotation servo à {position}°")

    # --- Enregistrement Vidéo ---
    def start_recording(self):
        """Démarre l'enregistrement vidéo"""
        self.logger.info("Début enregistrement vidéo")

    def stop_recording(self):
        """Arrête l'enregistrement vidéo"""
        self.logger.info("Fin enregistrement vidéo")

    # --- Méthodes Techniques ---
    def __getattr__(self, attr):
        """Gère les appels à des méthodes non implémentées"""
        self.logger.warning(f"Méthode non implémentée: {attr}")
        return lambda *args, **kwargs: None


   
