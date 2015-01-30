from Load import *
from Vector3D import *

class Avatar (Entity):
    def __init__(self,sqline):
        Entity.__init__(self)
        self.realPosition = Vec3d(0,0,0)
        self.id = 0
        
        self.ghost = Ghost()
        mE.mEntityManager.addEntity(self.ghost, "Ghost", "Avatar")
        mE.mAnimationManager.setEntityAnimation(self.ghost, "Ghost")

        self.ghost.updateRealPosition(sqline)
        
        self.DREntity = DeadReckoningEntity()
        mE.mEntityManager.addEntity(self.DREntity, "DeadReckoning", "Avatar")
        mE.mAnimationManager.setEntityAnimation(self.DREntity, "DeadReckoning")

        #Calc the first position/prediction for the Dead Reckoning
        self.DREntity.realPosition = self.realPosition
        #self.DREntity.predictPosition = Vec3d(1,0,0).rotate_around_y(self.ghost.angle)

    def updateGhostPosition(self,sqline):
        self.updated = True
        self.ghost.updateRealPosition(sqline)

        self.DREntity.adjust(self.ghost.realPosition)
        self.DREntity.updatePrediction()
        

class Ghost(Entity):
    def __init__(self):
        Entity.__init__(self)

    def updateRealPosition(self, sqline):
        sqlid = sqline[0]
        timestamp = sqline[1]
        self.id = sqline[2]
        x = sqline[3]
        y = sqline[4]
        z = sqline[5]
        angle = sqline[6]
        
        self.realPosition = Vec3d(x,y,z)
        self.angle = angle
       
        self.setPosition(normalizeToViewPosition(x,y))


class DeadReckoningEntity(Entity):
    def __init__(self):
        Entity.__init__(self)
        self.realPosition = Vec3d(0,0,0)
        self.angle = 0
        self.desloc = Vec3d(0,0,0)

        self.predictPosition = Vec3d(0,0,0)

        self.vecPrevision = Line()
        self.vecPrevision.color = (255,0,0)
        mE.mPrimitiveManager.addPrimitive(self.vecPrevision, "vecPrevision")

    def adjust(self, realPosition):
        #Calculate the difference of the actual desloc with the new desloc
        #If is greaten of the error, substitute
        newDesloc = realPosition - self.realPosition
        if(self.desloc.get_distance( newDesloc) > 5):
            self.desloc = newDesloc
            
    def calcNextPosition(self):
        self.predictPosition = self.desloc + self.realPosition
        self.realPosition = self.predictPosition

        viewPositionStart = normalizeToViewPosition(self.realPosition.x, self.realPosition.y)  
        viewPositionEnd = normalizeToViewPosition(self.predictPosition.x, self.predictPosition.y)
        self.vecPrevision.startPoint = (self.position.x+4, self.position.y+4)
        self.vecPrevision.endPoint = (viewPositionEnd.x+4, viewPositionEnd.y+4)

    def updatePrediction(self):
        self.setPosition(normalizeToViewPosition(self.predictPosition.x,self.predictPosition.y))
        self.calcNextPosition()


def normalizeToViewPosition(x,y):
    minPosition = mE.mGlobalVariables["MinPosition"]
    maxPosition = mE.mGlobalVariables["MaxPosition"]
    
    x = 1024 * (x - minPosition[0]) / (maxPosition[0] - minPosition[0])
    y = 768 * (y - minPosition[1]) / (maxPosition[1] - minPosition[1])
    return Vec2d(x,y)
        
