#ifndef __GEOPLANE__HPP__
#define __GEOPLANE__HPP__

class GeoPlane {
    private:
        bool tetaIsCalc;
        float teta1;
        float teta2;
        bool coordIsCalc;
        float l;
        float h;

    public:
        GeoPlane() : tetaIsCalc(false), teta1(0), teta2(0), coordIsCalc(0), l(0), h(0) {}

        void setAngle(float teta1, float teta2);
        void setCoord(float l, float h);

        void getAngle(float & teta1, float & teta2);
        void getCoord(float & l, float & h);

    private:
        static float calcCoordOfL(float teta1, float teta2);
        static float calcCoordOfH(float teta1, float teta2);
};


#endif
