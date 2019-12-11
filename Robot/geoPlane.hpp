#ifndef __GEOPLANE__HPP__
#define __GEOPLANE__HPP__

class GeoPlane {
    private:
        bool thetaIsCalc;
        float theta1;
        float theta2;
        bool coordIsCalc;
        float l;
        float h;

    public:
        // GeoPlane constructor
        GeoPlane() : thetaIsCalc(false), theta1(0), theta2(0), coordIsCalc(0), l(0), h(0) {}

        // Setters
        void setAngle(float theta1, float theta2);
        void setCoord(float l, float h);

        // Getters
        void getAngle(float & theta1, float & theta2); // We know the position
        void getCoord(float & l, float & h); // We know the angle

    private:
        // Plane position calculation
        static float calcCoordOfL(float theta1, float theta2);
        static float calcCoordOfH(float theta1, float theta2);

        // Theta1 value searching
        bool searchTheta1(bool withL, float & xStart, float & xEnd, float yTarget, float theta2, float & accuracy);
};


#endif
