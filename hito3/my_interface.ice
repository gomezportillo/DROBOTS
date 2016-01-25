// -*- mode:c++ -*-
#include <drobots.ice>

module drobots {

    interface ControllerFactory {
        Robotcontroller* make(Robot* bot);
    };

    interface Container { };    

    interface RobotControllerAttacker extends drobots::RobotController{ };
	interface RobotControllerDeffender extends drobots::RobotController{ };

    
};
