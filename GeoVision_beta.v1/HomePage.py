from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
from PIL import Image
import requests
import base64
import webbrowser
import os
import flet as ft
from DataClient import DataClient



# Azure credentialsGoogle Maps API Key
AZURE_SUBSCRIPTION_KEY = "2dBJsnA8n5oJSxVXm5kPJIWzNpWwW7hAHxkVzSqSwbTihmfJLaqNJQQJ99AKACYeBjFXJ3w3AAAFACOGLuar"
AZURE_ENDPOINT = "https://geovis.cognitiveservices.azure.com/"
GOOGLE_API_KEY = "AIzaSyAguajYZPdNBLSWvYWLfetpGRInLGC0ehE"

class HomePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page
        self.image_path = None  # Store the uploaded image path
        self.build_home_page()

    def build_home_page(self):
        # Clear existing controls on the page
        if self.page and hasattr(self.page, "controls"):
            self.page.controls.clear()
        else:
            raise ValueError("Invalid page object passed to HomePage.")

        # UI Components
        image_display = ft.Image(width=300, height=300)
        explanation_box = ft.TextField(
            value="Explanation, tags, and description will appear here.",
            read_only=True,
            multiline=True,
            border_color="black",
            width=300,
            height=300,
        )
        error_label = ft.Text("", color="red", visible=False)

        # Analyze Image with Azure AI
        def analyze_image():
            if not self.image_path:
                error_label.value = "Please upload an image first."
                error_label.visible = True
                self.page.update()
                return

            try:
                client = ComputerVisionClient(AZURE_ENDPOINT, CognitiveServicesCredentials(AZURE_SUBSCRIPTION_KEY))
                with open(self.image_path, "rb") as image_stream:
                    analysis = client.analyze_image_in_stream(
                        image_stream, visual_features=[VisualFeatureTypes.tags, VisualFeatureTypes.description]
                    )

                # Get description and tags
                description = analysis.description.captions[0].text if analysis.description.captions else "No description available."
                tags = [tag.name for tag in analysis.tags]

                # Update the explanation box with analysis results
                explanation_box.value = f"Description: {description}\n\nTags: {', '.join(tags)}"
                error_label.visible = False
                self.page.update()
            except Exception as err:
                error_label.value = f"Error analyzing image: {str(err)}"
                error_label.visible = True
                self.page.update()

        # Handle File Upload
        def process_image(e):
            if e.files:
                file = e.files[0]
                if file.path:
                    self.image_path = file.path
                    image_display.src = self.image_path
                    explanation_box.value = "Click 'Analyze' to process the image."
                    self.page.update()

        # Pick an Image
        def pick_image(e):
            file_picker = ft.FilePicker(on_result=process_image)
            self.page.add(file_picker)
            file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

        # Add Controls to the Page
        self.page.controls.extend([
            ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text("GeoVision", size=24),
                            image_display,
                            ft.ElevatedButton("Choose a Picture", on_click=pick_image),
                            ft.ElevatedButton("Analyze", on_click=lambda _: analyze_image()),
                            error_label,
                        ],
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    ft.Container(
                        content=explanation_box,
                        width=400,
                        height=300,
                        border=ft.border.all(1),
                        padding=10,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
                spacing=20,
            ),
            ft.ElevatedButton("Close App", on_click=lambda e: self.page.window.close()),
        ])
        self.page.update()