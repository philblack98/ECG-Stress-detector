import board
import analogio
import time
import usb_cdc

# Setup the ADC on a specific pin (adjust according to your setup)
adc = analogio.AnalogIn(board.GP27)

# Function to read the ECG value
def read_ecg():
    ecg_value = adc.value  # Read the ADC value
    voltage = (ecg_value / 65535.0) * 3.3  # Convert to voltage assuming 3.3V reference
    voltage = voltage*1000	#convert to millivolts
    return voltage

# Enable the serial connection over USB
serial = usb_cdc.data

# Calculate delay for 250 Hz sampling rate
sampling_period = 1 /250 # This calculates to 0.004 seconds or 4 milliseconds

# Main loop to send ECG values over serial
while True:
    start_time = time.monotonic()  # Get the current time
    ecg_voltage = read_ecg()
    serial.write(f"{ecg_voltage}\n".encode())  # Encode the string to bytes and write to serial
    print(ecg_voltage)  # Optional: print voltage for debugging

    # Calculate the time it took to execute the read and send operations
    elapsed_time = time.monotonic() - start_time
    
    # Sleep the remainder of the sampling period if any
    if elapsed_time < sampling_period:
        time.sleep(sampling_period - elapsed_time)
