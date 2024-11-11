import flet as ft

def main(page: ft.Page):
    # Set up page properties
    page.title = "GeoVision"
    page.theme = ft.Theme(color_scheme_seed="teal")
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"

    # Initialize image_data as a placeholder
    image_data = ft.Image(width=300, height=300)

    # Define the show_image function to handle selected files
    def show_image(e):
        nonlocal image_data  # Now referencing image_data inside the function
        if e.files:
            # Get the first file picked
            file = e.files[0]
            # Update the image with the selected file
            if file.path:
                image_data = ft.Image(src=file.path, width=300, height=300)

        # Update the page with new image and the option to upload another image
        page.controls.clear()
        page.controls.append(image_data)
        page.controls.append(ft.ElevatedButton("Upload Another Image", on_click=pick_image))
        page.update()

    # Function to trigger file picking
    def pick_image(e):
        # Dynamically create the FilePicker and add it to the page
        file_picker = ft.FilePicker(on_result=show_image)
        page.add(file_picker)  # Add the FilePicker to the page
        # Allow file picking for image files only
        file_picker.pick_files(allowed_extensions=["png", "jpg", "jpeg"])

    # Create initial page controls
    page.add(ft.ElevatedButton("Choose a picture", on_click=pick_image))

# Run the Flet app
ft.app(target=main)
