import serial

def read_serial(port, baudrate):
    ser = serial.Serial(port, baudrate)
    try:
        while True:
            if ser.in_waiting > 0:
                data=("50,20,70,90,10,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0")
                #data = ser.readline().decode('utf-8').rstrip()
                values = data.split(',')
                if len(values) == 22:  # Ensure there are exactly 22 values
                    sliders = [int(values[i]) for i in range(5)]
                    buttons = [int(values[i]) for i in range(5, 21)]
                    master = int(values[21])
                    print(f"Sliders: {sliders}, Buttons: {buttons}, Master: {master}")
                
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        ser.close()

if __name__ == "__main__":
    read_serial('COM11', 9600)