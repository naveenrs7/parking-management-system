import time


spaces = []
avail_spaces = 0
total_spaces = 0
rows = 0


space_count = 0
border = ""


class Vehicle:
    def __init__(self, v_type, plate):
        self.type = v_type
        self.plate = plate
        self.entry_time = time.time()

   
    def get_type(self):
        return self.type


    def get_type_string(self):
        # return "Car" if self.type == 1 else "Truck" if self.type == 2 else "Motorcycle"
        if self.type == 1:
            return "Car"
        elif self.type == 2:
            return "Truck"
        else:
            return "Motorcycle"


    def get_plate(self):
        return self.plate

    def get_entry_time(self):
        return self.entry_time

    
    def set_entry_time(self, new_time):
        self.entry_time = new_time

    def get_vehicle(self):
        return self.type, self.plate, self.entry_time




class Space:
    def __init__(self):
        self.vehicle = None
        self.occupied = False

    def add_vehicle(self, vehicle):
        self.vehicle = vehicle
        self.occupied = True

    def remove_vehicle(self):
        v_exit = self.vehicle
        self.vehicle = None
        self.occupied = False
        return v_exit

    def vehicle_info(self):
        return self.vehicle

    def is_available(self):
        return self.occupied


def print_row(row):
    output = ""
    output += "|"
    for s in range(space_count * row, space_count * (row + 1)):
        if not spaces[s].is_available():
            output += "[ ]"
        else:
            output += "["
            output += "c" if spaces[s].vehicle_info().get_type() == 1 \
                else "t" if spaces[s].vehicle_info().get_type() == 2 \
                else "m"
            output += "]"
        if s < space_count * (row + 1) - 1:
            output += " "
    output += "|"

    return output



def display_lot():
    global spaces, avail_spaces, total_spaces, rows

    
    output = "SPOTS AVAILABLE: " + str(avail_spaces) + "\n"

    output += border

    for row in range(rows):
        output += print_row(row) + "\n"

    output += border
    print(output)



def display_row_selection():
    global spaces, avail_spaces, total_spaces, rows

    
    output = "SPOTS AVAILABLE: " + str(avail_spaces) + "\n"

    output += border
    for row in range(rows):
        output += print_row(row)
        output += " <" + str(row) + ">\n"
    output += border
    print(output)


def display_space_selection(row):
    global spaces, avail_spaces, total_spaces, rows

    output = "VIEWING ROW: " + row + "\n"

    output += border
    output += print_row(int(row)) + "\n"

    output += " "
    for count in range(space_count):
        if count < 10:
            output += "<" + str(count) + "> "
        else:
            output += "<" + str(count) + ">"

    output += "\n"
    output += border
    print(output)

    return space_count



def enter_vehicle(v_type, plate, row, space):
    global spaces, avail_spaces, total_spaces, rows

    
    if avail_spaces == 0:
        display_lot()
        print("Error: No Available Spaces")
        time.sleep(2)
        return

    
    if spaces[(int(row) * space_count) + int(space)].is_available():
        display_space_selection(row)
        print("Error: Vehicle Already In Space")
        time.sleep(2)
        return -1

    
    for uniq in spaces:
        if uniq.is_available():
            if uniq.vehicle_info().get_plate() == plate:
                display_lot()
                print("Error: Vehicle Already In Lot")
                time.sleep(2)
                return


    new_vehicle = Vehicle(v_type, plate)
    spaces[(int(row) * space_count) + int(space)].add_vehicle(new_vehicle)
    avail_spaces -= 1
    # display_lot()
    print("Vehicle Added to Lot!\n"
          "Time Entered: " + str(time.strftime('%I:%M %p \n',
                                               time.localtime(new_vehicle.get_entry_time()))))
    time.sleep(2)

    return new_vehicle



def fare_calculation(vehicle):
    total_time = time.time() - vehicle.get_entry_time()
    if total_time < 3600:
        hours = 1
    else:
        hours = int(total_time / 3600)+1

   
    if vehicle.get_type() == 1:
        rate = hours * 2.50
    elif vehicle.get_type() == 2:
        rate = hours * 3.50
    else:
        rate = hours * 1.00

    ret = "Vehicle Removed!\n" \
          "Your Total Amount for " + "{}".format(hours) + " hour is $" + "{:.2f} \n".format(rate) + "Kindly Pay the Amount \n"

    return ret



def exit_lot(row, space):
    global avail_spaces

    
    if not spaces[(int(row) * space_count) + int(space)].is_available():
        # display_space_selection(row)
        print("Error: No Vehicle In Space \n")
        time.sleep(2)
        return

    removed = spaces[(int(row) * space_count) + int(space)].remove_vehicle()
    avail_spaces += 1

    print(fare_calculation(removed))
    time.sleep(3)



