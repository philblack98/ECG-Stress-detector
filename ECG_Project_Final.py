import serial
import time
import pandas as pd
import serial.tools.list_ports
import neurokit2 as nk



#set up connection to port 
ports = serial.tools.list_ports.comports()

for port in ports:
    print(port.device) #gives list of devices connected via serial port  

#Fill in the port 
ser = serial.Serial('/dev/cu.usbmodem11103', 2000000, timeout=5)

#debug: is there data
if ser.in_waiting > 0:
    print("There is data waiting to be read.")
else:
    print("There is no data waiting to be read.")

#Calibrate thresholds 

# Setup serial connection (replace 'COM_PORT' with the actual port)
ser = serial.Serial('/dev/cu.usbmodem11103', 2000000, timeout=1)

# Get the start time
start_time1 = time.time()

# Set the maximum duration
max_duration1 = 30  # seconds

# List to store the ECG voltage values
data = []

# Main loop to read data from serial
while time.time() - start_time1 < max_duration1:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()  # Read a line and decode it from bytes to string
        print(f"Received ECG Voltage: {line} V")
        # Append the line to the DataFrame
        data.append(float(line))
ser.close()

# Convert list to Pandas DataFrame after collecting all data
dfc = pd.DataFrame(data, columns=['ECG Voltage'])

# Make df numeric 
dfc['ECG Voltage'] = pd.to_numeric(dfc['ECG Voltage'], errors='coerce')
# Process data 
sampling_rate = len(dfc) / max_duration1
dfc_clean = nk.ecg_clean(dfc, sampling_rate=sampling_rate)    
processed_datac, info = nk.ecg_process(dfc_clean, sampling_rate=sampling_rate)
ECG_intervalrelatedc = nk.ecg_intervalrelated(processed_datac, sampling_rate=sampling_rate)
#check Quality 

signal_quality = processed_datac['ECG_Quality']
mean_signal_value = signal_quality.mean()
print(f"Mean Signal Value: {mean_signal_value}")

#set thresholds 
HRC = int(ECG_intervalrelatedc['ECG_Rate_Mean'].iloc[0])
HRVC = int(ECG_intervalrelatedc['HRV_RMSSD'].iloc[0])
HR_threshold = HRC+ 15
HRV_threshold =  HRVC-HRVC*0.25 

#End calibration 
print(HR_threshold)
print(HRV_threshold)
print("Calibration complete")



#Main loop for prorocessing 

while True:
    # Setup serial connection (replace 'COM_PORT' with the actual port)
    ser = serial.Serial('/dev/cu.usbmodem11103', 2000000, timeout=1)

    # Get the start time
    start_time = time.time()

    # Set the maximum duration
    max_duration = 30  # seconds

    # List to store the ECG voltage values
    data = []

    # Main loop to read data from serial
    while time.time() - start_time < max_duration:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Read a line and decode it from bytes to string
            print(f"Received ECG Voltage: {line} V")
            # Append the line to the DataFrame
            data.append(float(line))
    ser.close()

    # Convert list to Pandas DataFrame after collecting all data
    df = pd.DataFrame(data, columns=['ECG Voltage'])


    # Make df numeric 
    df['ECG Voltage'] = pd.to_numeric(df['ECG Voltage'], errors='coerce')
    # Process data 
    sampling_rate = len(df) / max_duration
    df_clean = nk.ecg_clean(df, sampling_rate=sampling_rate)    
    processed_data, info = nk.ecg_process(df_clean, sampling_rate=sampling_rate)
    ECG_intervalrelated = nk.ecg_intervalrelated(processed_data, sampling_rate=sampling_rate)
    #check Quality 

    signal_quality = processed_data['ECG_Quality']
    mean_signal_value = signal_quality.mean()
    print(f"Mean Signal Value: {mean_signal_value}")
    
    HR = int(ECG_intervalrelated['ECG_Rate_Mean'].iloc[0])
    HRV = int(ECG_intervalrelated['HRV_RMSSD'].iloc[0])
    Stress = False

    if mean_signal_value > 0.3:  
        
        # Check if values are within thresholds
        if HR > HR_threshold:
            if HRV < HRV_threshold:
                Stress = True
        else:
            Stress = False

        # Stress detected?
        if Stress == True:
            print('Stress detected')
        else: 
            print('No stress detected')
        # Create a text file to connect to C#
        with open('/Users/philippschwarzmann/Desktop/Master HFE/MyNewProject/stress_state.txt', 'w') as file:
            
            # Write the state of the stress variable to the file
            file.write('Stress: ' + str(Stress))
    else:
        print("Signal quality is too low. Please check the connection.")
    del df
    print(HR)
    print(HRV)

    # Wait for 5 seconds before the next iteration
    time.sleep(20)
