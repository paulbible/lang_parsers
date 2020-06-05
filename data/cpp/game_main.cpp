/*
	Video Lecture: https://www.youtube.com/watch?v=fCkeLBGSINs
	Watch before starting the assignment.

	Author: Paul W. Bible
	Description: A simple battle game inspired by Pokemon.
	Course: CST 171
*/
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <climits>
#include "Pokemon.hpp"
using namespace std;


/*
	This function simulates a coin flip.
	50% of the time it is heads and 50% tails
*/
bool coinFlip() {
	return rand() % 2 == 0;
}

// a function to pause the progression to the game
void pause() {
	cout << "Press enter to continue" << endl;
	cin.ignore(INT_MAX, '\n');
}

// simple function to take care of '\n' input issues.
char getChar() {
	string tmp;
	getline(cin, tmp);
	if (tmp.size() > 0) {
		return tmp.at(0);
	}
	return '\0';
}

string getString() {
	string tmp;
	getline(cin, tmp);
	if (tmp.size() > 0) {
		return tmp;
	}
	return "No name";
}


/*
	This function loads pokemon data into an array
*/
void loadPokemon(Pokemon pokeArray[], string filename, int n) {

	ifstream in = ifstream(filename);
	if (!in.good()) {
		cout << "file count not be open" << endl;
		pause();
	}
	string name;
	int level;
	int health;
	int attack;
	float percentHit;
	
	for (int i = 0; i < n; i++) {
		in >> name;
		in >> level;
		in >> health;
		in >> attack;
		in >> percentHit;
		pokeArray[i] = Pokemon(name, level, health, attack, percentHit);
	}
	in.close();
}


char playerOptionsBattle() {

	char choice = '\0';
	while (choice != 'a' && choice != 'h' && choice != 'f') {
		cout << endl;
		cout << ">>>++- Choose your actions -++<<<" << endl;
		cout << "a) Attack" << endl;
		cout << "h) Heal (recover some health)" << endl;
		cout << "f) Forfeit (end the battle)" << endl;
		choice = getChar();
	}
	
	return choice;
}


char playerOptionsMain() {

	char choice = '\0';
	while (choice != 'f' && choice != 'n' && choice != 's' 
		&& choice != 'b' && choice != 'q') 
	{
		cout << endl;
		cout << ">>>++- Main Menu -++<<<" << endl;
		cout << "f) Fight a battle at the current stage" << endl;
		cout << "n) Next Stage, move on to a bigger challenge" << endl;
		cout << "s) Stats, show the states for your self and Pokemon" << endl;
		cout << "b) Buy something from the store." << endl;
		cout << "q) Quit Game" << endl;
		choice = getChar();
	}

	return choice;
}


