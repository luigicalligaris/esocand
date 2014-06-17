// Estrazione a SOrte dei CANDidati (ESoCand)
// Copyright (C) 2014  Luigi Calligaris
// 
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation; either version 3 of the License, or
// (at your option) any later version.
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
// You should have received a copy of the GNU General Public License
// along with this program, in the file named LICENCE; if not, write 
// to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, 
// Boston, MA 02110-1301  USA

#include <iostream>
#include <iomanip>
#include <string>
#include <sstream>
#include <vector>
#include <iterator>
#include <random>
#include <algorithm>
#include <functional>

static const char* PROGRAM_VERSION = "0.1a";

static const char* LICENCE_NOTICE = 
"**************************************************\n"
"* Estrazione a SOrte dei CANDidati (ESoCand)     *\n"
"* Copyright (C) 2014  Luigi Calligaris           *\n"
"* Released under the terms of the GNU General    *\n"
"* Public Licence v3, see documentation  included *\n"
"* in this package.                               *\n"
"**************************************************";




int main(int argc, char* argv[])
{
	using namespace std;
	
	cout << LICENCE_NOTICE << endl;
	cout << "ESoCand version " << PROGRAM_VERSION << endl;
	
	
	// Get rng seed
	
	string rngseed_input_string;
	cout << "Introdurre il seed del generatore casuale [default stringa vuota]: ";
	getline(cin,rngseed_input_string);
	
	
	// Get candidate names
	
	vector<string> candidate_names_asinput;
	cout << "Introdurre linea per linea i nomi di ciascuno dei candidati, terminando ogni linea con il tasto Invio/Enter.\n"
	"Per terminare l'introduzione dei candidati, inserire una linea vuota." << endl;
	
	while (true)
	{
		cout << "Nome candidato " << setw(4) << right << candidate_names_asinput.size() + 1 << ") ";
		string candidate_name;
		getline(cin,candidate_name);
		
		if (candidate_name != "")
			candidate_names_asinput.push_back(candidate_name);
		else
			break;
	}
	
	
	// Sort the candidate names vector
	
	vector<string> candidate_names_sorted = candidate_names_asinput;
	sort(candidate_names_sorted.begin(), candidate_names_sorted.end());
	
	
	// Generate a random seed based on the one given as input and on the candidate names
	
	std::ostringstream  candidate_names_sorted_merged;
	const char* const candidate_names_sorted_merged_separator = ";";
	copy(candidate_names_sorted.begin(), candidate_names_sorted.end(), ostream_iterator<string>(candidate_names_sorted_merged, candidate_names_sorted_merged_separator));
	
	string rngseed_string(rngseed_input_string + candidate_names_sorted_merged_separator + candidate_names_sorted_merged.str());
	
	mt19937 rng( hash<std::string>()(rngseed_string) );
	
	vector<string> candidate_names_randomized = candidate_names_sorted;
	shuffle(candidate_names_randomized.begin(), candidate_names_randomized.end(), rng);
	
	
	cout << endl;
	cout << "*** ESTRAZIONE COMPLETATA ***" << endl;
	cout << "ESoCand version " << PROGRAM_VERSION << endl;
	
	cout << "Hai scelto il seguente seed di randomizzazione: \"" << rngseed_input_string << "\"" << endl;
	
	cout << "Questa e' la lista dei candidati, ordinata per come li hai inseriti:" << endl;
	for (size_t i = 0, iEnd = candidate_names_asinput.size(); i != iEnd; ++i)
	{
		cout << "--> Lista nomi inserita, candidato " << setw(4) << right << i + 1 << ") \"" << candidate_names_asinput[i] << "\"" << endl;
	}
	
	cout << "Questa e' la lista dei candidati, ordinata per lunghezza/ordine ASCII:" << endl;
	for (size_t i = 0, iEnd = candidate_names_sorted.size(); i != iEnd; ++i)
	{
		cout << "--> Lista nomi ordinata, candidato " << setw(4) << right << i + 1 << ") \"" << candidate_names_sorted[i] << "\"" << endl;
	}
	
	cout << "Questa e' la lista dei candidati, estratta a sorte:" << endl;
	for (size_t i = 0, iEnd = candidate_names_randomized.size(); i != iEnd; ++i)
	{
		cout << "--> Lista nomi sorteggiata, candidato " << setw(4) << right << i + 1 << ") \"" << candidate_names_randomized[i] << "\"" << endl;
	}
	
	return 0;
}