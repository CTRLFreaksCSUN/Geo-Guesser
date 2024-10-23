## Team members:
Jessica Babos

Andrew Hua

Kenneth Riles

Shadi Zgheib

Zachary Mclaughlin

## 1. Project Overview
### 1.1 Project Name
GeoVision AI
### 1.2 Purpose
This artificial intelligence aims to help tourists identify specific locations to travel to based on captivating images of landmarks, topography, ecosystems and other geographical features using a precise global navigation system. It can also be of support to archaeologists and historians, since it can pinpoint a location from analyzing a snapshot of a distinguishable artifact, structure, or even symbols on a wall.
### 1.3 Target Audience
Travel Enthusiasts and Photographers: People interested in learning more about the places they’ve visited or photographed can use the app to quickly identify locations from images.

Cultural Heritage Researchers and Historians: Academics or enthusiasts studying artifacts, historical buildings, or landscapes can benefit from easily identifying locations or objects from photos.

Content Creators and Social Media Influencers: Individuals who post about travels or locations can use it to pinpoint locations they might have forgotten or want to promote.

Curators and Museum Professionals: They can identify and tag artifacts or sites based on images for cataloging or exhibition purposes.

Geography and Earth Science Students and Educators: As an educational tool, it could be used in classrooms to help students identify and learn about world geography, historical sites, and natural landmarks.

## 2. Features
### 2.1 Required Features
User logs into or creates account

Display invalid user credentials

User account is authenticated via email verification

Passwords are encrypted

Internal database stores user credentials

User has the ability to upload or drag and drop image file from file system

Image file formats (.jpg, .png, .gif, .bmp, etc..) supported

External database stores image files from the internet

Location results are displayed if found or not found

Error message is displayed if search and photo-matching algorithm fails

The AI can detect objects (landmarks, artifacts, plantlife, etc..) within image 

### 2.2 Desired Features
Software supports multiple platforms (desktop and mobile)

Multiple users can use this AI simultaneously

Users can choose to save credentials in cloud for quicker access

Users can update account credentials

Image in results screen has increased resolution, quality and lighting contrast

GUI is specific and readable

GUI fits on different platforms

Results screen displays full location (city, state, region, country, continent), distance coordinates (latitude and longitude) and facts about the location

Location search algorithm is fast and optimized for multi-user use

If no local match is detected within search, then Azure AI API will search within cloud database
### 2.3 Aspirational
User can change from map-view to street-view

User can interact with the map or street-view widget to explore location


GUI will be unique and defining the software as its own property
## 3. Technology Stack
Frontend: Flutter

Backend: Python (OpenCV, Azure AI Vision integration)

Database: MongoDB for local storage. Cloud DB

AI Processing: OpenCV, Azure AI Vision API

Mapping Service: Google Maps API (via Flutter web or external browser)

Package Manager: pip (for Python dependencies)

## 4. Tools used for Assignments
### 4.1 Document editing
Google Docs

TextEdit

### 4.2 Diagrams
Draw.io
### 4.3 Group sharing/communication
Gmail

Discord
### 4.4 Updating GitHub Repository
Git/Git Bash

Windows shell
## 5. Risk Analysis/Security Concerns
The user could lose their account information from a cyber attack if they decide to not save it into the cloud.

* Mitigation: Implement a secure password policy, and require MFA

An unauthenticated user could get blocked from some client-specified services (such as changing their email or password).

* Mitigation: Make users verify that it is them requesting the change of password via MFA.

If a user decides to save their username and password in cookies (so they won’t have to login next time), then their data is at risk of getting stolen.

* Mitigation: set up two-factor authentication (private PIN number or security questions) for logging into the account.

Google Maps API could expose the client’s location to hackers attempting to spy on the user.

* Mitigation: disable location tracking when not using the app.

Server maintenance could delay or disable user progress in the application.

Users may upload sensitive or personal images that contain identifiable information or sensitive locations. 

* Mitigation: ensure end to end encryption.

Users with malicious intent could upload tampered images to manipulate the program or get unintended information. 

* Mitigation: implement image integrity checks like a hash to detect tampering.

Storing user uploaded images in a publicly accessible location could lead to a data breach.

* Mitigation: securing the image by encryption and or restricting access to the location for only authorized users.

Man in the middle attacks are also a threat. For example data exchanged between the app and google maps could be intercepted and modified in transit.

* Mitigation: encrypt our data for all communications with external services.  

The app may inadvertently store or use copyrighted images.

* Mitigation: include a terms of service and user agreement that defines the usage of uploaded images and ensures compliance with international and local data protection laws.

## 6. Cost of components
This app must support at least 1000 users (must be able to hold multiple user requests at once).

Multiple user requests initiated simultaneously could lead to slower server time (increased overhead).

In testing cases, each execution of an Azure API function costs $0.000016 per GB-s at execution time (after the free trial period has passed).

Every one million executions of Azure API functions from users would cost $0.20.

Since the app will have to support 1000 users, we have two options for MongoDB. The first is $0.08 per hour and the max 

storage is 10GB with 2GB of ram. The second option is $0.10 per 1M reads. The max storage for this plan is 1TB with auto scaling ram. 

## 7. Architecture Design Diagram

![Screenshot 2024-10-15 152358](https://github.com/user-attachments/assets/c310e43c-3ea9-4ede-b00c-c56e5d9c824c)

## 8. Application Design Diagram

![Screenshot 2024-09-24 193023](https://github.com/user-attachments/assets/2ef19714-e11f-41c3-85f7-e7fb82559a52)
