// -*- mode:c++ -*-
#include "drobots.ice"

module drobots {

    dictionary<int, Object*> ObjectPrxDict;
    
    interface Container {
        void link(int key, Object* proxy);
        void unlink(int key);
        ObjectPrxDict list();
        Object* getElementAt(int key);
        void setType(string type);
        string getType();
    };   

    interface ControllerFactory {
        drobots::RobotController* make(drobots::Robot* bot, Container* container);
    };

    interface RobotControllerAttacker extends drobots::RobotController{
        void setContainer(Container* container);
        void informEnemyPosition(drobots::Point point);
        string enviarMensaje(string msg);
    };

	interface RobotControllerDefender extends drobots::RobotController{ 
        void setContainer(Container* container);
        //void getInformedAboutEnemy(drobots::Point point, int angle);
    };
   
};
