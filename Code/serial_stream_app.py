import serial
import os
from datetime import datetime
from serial.tools.list_ports import comports

baud_possibilities = [50, 75, 110, 134, 150, 200, 300, 600, 1200,
                      1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]

last_com_port = "COM8"
last_baud_rate = int(115200)
last_file_name = "MAXM86161_Data"
# last_save_place = os.path.dirname(__file__)
last_save_place = "C:/Users/kawoo/OneDrive/Documents/Woog School/Western/Software"


def select_port():
    global last_com_port
    if comports():
        print("Default Port:", last_com_port)
        list_ports = []
        print("Available COM Ports:")
        for avail_port in comports():
            print(avail_port)
            list_ports.append(str(avail_port))
        print()
        print("Press Enter for default.")
        port_num = input("Otherwise, enter port number: ")
        if not port_num:
            port_full = last_com_port
        else:
            port_full = "COM" + port_num
            last_com_port = port_full
        print("Selected", port_full)
        print()

        for open_port in list_ports:
            if port_full in open_port:
                return True, port_full

        input("Selected port not in list. Hit enter and try again.")
        print()
        return False, ""
    else:
        print("No COM Ports Available")
        _ = input("Please hit return and try again.")
        print()
        return False, ""


def set_baud_rate():
    global last_baud_rate
    print("Default Baud Rate: ", last_baud_rate)
    print("Possible Baud Rates:")
    print(baud_possibilities)
    print("Press enter for default")
    baud_input = input("Otherwise, select a baud rate: ")
    if not baud_input:
        baud_input = last_baud_rate
    else:
        baud_input = int(baud_input)
        last_baud_rate = baud_input
    if baud_input in baud_possibilities:
        print("Selected ", baud_input)
        print()
        return True, baud_input
    else:
        input("Selected baud not in list. Hit enter to try again.")
        return False, 9600


def print_opening_message():
    print("*" * 30)
    print("Reading Serial Port")
    print("*" * 29, "*\n\n\n")


def save_data_choice():
    choice = input("Enter 'Y' to save data:")
    if choice == "y" or choice == "Y":
        print("Saving Data")
        print()
        return True
    else:
        print("Not saving data")
        print()
        return False


def set_up_save():
    global last_save_place
    global last_file_name
    print("Save file location:", last_save_place)

    location_change = input("Enter 'Y' to change location:")
    if location_change == "y" or location_change == "Y":
        save_location = choose_save_location()
        last_save_place = save_location
    else:
        save_location = last_save_place

    print("Save file name:", last_file_name)
    date_string = str(datetime.now().strftime("_%Y_%m_%d_%H_%M_%S")) + ".csv"
    print("With date:", date_string)

    name_change = input("Enter 'Y' to change name:")
    if name_change == "y" or name_change == "Y":
        new_file_name = input("Enter new file name: ")
        last_file_name = new_file_name
    else:
        new_file_name = last_file_name

    new_file_name = new_file_name + date_string
    print("Creating File: ", new_file_name)

    full_file_name = os.path.join(save_location, new_file_name)

    # open the file to save the output to
    file = open(full_file_name, "w+")

    header_text = "Red,Green,IR,Force,Time"
    # Write the header information
    file.write(header_text + "\n")
    return file


def choose_save_location():
    global last_save_place
    directory_search = True
    current = os.path.dirname(last_save_place)
    default = os.path.dirname(last_save_place)
    print()
    print("Press Enter to set location")
    while directory_search:
        files = [name for name in os.listdir(current) if
                 os.path.isdir(os.path.join(current, name))]
        print("Current path:")
        print(current)
        print("Folders: ", files)
        addition = input("Please enter file name: ")
        if addition:
            current = os.path.join(current, addition)
            print()
        else:
            directory_search = False

        if not os.path.exists(current):
            print("This directory does not exist.")
            create = input("Do you want to create this directory? Y or N :")
            if create == "Y" or create == "y":
                print("Creating directory")
                os.makedirs(current)
                print(current)
                print()
            else:
                print("Location not created, resorting to default.")
                print(default)
                print()
                current = default
                directory_search = False

    return current


def main():

    # Initialize a serial port object
    serial_port = serial.Serial(timeout=1)

    # Select the port to use
    port_selection = False
    while not port_selection:
        port_selection, serial_port.port = select_port()

    # Select the baud rate to use
    baud_selection = False
    while not baud_selection:
        baud_selection, serial_port.baudrate = set_baud_rate()

    save = save_data_choice()
    if save:
        f = set_up_save()

    print("Opening Serial Port")
    serial_port.open()

    if serial_port.isOpen():
        print(serial_port.name, "serial is open! \n")
        print_opening_message()
        serial_port.flushInput()
    else:
        print("Serial Port is not open.")

    while True:
        try:
            line = serial_port.readline().strip().decode()  # read a byte string
            # print(line, (time.time_ns() - start_time))
            if line:
                # pass
                print(line)
                if save:
                    f.write(line)
                    f.write("\n")

        except KeyboardInterrupt:
            print("Keyboard Interrupt")
            break

        except Exception as e:
            print(f"Error: {str(e)}")
            break

    if not (serial_port is None):
        serial_port.close()
        print("Disconnecting Serial")

    print("No Connection\n")
    print("Serial Communication Closed\n\n\n")


if __name__ == "__main__":
    while True:
        main()
