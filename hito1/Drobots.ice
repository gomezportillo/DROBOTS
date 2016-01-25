// -*- mode:c++ -*-

module drobots {

  struct Point {
    int x;
    int y;
  };

  interface Robot {
    int scan(int angle, int wide);
    bool cannon(int angle, int distance);
    void drive(int angle, int speed);
    short damage();
    int speed();
    Point location();
  };

  interface RobotController {
    void turn();
    void robotDestroyed();
  };

  interface Player {
    RobotController* makeController(Robot* bot);
    void win();
    void lose();
  };

  exception GameInProgress{};
  exception InvalidProxy{};

  interface Game {
    void attach(Player* p) throws GameInProgress, InvalidProxy;
  };
};
