import random
import time
import sys
import sqlite3
sys.path.insert(0, './/miniEngine/')
from miniEngine import *
from DataBaseManager import *

#Global Variables
mE = MiniEngine(1024,768)
mDB = DataBaseManager()

databasePath = './/resources//DataBases//'
