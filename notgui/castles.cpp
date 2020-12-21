#include <iostream> 
#include <iomanip>
#include <vector>
#include <deque> 
#include <stack> 
#include <algorithm> 
#include <ofstream> 
#include <ostream> 
#include <fstream> 
using namespace std; 

class game{
private: 
    int numPlayers; 
    int numHP; 
    int numCP; 
    struct room(){
        int points; 
        int entrances; 
        int attachVal; 
        string name; 
        char type;
        vector<char> colors; 
    }; 
    // includes all of the rooms being used 
    deque<room> p100; 
    deque<room> p150; 
    deque<room> p200; 
    deque<room> p250; 
    deque<room> p350; 
    deque<room> p350; 
    deque<room> p400; 
    deque<room> p450; 
    deque<room> p500; 
    deque<room> p600; 
    stack<room> displayRooms; 

public: 
    vector<room> readIn(int roomSize){
        // NAME_TYPE_POINTS_ENTRANCES_ATTACHVAL_NUMATTACH_COLORS
        ostream f(roomSize + ".txt"); 
        string junk; 
        f >> junk; 
        vector<room> temp; 
        int numRooms = 9; 
        if(roomSize > 300){
            numRooms = 6; 
        }
        temp.resize(numRooms); 
        string numHundredRooms; 
        for(int i = 0; i < numHundredRooms; ++i){
            string text; 
            int in; 
            f >> text; 
            temp[i].name = text; 
            f >> text; 
            char tmp = text[0]; 
            temp[i].type = tmp; 
            f >> in; 
            temp[i].points = in; 
            f >> in; 
            temp[i].entrances = in; 
            f >> in;  
            temp[i].attachVal = in; 
            f >> in; 
            temp[i].colors.resize(in); 
            for(int p = 0; p < in; ++p){
                f >> text; 
                char t = text[0]; 
                colors[p] = t; 
            }
        }
        return temp; 
    }
    room genRoom(){
        int num; 
        num = rand % 10; 
        switch(num){
            case '0'{
                return p100.front(); 
            }
            case '1'{
                return p150.front(); 
            }
            case '2'{
                return p200.front(); 
            }
            case '3'{
                return p250.front(); 
            }
            case '4'{
                return p300.front(); 
            }
            case '5'{
                return p350.front(); 
            }
            case '6'{
                return p400.front(); 
            }
            case '7'{
                return p450.front(); 
            }
            case '8'{
                return p500.front(); 
            }
            case '9'{
                return p600.front(); 
            }

        }
    }
    void cmndLine (int argc, char** argv){
        // ./castles -p/players 1/2/3/4 -c/computer 1/2/3/4 -h/human 1/2/3/4 
            int option_index = 0;
             int gotopts = 0;
            opterr = false;
            struct option longopts[] =
            {
                {"computer", required_argument, nullptr, 'c'},
                {"human", required_argument, nullptr, 'h'},
                {"players", required_argument, nullptr, 'p'},
                {nullptr, 0, nullptr, '\0'}
            };
            while ((gotopts = getopt_long(argc,argv, "c:h:p:", longopts, &option_index)) != -1){
                switch(gotopts) {
                        case 'p' : {
                            if (*optarg == '1'){
                                numPlayers = 1;  
                            }
                            if (*optarg == '2'){
                                numPlayers = 2; 
                            }
                            if(*optarg == '3'){
                                numPlayers = 3; 
                            }
                            if(*optarg == '4'){
                                numPlayers = 4; 
                            }
                            else{
                                cerr << " invalid output " << '\n';
                                exit(1);
                            }
                            break;
                        } // case end 
                          case 'c' : {
                            if (*optarg == '1'){
                                numCP = 1;  
                            }
                            if (*optarg == '2'){
                                numCP = 2; 
                            }
                            if(*optarg == '3'){
                                numCP = 3; 
                            }
                            if(*optarg == '4'){
                                numCP = 4; 
                            }
                            else{
                                cerr << " invalid output " << '\n';
                                exit(1);
                            }
                            break;
                        } // case end 
                         case 'h' : {
                            if (*optarg == '1'){
                                numHP = 1;  
                            }
                            if (*optarg == '2'){
                                numHP = 2; 
                            }
                            if(*optarg == '3'){
                                numHP = 3; 
                            }
                            if(*optarg == '4'){
                                numHP = 4; 
                            }
                            else{
                                cerr << " invalid output " << '\n';
                                exit(1);
                            }
                            break;
                        } // case end 

                }
                
        }
         if((numHP + numCP) > numPlayers){
            cout << "Too many human/computer players"
            exit(1); 
        } //if end 
        }// cmndline funct end 

}; // end class 



