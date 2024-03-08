import os
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from helmdect.settings import FIREBASE_CONFIG, STATIC_ROOT
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
import pyrebase
from .forms import SignUpForm, UserLoginForm
from django.contrib.auth import authenticate, login as auth_login 
from django.contrib.auth.views import LoginView
from rest_framework.views import APIView
from rest_framework.response import Response
from firebase_admin import storage
import base64
from datetime import datetime, timedelta
from .firebase_init import firebase_admin  # Import the firebase initialization
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render
from .models import *
from django.core.mail import EmailMessage
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
import cv2
import threading
from ultralytics import YOLO
import time
import numpy as np
from urllib.request import urlopen
from django.views.generic import TemplateView
from PIL import Image
from firebase_admin import credentials, storage, db
import json
from skimage.metrics import structural_similarity

# Initialize Firebase Realtime Database
# cred = credentials.Certificate('helmetdetect2-firebase-adminsdk-r98rq-7b231713df.json')  # Replace with your service account key
# firebase_admin.initialize_app(cred, {
#     'databaseURL':  'https://helmetdetect2-default-rtdb.asia-southeast1.firebasedatabase.app',
#     'storageBucket': 'helmetdetect2.appspot.com'
# })
ref = db.reference('reports')

class UploadImageView(APIView):
    def post(self, request):
        try:
            base64_image = request.data.get('base64_image')

            if not base64_image:
                return Response({'error': 'Base64 image data is missing'}, status=400)

            filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_uploaded_image.jpg"

            image_bytes = base64.b64decode(base64_image)
            bucket = storage.bucket()

            destination_blob_name = f"images/{filename}"
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_string(image_bytes, content_type='image/jpeg')

            blob.make_public()
            image_url = blob.public_url

            return Response({'image_url': image_url}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=500)

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update the session with the new password
            messages.success(request, 'Your password was changed successfully.')
            return redirect('home')
    else:
        form = PasswordChangeForm(request.user)

    context = {
        'form': form,
    }
    return render(request, 'helmdectpages/change_password.html', context)

# Create your views here.
def register(request):
    context = {}
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("home")
        context['form_errors'] = form.errors
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = SignUpForm()
    context["form"] = form
    return render(request=request, template_name="helmdectpages/register.html", context=context)

class MyLoginView(LoginView):
    # form_class=LoginForm
    redirect_authenticated_user=True
    template_name='helmdectpages/login.html'

    def get_success_url(self):
        # write your logic here
        # if self.request.user.is_superuser:
        return reverse('home')# '/progress/'



def signout(request):
    logout(request)
    return redirect('login')
    
# @login_required(login_url='/login/')
def home(request):
    return render(request, 'helmdectpages/home.html')

def about(request):
    return render(request, 'helmdectpages/about.html')

