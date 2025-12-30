#from base_module import *
import os
import datetime
import random
import numpy as np
import pandas as pd
from statistics import mean
import math
from datetime import timedelta

import mysql.connector

class Module:
    def __init__(self, param):

        print("Init module")
        self.name = "VALCO2T module"

    def reset(self):
        print(f"Reset module {self.name}")

    def run(self):
        print("Run module")