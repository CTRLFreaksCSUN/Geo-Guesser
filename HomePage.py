import sys
import os
import requests
from PyQt5.QtWidgets import QMessageBox, QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QLabel, QPushButton, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QUrl, Qt
import folium
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import requests
import base64
import webbrowser
from DataClient import DataClient

# Azure credentialsGoogle Maps API Key
AZURE_SUBSCRIPTION_KEY = "EGtF8U8ziSxlgBdvtpnvwczTCN0jfayyQYOXXy6HidlES1FJ6wzUJQQJ99ALACYeBjFXJ3w3AAAFACOGlzGm"
AZURE_ENDPOINT = "https://geovision.cognitiveservices.azure.com/"
GOOGLE_API_KEY = "AIzaSyAguajYZPdNBLSWvYWLfetpGRInLGC0ehE"


from PyQt5.QtWidgets import QGridLayout

class HomePage(QMainWindow):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.apply_stylesheet()
        self.setWindowTitle("GeoVision")
        self.setGeometry(100, 100, 1200, 600)

        self.computer_vision_client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_SUBSCRIPTION_KEY))

        # Central widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QGridLayout(self.central_widget)

        # Image section
        self.image_label = QLabel("Select an image")
        self.image_label.setFixedSize(500, 300)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setStyleSheet("font-size: 16px;")

        # Description label for Azure AI results
        self.description_label = QLabel("Image details will appear here.")
        self.description_label.setWordWrap(True)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.description_label.setStyleSheet("padding: 10px; background-color: #3e3e3e; color: white; font-size: 16px")

        # Select image button
        self.select_image_button = QPushButton("Select Image")
        self.select_image_button.clicked.connect(self.open_file)
        self.select_image_button.setFixedSize(260,40)

        # Starting location input
        self.starting_location = QLineEdit()
        self.starting_location.setPlaceholderText("Enter starting location...")
        self.starting_location.setStyleSheet("background-color: #666262; color: white;")
        self.starting_location.setFixedSize(260,40)  # Fixed width for alignment

        # Destination location input
        self.destination = QLineEdit()
        self.destination.setPlaceholderText("Enter destination...")
        self.destination.setStyleSheet("background-color: #666262; color: white;")
        self.destination.setFixedSize(260,40)

        # Get directions button
        self.directions_button = QPushButton("Get Directions")
        self.directions_button.clicked.connect(self.get_directions)
        self.directions_button.setFixedSize(260,40)

        # Create an HBox for starting, destination, and button
        input_layout = QHBoxLayout()
        input_layout.addWidget(self.starting_location)
        input_layout.addWidget(self.destination)
        input_layout.addWidget(self.directions_button)

        # Map section
        self.map_viewer = QWebEngineView()
        self.map_viewer.setFixedSize(1000, 300)

        # Add widgets to the grid layout
        self.layout.addWidget(self.map_viewer, 0, 0, 1, 2, Qt.AlignCenter)  # Map is centered and spans 2 columns
        self.layout.addLayout(input_layout, 1, 0, 1, 2, Qt.AlignCenter)  # Inputs are centered below the map
        self.layout.addWidget(self.image_label, 2, 0, 1, 2, Qt.AlignCenter)  # Image below the inputs, centered
        self.layout.addWidget(self.description_label, 3, 0, 1, 2)  # Spans two columns below the image
        self.layout.addWidget(self.select_image_button, 4, 0, 1, 2, Qt.AlignCenter)

        # Initial state
        self.api_key = "AIzaSyDyPin-fSQ8BsipK8sSV80TCsLijci2PbY"
        self.geolocator = Nominatim(user_agent="ImageMapApp")
        self.current_location = [37.7749, -122.4194]  # Default to San Francisco
        self.generate_map()

    # Fetch coordinates using Google Maps API
    def fetch_coordinates_from_google_maps(self, query):
        try:
            url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={GOOGLE_API_KEY}"
            response = requests.get(url)
            data = response.json()

            if data["status"] == "OK" and data["results"]:
                location = data["results"][0]["geometry"]["location"]
                return f"{location['lat']}, {location['lng']}"
            else:
                return None
        except Exception as e:
            return f"Error fetching coordinates: {str(e)}"

    def analyze_image(self, file_path):
        try:
            with open(file_path, "rb") as image_stream:
                analysis = self.computer_vision_client.analyze_image_in_stream(
                    image_stream, visual_features=[VisualFeatureTypes.description]
                )

            description = analysis.description.captions[0].text if analysis.description.captions else "No description available."

            # Fetch coordinates from Google Maps
            location_query = description or ', '
            coordinates = self.fetch_coordinates_from_google_maps(location_query)

            if coordinates:
                self.description_label.setText(f"Description: {description}\n\nCoordinates: {coordinates}")
                self.destination.setText(coordinates)  # Automatically insert into the destination text box
            else:
                self.description_label.setText(f"Description: {description}\n\nCoordinates not found.")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"Error analyzing image: {str(e)}")

    def apply_stylesheet(self):
        self.setStyleSheet("""
        QWidget {
            background-color: #3e3e3e;
            color: white;
        }
        QPushButton {
            background-color: #666262;
            color: white;
            border-radius: 8px; 
            padding: 8px; 
            font-size: 16px;
            
        
        }
        QPushButton:hover {
            background-color: #535353;
        }
        QLineEdit { 
            color: black;
            border-radius: 8px;
            padding: 8px;
            font-size: 16px;
            min-width: 200px;
        }
    """)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image", "", "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_name:
            self.display_image(file_name)
            self.analyze_image(file_name)

    def display_image(self, file_path):
        pixmap = QPixmap(file_path)
        pixmap = pixmap.scaled(self.image_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.image_label.setPixmap(pixmap)

    def generate_map(self, route=None, center_location=None):
        map_object = folium.Map(location=center_location if center_location else self.current_location, zoom_start=12)

        # If a route is provided, add it to the map and adjust the view to fit the entire route
        if route:
            folium.PolyLine(route, color="blue", weight=5).add_to(map_object)
            # Calculate the bounds of the route
            latitudes = [point[0] for point in route]
            longitudes = [point[1] for point in route]
            map_bounds = [(min(latitudes), min(longitudes)), (max(latitudes), max(longitudes))]
            map_object.fit_bounds(map_bounds)  # Adjusts the zoom and centering to fit the specified bounds

        # Save the map to an HTML file
        map_path = "map.html"
        map_object.save(map_path)

        # Load the map into the web viewer
        map_url = QUrl.fromLocalFile(os.path.abspath(map_path))
        self.map_viewer.setUrl(map_url)


    def get_current_location(self, location_name="Your current location"):
        try:
            location = self.geolocator.geocode(location_name, timeout=10)
            if location:
                return [location.latitude, location.longitude]
            else:
                self.statusBar().showMessage(f"Could not determine location: {location_name}", 5000)
                return None
        except GeocoderTimedOut:
            self.statusBar().showMessage("Geocoding timed out. Try again.", 5000)
            return None

    def get_directions(self):
        starting_location = self.starting_location.text()
        destination = self.destination.text()
        if not starting_location or not destination:
            self.statusBar().showMessage("Enter both starting location and destination to get directions.", 5000)
            return

        # Fetch the starting and destination locations
        start_coords = self.get_current_location(starting_location)
        if not start_coords:
            return

        destination_coords = self.get_current_location(destination)
        if not destination_coords:
            return

        # Use Google Maps API to get driving directions
        url = (
            f"https://maps.googleapis.com/maps/api/directions/json"
            f"?origin={start_coords[0]},{start_coords[1]}"
            f"&destination={destination_coords[0]},{destination_coords[1]}"
            f"&mode=driving"
            f"&key={self.api_key}"
        )

        try:
            response = requests.get(url)
            print(response.text)

            if response.status_code == 200:
                data = response.json()
                if data["status"] == "OK":
                    route = []
                    all_latitudes = []
                    all_longitudes = []

                    for step in data["routes"][0]["legs"][0]["steps"]:
                        lat = step["end_location"]["lat"]
                        lng = step["end_location"]["lng"]
                        route.append((lat, lng))
                        all_latitudes.append(lat)
                        all_longitudes.append(lng)

                    # Calculate center of the route by averaging latitudes and longitudes
                    center_lat = sum(all_latitudes) / len(all_latitudes)
                    center_lng = sum(all_longitudes) / len(all_longitudes)

                    # Center the map on the calculated center of the route
                    self.generate_map(route, center_location=[center_lat, center_lng])
                else:
                    self.statusBar().showMessage("Failed to get directions: " + data["status"], 5000)
            else:
                self.statusBar().showMessage(f"Error fetching directions: {response.text}", 5000)
        except Exception as e:
            self.statusBar().showMessage(f"Error: {str(e)}", 5000)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HomePage(None)
    window.show()
    sys.exit(app.exec_())