@login_required
def report_history(request):
    reports = database.child("reports").get().val()
    start_date_param = request.GET.get('start_date')
    end_date_param = request.GET.get('end_date')

    if start_date_param and end_date_param:
        try:
            start_date = datetime.strptime(start_date_param, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_param, '%Y-%m-%d') + timedelta(days=1)  # Add one day to include the end date
            
            filtered_reports = {}
            if reports:
                for key, value in reports.items():
                    timestamp = value.get('dateTime', 0)  # Assuming 'dateTime' is the timestamp field
                    
                    # Check if timestamp is valid
                    if isinstance(timestamp, int) and timestamp > 0:
                        try:
                            report_date = datetime.fromtimestamp(timestamp / 1000.0)
                            if start_date <= report_date < end_date:  # Check if report_date falls between start_date and end_date
                                if 'passed' not in value or value['passed'] == False:
                                    continue
                                # Check and set default value for helmet_type if missing                                
                                # if 'helmet_type' not in value:
                                #     value['helmet_type'] = 'Unknown'
                                if 'image' not in value or not value['image'].startswith("http"):
                                    continue
                                filtered_reports[key] = value
                        except (ValueError, OSError) as e:
                            # Handle conversion errors
                            pass
                        
                reports = filtered_reports

        except ValueError:
            # Handle the case when dates are not in the correct format
            pass
    else:
        # When start_date_param and end_date_param are not set, return a list of dates grouped by report_date
        grouped_reports = {}
        if reports:
            for key, value in reports.items():
                passed = value.get('passed', False)
                if passed == False:
                    continue
                timestamp = value.get('dateTime', 0)  # Assuming 'dateTime' is the timestamp field
                
                # Check if timestamp is valid
                if isinstance(timestamp, int) and timestamp > 0:
                    try:
                        report_date = datetime.fromtimestamp(timestamp / 1000.0).date()
                        if(report_date.year < 2000):
                            continue
                        if report_date not in grouped_reports:
                            grouped_reports[report_date] = []
                        grouped_reports[report_date].append(value)
                    except (ValueError, OSError) as e:
                        # Handle conversion errors
                        pass
        
        # Sort grouped_reports by report_date
        grouped_reports = dict(sorted(grouped_reports.items()))

        return render(request, 'helmdectpages/report_grouped_dates.html', {'grouped_reports': grouped_reports})

    report_datas = {}
    if reports:
        for key, value in reports.items():
            if 'image' not in value:
                continue
            if not value['image'].startswith("http"):
                continue
            value['location'] = 'Mati City'
            report_datas[key] = value

    # Sort report_datas by dateTime field in descending order (latest first)
    report_datas = dict(sorted(report_datas.items(), key=lambda item: item[1].get('dateTime', 0), reverse=True))

    return render(request, 'helmdectpages/report_history.html', {'reports': report_datas})



@login_required
def detailed_reports(request):
    
    return render(request, 'helmdectpages/detailed_reports.html')

@login_required
def settings(request):
    return render(request, 'helmdectpages/settings.html')


@gzip.gzip_page
def transmition(request):
    try:
        cam = VideoCamera()
        return StreamingHttpResponse(gen(cam), content_type="multipart/x-mixed-replace;boundary=frame")
    except Exception as e:
        print(e)
        return HttpResponseServerError(e)
    # return render(request, 'stream.html')

def video_stream(request):
    # Path to your video file
    video_path = os.path.join(STATIC_ROOT, '1103131475-preview.mp4')

    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if video opened successfully
    if not video.isOpened():
        return HttpResponse("Could not open video file")

    # Get video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    model_path = os.path.join(STATIC_ROOT, 'best.pt')
    model = YOLO(model_path)

    # Loop through the frames
    while True:
        ret, frame = video.read()

        # Check if frame is read correctly
        if not ret:
            break

        # Convert the frame to JPEG format
        ret, jpeg = cv2.imencode('.jpg', frame)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
        # Create a PIL Image from the RGB frame array
        pil_image = Image.fromarray(rgb_frame)
        results = model.predict(source=pil_image, save=False, imgsz=320, conf=0.1, stream=True, show_labels=True, show_boxes=True, show_conf=True)
        
        for result in results:
            im_array = result.plot()  # plot a BGR numpy array of predictions

            img = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            # Convert PIL image to numpy array
            img_array = np.asarray(img)

            img_array_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            _, jpeg = cv2.imencode('.jpg', img_array_bgr)

        

        # Send the frame to the template
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    # Release the video object
    video.release()

def video_feed(request):
    # Set response content type
    return StreamingHttpResponse(video_stream(request), content_type='multipart/x-mixed-replace; boundary=frame')


