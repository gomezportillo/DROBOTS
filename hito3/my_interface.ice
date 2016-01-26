// -*- mode:c++ -*-
#include "drobots.ice"

module drobots {

    interface Container { };    

    interface ControllerFactory {
        drobots::RobotController* make(drobots::Robot* bot, Container* container);
    };

    interface RobotControllerAttacker extends drobots::RobotController{ };
	interface RobotControllerDefender extends drobots::RobotController{ };
   
};
