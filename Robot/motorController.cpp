#include "motorController.hpp"

void MotorController::positionCalculator() {
    float normMove; // In mm
    float dirX, dirY, dirZ; // In mm, translation vector
    long  tmpsMove; // In ms
    int   nbDivMove;
    float tmpFloat1, tmpFloat2, tmpFloat3;

    while (1) {
        // Figure out the norm of the deplacement
        dirX = (targetX-truePosX);
        dirY = (targetY-truePosY);
        dirZ = (targetZ-truePosZ);
        normMove  = dirX*dirX;
        normMove += dirY*dirY;
        normMove += dirZ*dirZ;
        normMove = sqrt(normMove);

        // If the move is not null
        if (normMove > 1) {
            // Figure out the time to move to the target position
            tmpsMove = ((normMove / SPEED) * 1000) - 1;

            // Figure out the number of division
            nbDivMove = (tmpsMove / DIV_TIME) + 1;
            
            // Figure out the vector to add
            dirX = dirX / nbDivMove;
            dirY = dirY / nbDivMove;
            dirZ = dirZ / nbDivMove;

            // Figure out the new position (with a path ahead if he exists)
            truePosX += dirX;
            truePosY += dirY;
            truePosZ += dirZ;
            if (nbDivMove != 1) {
                tmpFloat1 = truePosX + dirX;
                tmpFloat2 = truePosY + dirY;
                tmpFloat3 = truePosZ + dirZ;
                timeToDest = DIV_TIME * 2;
            }else{
                tmpFloat1 = truePosX;
                tmpFloat2 = truePosY;
                tmpFloat3 = truePosZ;
                timeToDest = DIV_TIME;
            }

            // Wait for the send of the data
            motorAngleSended.acquire();

            // Figure out the angle motor require
            geoSpace.setCoord(tmpFloat1, tmpFloat2, tmpFloat3);
            geoSpace.getAngle(motTheta1, motTheta2, motTheta3);
        }
    }
}

void MotorController::posMove() {
    // If new data is figureout
    if (motorAngleSended.try_acquire() == false) {
        // Send to motors the new angle
        motorTheta1->setPositionWithDuration(motTheta1, timeToDest/1000);
        motorTheta2->setPositionWithDuration(motTheta2, timeToDest/1000);
        motorTheta3->setPositionWithDuration(motTheta3, timeToDest/1000);
    }

    motorAngleSended.release();
}

void MotorController::waitUntilMove() {
    while ((targetX-truePosX) > 1 || (targetY-truePosY) > 1 || (targetZ-truePosZ) > 1) {
        motorTheta1->waitUntilMove();
        motorTheta2->waitUntilMove();
        motorTheta3->waitUntilMove();
    }
}

void MotorController::go(float posX, float posY, float posZ) {
    targetX = posX;
    targetY = posY;
    targetZ = posZ;
}

// Go to the pause position
void MotorController::goPausePosition(bool withControlledTrajectory) {
    float x,y,z;

    // We target the pause position
    go(-200, 0, 20);
    
    if (withControlledTrajectory == false) {
        truePosX = targetX; truePosY = targetY; truePosZ = targetZ;
        geoSpace.setCoord(targetX, targetY, targetZ);
        geoSpace.getAngle(x, y, z);

        motorTheta1->setPosition(x, 400);
        motorTheta2->setPosition(y, 400);
        motorTheta3->setPosition(z, 1200);
    }

    // We wait for the movement to end
    waitUntilMove();
}
