#include <iostream>
#include <map>
#include <unordered_map>
#include <string>
using namespace std;
class BookingsClass {
public:
    BookingsClass();
    bool GetBooking(const string &);
    void SetBooking(const string &, int);
    void parse();
private:
    map< string, int > Inventory;
    map< string, map<string, int> > Packages;
};

BookingsClass::BookingsClass() { //Inventory and Packages
    // merely your example values posted.
    Inventory.insert({"MiniOtto", 18});
    Inventory.insert({"Otto", 12});
    Inventory.insert({"Armless", 8});
    Inventory.insert({"Corner", 4});
    Inventory.insert({"LED", 24});
    Inventory.insert({"Backed", 8});
    Inventory.insert({"FlatBig", 8});
    Inventory.insert({"MiniRectangle", 12});
    Inventory.insert({"LegMini", 8});
    Inventory.insert({"LegOtto", 8});
    Inventory.insert({"LegArmless", 8});
    Inventory.insert({"LegCorner", 4});
    Inventory.insert({"UltraBench", 8});
    Inventory.insert({"UltraSerp", 8});
    Inventory.insert({"UltraRound", 8});


}
void BookingsClass::SetBooking(const string &seat_number, int quantity) {
    Inventory[seat_number] = quantity;
}
bool BookingsClass::GetBooking(const string &seat_number) {
    return Inventory[seat_number];
}
void BookingsClass::parse() {
    map<std::string, int>::iterator it = Inventory.begin();
    while (it != Inventory.end())
    {
        std::string word = it->first;
        int count = it->second;
        std::cout << word << " :: " << count << std::endl;
        it++;
    }
}

int main() {


    // PACKAGES:
    // V298: 4 Ottomans and 2 LEDs
    // AddV298(){ //Must be able to access the inventory map when calling this function
    //      Inventory


    //can we invoke an item with a usage time right here???
    cout << "\nTesting Program\n" <<endl;
    BookingsClass Booking;
    int time[] = {11042022, 1000, 2300}; //december 4[0], 10am[1] to 11pm[2]
    string package = "V2_101"; //For custom order, invoke a method within its class that will create the package custom for you

    //set(package, "Logan F"); //all for now
    Booking.parse();
   // cout << "Here is your newly added Booking -- >  \nDetails: " << Booking.parse() << endl;

    return 0;
}
