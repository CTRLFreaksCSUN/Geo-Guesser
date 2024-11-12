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
    screen.theme_mode = 'dark'
    screen.update()
    try:
        # connect to MongoDB Database
        client = MongoClient("mongodb+srv://ctrl_freaks2024:<Zwh5i908Ly0yUkMt>@geovisioncloud.jrl02.mongodb.net/?retryWrites=true&w=majority&appName=GeoVisionCloud")

        #print("Connected to database")
        #db = client["ImageLocator_AI"]
        #db.create_collection("User")
        #db.create_collection("Image")
        #db.create_collection("Location")
     
    except ConnectionError as cerr:
        print(f"Error in MongoDB connection: {cerr}")

    except RuntimeError as rerr:
        print(f"Runtime error: {rerr}")

    except TypeError as terr:
        print(f"Invlaid type detected: {terr}")

    except pymongo.errors.OperationFailure as operr:
        print(f"Error in MongoDB authentication: {operr}")
 
    sign_in = Window(screen)
    client.close()


if __name__ == '__main__':
    ft.app(target=main)