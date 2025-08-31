from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
from django.utils import timezone
from datetime import timedelta
import secrets
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import stripe
from django.conf import settings
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

#test
from .cd import createCD, getCD

from django.contrib.auth.decorators import login_required
from .models import users, userMedia, userTexts
from django.views.decorators.csrf import csrf_exempt
####################################################


from django.template import loader


#FIX

@login_required
def upload_media(request):
    if request.method == 'POST':
    
        file = request.FILES.get('image') or request.FILES.get('video')
        print(file)
        profile = request.user.users

        if request.FILES.get('image'):
            content = "image";  

            try:
            # Get or create user profile
                fileCreate = userMedia.objects.create(
                    profile=profile,
                    file = file,
                    content_type = content
                )
                return JsonResponse({
                    'success': True,
                    'image_url': fileCreate.file.url,
                    "id": fileCreate.id,
                    "size": round(fileCreate.file_size / (1024 * 1024), 2)
                })
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })      
        elif request.FILES.get('video'):
            content = "video";  
            try:
                fileCreate = userMedia.objects.create(profile = profile, file = file, content_type = content )
                return JsonResponse({
                    'success': True,
                    'video_url': fileCreate.file.url,
                    "id": fileCreate.id,
                    "size": round(fileCreate.file_size / (1024 * 1024), 2)
                })
            
            except Exception as e:
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })      
    return JsonResponse({
        'success': False,
        'error': 'No image provided'
    })


@login_required
def upload_text(request):
    # when user uploads text or messages
    
    if request.method == 'POST':
        try:

            profile = request.user.users
            messageCont = request.POST.get('text')
            
          
            if messageCont:
                textCont = userTexts.objects.create(profile=profile, message=messageCont)

                return JsonResponse({
                    'success': True,
                    'id': textCont.id,
                    'message': messageCont
                })
        
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
        



    return JsonResponse({
        'success': False,
        'error': 'Invalid request'
    })





@login_required
def remove_content(request):

    if request.method == "POST":
        profile = request.user.users
        content_id = request.POST.get("file") or request.POST.get("text")
        file = None
        if content_id == request.POST.get("file"):
            file = userMedia.objects.get(id=content_id)
           
        elif content_id == request.POST.get("text"):
            file = userTexts.objects.get(id=content_id)
            file.delete()
            return JsonResponse({'success': True, 'storage_left':profile.storage})
        else:
            return JsonResponse({'success': False})
        
        size = round(file.file_size / (1024 * 1024), 2)
        updateSTOR = users.objects.get(user=profile.user)
      
        updateSTOR.storage += size
      
        updateSTOR.save()
        file.delete()
        return JsonResponse({'success': True, 'storage_left':updateSTOR.storage})


             




def Main(request, boardLink):

    
    
    owner_profile = get_object_or_404(users, uniLink=boardLink)
    viewer_profile = request.user.users if request.user.is_authenticated else None
    is_owner = (
        request.user.is_authenticated
        and request.user.id == owner_profile.user_id
    )
    is_guest =  request.user.is_authenticated and owner_profile.is_guest
    is_premium = owner_profile.is_premium
    session_is_expired = owner_profile.is_expired

    files = userMedia.objects.filter(profile=owner_profile).order_by('uploaded_at')
    texts = userTexts.objects.filter(profile=owner_profile).order_by('uploaded_at')



    storedTexts = []
    storedFiles = []

    for text in texts:
        storedTexts.append({
            'type': 'text',
            'content': text.message,
            'timestamp': text.uploaded_at.isoformat(),
            'id': text.id
        })


    for file in files:
        if file.content_type == "video":
            key = "video"
        else:
            key = "image"
        storedFiles.append({
            'type' : 'file',
            'key' : key,
            'content' : file.file.url,
            'timestamp': file.uploaded_at.isoformat(),
            'id' : file.id
        })


    storedTexts.sort(key=lambda x: x['timestamp'])
    storedFiles.sort(key=lambda x: x['timestamp'])

    if owner_profile.is_guest:
        time_left = owner_profile.time_left_dictionary
    else:
        time_left = {"seconds":1, "minutes":1, "hours": 1}
    context = {
        'storedTexts': storedTexts,
        'storedFiles' : storedFiles,
        'profile' : viewer_profile,
        'profile2': owner_profile,
        'is_owner': is_owner,
        'is_guest': is_guest,
        'time_left': time_left,
        'storage_left': owner_profile.storage,
        'is_premium': is_premium,
        'is_expired': session_is_expired,
    }
    
    template = loader.get_template("main/creation.html")    
    return HttpResponse(template.render(context, request))
    
   



def index(request):
    template = loader.get_template("entries/index.html")
    context = {}  


    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password']

    
        user = authenticate(request, username=username, password=password1)

        if user is not None:
             login(request, user)
             return render(request, 'entries/home.html', {'username': username})
        else:
            context['error'] ="ah"
            return render(request, 'entries/index.html', context)

    return HttpResponse(template.render(context, request))



