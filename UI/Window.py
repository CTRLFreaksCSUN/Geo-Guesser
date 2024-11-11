import os
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import flet as ft
import pymongo
from pymongo import MongoClient
from login_interface import login_interface

class Window(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        login_interface(self, page)

    def close_app(self, e):
        e.control.page.window.close()
        e.control.page.update()

# creates new window
def main(screen: ft.Page):
    screen.title = "GeoVision--prototype"

    # connect to MongoDB Database
    # client = MongoClient({ connection string })

    sign_in = Window(screen)


if __name__ == '__main__':
    ft.app(target=main)