# -*- coding: cp1252 -*-
from SimulationManager import *

class Simulation:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.mSM = SimulationManager()

    def simulationLoop(self):
        global mE
        mE.cleanEntitys()

        mE.mGlobalVariables["Conn"]     = self.conn
        mE.mGlobalVariables["Cursor"]   = self.cursor

        self.mSM.startSimulation()


    def endSimulation(self):
        self.end = True

    def menuLoop(self):
        loadDB = 0
        convertDB = 1
        startSimulation = 2
        end = -1
        option = 0
        while(option != end):

            print "Escolha uma das opções abaixo:"
            print str(loadDB)       +"\tCarregar uma base de dados"
            print str(convertDB)    + "\tConverter um txt em uma base de dados"
            if(mDB.isConnected()):
                print str(startSimulation)   + "\tIniciar simulação"
            print str(end) +"\tSair"
            option = int(input("Escolha:\t"))
            
            if(option == loadDB):
                fileName = str(raw_input("Qual base deve ser carregada?\t"))
                mDB.loadDataBase(fileName)
                
            elif(option == convertDB):
                fileName = str(raw_input("Qual base deve ser convertida?\t"))
                mDB.convertTxtToSql(fileName)

            elif(option == startSimulation and mDB.isConnected()):
                mDB.simulationLoop()
                
            else:
                pass
            print "======================================================================"
        self.closeDataBase()
        
#mE.mGlobalVariables["Map"]     = ".//resources//WorldMap-Ironforge.png"
g = Simulation()
#mDB.loadDataBase(databasePath + "Ironforge-1d")
mDB.loadDataBase("miniIronForge")
#mDB.convertTxtToSql("Ironforge-1d.txt")
#mDB.convertTxtToSql("miniIronForge.txt")
g.simulationLoop()
#g.menuLoop()
