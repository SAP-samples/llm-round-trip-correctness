import pandas as pd

# Your JSON data
data = {
    "5_2.txt": {
        "0": [
            0.95,
            0.975,
            0.5504406336794562,
            0.5238365800865801
        ],
        "1": [
            0.92,
            0.6028571428571429,
            0.6663569972416707,
            0.6359432234432234
        ],
        "2": [
            0.91,
            0.5383333333333333,
            0.642523256341066,
            0.6376068376068376
        ]
    },
    "10_13.txt": {
        "0": [
            0.8,
            0.525,
            0.4421119592875319,
            0.49166666666666664
        ],
        "1": [
            0.83,
            0.4983333333333333,
            0.5413910093299407,
            0.5555555555555556
        ],
        "2": [
            0.82,
            0.51,
            0.28897227092811584,
            0.3415704665704666
        ]
    }
}

# Create an Excel writer object
with pd.ExcelWriter('iter_results/output_separate_sheets.xlsx', engine='openpyxl') as writer:

    # Loop over keys (0, 1, 2) and collect the data for each key in all files
    for key in range(3):
        # Collect the data for this key across all files
        combined_data = []
        for file_name, values in data.items():
            combined_data.append([file_name, key] + values[str(key)])

        print(combined_data)
        # Create a DataFrame for the collected data
        df = pd.DataFrame(combined_data, columns=['File Name', 'Key', 'Value 1', 'Value 2', 'Value 3', 'Value 4'])

        # Write the DataFrame to the corresponding sheet
        df.to_excel(writer, sheet_name=f'Key {key}', index=False)

print("Excel file saved as 'output_separate_sheets.xlsx'")
