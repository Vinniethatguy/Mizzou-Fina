import sys, csv, itertools

def get_seating_costs():
    seat_matrix = [[300, 200, 100, 200, 300] for row in range(10)]
    return seat_matrix

def load_credentials():
    try:
        with open("admins.txt", "r") as creds_file:
            pairs = map(lambda line: line.split(':'), creds_file.read().split())
            creds = dict()
            for pair in pairs:
                creds[pair[0]] = pair[1]
            
            return creds
    except:
        print("Error: Couldn't read admin credentials!")
        sys.exit(1)

def load_reservations():
    try:
        reservations = [[None for _ in range(5)] for _ in range(10)] 
        with open("reservation.txt", "r") as reservationFile:
            reader = csv.reader(reservationFile)
            for row, seat, firstname, lastname, code in reader:
                rowIndex = int(row)
                seatIndex = int(seat)
                reservations[rowIndex-1][seatIndex-1] = {
                    "first_name": firstname,
                    "last_name": lastname,
                    "code": code,
                    "seat": seat,
                    "row": row
                }
            return reservations
    except:
        print("Error: Couldn't read reservation data!")
        sys.exit(1)


class ReservationSystem:    
    def __init__(self):
        self.credentials = load_credentials()
        self.reservations = load_reservations()

        print('       Mizzou IT Airlines      ')
        print('-------------------------------')

        while True:
            print('1. Administrator Log-In Portal ')
            print('2. Make a Reservation          ')
            print('3. Close Application         \n')

            # We do this trick because python will sometimes 
            # bug and display the input() text before
            # previously called print()s are displayed

            print('What would you like to do? ', end='')

            choice = input('').strip() 

            while not choice in ['1', '2', '3']:
                print('ERROR: Not a valid selection! Select one of 1, 2, or 3\n')

                print('What would you like to do? ', end='')
                choice = input('').strip()
            
            if choice == '1':
                self.admin_dialogue()
            elif choice == '2':
                self.reservation_dialogue()
            else:
                # last option remaining - exit
                break

        print("Thank you for choosing Mizzou IT Airlines")
        print('')

    def reservation_dialogue(self):
        print('')
        print('       Make a Reservation      ')
        print('-------------------------------')
        print('')

        print('Enter Passenger First Name: ', end='')
        first_name = input('').strip()
        print('Enter Passenger Last Name: ', end='')
        last_name = input('').strip()

        while first_name == '' or last_name == '':
            print('Error: Name must not be empty')
            print('')

            print('Enter Passenger First Name: ', end='')
            first_name = input('').strip()
            print('Enter Passenger Last Name: ', end='')
            last_name = input('').strip()

        print('')
        print('Printing the Seating Chart...') 
        self.print_reservations()
        print('')

        row = 0

        while True:
            while True:
                print('Which row would you like to sit in? ', end='')
                row = input('').rstrip()
                try:
                    row = int(row)
                    if row < 1 or row > 10:
                        print("Error: Row must be between 1-10")
                        print('')
                        continue
                    else:
                        break
                except:
                    print('Error: Row must be a number')
                    print('')
            print('')

            seat = 0

            while True:
                print('Which seat would you like to sit in? ', end='')
                seat = input('').rstrip()
                try:
                    seat = int(seat)
                    if seat < 1 or seat > 5:
                        print("Error: Seat must be between 1-5")
                        print('')
                        continue
                    else:
                        break
                except:
                    print('Error: Seat must be a number')
                    print('')
            print('')

            if self.reservations[row-1][seat-1] != None:
                print(f"Row:{row} Seat:{seat} is not available. Please choose another row and seat")
                print('')
            else:
                code = self.confirmation_code(first_name)

                self.reservations[row-1][seat-1] = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "code": code,
                    "seat": seat,
                    "row": row
                }

                self.save_reservations()

                print("Printing the Flight Map...")
                self.print_reservations()

                print(f"Congratulations {first_name} {last_name}!")
                print(f"Your reservation for seat {seat} in row {row} has been placed.")
                print(f"Your confirmation code is {code}")
                print('')
                break
            

    def admin_dialogue(self):
        print('')
        print('   Administrator Login Portal  ')
        print('-------------------------------')
        print('')

        print("Enter Username: ", end='')
        user = input('').strip()
        print("Enter Password: ", end='')
        passw = input('').strip()

        while user not in self.credentials or self.credentials[user] != passw:
            print('Error: Invalid username/password combination\n')

            print("Enter Username: ", end='')
            user = input('').strip()
            print("Enter Password: ", end='')
            passw = input('').strip()
        
        print('')
        print('Printing the Seating Chart...')
        self.print_reservations()

        print(f"Total sales: ${self.calculate_revenue()}")
        print("You are logged out now!\n")

    def print_reservations(self):
        for row in self.reservations:
            print(['X' if taken else 'O' for taken in row])

    def save_reservations(self):
        try:
            with open("reservation.txt", "w") as file:
                # row, seat, first_name, last_name, code
                for row in self.reservations:
                    for seat in row:
                        if seat != None:
                            file.write(f"{str(seat['row'])},{int(seat['seat'])},{seat['first_name']},{seat['last_name']},{seat['code']}\n")

        except:
            print("Error saving reservations to file")
            sys.exit(1)
    
    def calculate_revenue(self):
        total = 0
        costs = get_seating_costs()
        for i in range(10):
            for j in range(5):
                if self.reservations[i][j] != None:
                    total += costs[i][j]
        return total

    def confirmation_code(self, name):
        result = ""
        for pair in itertools.zip_longest(name, "INFOTC1040"):
            result += pair[0] if pair[0] else ''
            result += pair[1] if pair[1] else ''
        return result


if __name__ == "__main__":
    # Using an object to manage internal state
    # instead of globals
    ReservationSystem()