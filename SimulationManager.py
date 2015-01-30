# -*- coding: cp1252 -*-
from Load import *
from Avatar import *

class SimulationManager:
    def __init__(self):
        self.end = False
        self.avatars = {}
        self.updatedAvatars = []

    def update(self):
        if(mE.keyboard.isPressed(pygame.K_SPACE)):
            self.end = True

        self.updatePositions()
        self.tTimestamp.content = "Timestamp:  " +str(self.actualTimestamp)
        time.sleep(0.2)


    def startSimulation(self):
        global mE

        print "Carregando os recursos"
        self.actualTimestamp = mDB.getFirstTimestamp()
        self.lastTimestamp = mDB.getLastTimestamp()

        self.minPosition = mDB.getMinPosition()
        self.maxPosition = mDB.getMaxPosition()

        mE.mGlobalVariables["MinPosition"]  = self.minPosition
        mE.mGlobalVariables["MaxPosition"]  = self.maxPosition

        #Create GUI
        font  = pygame.font.Font(None,20)
        self.tTimestamp = Text()
        self.tTimestamp.color = (255,255,255)
        self.tTimestamp.content = "Timestamp:  " +str(self.actualTimestamp)
        
        mE.mTextManager.addFont(font, "Arial24")
        mE.mTextManager.addText(self.tTimestamp, "GUITimestamp")
        mE.mTextManager.setTextFont("GUITimestamp", "Arial24")

        self.tNAvatars = Text()
        self.tNAvatars.setPosition(300,0)
        self.tNAvatars.color = (255,255,255)
        self.tNAvatars.content = "NAvatars:  " +str(len(self.avatars))

        mE.mTextManager.addText(self.tNAvatars, "NAvatars")
        mE.mTextManager.setTextFont("NAvatars", "Arial24")

        #Load background
        try:
            mE.mAnimationManager.addAnimation([mE.mGlobalVariables["Map"]], 1, "Background")
            background = Entity()
            mE.mEntityManager.addEntity(background, "Background", "BG")
            mE.mAnimationManager.setEntityAnimation(background, "Background")
        except KeyError:
            print "Nenhum arquivo foi fornecido para o background da simulação"

        mE.mAnimationManager.addAnimation([".//resources//dotWhite.png"], 1, "Ghost")
        mE.mAnimationManager.addAnimation([".//resources//dotBlue.png"], 1, "DeadReckoning")
        
        print "Inicializando a simulação"
        mE.mEntityManager.defineLayerOrder(["BG", "Avatar"])
        while not self.end:
            mE.update()
            self.update()
            mE.render()
        print "Acabou"

    def updatePositions(self):
        #if this timestamp is the last just close the simulation
        if(self.actualTimestamp >= self.lastTimestamp):
            self.end = True
            return
        #Get the positions in the database
        sqlines = mDB.getPositions(self.actualTimestamp)
        #Update all avatar positions
        
        for line in sqlines:
            avatarId = line[2]
            try:
                self.avatars[avatarId].updateGhostPosition(line)
            except KeyError:
                self.avatars[avatarId] = Avatar(line)
                self.tNAvatars.content = "NAvatars:  " +str(len(self.avatars))

            self.updatedAvatars.append(avatarId)
        self.actualTimestamp += 1

        #Remove all not updated avatars
        if(self.actualTimestamp % 10 == 0):
            self.removeNotUpdated()
            

    def removeNotUpdated(self):
        avatars = mE.mEntityManager.getTagEntitys("Avatar")
        for avatar in avatars:
            if not avatar.updated:
                mE.mEntityManager.removeEntity(avatar,"Avatar")
                self.avatars.pop(avatar.id, None)
            else:
                avatar.updated = False
        

        
