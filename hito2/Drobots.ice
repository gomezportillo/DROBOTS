// -*- mode:c++ -*-

module drobots {

  struct Point {
    int x;
    int y;
  };

  exception NoEnoughEnergy{};

  interface Robot {
    int scan(int angle, int wide) throws NoEnoughEnergy;
    bool cannon(int angle, int distance) throws NoEnoughEnergy;
    void drive(int angle, int speed) throws NoEnoughEnergy;
    short damage() throws NoEnoughEnergy;
    short speed() throws NoEnoughEnergy;
    Point location() throws NoEnoughEnergy;
    short energy() throws NoEnoughEnergy;
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
  exception InvalidName{
    string reason;
  };

  interface Game {
    void login(Player* p, string nick)
      throws GameInProgress, InvalidProxy, InvalidName;
  };
};
