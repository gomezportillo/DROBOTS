#include "./ControllerFactory.ice"

module drobots {
	interface Container {
		void link(int key,drobots::RobotController* controller);
		drobots::RobotController* unlink(int key);
		//list<drobots::RobotController*> list();
		drobots::RobotController* getValue(int key);
	};
};
