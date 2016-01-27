#include "./Drobots.ice"

module drobots {

dictionary<string, Object*> ObjectPrxDict;

	interface Container {
		void link(int key,drobots::RobotController* controller);
		void linkRB(drobots::RobotController* controller);
		void unlink(int key);
		ObjectPrxDict list();
		drobots::RobotController* getValue(int key);
	};
	interface RobotControllerAttacker extends drobots::RobotController{
		void attackPos(Point p);
		Point getSelfPos();
	};
	interface RobotControllerDefender extends drobots::RobotController{
		void sendAngleScan();
		void receiveAngleScan();
		Point getSelfPost();
		void receivePos();
	};
	
	interface ControllerFactory {
		drobots::RobotController* make(drobots::Robot* bot, drobots::Container* container);
	};	
  
};