def create_guest(request):
    

    guestName =  f"guest_{secrets.token_hex(3)}"
    guestUser = User.objects.create_user(username=guestName, password=secrets.token_urlsafe(16))

    p = guestUser.users

    p.is_guest = True

    p.guest_expires_at = timezone.now() + timedelta(hours=2)

    createCD(request, "guest_cd", p.guest_expires_at)

    # ensure their board slug is set (save calls slugify)
    if not p.uniLink:
        p.uniLink = guestName
    p.save()

    login(request, guestUser)
    return redirect("Main", boardLink=p.uniLink)


def signup(request):

    template = loader.get_template("entries/signup.html")
    context = {} 
    
    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        time = datetime.datetime.now()

        if not username or not password or not email:
            # If any field is missing, pass an error message back to the template
            context['error'] = "All fields are required."
            return render(request, 'entries/signup.html', context)
        
        createduser = User.objects.create_user(username = username, email = email, password = password)

        createduser.save()
        return redirect('/Signup/?success=1')
        
    # In theory, we are getting the success paramater from our url, this way if it does exist pass it through context so html can read it and show us basically our success message
    # leverages the query paramater aka the words after ? in url
    success = request.GET.get('success')
    if success:
        context['success'] = success

    return HttpResponse(template.render(context, request))

    

def log_out_view(request):
   
    logout(request)
    return redirect('home')



def choice_view(request):
    template = loader.get_template("entries/choice.html")

    userAuth = request.user.is_authenticated
    guest_cd = 0
    is_guest = False
    username = "Anon"
    if userAuth:
        guest_cd = getCD(request, "guest_cd")
        is_guest = request.user.users.is_guest
        username = request.user.users.user.username
    print(guest_cd)
    context = {
        'is_authenticated': userAuth,
        'guest_cd': guest_cd,
        'is_guest': is_guest,
        'username': username
    }
    return HttpResponse(template.render(context, request))


     
def home(request):
    template = loader.get_template("entries/home.html")
    context = {}
    return HttpResponse(template.render(context, request))




def update_user(request):
    print("POST payload:", request.POST)
    if request.method == "POST":
        profile = request.user.users
       
        if request.POST.get("update_storage"):
            profile.storage = request.POST["update_storage"]
            profile.save(update_fields=["storage"])
            return JsonResponse({'success': True, 'storage_left':profile.storage})
        return JsonResponse({"success": False, "error": "No value provided"})

    
    return JsonResponse({"success": False, "error": "Wrong method"})


#sales

def premium_sale(request):
    template = loader.get_template("entries/payment.html")
    userAuth = request.user.is_authenticated and not request.user.users.is_guest

    is_guest = request.user.users.is_guest

    context = {
        'is_authenticated': userAuth,
        'is_guest': is_guest,
    }
    return HttpResponse(template.render(context, request))


@require_POST
@csrf_exempt
def create_checkout_session(request):
    """
    Creates a Stripe Checkout Session and returns its URL as JSON.
    Post 'amount' in dollars (string or number). Ex: "0.99"
    """
    username = request.POST.get("full_name")
    email = request.POST.get("email")


    secret = settings.STRIPE_SECRET_KEY
    if not secret:
        return HttpResponseBadRequest("Stripe not configured")
    stripe.api_key = secret

    amount_str = request.POST.get("amount", "0.99")
    try:
        amount_cents = int(round(float(amount_str) * 100))
        if amount_cents < 50:  # optional: minimum 50¢
            return HttpResponseBadRequest("Amount too low.")
    except ValueError:
        return HttpResponseBadRequest("Invalid amount.")

    success_url = getattr(settings, "STRIPE_SUCCESS_URL", "http://127.0.0.1:8000/success/")
    cancel_url  = getattr(settings, "STRIPE_CANCEL_URL",  "http://127.0.0.1:8000/cancel/")


    customer = stripe.Customer.create(
        name=username or None,
        email=email or None,
        metadata={
            "app_username": request.user.users if request.user.is_authenticated else request.POST.get("username", ""),
        }
    )


    session = stripe.checkout.Session.create(
        mode="payment",
        customer=customer.id,
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "MyBoard Premium"},
                "unit_amount": amount_cents
            },
            "quantity": 1
        }],
        success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url=cancel_url,
       
        metadata={
            "username": username,
            "email": email
        },
        payment_intent_data={
            "metadata": {
                "username": username,
                "email": email
            }
        }
    )
    return JsonResponse({"url": session.url})


def checkout_success(request): 
    profile = request.user.users
    profile.is_premium = True
    profile.save(update_fields=["is_premium"])
    profile.storage = 1e9
    profile.save(update_fields=["storage"])
    template = loader.get_template("entries/payment.html")
    print(profile.user.username)
    context = {
       'sale_complete': True,
       'sale_name':profile.user.username 
    }

    return HttpResponse(template.render(context, request))

def checkout_cancel(request):  
    return HttpResponse("❌ Canceled.")