def view_vehicle(row, space):

    
    if not spaces[(int(row) * space_count) + int(space)].is_available():
        print("Error: No Vehicle In Space...Please Enter a Valid Entry \n")
        time.sleep(2)

    
    else:
        vehicle = spaces[(int(row) * space_count) + int(space)].vehicle_info()
        input("Vehicle Type: " + vehicle.get_type_string() + "\n"
                                                             "Plate Number: " + vehicle.get_plate() + "\n"
                                                                                                      "Entry Time: " + str(
            time.strftime('%m-%d-%Y %I:%M %p',
                          time.localtime(vehicle.get_entry_time()))) + "\n"
                                                                       "\nPress Enter to return to menu")



def command_handler(command):
    
    if command == "P" or command == "p":
        if avail_spaces == 0:
            print("There is no Available Spaces...\n"
                  "Kindly wait for others to exit the lot\n"
                  "Thank you for your patience !\n")
            time.sleep(2)
        else:
            while True:
                new_type = input("Enter Vehicle Type:\n"
                                 "1. Car\n"
                                 "2. Truck\n"
                                 "3. Motorcycle\n"
                                 ">")

                if new_type == "1" or new_type == "2" or new_type == "3":
                    break
                else:
                    print("Invalid Entry... Please Enter a Valid Entry \n")
                    time.sleep(1)

            new_plate = input("Enter New Vehicle Plate Number:\n"
                          ">")

        
            ret_val = -1
            while ret_val == -1:
                while True:
                    display_row_selection()
                    row = input("Select Row to Park In:\n"
                                ">")
                    if row.isnumeric():
                        if int(row) < rows:
                            break
                        else:
                            print("Invalid Entry... Please Enter a Valid Entry \n")
                            time.sleep(1)

                while True:
                    display_space_selection(row)
                    space = input("Select Space to Park In:\n"
                                  ">")
                    if space.isnumeric():
                        if int(space) < space_count:
                            break
                        else:
                            print("Invalid Entry... Please Enter a Valid Entry \n")
                            time.sleep(1)

                ret_val = enter_vehicle(int(new_type), new_plate, row, space)

    
    elif command == "E" or command == "e":

        
        while True:
            display_row_selection()
            row = input("Select Row of Vehicle:\n"
                        ">")
            if row.isnumeric():
                if int(row) < rows:
                    break
                else:
                    print("Invalid Entry... Please Enter a Valid Entry \n")
                    time.sleep(1)

        while True:
            display_space_selection(row)
            space = input("Select Space of Vehicle:\n"
                          ">")
            if space.isnumeric():
                if int(space) < space_count:
                    break
                else:
                    print("Invalid Entry... Please Enter a Valid Entry \n")
                    time.sleep(1)
        exit_lot(row, space)

    
    elif command == "V" or command == "v":

        
        while True:
            display_row_selection()
            row = input("Select Row to View:\n"
                        ">")
            if row.isnumeric():
                if int(row) < rows:
                    break
                else:
                    print("Invalid Entry... Please Enter a Valid Entry \n")
                    time.sleep(1)

        while True:
            display_space_selection(row)
            space = input("Select Space to View:\n"
                          ">")
            if space.isnumeric():
                if int(space) < space_count:
                    break
                else:
                    print("Invalid Entry... Please Enter a Valid Entry \n")
                    time.sleep(1)

        view_vehicle(row, space)

    
    elif command == "R" or command == "r":
        input("Current Parking Rates:\n"
              "Cars - $2.50/hour\n"
              "Trucks - $3.50/hour\n"
              "Motorcycles - $1.00/hour\n"
              "\nPress Enter to return to menu")

    
    elif command == "Q" or command == "q":
        return

    
    else:
        print("Error: Invalid Command...Please Enter a Valid Command \n")
        time.sleep(1)



def read_config():
    global spaces, total_spaces, avail_spaces, rows, space_count, border

    config = open('config.txt', 'r')
    while True:
        line = config.readline()
        if line.find("total_spaces") != -1:
            total_spaces = int(line[15:17])
            avail_spaces = total_spaces

        elif line.find("rows") != -1:
            rows = int(line[7:8])

            for i in range(total_spaces):
                spaces.append(Space())

            space_count = int(total_spaces / rows)

            border = "|"
            for i in range(space_count - 1):
                for j in range(4):
                    border += "-"
            border += "---|\n"
            break

    config.close()


def main():

    read_config()

    command = ""
    while command != "Q" and command != "q":
        display_lot()
        print("Please Select An Option:\n"
              "P - Park a Vehicle\n"
              "E - Exit the Lot\n"
              "V - View a Parked Vehicle\n"
              "R - Display Vehicle Rates\n"
              "Q - Quit Application\n")

        command = input(">")
        command_handler(command)

main()

# if __name__ == '__main__':
#
#     main()
