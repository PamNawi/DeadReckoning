# -*- coding: cp1252 -*-
from Load import *

databasePath = './/resources//DataBases//'

class DataBaseManager:
    def __init__(self):
        self.conn = None
        self.cursor = None

    def closeDataBase(self):
        if(self.conn):
            self.conn.close()
            self.cursor = None

    def loadDataBase(self, fileName):
        self.closeDataBase()

        dataBaseFile = databasePath + fileName.strip(".txt") + ".db"
        self.conn = sqlite3.connect(dataBaseFile)
        print "Foi criada a conexao com "+ dataBaseFile
        self.cursor = self.conn.cursor()

    def convertTxtToSql(self, fileName):
        self.closeDataBase()

        #Create DB
        dataBaseFile = databasePath + fileName.strip(".txt") + ".db"
        self.conn = sqlite3.connect(dataBaseFile)
        print "Foi criada "+ dataBaseFile
        self.cursor = self.conn.cursor()
        
        print "Dropando tabelas antigas caso existam"
        sqlcmd = "DROP TABLE IF EXISTS POSITIONS"
        self.cursor.execute(sqlcmd)
        
        #Create tables
        print "Criando novas as tabelas"
        sqlcmd = '''CREATE TABLE POSITIONS ( ID INTEGER PRIMARY KEY,
        TIMESTAMP INTEGER, PLAYERID INTEGER, X REAL, Y REAL, Z REAL, ANGLE REAL)'''
        self.cursor.execute(sqlcmd)

        print "Fazendo parser no arquivo"
        f = open(databasePath + fileName).read()
        lines = f.split("\n")
        #Insert itens
        print "Inserindo todas as entradas"
        for l in lines:
            line = l.split(", ")
            sqlcmd = "INSERT INTO POSITIONS (TIMESTAMP, PLAYERID, X, Y, Z, ANGLE) VALUES (" + line[0] +","+ line[1] +","+ line[2] +","+ line[3] +","+ line[4] +"," + line[5]+ ");"
            self.cursor.execute(sqlcmd)

        self.conn.commit()
        print "Terminei a conversão"


    def getFirstTimestamp(self):
        global mE
        sqlcmd = "SELECT MIN(TIMESTAMP) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        result = int(self.cursor.fetchone()[0])
        return result

    def getLastTimestamp(self):
        global mE
        sqlcmd = "SELECT MAX(TIMESTAMP) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)

        result = int(self.cursor.fetchone()[0])
        return result

    def getMinPosition(self):
        global mE
        sqlcmd = "SELECT MIN(X) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        x = int(self.cursor.fetchone()[0])
        
        sqlcmd = "SELECT MIN(Y) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        y = int(self.cursor.fetchone()[0])
        return (x,y)

    def getMaxPosition(self):
        global mE
        sqlcmd = "SELECT MAX(X) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        x = int(self.cursor.fetchone()[0])
        
        sqlcmd = "SELECT MAX(Y) FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        y = int(self.cursor.fetchone()[0])
        return (x,y)

    def getNAvatars(self):
        global mE
        sqlcmd = "SELECT DISTINCT PLAYERID FROM POSITIONS;"
        self.cursor.execute(sqlcmd)
        return len(self.cursor.fetchall())

    def isConnected(self):
        if(self.conn):
            return True
        return False

    def getPositions(self, timestamp):
        #Get the positions in the database
        sqlcmd = "SELECT * FROM POSITIONS WHERE TIMESTAMP =" + str(timestamp) +" ;"
        self.cursor.execute(sqlcmd)

        result = self.cursor.fetchall()
        return result
