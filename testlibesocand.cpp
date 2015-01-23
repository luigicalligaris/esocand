#include "libesocand.hpp"

#include <iostream>
#include <string>
#include <vector>

int main (int argc, char* argv[])
{
	std::vector<std::string> testVec;
	testVec.push_back(std::string("foxtrot"        ));
	testVec.push_back(std::string("bravo"          ));
	testVec.push_back(std::string("alpha"          ));
	testVec.push_back(std::string("delta"          ));
	testVec.push_back(std::string("charlie"        ));
	testVec.push_back(std::string("echo"           ));
	
	
	std::cout << "Test vector before shuffling:" << std::endl;
	std::cout << "[";
	for (std::string& s : testVec)
	{
		std::cout << "\"" << s << "\",";
	}
	std::cout << "]" << std::endl;
	
	
	const std::string seed_string = "FOO BAR";
	std::cout << "Seed string for shuffler: " << seed_string << std::endl;
	esocand::EsocandShuffler shuffler(seed_string);
	
	std::vector<std::string> shuffledVec = shuffler.GetShuffledCopy(testVec);
	
	std::cout << "Test vector after shuffling:" << std::endl;
	std::cout << "[";
	for (std::string& s : shuffledVec)
	{
		std::cout << "\"" << s << "\",";
	}
	std::cout << "]" << std::endl;
	
// 	int u = std::lexical_cast<int>(std::string("100"));
// 	std::cout << u << std::endl;
	
	return 0;
}