class VideoCamera(object):
    

    def __init__(self):
        model_path = os.path.join(STATIC_ROOT, 'best.pt')
        self.sample_image_path = os.path.join(STATIC_ROOT, 'download.jpg')
        self.sample_video_path = os.path.join(STATIC_ROOT, '1103131475-preview.mp4')
        # Load YOLO model
        self.model = YOLO(model_path)
        self.previous_frame = None
        self.previous_bytes = None
        # self.video = cv2.VideoCapture(self.sample_video_path)
        self.video = cv2.VideoCapture(
            "rtsp://0.tcp.ap.ngrok.io:19835/mjpeg/1")
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        if image is None:
            return b''
        rgb_frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
        # Create a PIL Image from the RGB frame array
        pil_image = Image.fromarray(rgb_frame)
        # test_path = os.path.join(STATIC_ROOT, 'download.jpg')
        results = self.model.predict(stream_buffer=True, source=pil_image, save=False, imgsz=320, conf=0.1, stream=True, show_labels=True, show_boxes=True, show_conf=True)
        # results = self.model(source=self.sample_video_path, stream=True, stream_buffer=True)
        # img = image

        bounding_box_data = []
        rider_found = False
        classes = []


        jpeg = None        

        for result in results:
            boxes = result.boxes
            for idx in range(len(boxes)):
                box = boxes.data[idx]
                class_id = int(box[-1])
                class_name = self.model.names[class_id]
                classes.append(class_name)

                if class_name == 'rider':
                    rider_found = True
                # Extracting the bounding box coordinates and format
                xyxy = boxes.xyxy[idx]
                x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
                width, height = x2 - x1, y2 - y1

                # Convert Tensor data to Python types for serialization
                bounding_box_data.append({
                    'class': class_name,
                    'x': float(x1), 'y': float(y1),
                    'width': float(width), 'height': float(height)
                })
            im_array = result.plot()  # plot a BGR numpy array of predictions

            img = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            # Convert PIL image to numpy array
            img_array = np.asarray(img)

            img_array_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

            _, jpeg = cv2.imencode('.jpg', img_array_bgr)

            # print(classes)
            violations = ''
            if rider_found:
                
                

                if are_images_same(self.previous_frame, img_array):
                    print('skipping same image')
                    continue
                self.previous_frame = img_array

                # Convert color space from RGB to BGR
                img_array_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)

                # Encode the numpy array
                ret, jpeg = cv2.imencode('.jpg', img_array_bgr)
                # ret, jpeg = cv2.imencode('.jpg', img)

                if not ret:
                    continue
                
                # Convert the JPEG frame buffer to base64
                base64_string = base64.b64encode(jpeg).decode('utf-8')
                upload_url = upload_base64_image(base64_string)
                if upload_url is None:
                    continue
                current_datetime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                json_data = {
                    "dateTime": current_datetime,
                    "image": '',
                    "location": 'Mati City',
                    "violations": violations
                }
                print(json_data)
                # Save bounding box data to Firebase Realtime Database
                new_post_ref = ref.push()
                new_post_ref.set(json_data)
                
        if jpeg is None:
            return b''

        previous_bytes = jpeg.tobytes()
        return previous_bytes

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()
            pass


def gen(camera):
    while True:
        frame = camera.get_frame()
        
        if not frame:
            # If both current frame and previous frame are not available,
            # yield an empty bytes object
            if camera.previous_bytes:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + camera.previous_bytes + b'\r\n\r\n')
            else:
                yield b''
        else:
            camera.previous_bytes = frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


class StreamView(TemplateView):
    template_name = 'helmdectpages/home.html'


def are_images_same(img1, img2):
    # Check if either of the images is None
    if img1 is None or img2 is None:
        return False  # Images are different if one of them is None

    # Resize images to the same dimensions (if needed)
    if img1.shape != img2.shape:
        img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))

    # Compute Structural Similarity Index (SSI)
    ssim_score = structural_similarity(img1, img1, multichannel=True, channel_axis=-1)

    # If SSI is 1, images are identical
    return ssim_score >= 1

def is_multichannel(image):
    return len(image.shape) == 3 and image.shape[2] > 1

def upload_base64_image(base64_string):
    try:
        # Decode base64 string to bytes
        image_bytes = base64.b64decode(base64_string)
        
        current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        current_date = datetime.now().strftime('%Y-%m-%d')
        
        destination_path = f'images/{current_date}/{current_datetime}.jpg'
        
        # Replace 'bucket' with your Firebase storage bucket reference
        bucket = storage.bucket()
        
        # Create a new file in Firebase storage
        blob = bucket.blob(destination_path)
        
        # Upload the image bytes
        blob.upload_from_string(
            image_bytes,
            content_type='image/jpeg'  # Replace with your image file type
            # You can add more metadata if needed
        )
        
        print('File uploaded successfully!')
        
        # Get the download URL of the uploaded file
        return blob.generate_signed_url(method='GET')
    except Exception as e:
        print(e)
        return None