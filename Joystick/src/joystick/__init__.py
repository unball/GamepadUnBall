import pygame
import numpy as np
import time
from threading import Thread

pygame.init()

if pygame.joystick.get_count() == 0:
    raise Exception('Não há joystick conectado')

joystick = pygame.joystick.Joystick(0)
joystick.init()

class Joystick:
    def __init__(self):
        self.angle = 0
        self.speed = 0
        self.w = 0
        self.vector = [1,0]
        self.stopped = True
        self.turbo = False
        self.spin = 0

        self.doUpdate = True
        
        self.thread = Thread(target=self.update)
        self.thread.start()

    def stop(self):
        self.doUpdate = False

    def update(self):
        while self.doUpdate:
            self.loop()
        
            time.sleep(1.0 / 120.0)

    def loop(self):
        for event in pygame.event.get():
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 16:
                        pass
                    elif event.button == 15:
                        pass
                        self.w = -1

                    # if event.button == 0: # A
                    #     self.spin = 1
                    # elif event.button == 1: # B
                    #     pass
                    # if event.button == 2: # X
                    #     self.spin = -1
                    #     pass
                    # if event.button == 3: # Y
                    #     self.turbo = True

                if event.type == pygame.JOYBUTTONUP:
                    self.w = 0

                    # if event.button == 0: # A
                    #     self.spin = 0
                    # elif event.button == 1: # B
                    #     pass
                    # if event.button == 2: # X
                    #     self.spin = 0
                    # if event.button == 3: # Y
                    #     self.turbo = False

                elif event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0 or event.axis == 1:
                        vector = self.vector.copy()
                        angle = 0

                        if event.axis == 0:
                            vector[1] = event.value
                            angle = np.arctan2(*vector)
                        elif event.axis == 1:
                            vector[0] = -event.value
                            angle = np.arctan2(*vector)
                        
                        if np.linalg.norm(vector) > 1:
                            self.vector = vector.copy()
                            self.angle = angle
                            self.stopped = False
                        
                        else:
                            self.stopped = True

                    elif event.axis == 2:
                        self.speed = -np.abs((event.value + 1) / 2.0) / 3
                    
                    elif event.axis == 5:
                        self.speed = np.abs((event.value + 1) / 2.0) / 3
                    elif event.axis == 3:
                        print(event, "AAAAAAAAAAA")
                        if abs(event.value) > 0.09:
                            self.w = event.value * 1.5
                        else:
                           self.w = 0
                    #else:
                    #    self.w = 0