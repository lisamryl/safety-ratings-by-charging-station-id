# Volta Code Challenge
> The goal of this challenge is to demonstrate your skills, with a tool of your choice, taking data and turning it into something meaningful.

## Problem
We have a publicly available endpoint, documented here:
http://docs.voltaapi.com/api/#get--stations.
Build an interface that exposes this data in whatever form you like.

### Requirements
- Spend no more than a couple of hours on this, focus on one feature is a plus
- Deliver in a method that is easy for us to consume
- Commit history showing your thought/development process is always interesting

If you have any questions do not hesitate to reach out via email or phone. In consideration of your schedule, take as long as you need to return the challenge. 

### Some examples/ideas for inspiration:
- Display the stations on a map
- Render a searchable table of the stations
- Aggregate data about the stations and display a high-level metric

## Tips and Tricks
We don't spend much time reinventing wheels here at Volta. Depending on the meaning you would like to derive from our data, find a tool or library that helps you express it without writing an excessive amount of code or re-implementing existing technology.

Conversely, if you already have a tool or library in mind: show off your skills by using something you know when to provide new insight into our data. Engineering hours are expensive so we like to find a middle-ground between correctness and efficiency.

## Solutions

# Safety Ratings by Volta Charging Location
This program takes in the volta data by location, as well as SF crime data (from SF Gov API), calculates safety ratings for each id based on crimes (and crime severity) nearby each location, and returns a list of safety ratings (from 0 - 5 (safest)) for each volta charging station, by id. 

Sample Output:

```[[u'a176fe56-1c02-4334-9a94-c103074453a9', 0.75], [u'c0d24381-6d05-4712-b0a8-51b6ef5339e2', 0.13], [u'204b96f4-ceea-48c5-9159-8fb4fbe4d23c', 1.13], [u'4f552d40-ea08-4702-addf-8feb7a9e4b16', 0.75], [u'bd28098e-c331-4d7a-8e46-e2f48240fbf9', 0.75], [u'200fc98b-7a50-4504-ac8b-b0b242ace710', 0.13], [u'4a773d5e-6bc4-4bc5-9113-812353d8b786', 5.0], [u'135253dd-8799-412a-a911-f3039188dc38', 4.63], [u'ae731c2e-3d66-4619-804e-699f2eaf173c', 1.62], [u'535bcd75-2913-459f-a6fc-3e8271f97bbf', 1.62], [u'bee7f63f-5069-4f27-9952-c9f60baa73b5', 0.75], [u'30b24757-2a14-4f75-b675-866f74e26a4f', 3.75], [u'7e87de61-eae4-4cfa-98be-9a182019855f', 5.0], [u'a4e4a808-c086-4897-8d8a-70d52d1f945c', 3.75], [u'1b7ce581-0bf0-4424-a266-572cdd058802', 4.63]]```

# To Run
* Git clone into a new folder
* Set up a virtual environment (e.g. `virtualenv env`)
* Activate it (e.g. `source env/bin/activate`)
* Install all requirements (`pip install -r requirements.txt`)
* Run `python volta_safety_ratings.py` (runs program (will print to terminal, but is intended to be used as an API to connect to the front end))
