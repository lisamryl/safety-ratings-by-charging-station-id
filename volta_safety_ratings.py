import requests
from flask import (Flask, request, jsonify)
from sodapy import Socrata
from geopy.distance import vincenty

app = Flask(__name__)

# Scale of 1 - 5 (increasing in severity)
# Crimes not in the map are less severe (severity 1)
CRIME_SEVERITY = {
    'ASSAULT': 5, 'SEX OFFENSES, FORCIBLE': 5, 'LARCENY/THEFT': 4, 'ROBBERY': 4,
    'WEAPON LAWS': 4, 'BURGLARY': 4, 'ARSON': 4, 'VEHICLE THEFT': 4,
    'VANDALISM': 3, 'DISORDERLY CONDUCT': 3, 'STOLEN PROPERTY': 3,
    'DRUG/NARCOTIC': 3, 'PROSTITUTION': 2, 'EXTORTION': 2, 'DRUNKENNESS': 2,
    'TRESPASS': 2, 'LIQUOR LAWS': 2,
    }
# Threshold of max distance between charging station and crime (in miles)
CRIME_MAX_DISTANCE = 0.25
# Date range of crime incidents
CRIME_DATE_START = '2018-01-01'
# Crime threshold to base safety ratings on. Over time, this number would be
# based off historical data (or data across the entire city). For now, this
# number is arbitrary.
SAFETY_THRESHOLD = 40


# GET DATA FROM APIs
def get_volta_data():
    """
    Get volta data for SF area and return as a list of tuples.
    Args:
        None
    Returns:
        List of volta locations with x and y coordinates
    """
    location_url = 'https://api.voltaapi.com/v1/stations'
    location_json = requests.get(location_url).json()
    locations_list = []
    for item in location_json:
        if item['city'] == 'San Francisco':
            locations_list.append(tuple([item['id'],
                                         item['location']['coordinates'][0],
                                         item['location']['coordinates'][1]]))
    return locations_list


def get_SF_crime_data():
    """
    Pulls SF crime data and returns it as a list with coordinates.
    Args:
        None
    Returns:
        List of SF crimes (including category, coordinates, and date) occurring
        after a specific date
    """
    client = Socrata("data.sfgov.org", None)
    # Returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("cuks-n6tp")
    crimes_by_location = []
    for item in results:
        if item['date'] > CRIME_DATE_START:
            crimes_by_location.append(tuple([item['category'],
                                             item['x'],
                                             item['y'],
                                             item['date']]))
    return crimes_by_location


#API Endpoints
def get_crime_by_loc(locations_list, crime_list):
    """
    Given a list of locs and crimes, return counts, severity and details by loc.
    Args:
        Locations list (volta locations - includes id, x-coord, y-coord)
        Crime List (SF crimes - includes crime type, x-coord, y-coord, date)
    Returns:
        Dictionary of crime severities by location id
    """
    loc_crime_severity = {}
    for location in locations_list:
        loc_id, loc_x_coord, loc_y_coord = location
        # Show all results, even if no crimes are commited near the area.
        loc_crime_severity[loc_id] = 0
        for crime in crime_list:
            crime_type, crime_x_coord, crime_y_coord, crime_date = crime
            # Look up crime severity, if not there, assign value of 1
            crime_factor = CRIME_SEVERITY.get(crime_type, 1)
            # Using geopy library function to get distance between 2 locations
            distance = vincenty((loc_x_coord, loc_y_coord),
                                (crime_x_coord, crime_y_coord)).miles
            # If distance is within max crime distance, consider crime "nearby"
            if distance <= CRIME_MAX_DISTANCE:
                loc_crime_severity[loc_id] = (loc_crime_severity.get(loc_id, 0)
                                              + crime_factor)
    return loc_crime_severity


def convert_crimes_to_ratings(loc_crime_severity):
    """
    Given crime severity by location, return list of safety ratings by loc_id.
    Safety is on a scale from 0-5, with 5 being the safest, 0 being very unsafe.
    Args:
        Loc_crime_severity (dictionary)
    Returns:
        List of safety ratings by LOC id
    """
    safety_rating_list = []
    for key in loc_crime_severity:
        # Convert crime severity into a safety rating from 0 - 5 (safest)
        safety_rating = round(max(min(5 * ((1 - float(loc_crime_severity[key])
                                      / SAFETY_THRESHOLD)), 5), 0), 2)
        safety_rating_list.append([key, safety_rating])
    return safety_rating_list


def get_crime_details_by_id(loc_id, loc_details):
    """
    Given an id and loc_details, return crime details for id.
    Args:
        loc_id: ID of the charging station
        loc_details: List of LOC Details (Tuple), crime type, and date.
    Returns:
        List of crimes_by_loc_id
    """
    crimes_by_loc_id = []
    for item in loc_details:
        if item[0] == loc_id:
            crimes_by_loc_id.append([item[1], item[2]])
    return crimes_by_loc_id

if __name__ == "__main__":
    #app.run(port=5000, host='0.0.0.0')
    volta_locs = get_volta_data()
    crime_list = get_SF_crime_data()

    loc_crime_severity = get_crime_by_loc(volta_locs, crime_list)

    # Get safety ratings list by location (factoring in severity of crime)
    # scale of (0 (least safe) - 5 (safest))
    safety_rating_list = convert_crimes_to_ratings(loc_crime_severity)
    print safety_rating_list
