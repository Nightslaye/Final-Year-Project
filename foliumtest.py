import tkinter as tk
from tkinter import ttk
import folium
import json
import webbrowser
import os
from shapely.geometry import Polygon
import csvReader

# Function to filter GeoJSON features by borough name
def filter_geojson_by_borough(geojson_file, borough_names):
    with open(geojson_file) as f:
        data = json.load(f)

    filtered_features = []
    for feature in data['features']:
        if feature['properties']['name'] in borough_names:
            filtered_features.append(feature)

    filtered_geojson = {
        "type": "FeatureCollection",
        "features": filtered_features
    }
    return filtered_geojson

# Function to generate HTML content with header, sample text, and embedded map
def generate_html_content(borough_names, map_filename):
    map_abs_path = os.path.abspath(map_filename)
    borough_info = ", ".join(borough_names)
    imageName = "_".join(borough_names)+"_comparison_chart"
    para_1_lines = csvReader.para_1.split('\n')
    para_2_lines = csvReader.para_2.split('\n')
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{borough_info} Map</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #333;
            color: #eee;
        }}
        .container {{
            max-width: 800px;
            margin: 20px auto;
            padding: 20px;
            background-color: #444;
            border: 1px solid #555;
            border-radius: 5px;
        }}
        h1, h2, p {{
            color: #eee;
        }}
        iframe {{
            border: none;
            width: 100%;
            height: 400px;
        }}
        .map-container {{
            margin-top: 20px;
            border: 1px solid #555;
            border-radius: 5px;
            overflow: hidden;
        }}
        .map-container img {{
            width: 100%;
            display: block;
        }}
    </style>
    </head>
    <body>
    <div class="container">
    <h1>{borough_info} Map</h1>
    <p>This map displays the boroughs of London.</p>
    <div class="map-container">
    <iframe src="{map_abs_path}" frameborder="0"></iframe>
    </div>
    <div class="map-container">
    <p>Comparison chart:</p>
    <img src="{imageName}.png" alt="Comparison Chart">
    </div>
   """

    # Add paragraphs as separate elements
    html_content += "<h2>"
    html_content += borough_names[0]
    html_content += "</h2>"
    html_content += "<p>"
    for line in para_1_lines:
        html_content += f"{line}<br>"
    html_content += "</p>"

    html_content += "<h2>"
    html_content += borough_names[1]
    html_content += "</h2>"
    html_content += "<p>"
    for line in para_2_lines:
        html_content += f"{line}<br>"
    html_content += "</p>"

    html_content += """
    </div>
    </div>
    </body>
    </html>
    """

    html_content = html_content.replace('£', '&pound;')

    return html_content

valid_borough_list = [
    "Barking and Dagenham",
    "Bexley",
    "Newham",
    "Croydon",
    "Havering",
    "Sutton",
    "Greenwich",
    "Enfield",
    "Hillingdon",
    "Tower Hamlets",
    "Hounslow",
    "Lewisham",
    "Redbridge",
    "Waltham Forest",
    "Harrow",
    "Bromley",
    "Ealing",
    "Kingston upon Thames",
    "Southwark",
    "Lambeth",
    "Brent",
    "Merton",
    "Barnet",
    "Wandsworth",
    "Haringey",
    "Hackney",
    "Islington",
    "Richmond upon Thames",
    "Hammersmith and Fulham",
    "Camden",
    "City of London",
    "City of Westminster",
    "Kensington and Chelsea"
]


def capitalise_borough_names(names):
    capitalised_names = []
    for name in names:
        # Split the name into individual words
        words = name.split() #['Kingston' 'upon' 'Thames']

        # Capitalize the first letter of each word except for specified exceptions
        capitalised_words = [word.capitalize() if word.lower() not in ['and', 'upon', 'of'] else word.lower() for word in
                             words]

        # Join the words back into a single string
        capitalised_name = ' '.join(capitalised_words)

        capitalised_names.append(capitalised_name)

    return capitalised_names

# Function to update the map with highlighted boroughs
def highlight_boroughs(entries):
    borough_names = [entry.get().lower() for entry in entries if entry.get()]
    borough_name = capitalise_borough_names(borough_names)

    if len(borough_names) != 2:
        # If less than 2 boroughs are entered, show a warning message
        tk.messagebox.showwarning("Warning", "Please enter two borough names.")
        return

    # Convert valid borough list to lowercase
    valid_borough_list_lower = [borough.lower() for borough in valid_borough_list]

    # Check if all entered borough names are valid
    invalid_boroughs = [borough for borough in borough_names if
                        borough not in valid_borough_list_lower]

    if invalid_boroughs:
        # If any entered borough is not valid, show a warning message
        invalid_boroughs_str = ", ".join(invalid_boroughs)
        tk.messagebox.showwarning("Warning",
                                  f"The following boroughs are not valid: {invalid_boroughs_str}. Please enter valid borough names.")
        return

    if borough_name:
        # Filter the GeoJSON data by the inputted borough names
        filtered_geojson = filter_geojson_by_borough("london_boroughs.json", borough_name)

        # Create a map centered on London
        m = folium.Map(location=[51.5074, -0.1278], zoom_start=10)

        # Add markers and GeoJSON layers for each borough
        for feature in filtered_geojson['features']:
            name = feature['properties']['name']
            coordinates = feature['geometry']['coordinates']
            if feature['geometry']['type'] == 'MultiPolygon':
                centroid_coordinates = get_multi_polygon_centroid(coordinates)
                for centroid_coord in centroid_coordinates:
                    folium.Marker(
                        location=[centroid_coord[1], centroid_coord[0]],  # [latitude, longitude]
                        popup=f'<b>{name}</b>',
                    ).add_to(m)
            else:  # Single Polygon
                centroid = get_polygon_centroid(coordinates)
                folium.Marker(
                    location=[centroid[1], centroid[0]],  # [latitude, longitude]
                    popup=f'<b>{name}</b>',
                ).add_to(m)

            # Add GeoJSON layer with borough name as label
            folium.GeoJson(
                feature,
                name=name,
                style_function=lambda x: {'color': 'blue', 'fillOpacity': 0.1}
            ).add_to(m)

        csvReader.compare_boroughs(borough_name[0], borough_name[1], csvReader.file_path)
        # Save the map to an HTML file
        map_filename = "_".join(borough_name) + "_map.html"
        m.save(map_filename)

        # Generate HTML content with header, sample text, and embedded map
        html_content = generate_html_content(borough_name, map_filename)

        # Open the HTML content in the default web browser
        with open("highlighted_borough_map.html", "w") as html_file:
            html_file.write(html_content)
        webbrowser.open("highlighted_borough_map.html")

        # Update the labels with the inputted borough names
        #for label, name in zip(labels, borough_names):
        #    label.config(text=name)

# Function to get the centroid of a polygon
def get_polygon_centroid(coordinates):
    polygon = Polygon(coordinates[0])
    return polygon.centroid.coords[0]

# Function to get the centroid of a multipolygon
def get_multi_polygon_centroid(coordinates):
    centroid_coordinates = []
    for polygon_coords in coordinates:
        polygon = Polygon(polygon_coords[0])
        centroid_coordinates.append(polygon.centroid.coords[0])
    return centroid_coordinates

'''
# Create the main Tkinter window
win = tk.Tk()
win.title("London Borough Highlighter")

# Create a frame to hold the input widgets
input_frame = ttk.Frame(win)
input_frame.pack(fill="x", padx=10, pady=5)

# Create entry widgets and labels for borough names
entries = []
labels = []
for i in range(2):  # Adjust this number as needed
    entry = ttk.Entry(input_frame)
    entry.grid(row=i, column=0, padx=5, pady=5)
    entries.append(entry)

    label = ttk.Label(input_frame, text="")
    label.grid(row=i, column=2, padx=5, pady=5)
    labels.append(label)

# Create a button to trigger highlighting for both boroughs
highlight_button = ttk.Button(input_frame, text="Highlight Boroughs",
                              command=lambda: highlight_boroughs(entries)) #Edit 'entries' to the inputs from main.py
highlight_button.grid(row=0, column=1, padx=5, pady=5)

# Start the Tkinter event loop
win.mainloop()
'''