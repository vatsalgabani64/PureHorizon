def calculate_aqi(pollutant_name, concentration):
    # Define the AQI breakpoints and associated sub-index values for each pollutant
    breakpoints = {
        "PM2.5": [(0, 30), (31, 60), (61, 90), (91, 120), (121, 250), (251, 350)],
        "PM10": [(0,50),(51,100),(101,250),(251,350),(351,430),(431,500)],
        "O3": [(0,50),(51,100),(101,168),(169,208),(209,748),(749,1000)],
        "CO": [(0, 1.0), (1.1, 2.0), (2.1, 10), (10.1, 17), (17.1, 34),(34.1,50)],
        "NO2": [(0, 40), (41, 80), (81, 180), (181, 280), (281, 400),(401,500)],
        "SO2": [(0, 40), (41, 80), (81, 380), (381, 800), (801, 1600),(1601,2000)],
        "NH3": [(0,200),(201,400),(401,800),(801,1200),(1201,1800),(1801,2000)]
    }
    st_range=[(0,50),(51,100),(101,200),(201,300),(301,400),(401,500)]

    if pollutant_name not in breakpoints:
        return "Pollutant not supported"

    for i in range(len(breakpoints[pollutant_name])):
        low, high = breakpoints[pollutant_name][i]
        if low <= concentration <= high:
            aqi_low, aqi_high = st_range[i]
            aqi = ((aqi_high - aqi_low) / (high - low)) * (concentration - low) + aqi_low
            return aqi

    return "Invalid concentration value"

# Example usage:
pollutant_name = "PM2.5"
concentration = 25  # Replace with your actual pollutant concentration
aqi = calculate_aqi(pollutant_name, concentration)
print(f"The AQI for {pollutant_name} is {aqi}")
