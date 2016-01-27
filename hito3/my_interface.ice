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
    };   

    interface ControllerFactory {
        drobots::RobotController* make(drobots::Robot* bot, Container* container);
    };

    interface RobotControllerAttacker extends drobots::RobotController{
        void informEnemyPosition(drobots::Point point);
        void setContainer(Container* container);
    };

	interface RobotControllerDefender extends drobots::RobotController{ 
        void setContainer(Container* container);
    };
   
};
