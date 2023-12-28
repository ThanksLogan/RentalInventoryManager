# Rental Inventory Manager
## Description: 
This Rental Inventory Manager is a comprehensive GUI application designed to streamline the management of rental inventory, particularly for furniture and event supplies. This tool offers an intuitive user interface for tracking inventory items, managing bookings, and organizing rental packages. The management tools can prevent common inventory management mishaps like overbooking items for a particular day, and displaying the correct number of items available for rent.

Modeled for furniture rental business, [Event Lounge Co.](https://www.eventlounge.co/lounge-furniture.html)
## Features
**Inventory Management:** Track and manage various inventory items, including furniture, electronics, and other rental equipment.

**Package Configurations:** Create and manage pre-defined rental packages for events.

**Booking System:** Handle customer bookings, including date ranges, item quantities, and pricing.

**Availability Checker:** Check the availability of individual items and packages for specific dates.

**User Authentication:** Secure login system for different user roles.

**More TBD**

## Get Started
### Prerequisites for Usage
+ Python 3.8 or higher
+ PyQt5
+ SQLite3 (recommended)

### Installation
Clone the repository:
```
git clone https://github.com/thankslogan/rental-inventory-manager.git
```

Navigate to the project directory:
```
cd rental-inventory-manager
```
### Running the Applicatiion
Execute main:
```
python3 main.py
```

## Walkthrough of usage:

### Logging In: 

Username: ```admin```

Password: ```password```

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/f327690f-7eb7-4842-a1b4-54f425011ea4" width="690" height="396">

****

### Select Dates to Book Rental & Check Availability:

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/088266c3-14ef-438c-a2f4-f64021e933af" width="690" height="396">

****

### Choose Items to Add to Booking for Specified Day and See Possible Conflicting Bookings:

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/cbe8bf0d-1980-4dd1-a228-3e9ecc2f193f" width="690" height="396">

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/b892e9e0-d359-448c-9373-c069699f591d" width="690" height="396">

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/40ba9e54-7bda-412d-b2f7-2a9aee476a8d" width="690" height="420">

****

### Finalize Booking Details by Filling out Booking Details 

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/7d7370d4-4b8c-4299-980c-167e4fbf0abb" width="848" height="477">

****

### Export Details to Rental Agreement HTML+CSS Template, to be Saved Locally 

<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/a4d141cd-0163-4b04-9708-1a9ba05c2f0d" width="690" height="396">

![image](https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/67153bcf-8e94-41ca-91bf-1b13d4095e77)

****

### SQLite Studio - Tables and Example Bookings Inside Database:
<img src="https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/ac7c25b3-3d41-44aa-a295-aac4d0a1d0f6" width="690" height="396">

![image](https://github.com/ThanksLogan/RentalInventoryManager/assets/89110766/2e9e41bd-a090-4e25-8540-3e79b7c7c933)


****

## Acknowledgements
Author: Myself 🤓

**Built with:**
+ QTDesigner 5.15.2 for building GUI template
+ SQLiteStudio 3.4.4 for database verification
+ Additional tools include: PyQt libraries and Pip libraries