/*
	This function causes 2 pokemon to battle.
	Notice the pass-by-reference

	return type reports true if the player wins the battle
*/
bool battle(Pokemon& pokemon1, Pokemon& pokemon2) {
	// main battle loop
	cout << endl;
	cout << "########## BATTLE! ##########" << endl;
	cout << "In this battle " << pokemon1.getName() << " goes up against " << pokemon2.getName() << "!" << endl;
	cout << "Who will be the very best like no one ever was?!" << endl;
	pause();

	bool isQuit = false;

	int round = 0;
	while (pokemon1.isGood() && pokemon2.isGood() && !isQuit) {
		// output the round number
		round++;
		cout << "***** Round " << round << " *****" << endl;
		cout << endl;
		cout << ">>>> stats <<<<" << endl;
		pokemon1.print();
		cout << "-----" << endl;
		pokemon2.print();
		cout << "<<<<< >>>>>" << endl;
		cout << endl;

		// player chooses action
		char choice = playerOptionsBattle();

		
		if (choice == 'a') {
			if (pokemon1.attackPokemon(pokemon2)) {
				cout << endl;
				cout << "----------" << endl;
				cout << pokemon1.getName() << " attacks " << pokemon2.getName();
				cout << " for " << pokemon1.getAttackDamage() << " damage!" << endl;

				if (!pokemon2.isGood()) {
					cout << pokemon2.getName() << " has fallen unconcious!" << endl;
				}

			}
			else {
				cout << pokemon1.getName() << "'s attack failed." << endl;
			}
			cout << "----------" << endl;
			cout << endl;
		}
		else if (choice == 'h') {
			// heal pokemon
		}
		else if (choice == 'f') {
			// quite the match
			isQuit = true;
			break;
		}
		

		// pokemon 2 attacks
		if (pokemon2.isGood() && pokemon2.attackPokemon(pokemon1)) {
			cout << endl;
			cout << "----------" << endl;
			cout << pokemon2.getName() << " attacks " << pokemon1.getName();
			cout << " for " << pokemon2.getAttackDamage() << " damage!" << endl;
			if (!pokemon1.isGood()) {
				cout << pokemon1.getName() << " has fallen unconcious!" << endl;
			}
		}
		else {
			cout << pokemon2.getName() << "'s attack failed." << endl;
		}
		cout << "----------" << endl;

	}// end battle loop

	// assess outcome
	if (pokemon1.isGood() && !isQuit) {
		cout << endl;
		cout << pokemon1.getName() << " is the winner!" << endl;
		pokemon1.gainReward(pokemon2.getReward());
		return true;
	}

	// assess outcome
	if (pokemon2.isGood()) {
		cout << endl;
		cout << pokemon2.getName() << " is the winner!" << endl;
		pokemon2.gainReward(pokemon1.getReward());
		return false;
	}

	return false;
}


int main() {
	//----- intro -----
	cout << "----====++++ Welcome to Pokemon Battle Arena! ++++====----" << endl;
	cout << endl;

	//----- Create Player -----
	cout << "Enter your name: ";
	string name = getString();

	//create your playere here ...
	// cout << "Welcome " << player.getName() << "!" << endl;
	cout << "Welcome " << name << "!" << endl;

	//----- Load Pokemon -----
	// create an array of monsters
	int pokeCount = 3;
	Pokemon monsters[3];
	// load them from file.
	loadPokemon(monsters, "pokemon_data.txt", pokeCount);

	// initialize the pokemon
	// pokemon 0 is the player's main, this is a COPY of the class.
	Pokemon mainPokemon = monsters[0];

	// There will be up to 5 stages.
	int stage = 1;
	bool keepPlaying = true;
	bool youWin = false;

	while (keepPlaying) {
		cout << "]]]] STAGE " << stage << " [[[[" << endl;

		char choice = playerOptionsMain(); // fnsbq
		if (choice == 'f') { // >>>>>>>>>>>>>>>>>>>> fight a battle
			Pokemon opponent = monsters[stage];
			// battle
			bool didWin = battle(mainPokemon, opponent);

			/////// Post battle
			// add 1 to player battle count.

			if (didWin) {
				cout << "You won!" << endl;
				// add 1 to player win count.
				
				// other win actions
				// add money to player's pokedollar count
				int winPokedollars = 10 * stage;

				// heal ...

				// win the game
				if (stage == 4) {
					keepPlaying = false;
					youWin = true;
				}

			}
			else {
				// restor your pokemon's health
				//add 1 to player loss count
			}
		}
		else if (choice == 'n') { // >>>>>>>>>>>>>>>>>>>> advance next stage
			if (stage < 4) {
				stage++;
			}
			cout << "You advance to stage " << stage << endl;
		}
		else if (choice == 's') { // >>>>>>>>>>>>>>>>>>>> Show stats
			// print stats
			mainPokemon.print();
			// print player stats

		}
		else if (choice == 'b') { // >>>>>>>>>>>>>>>>>>>> buy something at the shop
			// allow the player to buy something at the shop.
		
		}
		else if (choice == 'q') { // >>>>>>>>>>>>>>>>>>>> quit the game
			// allow the player to buy something at the shop.
			keepPlaying = false;
		}


	}
	/////// End of main game loop



	if (youWin) {
		cout << "You became the very best like no one ever was!!!" << endl;
		cout << "Congratulations! You Win!" << endl;
	}
	cout << "Thank you for playing!" << endl;
	

	

	

	cout << "hello" << endl;

	return 0;
}