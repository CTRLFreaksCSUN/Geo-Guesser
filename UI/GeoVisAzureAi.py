from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import requests
import base64
import webbrowser
import os
import flet as ft

# Azure credentials
AZURE_SUBSCRIPTION_KEY = "2dBJsnA8n5oJSxVXm5kPJIWzNpWwW7hAHxkVzSqSwbTihmfJLaqNJQQJ99AKACYeBjFXJ3w3AAAFACOGLuar"
AZURE_ENDPOINT = "https://geovis.cognitiveservices.azure.com/"

# Google Maps API Key
GOOGLE_API_KEY = "AIzaSyAguajYZPdNBLSWvYWLfetpGRInLGC0ehE"

# Initialize Azure Computer Vision client
vision_client = ComputerVisionClient(
    AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_SUBSCRIPTION_KEY)
)

# Function to analyze the image with Azure AI
def analyze_image(image_path):
    with open(image_path, "rb") as image_stream:
        analysis = vision_client.analyze_image_in_stream(
            image_stream, visual_features=[VisualFeatureTypes.tags, VisualFeatureTypes.description]
        )
    description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
    tags = [tag.name for tag in analysis.tags]
    return description, tags

# Function to get coordinates using Google Maps API
def get_coordinates(query):
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={query}&key={GOOGLE_API_KEY}"
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        return location["lat"], location["lng"]
    return None, None

# Function to encode image for Flet display
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode("utf-8")
    return encoded

# Main Flet application
def main(page: ft.Page):
    page.title = "Geolocation Detection with Azure AI and Google Maps"
    page.window_width = 800
    page.window_height = 600

    # UI components
    description_label = ft.Text("")
    tags_label = ft.Text("")
    image_display = ft.Image(src_base64="", width=300, height=300)

    # File picker
    def pick_file(e):
        if e.files and e.files[0]:
            file_path = e.files[0].path
            if not file_path:
                return

            # Encode and display the uploaded image
            encoded_image = encode_image(file_path)
            image_display.src_base64 = encoded_image
            page.update()

            # Analyze image with Azure AI
            description, tags = analyze_image(file_path)
            query = tags[0] if tags else description

            # Get coordinates using Google Maps API
            latitude, longitude = get_coordinates(query)
            if latitude and longitude:
                # Generate map URL and open in browser
                map_url = f"https://www.google.com/maps?q={latitude},{longitude}&z=13"
                webbrowser.open(map_url)
                description_label.value = f"Description: {description}"
                tags_label.value = f"Tags: {', '.join(tags)}\nCoordinates: {latitude}, {longitude}"
            else:
                description_label.value = f"Description: {description}"
                tags_label.value = f"Tags: {', '.join(tags)}\nCould not find coordinates for '{query}'."

            page.update()

    # File picker control
    file_picker = ft.FilePicker(on_result=pick_file)

    # Add the FilePicker control to the page
    page.overlay.append(file_picker)

    # Add controls to the page
    page.add(
        ft.Column(
            [
                ft.Row([ft.TextButton("Upload Image", on_click=lambda _: file_picker.pick_files())]),
                image_display,
                description_label,
                tags_label,
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=10,
        )
    )
    page.overlay.append(file_picker)

# Run the Flet app
ft.app(target=main)