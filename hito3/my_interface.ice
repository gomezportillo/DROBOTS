// -*- mode:c++ -*-
#include "drobots.ice"

module drobots {

    interface ControllerFactory {
        drobots::RobotController* make(drobots::Robot* bot);
    };

    interface Container { };    

    interface RobotControllerAttacker extends drobots::RobotController{ };
	interface RobotControllerDeffender extends drobots::RobotController{ };

    
};
