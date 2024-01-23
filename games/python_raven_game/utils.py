import random
import threading
import pygame
from constans import *
import time

    
import requests
import json

import platform
import socket
import os
# import psutil

import hashlib

def get_image(sheet, width, height, scale, colour, start_position, rotation=0):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), (start_position[0]*width,
               start_position[1] * height, (start_position[0]+1)*width, (start_position[1]+1)*height))
    image = pygame.transform.scale(image, (width*scale, height * scale))
    image = pygame.transform.rotate(image, rotation)
    image.set_colorkey(colour)
    return image


def check_collision(raven_position, arrow_position):
    arrow_point = (
        arrow_position[0] + ARROW_SPRITE_WIDTH * ARROW_SCALE / 2, arrow_position[1] + ARROW_SPRITE_HEIGHT * ARROW_SCALE / 2)
    xIsInCollision = arrow_point[0] > raven_position[0] and arrow_point[0] < raven_position[0] + \
        RAVEN_SPRITE_WIDTH * SCALE

    yisInCollision = arrow_point[1] > raven_position[1] and arrow_point[1] < raven_position[1] + \
        RAVEN_SPRITE_HEIGHT * SCALE
    return xIsInCollision and yisInCollision


class Time_Manager:
    def __init__(self, fire_arrow_fun, update_raven_fun, increase_score_fun):
        self.time_elapsed_since_last_animation_change = 0
        self.time_elapsed_since_last_arrow_fired = 0
        self.time_elapsed_since_incresed_score = 0
        self.clock = pygame.time.Clock()
        self.fire_arrow_fun = fire_arrow_fun
        self.update_raven_fun = update_raven_fun
        self.increase_score_fun = increase_score_fun
        self.arrow_speed = 4000

    def tick(self):
        dt = self.clock.tick()
        [anim, arr, score] = [dt, dt, dt]
        self.time_elapsed_since_last_animation_change += anim
        self.time_elapsed_since_last_arrow_fired += arr
        self.time_elapsed_since_incresed_score += score

        if self.time_elapsed_since_last_animation_change > MOVEMENT_SPEED * 50:
            self.update_raven_fun()
            self.time_elapsed_since_last_animation_change = 0

        if self.time_elapsed_since_last_arrow_fired > MOVEMENT_SPEED * self.arrow_speed:
            self.fire_arrow_fun()
            self.time_elapsed_since_last_arrow_fired = 0

        if self.time_elapsed_since_incresed_score > MOVEMENT_SPEED * 4000:
            self.increase_score_fun()
            self.arrow_speed = self.arrow_speed-50
            self.time_elapsed_since_incresed_score = 0

    def reset(self):
        self.time_elapsed_since_last_animation_change = 0
        self.time_elapsed_since_last_arrow_fired = 0
        self.time_elapsed_since_incresed_score = 0
        self.clock = pygame.time.Clock()
        self.arrow_speed = 4000

class License_Manager:
    def __init__(self,userId,gameId,jwt):
        self.userId = userId
        self.gameId = gameId
        self.jwt = jwt
    # @staticmethod
    # def getSystemInfo(isAnalytics=True):
    #     system_info = {
    #         "Os": platform.system(),
    #         "Arch": platform.architecture(),
    #         "CPUCoreReal": psutil.cpu_count(logical=False),
    #         "CPUCoreLogical": psutil.cpu_count(logical=True),
    #         "CPUFreq": psutil.cpu_freq().current,
    #         "Ram": psutil.virtual_memory().total,
    #     }
    #     if isAnalytics:
    #         system_info['OsVer']=platform.version()
    #         system_info['RamAval']=psutil.virtual_memory().available

    #         disk_info = []
    #         partitions = psutil.disk_partitions()
    #         for partition in partitions:
    #             usage = psutil.disk_usage(partition.mountpoint)
    #             disk_info.append({
    #                 "Device": partition.device,
    #                 "Mountpoint": partition.mountpoint,
    #                 "File System Type": partition.fstype,
    #                 "Total Space": usage.total,
    #                 "Used Space": usage.used,
    #                 "Free Space": usage.free,
    #             })
    #         system_info['HDD']=disk_info

            

    #     return system_info
    
    # def getFingerPrint():
    #     fingerprint=License_Manager.getSystemInfo(False)
    #     data_str = json.dumps(fingerprint, sort_keys=True)
    #     return hashlib.sha512(data_str.encode()).hexdigest()


    @staticmethod
    def isLicensed(userId, gameId, jwt):
        _isLicensed = False
        print("Checking license")

        try:
            data = dict(userId=userId, gameId=gameId, jwt=jwt)
            response = requests.post('http://localhost:8000/api/checkSessionValidity', json=data)
            response.raise_for_status()
            print(response.json())

            _isLicensed =response.json() == response.json()

        except requests.exceptions.RequestException as e:
            print(f"Error in network request: {e}")
        except Exception as e:
            print(f"Error: {e}")

        return _isLicensed
    
    @staticmethod
    def LicensePooler(flag,userId,gameId,jwt):
        while(True):
            time.sleep(60)

            if License_Manager.isLicensed(userId,gameId,jwt):
                print("Secondary thread is signaling the main thread to exit.")
                flag.set()
                break


    @staticmethod
    def StartLicensePooler(flag,userId,gameId,jwt):
        secondary_thread = threading.Thread(target=License_Manager.LicensePooler,args=(flag,userId,gameId,jwt))
        secondary_thread.start()