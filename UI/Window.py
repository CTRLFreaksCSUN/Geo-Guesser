import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import flet as ft
from login_interface import login_interface
import DataClient
from DataClient import DataClient

class Window(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page=page
        login_interface(self, page)

    def close_app(self, e):
        self.page.window.close()

# creates new window
def main(screen: ft.Page):
    screen.title = "GeoVision--prototype"
    screen.theme_mode = 'dark'
    screen.update()

    # load up main program initerface
    sign_in = Window(screen)

if __name__ == '__main__':
    ft.app(target=main)