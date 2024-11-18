import flet as ft

class HomePage(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page  # Store the page object
        self.build_home_page()

    def build_home_page(self):
        # Clear existing controls on the page
        if self.page and hasattr(self.page, "controls"):
            self.page.controls.clear()
        else:
            raise ValueError("Invalid page object passed to HomePage.")

        self.page.horizontal_alignment = "center"
        self.page.vertical_alignment = "center"

        image_data = ft.Image(width=300, height=300)

        # Function to handle selected files
        def show_image(e):
            nonlocal image_data
            if e.files:
                file = e.files[0]
                if file.path:
                    image_data.src = file.path
            self.page.controls.clear()
            self.page.controls.extend([
                image_data,
                ft.ElevatedButton("Upload Another Image", on_click=pick_image),
                ft.ElevatedButton("Close App", on_click=lambda e: self.page.window.close()),
            ])
            self.page.update()

        # Function to pick an image
        def pick_image(e):
            file_picker = ft.FilePicker(on_result=show_image)
            self.page.add(file_picker)
            file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

        # Add GeoVision controls
        self.page.controls.extend([
            ft.Text("GeoVision", size=24),
            ft.ElevatedButton("Choose a Picture", on_click=pick_image),
            ft.ElevatedButton("Close App", on_click=lambda e: self.page.window.close()),
        ])
        self.page.update()