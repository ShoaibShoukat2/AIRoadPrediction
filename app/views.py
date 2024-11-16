from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from .models import Report
from django.shortcuts import render, redirect, get_object_or_404
from tensorflow.keras.preprocessing import image as keras_image
import numpy as np
import tensorflow as tf
from django.contrib.auth import logout
from PIL import Image
from torchvision import models, transforms
import os
import torch
from django.conf import settings

# Create your views here.


def index(request):
    
    return render(request,'index.html')


def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Check if passwords match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')

        # Check if the email is already registered
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('app:signup') 



        # Create the user
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()

        # Log the user in and redirect
        login(request, user)
        return redirect('app:index')

    return render(request, 'signup.html')


def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Authenticate user
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('app:index')          

            
        else:
            messages.error(request, 'Invalid email or password.')
            redirect('app:login')

    return render(request, 'login.html')



# interview for em
# Load the pre-trained Mask R-CNN model (from torchvision)
model = models.detection.maskrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Transformation for the input image
transform = transforms.Compose([
    transforms.ToTensor()
])



def check_car_on_road(image_path):
    # Resolve the full image path using MEDIA_ROOT and ensure 'images' subdirectory is included
    full_image_path = os.path.join(settings.MEDIA_ROOT, image_path)
    
    try:
        # Open the image file and check if it exists
        if not os.path.exists(full_image_path):
            print(f"File not found at path: {full_image_path}")
            return False
        
        # Open and process the image
        image = Image.open(full_image_path).convert("RGB")
        image_tensor = transform(image).unsqueeze(0)

        with torch.no_grad():
            prediction = model(image_tensor)

        labels = prediction[0]['labels'].numpy()
        boxes = prediction[0]['boxes'].detach().numpy()
        scores = prediction[0]['scores'].detach().numpy()

        car_on_road = False
        for i in range(len(labels)):
            if labels[i] == 3 and scores[i] > 0.5:
                car_box = boxes[i]
                _, car_y_min, _, car_y_max = car_box
                road_region_y_min = image.height // 2

                if car_y_max > road_region_y_min:
                    car_on_road = True
        return car_on_road

    except Exception as e:
        print(f"Error processing image: {e}")
        return False
    
    
    


@login_required
def Report_Options(request):
    if request.method == 'POST':
        report_file = request.FILES.get('report_file')
        report_location = request.POST.get('report_location')
        
        if report_file:
            # Save the uploaded file to the correct subdirectory within media
            fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'images'))
            filename = fs.save(report_file.name, report_file)
            file_path = os.path.join('images', filename)  # Save relative path for later use
            print(f"File '{filename}' uploaded successfully at: {file_path}")

            # Check if the car is on the road
            is_car_on_road = check_car_on_road(file_path)
            print(f"Car on road: {is_car_on_road}")
            
            # Set status based on AI analysis
            status = 'accepted' if is_car_on_road else 'rejected'
            

            # Save report info to the database
            report = Report.objects.create(
                user=request.user,
                file_image=report_file,
                location=report_location,
                status=status
            )
            
            
                        
            print(f"Report created with ID: {report.id}, Location: {report_location}, Status: {report.status}")
            
            return redirect('app:success-page')
        else:
            print("No file uploaded.")

    return render(request, 'ReportOption.html')
















@login_required  # Ensure that only logged-in users can access this view
def Report_Status(request):
    # Check if the user is authenticated
    if request.user.is_authenticated:
        # Fetch reports filed by the logged-in user
        user_reports = Report.objects.filter(user=request.user)  # Assuming your Report model has a foreign key to User

        context = {
            'user_reports': user_reports,  # Add user reports to context
        }
        
        return render(request, 'report_status.html', context)  # Render report status page with user reports
    else:
        messages.error(request, 'You need to be logged in to view your reports.')  # Send error message
        return redirect('app:login')  # Redirect to the login page (replace with your actual login URL name)







def Admin(request):
    context = {}  # Initialize context as an empty dictionary

    # Check if the user is a superuser
    if request.user.is_superuser:
        reports = Report.objects.all()  # Fetch the reports
        context['reports'] = reports  # Add reports to context
        return render(request, 'Admin.html', context)  # Render admin page with context
    
    
    
    
    
    else:
        messages.error(request, "Access to this page is restricted to admins only.")
        return redirect('app:adminlogin')  # Redirect to the login page or another page








def manual_accept_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.manual_status = 'accepted'
    report.save()
    return redirect('app:admin-reports')

def manual_reject_report(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    report.manual_status = 'rejected'
    report.save()
    return redirect('app:admin-reports')
  
  































def adminlogin(request):
    print("Request method:", request.method)  # Verify the request method (POST or GET)

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Debugging output for email (avoid printing passwords in production)
        print("Received Email:", email)
        print("Received Password:", password)  # For testing only; remove in production!

        try:
            # Attempt to retrieve the user by email
            user = User.objects.get(email=email)
            print("User found:", user)

            # Manually check the password
            if user.check_password(password):
                print("Password is correct for user:", email)

                # Check if user has admin privileges
                if user.is_staff and user.is_superuser:
                    print("User is staff and superuser, logging in as admin.")
                    login(request, user)  # Log in the user
                    return redirect('app:admin-reports')  # Redirect to admin dashboard
                
                elif user.is_staff:
                    print("User is staff but not a superuser, logging in as user.")
                    login(request, user)  # Log in the user as a regular user
                    return redirect('app:user-dashboard')  # Redirect to user dashboard

                else:
                    print("User is not an admin or staff.")

            else:
                print("Authentication failed: incorrect password for user:", email)

        except User.DoesNotExist:
            print("Authentication failed: no user found with email", email)

        # Display error message for invalid credentials or permissions
        messages.error(request, 'Invalid login credentials or insufficient permissions.')

    # For GET requests or failed login, render login page
    print("Rendering login page")
    return render(request, 'AdminAuth/login.html')

























def success(request):
    
    return render(request,'success.html')



def logout_view(request):
    logout(request)
    return redirect('app:login')









