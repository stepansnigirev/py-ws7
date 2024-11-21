"""
Script to read a .lta file and extract the time vs frequency data.
Alix Merolle - 1D experiment
"""

import pandas as pd
import numpy as np
import scipy.constants
from scipy.signal import argrelextrema
import matplotlib.pyplot as plt
import datetime
import os

# Path to the .lta file
file_path = 'C:/Users/Curie2.0/Documents/rampa1Hz_6.lta'
current_date = datetime.date.today().isoformat()
current_time = datetime.datetime.now().strftime("%H-%M-%S")
# Creates a folder with the name of the current date if it doesn't already exist
path = os.path.join(r'//leon.lkb.upmc.fr/partages/EQ15B/LEON-15B/DATA/Atoms/2024/GVD/Interf/DATASET', current_date, current_time)
if not os.path.exists(path):
    os.makedirs(path)

# File names for saving data
frequency_file_name = "frequency.npy"
time_frequency_file_name = "time_frequency.npy"
figure_file_name = "frequency_vs_time.svg"

frequency_path = os.path.join(path, frequency_file_name)
time_frequency_path = os.path.join(path, time_frequency_file_name)
figure_path = os.path.join(path, figure_file_name)

# Constants
c = scipy.constants.c
subtract_frequency_thz = 384.230484468
subtract_frequency_ghz = subtract_frequency_thz * 1e3  # Convert THz to GHz

# Open and read the file
with open(file_path, 'r') as file:
    lines = file.readlines()

# Find the [Measurement data] section
start_index = None
for i, line in enumerate(lines):
    if line.startswith('[Measurement data]'):
        start_index = i + 2  # Data starts two lines after this line
        break

# Initialize the list to store values
time_signal_data = []

# If the [Measurement data] section is found, read the data
if start_index is not None:
    data_lines = lines[start_index:]
    
    # Create a DataFrame from the data lines
    data = [line.strip().split('\t') for line in data_lines]
    
    # Check if the file has headers and data lines
    if len(data) > 1:
        # Create DataFrame with the first row as header
        df = pd.DataFrame(data[1:], columns=data[0])
        df.columns = ['Time [ms]', 'Signal 1 Wavelength [nm]']
        
        # Convert columns to appropriate types
        df['Time [ms]'] = df['Time [ms]'].astype(float)
        df['Signal 1 Wavelength [nm]'] = df['Signal 1 Wavelength [nm]'].astype(float)

        # Convert wavelength [nm] to frequency [GHz]
        df['Signal 1 Frequency [GHz]'] = (c / (df['Signal 1 Wavelength [nm]'] * 1e-9)) * 1e-9
        
        # Subtract the specified frequency
        df['Signal 1 Frequency [GHz]'] -= subtract_frequency_ghz
        
        # Drop the 'Signal 1 Wavelength [nm]' column
        df = df[['Time [ms]', 'Signal 1 Frequency [GHz]']]
        
        # Store the data in the list
        time_signal_data = df.values.tolist()

        # Convert list back to DataFrame for processing
        df_processed = pd.DataFrame(time_signal_data, columns=['Time [ms]', 'Signal 1 Frequency [GHz]'])

        # Print the original data
        print("Original data:")
        print(df_processed.to_string(index=False, header=False))

        # Find the index of the global minimum value in frequency
        min_index = df_processed['Signal 1 Frequency [GHz]'].idxmin()
        print(f"Index of minimum frequency value: {min_index}")

        # Find all local maxima in frequency
        maxima_indices = argrelextrema(df_processed['Signal 1 Frequency [GHz]'].values, np.greater)[0]
        print(f"Indices of local maxima: {maxima_indices}")

        # Find the first local maximum index after the global minimum
        maxima_after_min = maxima_indices[maxima_indices > min_index]

        if len(maxima_after_min) > 0:
            first_max_index = maxima_after_min[0]
            
            # Select data between the minimum and the first maximum
            new_data = df_processed.iloc[min_index:first_max_index+1].copy()
            
            # Reset time to zero at the minimum frequency
            new_data['Time [ms]'] -= new_data['Time [ms]'].iloc[0]
            
            # Save the adjusted frequency data
            np.save(frequency_path, new_data['Signal 1 Frequency [GHz]'].values)
            
            # Save the time and frequency data together
            np.save(time_frequency_path, new_data.values)
            
            # Print the selected and adjusted data
            print("\nData between minimum and first local maximum (time reset to zero at minimum):")
            print(new_data.to_string(index=False, header=False))

            # Plot the data
            plt.figure(figsize=(12, 6))
            plt.plot(new_data['Time [ms]'], new_data['Signal 1 Frequency [GHz]'], label='Frequency vs Time (Adjusted)')
            plt.axvline(x=0, color='r', linestyle='--', label='Global Minimum (Time = 0)')
            plt.axvline(x=new_data['Time [ms]'].iloc[-1], color='g', linestyle='--', label='First Local Maximum')

            plt.xlabel('Time [ms]')
            plt.ylabel('Frequency [GHz]')
            plt.title('Frequency vs Time (Adjusted)')
            plt.legend()
            plt.grid(True)
            
            # Save the figure
            plt.savefig(figure_path)
            
            # Show the plot
            plt.show()
        else:
            print("No local maxima found after the minimum.")
    else:
        print("Data is missing or poorly formatted.")
else:
    print("Section [Measurement data] not found in the file.")
