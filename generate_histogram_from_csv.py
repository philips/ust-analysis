
import pandas as pd
import matplotlib.pyplot as plt

# Load the UST facilities and violations CSV files
facilities_df = pd.read_csv('USTFacilitiesZip.csv', encoding='ISO-8859-1')
violations_df = pd.read_csv('tanks.csv', encoding='ISO-8859-1')

# Dropping the irrelevant first few rows and renaming columns for the facilities dataframe
facilities_df_cleaned = facilities_df.iloc[3:].reset_index(drop=True)
facilities_df_cleaned.columns = ['Facility_ID', 'Facility_Name', 'Address', 'City', 'Zip', 'Phone', 'Permittee', 
                                 'All_Tanks', 'Active_Tanks', 'Decomm_Tanks', 'Permit_Tanks']
facilities_df_cleaned['Facility_ID'] = pd.to_numeric(facilities_df_cleaned['Facility_ID'], errors='coerce')

# Convert inspection start dates and extract the year for analysis
violations_df['InspectionStartDate'] = pd.to_datetime(violations_df['InspectionStartDate'], errors='coerce')
violations_df['InspectionYear'] = violations_df['InspectionStartDate'].dt.year

# Group by Facility_ID and count distinct years they had violations
facility_violation_years = violations_df.groupby('Facility_ID')['InspectionYear'].nunique().reset_index(name='DistinctViolationYears')

# Create bins to categorize facilities by how many years (1-5) they had violations
bins = [0, 1, 2, 3, 4, 5]
labels = ['1 of 5 years', '2 of 5 years', '3 of 5 years', '4 of 5 years', '5 of 5 years']
facility_violation_years['ViolationFrequency'] = pd.cut(facility_violation_years['DistinctViolationYears'], bins=bins, labels=labels, right=True)

# Create a histogram of the counts
violation_frequency_counts = facility_violation_years['ViolationFrequency'].value_counts().sort_index()

# Save the histogram data to a CSV file
violation_frequency_counts.to_csv('violation_frequency_histogram.csv')

# Optionally, plot the histogram
plt.figure(figsize=(10, 6))
violation_frequency_counts.plot(kind='bar')
plt.title('Frequency of Violations Across 5 Years')
plt.xlabel('Years with Violations')
plt.ylabel('Number of Facilities')
plt.xticks(rotation=0)
plt.show()
