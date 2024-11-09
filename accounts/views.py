from pipes import quote
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from books.models import Book, Author
from users.models import User
from library.models import Loan
from django.conf import settings
from isodate import parse_duration
from googleapiclient.discovery import build

import requests

from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
import wikipedia
import random
from django.core.mail import send_mail
import random
from django.utils import timezone
from datetime import timedelta
from django.utils import timezone


class CustomPasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'login/password_reset_done.html'
 

def generate_otp():
    """Generate a 6-digit OTP."""
    return str(random.randint(100000, 999999))

# Step 1: Password reset request view
def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            otp = generate_otp()
            request.session['otp'] = otp
            request.session['email'] = email  # Store email in session to confirm OTP later
            request.session['otp_generated_time'] = timezone.now().isoformat()  # Store the time OTP was generated

            # Send OTP via email
            send_mail(
                'Password Reset OTP',
                f'Your OTP for resetting the password is {otp}.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'OTP sent to your email.')
            return redirect('password_reset_confirm')
        except User.DoesNotExist:
            messages.error(request, 'No user with this email found.')
            return redirect('password_reset_request')

    return render(request, 'login/password_reset_request.html')



# Step 2: Password reset confirmation view
def password_reset_confirm(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        otp_generated_time_str = request.session.get('otp_generated_time')
        if otp_generated_time_str:
            otp_generated_time = timezone.datetime.fromisoformat(otp_generated_time_str)
            current_time = timezone.now()

            # Check if OTP is older than 2 minutes
            if current_time - otp_generated_time > timedelta(minutes=2):
                messages.error(request, 'OTP has expired. Please request a new one.')
                return redirect('password_reset_request')

        if otp == request.session.get('otp'):
            if password == confirm_password:
                email = request.session.get('email')
                user = User.objects.get(email=email)
                user.set_password(password)
                user.save()
                messages.success(request, 'Password reset successful.')
                return redirect('login')  # Redirect to login after successful reset
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Invalid OTP.')

    return render(request, 'login/password_reset_confirm.html')





def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user based on email and password
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('dashboard')  # Redirect to the dashboard or home page
        else:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'login/login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        roll = request.POST.get('roll')
        department = request.POST.get('department')
        session = request.POST.get('session')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        membership_number = request.POST.get('membership_number')
        user_type = request.POST.get('user_type')
        image = request.FILES.get('image')
        password = request.POST.get('password')

        # Check if the required fields are provided
        if email and user_type:
            user = User(
                email=email,
                name=name,
                roll=roll,
                department=department,
                session=session,
                phone_number=phone_number,
                address=address,
                membership_number=membership_number,
                user_type=user_type,
                image=image,
            )
            user.set_password(password)
            user.save()
            messages.success(request, 'User created successfully.')
            return redirect('login/login')  # Redirect to a success page or another URL
        else:
            messages.error(request, 'Please fill in all required fields.')

    return render(request, 'login/registration.html')

def forgot_password_view(request):
    return render(request, 'login/forgotpassword.html')
def contact(request):
    return render(request, 'includes/contact.html')


@login_required(login_url='login')
def dashboard_view(request):
    total_members = User.objects.filter(user_type='MEM').count()
    total_books = Book.objects.count()
    total_authors = Author.objects.count()
    total_orders = Loan.objects.count()  # Assuming "Order" is represented by Loan
    total_admin = User.objects.filter(user_type='ADM').count()
    total_libraian = User.objects.filter(user_type='LIB').count()

    context = {
        'total_members': total_members,
        'total_books': total_books,
        'total_authors': total_authors,
        'total_orders': total_orders,
        'total_admin': total_admin,
        'total_libraian': total_libraian,
    }

    return render(request, 'admin/dashboard.html', context)

def youtube_search(request):
    videos = []
    if request.method == "POST":
        search_url = 'https://www.googleapis.com/youtube/v3/search'
        video_url = 'https://www.googleapis.com/youtube/v3/videos'

        search_params = {
            'part': 'snippet',
            'q': request.POST['search'],
            'key': settings.YOUTUBE_API_KEY,
            'maxResults': 6,
            'type': 'video',
        }

        video_ids = []
        r = requests.get(search_url, params=search_params)
        results = r.json()['items']
        for result in results:
            video_ids.append(result['id']['videoId'])

        video_params = {
            'part': 'snippet, contentDetails',
            'key': settings.YOUTUBE_API_KEY,
            'id': ','.join(video_ids),
            'maxResults': 6,
        }
        r = requests.get(video_url, params=video_params)
        results = r.json()['items']
        for result in results:
            video_data = {
                'title': result['snippet']['title'],
                'id': result['id'],
                'url': f'https://www.youtube.com/watch?v={result["id"]}',
                'thumbnail': result['snippet']["thumbnails"]['high']['url'],
                'duration': int(parse_duration(result['contentDetails']["duration"]).total_seconds()//60),
            }
            videos.append(video_data)
    context = {
        'videos': videos
    }
    return  render(request, 'youtube/youtube.html', context)




# Your view for Wikipedia search



def wikipedia_search(request):
    results = []
    
    if request.method == "POST":
        search_query = request.POST.get('search', '')

        try:
            # Perform the search using the wikipedia library
            search_results = wikipedia.search(search_query, results=5)  # Limit search to 10 results

            for title in search_results:
                try:
                    page = wikipedia.page(title)
                    result_data = {
                        'title': page.title,
                        'url': page.url,
                        'summary': page.summary[:200],  # First 500 characters of the summary
                        'image': page.images[0] if page.images else None,  # First image if available
                        'dimensions': "Not available"  # Dimensions info might not be available via the API
                    }
                    results.append(result_data)
                except wikipedia.exceptions.PageError:
                    results.append({'error': f'Page not found for "{title}"'})
                except Exception as e:
                    results.append({'error': f'An error occurred while fetching page "{title}": {e}'})

        except wikipedia.exceptions.DisambiguationError as e:
            results.append({'error': f'Disambiguation error: {e}'})
        except Exception as e:
            results.append({'error': f'An error occurred: {e}'})

    context = {
        'results': results
    }
    return render(request, 'wikipedia/wikipedia.html', context)





# Google Books API key from Google Developer Console
GOOGLE_BOOKS_API_KEY = ''

def google_books_search(request):
    books = []

    if request.method == "POST":
        search_query = request.POST.get('search', '')

        if not search_query:
            return render(request, 'google_books/google_books_search.html', {'books': books, 'error': 'No search query provided'})

        # Safely encode the search query
        encoded_query = quote(search_query)

        # API URL for Google Books search
        api_url = f'https://www.googleapis.com/books/v1/volumes?q={encoded_query}&key={GOOGLE_BOOKS_API_KEY}&maxResults=6'

        try:
            # Make a request to Google Books API
            response = requests.get(api_url)

            # Debug: Print the response
            print(f"API Response Status: {response.status_code}")
            print(f"API Response: {response.text}")

            # Check if the response is successful
            if response.status_code == 200:
                search_response = response.json()

                # Check if items key exists in the response
                if 'items' in search_response:
                    # Parse the search results
                    for item in search_response['items']:
                        volume_info = item.get('volumeInfo', {})
                        book_data = {
                            'title': volume_info.get('title', 'No title available'),
                            'authors': ', '.join(volume_info.get('authors', ['Unknown author'])),
                            'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'No image available'),
                            'description': volume_info.get('description', 'No description available'),
                            'infoLink': volume_info.get('infoLink', '#'),
                        }
                        books.append(book_data)
                else:
                    books.append({'error': 'No books found for the search query.'})
            else:
                # Handle unsuccessful API request
                books.append({'error': f'Google Books API error: {response.status_code}'})

        except Exception as e:
            # Handle any other exception
            books.append({'error': f'An error occurred: {e}'})

    context = {
        'books': books
    }
    return render(request, 'google_books/google_books_search.html', context)
