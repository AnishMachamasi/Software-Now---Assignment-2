import os
import csv
from collections import defaultdict

# define seasons 
seasons = {
    'Summer': ['December', 'January', 'February'],
    'Autumn': ['March', 'April', 'May'],
    'Winter': ['June', 'July', 'August'],
    'Spring': ['September', 'October', 'November']
}

# initialize data structures
all_data = []        # store all the data for all stations
station_stats = defaultdict(lambda: {
    'temps': [],
    'max_temp': -float('inf'),   # Max temps
    'min_temp': float('inf'),    # Min temps
    'total_temp': 0,          # Total temps for calculating average
    'count': 0               # Count of temps to calculate average
})
seasonal_temps = defaultdict(lambda: defaultdict(list))

# check the data files from 1986 to 2005
for year in range(1986, 2006):
    filename = f'/Users/gina/Documents/GitHub/Software-Now---Assignment-2/temperature_data/stations_group_{year}.csv'
    if not os.path.exists(filename):
        print(f"Warning: File not found - {filename}")
        continue

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            station_name = row['STATION_NAME']
            lat = float(row['LAT'])
            lon = float(row['LON'])

            # Process monthly tempes
            monthly_temps = []
            for month in ['January', 'February', 'March', 'April', 'May', 'June',
                          'July', 'August', 'September', 'October', 'November', 'December']:
                temp = float(row[month])
                monthly_temps.append(temp)

                # Update stats data
                station_stats[station_name]['temps'].append(temp)
                station_stats[station_name]['max_temp'] = max(station_stats[station_name]['max_temp'], temp)
                station_stats[station_name]['min_temp'] = min(station_stats[station_name]['min_temp'], temp)
                station_stats[station_name]['total_temp'] += temp
                station_stats[station_name]['count'] += 1

                # update tempes data 
                for season, months in seasons.items():
                    if month in months:
                        seasonal_temps[season][station_name].append(temp)
          #store the processed data
            all_data.append({
                'station': station_name,
                'year': year,
                'lat': lat,
                'lon': lon,
                'temps': monthly_temps
            })

# Calculate avg_tempes
seasonal_averages = defaultdict(dict)
for season in seasons:
    for station in seasonal_temps[season]:
        temps = seasonal_temps[season][station]
        seasonal_averages[season][station] = sum(temps) / len(temps)

# Get the avg_tempes
overall_seasonal_averages = {}
for season in seasons:
    all_temps = [] 
    for station_temps in seasonal_temps[season].values():
        all_temps.extend(station_temps)
    if all_temps:
        overall_seasonal_averages[season] = sum(all_temps) / len(all_temps)
    else:
        overall_seasonal_averages[season] = 0

# Save seasonal averages files
with open('average_temp.txt', 'w') as f:
    f.write("Average Temperatures by Season (across all stations and years):\n")
    for season, temp in overall_seasonal_averages.items():
        f.write(f"{season}: {temp:.2f}°C\n")
    
    f.write("\nDetailed Averages by Station:\n")
    for season in seasons:
        f.write(f"\n{season}:\n")
        for station, avg in seasonal_averages[season].items():
            f.write(f"  {station}: {avg:.2f}°C\n")

# identify the station(s) with the largest tempes  range 
max_range = -1
max_range_stations = []

for station, stats in station_stats.items():
    temp_range = stats['max_temp'] - stats['min_temp']
    if temp_range > max_range:
        max_range = temp_range
        max_range_stations = [station]
    elif temp_range == max_range:
        max_range_stations.append(station)
#save the largest tempes file
with open('largest_temp_range_station.txt', 'w') as f:
    f.write("Station(s) with the largest temperature range:\n")
    for station in max_range_stations:
        f.write(f"{station} (Range: {max_range:.2f}°C)\n")

# Find warmest and coolest stations
avg_temps = {}
for station, stats in station_stats.items():
    avg_temps[station] = stats['total_temp'] / stats['count']

warmest_temp = max(avg_temps.values())
warmest_stations = [s for s, t in avg_temps.items() if t == warmest_temp]

coolest_temp = min(avg_temps.values())
coolest_stations = [s for s, t in avg_temps.items() if t == coolest_temp]
#save the warmest and coolest files
with open('warmest_and_coolest_station.txt', 'w') as f:
    f.write("Warmest Station(s):\n")
    for station in warmest_stations:
        f.write(f"{station} (Average Temp: {warmest_temp:.2f}°C)\n")
    
    f.write("\nCoolest Station(s):\n")
    for station in coolest_stations:
        f.write(f"{station} (Average Temp: {coolest_temp:.2f}°C)\n")

print("Analysis complete. Results saved to:")
print("- average_temp.txt")
print("- largest_temp_range_station.txt")
print("- warmest_and_coolest_station.txt")
