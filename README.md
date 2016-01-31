# DROBOTS - Distributed [CROBOTS](https://en.wikipedia.org/wiki/Crobots)
Distributed Systems' final project using ZeroC Ice middleware

Two first milesotnes and basic version of the last one. Further information about this game, instructions and protocols can be seen on Documentation.pdf

* First milestone asked for connecting to the server and moving a single robot to the 500,500 position on the board
* Second milestone was aimed to develop a winning strategy for a single robot. A FSM was designed an implemented for this duty.

<p align="center">
  <img src="https://github.com/pedroma-gomezp/DROBOTS/blob/master/hito2/FSM%20diagram.png?raw=true" alt="FSM"/>
</p>

* Third and last milestone asked for a implementation of several distributed factories and containers for creating robot controllers and holding those factories and robot controllers in order to allow every element of the system to access others, regardless the physical computer they are located. A Makefile has been set up for launching four different terminals,
	* first one will set up the four factories of the system (each one can be launched independently)
	* second one will set up the containers
	* thrid one will build a naive player whose robot will only move to a random point of the map. This player will work apart from factories and containers
	* fourth one will set up the real player, who will establish contact with the distributed elements of the system setting up 2 defender and 2 attacker robots on the board and communicating them on a very basic way (each robot will only contact their partners to inform them about its position).
    
