Road Detection AI System
This project is a Django-based web application that uses AI to classify car images as either "On Road" or "Off Road." The application provides an admin verification system that allows an administrator to review and verify the AI-generated status for each image and decide whether to accept or reject the report. The final status is then displayed to the user, providing them with clear and accurate details on each image's classification.

Features
Image Upload: Users can upload images of vehicles for classification.
AI Classification: An integrated AI model automatically classifies each uploaded image as "On Road" or "Off Road."
Admin Verification: Admins can review the AI classifications and either confirm or override the AI's decision.
Report Management: Admins can accept or reject the final report based on the AI classification and their verification.
User Dashboard: Users can view the status of their uploaded images, including whether the report was accepted or rejected by the admin.
Workflow
Image Submission: Users upload images of vehicles.
AI Processing: The AI model processes each image to determine if the car is on or off the road.
Admin Verification: The admin reviews the AI classification, verifies the results, and has the option to approve or reject the report.
Final Status Display: Once verified by the admin, the final status is displayed on the user dashboard, showing detailed classification information.
Tech Stack
Backend: Python, Django
Frontend: Django templates, HTML, CSS
AI Model: Custom-trained model for road detection (integrated into the backend)
Database: PostgreSQL (or preferred database setup)
