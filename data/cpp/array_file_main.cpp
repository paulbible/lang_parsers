#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main() {
	// Arrays and File IO = Input Output
	cout << "hello" << endl;

	// Arrays, collections of like data (the same type)
	//  that are stored contiguously (side-by-side) in memory.

	/*
	// Want to store 5 elements, create a 5 element array.
	//const int n = 5;
	float scores[5]; // array declaration, "static arrays"

	// change a value in the array.
	scores[0] = 24; // 0-element, is the first element in the array.
	// "scores sub 0" --> subscript
	scores[1] = 19; // 1-element, 2nd element in the array??
	scores[2] = 27;
	scores[3] = 24;
	scores[4] = 19;
	*/


	float scores[5]; // declaration ....

	// create an input file stream
	ifstream in = ifstream("data.txt");
	for (int i = 0; i < 5; i++) {
		in >> scores[i]; // access
	}
	//  0   1   2 3 4
	// [24][19][][][]


	// 0, 1, 2, 3, 4, stop on 5.
	for (int i = 0; i < 5; i++) {
		cout << "score " << i << ": " << scores[i] << endl;
	}

	// calculate average
	float sum = 0;
	for (int i = 0; i < 5; i++) {
		sum += scores[i];
	}
	float average = sum / 5;
	cout << "avg: " << average << endl;

	// calculate relative to average
	float avgDiffs[5];
	for (int i = 0; i < 5; i++) {
		//avgDiffs[0] = scores[0] - average;
		//x = y - 35;
		//[float] = [float] - 35;
		avgDiffs[i] = scores[i] - average;
	}

	for (int i = 0; i < 5; i++) {
		cout << "score for Game " << i + 1 << " comp avg: " << avgDiffs[i] << endl;
	}
	

	/*
	float score1;
	float score2;
	float score3;
	float score4;
	float score5;

	cout << "Please enter a number: ";
	cin >> score1;
	cout << "Please enter a number: ";
	cin >> score2;
	cout << "Please enter a number: ";
	cin >> score3;
	cout << "Please enter a number: ";
	cin >> score4;
	cout << "Please enter a number: ";
	cin >> score5;

	float sum = score1 + score2 + score3 + score4 + score5;
	float average = sum / 5;

	cout << "Avg: " << average << endl;

	cout << "score 1 comp avg: " << score1 - average << endl;
	cout << "score 2 comp avg: " << score2 - average << endl;
	cout << "score 3 comp avg: " << score3 - average << endl;
	cout << "score 4 comp avg: " << score4 - average << endl;
	cout << "score 5 comp avg: " << score5 - average << endl;
	*/



	/*
	// average of a few numbers
	float sum = 0;
	float inValue = 0;
	for (int i = 0; i < 5; i++) {
		cout << "Please enter a number: ";
		cin >> inValue;
		sum += inValue;
	}
	float average = sum / 5;
	cout << "Avg: " << average << endl;
	*/


	// ... 



	return 0;
}