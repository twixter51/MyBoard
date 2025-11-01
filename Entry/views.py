# pages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import loader
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
import json
# models
from .models import Profile, userMedia, userTexts, User


####################################################


# extra (guest cooldown checks)
from .cd import createCD, getCD
import secrets
from django.conf import settings

# time
import datetime
from django.utils import timezone
from datetime import timedelta

# for stripe
import stripe
import logging
stripe.api_key = settings.STRIPE_API_KEY
logger = logging.getLogger(__name__)




######################## web page views    # reference this for rest of the functions in the future when cleaning up    --web page views    
def home(request):
    context = {
        
    }

    if request.user.is_authenticated:
        profile = request.user.profile
        is_authenticated = request.user.is_authenticated
    
        if profile.is_expired and profile.is_guest:
            context["is_expired"] = profile.is_expired
        if profile.is_premium and profile.premium_expires_at:
            context["time_left"] = profile.time_left_dictionary

        context["is_premium"] = profile.is_premium
        context["is_authenticated"] = is_authenticated
        context["username"] = profile.user.username
        
        
    template = loader.get_template("entries/home.html")

    return HttpResponse(template.render(context, request))


def log_in(request):
    template = loader.get_template("entries/login.html")
    context = {}  


    if request.method == "POST":
        username = request.POST['username']
        password1 = request.POST['password']

    
        user = authenticate(request, username=username, password=password1)

        if user is not None:
            login(request, user) 
            return redirect('home')
        else:
            context['error'] ="wrong credentials!"
            return render(request, 'entries/login.html', context)

    return HttpResponse(template.render(context, request))

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

            fields = []
            context['error'] = "ERROR! missing fields"
            if not username:
                fields.append("username")
            if not password:
                fields.append("password")
            if not email:
                fields.append("email")
              
            context['fields'] = json.dumps(fields)
            return render(request, 'entries/signup.html', context)
        
        #this creates a user in my database "Profile" wit only USERNAME while "User" djangos model has email/
        createduser = User.objects.create_user(username = username, email = email, password = password)
        createduser.email = email

        #if user was guest before signing up
        if request.user.is_authenticated:
            if request.user.profile.is_guest:
                guest_user  = request.user
                userMedia.objects.filter(profile=request.user.profile).update(profile=createduser.profile)

                userTexts.objects.filter(profile=request.user.profile).update(profile=createduser.profile)

                createduser.profile.storage = request.user.profile.storage
                
                login(request, createduser)
                guest_user.delete()

        #log in if not already
        if not request.user.is_authenticated:
            login(request, createduser)

        return redirect('/signup/?success=1')
        
  
    success = request.GET.get('success')
    if success:
        context['success'] = success

    return HttpResponse(template.render(context, request))

@never_cache
def choice_view(request):
    template = loader.get_template("entries/choice.html")

    userAuth = request.user.is_authenticated
    guest_cd = 0
    is_guest = False
    username = "Anon"
    is_expired = False
    if userAuth:
        guest_cd = getCD(request, "guest_cd")
        is_guest = request.user.profile.is_guest
        username = request.user.profile.user.username
        is_expired = is_guest and request.user.profile.is_expired
    print(guest_cd)
    context = {
        'is_authenticated': userAuth,
        'guest_cd': guest_cd,
        'is_guest': is_guest,
        'username': username,
        'is_expired': is_expired,
    }
    return HttpResponse(template.render(context, request))



@never_cache
def account_view(request):
    template = loader.get_template("entries/account.html")

    userAuth = request.user.is_authenticated
    guest_cd = 0
    is_guest = False
    username = "Anon"
    is_expired = False
    time_left =  request.user.profile.time_left_dictionary
    if userAuth:
        guest_cd = getCD(request, "guest_cd")
        is_guest = request.user.profile.is_guest
        username = request.user.profile.user.username
        is_expired = is_guest and request.user.profile.is_expired
        is_premium =  request.user.profile.is_premium
        ending_premium = request.user.profile.ending_premium
    print(guest_cd)
    context = {
        'is_authenticated': userAuth,
        'guest_cd': guest_cd,
        'is_guest': is_guest,
        'username': username,
        'is_expired': is_expired,
        'is_premium': is_premium,
        'time_left': time_left,
        'ending_premium': ending_premium,
    }
    return HttpResponse(template.render(context, request))

###################### end web page views


########################## guest features and logout
def create_guest(request):
    

    guestName =  f"guest_{secrets.token_hex(3)}"
    guestUser = User.objects.create_user(username=guestName, password=secrets.token_urlsafe(16))

    p = guestUser.profile

    p.is_guest = True

    p.guest_expires_at = timezone.now() + timedelta(seconds=5)

    createCD(request, "guest_cd", p.guest_expires_at)

    # ensure their board slug is set (save calls slugify)
    if not p.uniLink:
        p.uniLink = guestName
    p.save()

    login(request, guestUser)
    return redirect("Main", boardLink=p.uniLink)

def log_out_view(request):
   
    profile = request.user.profile

    if profile.is_guest:
        profile.delete()
    logout(request)
    return redirect('home')

##################### end guest features and logout


   


#################### sales
@never_cache
def sale_page(request):
    template = loader.get_template("entries/payment.html")
    userAuth = False
    is_guest = False
    is_premium = False
    time_left = False
    if request.user.is_authenticated:

        userAuth = request.user.is_authenticated and not request.user.profile.is_guest

        is_guest = request.user.profile.is_guest

        is_premium = request.user.profile.is_premium

        time_left = request.user.profile.time_left_dictionary

    context = {
        'is_authenticated': userAuth,
        'is_guest': is_guest,
        'is_premium': is_premium,
        'time_left': time_left,
    }
    return HttpResponse(template.render(context, request))



@csrf_exempt
def create_checkout_session(request):
    """
    Creates a Stripe Checkout Session 
    Post 'amount' in dollars (string or number). Ex: "0.99"
    """
    
    user_id = str(request.user.id)

    session = stripe.checkout.Session.create(
        mode="subscription",
        line_items=[{
            "price": "price_1S59MeJJVQIXKbuJlR5LHHDy",  # replace with your Price ID
            "quantity": 1,
        }],
        success_url=settings.STRIPE_SUCCESS_URL,
        cancel_url=settings.STRIPE_CANCEL_URL,
        customer_email=request.user.email,
        client_reference_id=user_id,   # ties session to Django user
    )

    return redirect(session.url)


def checkout_success(request): 

    # to show user that they are premium now, to update their intermediate view that redirects them
    userAuth = False
    is_guest = False
    is_premium = False
    if request.user.is_authenticated:

        userAuth = request.user.is_authenticated and not request.user.profile.is_guest

        is_guest = request.user.profile.is_guest

        is_premium = request.user.profile.is_premium

    template = loader.get_template("entries/payment.html")
 
    context = {
       'sale_complete': True,
       'sale_name':request.user,
       'is_authenticated': userAuth,
       'is_guest': is_guest,
       'is_premium': is_premium,
    }

    return HttpResponse(template.render(context, request))



def cancel_sub(request):
    profile = request.user.profile
   
    if profile.is_premium and profile.stripe_subscription_id:
        sub = profile.stripe_subscription_id
        stripe.Subscription.modify(sub, cancel_at_period_end=True)
        profile.ending_premium = True

        profile.save()
    return redirect('home')

    


def checkout_cancel(request):  
    return HttpResponse("Canceled.")


#webhook for payments
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None
    sub_ID = None
    cus_ID = None
    profile1 = None
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError as e:
        print('⚠️  Webhook signature verification failed.' + str(e))

        return HttpResponse(status=400)
    eventType = event.get("type")
    obj = (event.get("data") or {}).get("object") or {}

 

    if eventType == "checkout.session.completed":
        #complete checkout



        if obj.get("mode") != "subscription":
            logger.warning("Mode error: %s",  obj.get("mode"))
            return HttpResponse(status=200)
        sub_id = obj.get("subscription")
        if not sub_id:
            logger.warning("id error: %s",  obj.get(obj.get("subscription")))
            return HttpResponse(status=200)

        sub = stripe.Subscription.retrieve(sub_id)

        
        user_id = obj.get("client_reference_id")

        user = User.objects.filter(id=user_id).first()



        profile1 = user.profile 
        profile1.stripe_subscription_id = sub_id
        profile1.stripe_customer_id = obj["customer"]

       

    elif eventType == "invoice.payment_succeeded":
        #complete billing cycle


        cus_ID = obj.get("customer")
        sub_ID = obj.get("subscription")

        if not sub_ID:
            logger.warning("no sub%s", sub_ID)

            subs = stripe.Subscription.list(customer=cus_ID, status="all", limit=1)

            if subs.data:
                sub_ID = subs.data[0].id
            else:
                logger.warning("No subscription found for customer=%s", cus_ID)
                return HttpResponse(status=200)
        try:
            sub = stripe.Subscription.retrieve(sub_ID)
        except Exception as e:

            logger.warning("can't retreive sub %s", sub)
            return HttpResponse(status=200)
        
      

        current_period_end = sub.get("current_period_end")
        if not current_period_end:
            logger.warning("curr period end errorr %s",  sub.get("current_period_end"))

            current_period_end = obj["lines"]["data"][0]["period"]["end"]
    
        
        profile1 = Profile.objects.filter(stripe_customer_id=cus_ID).first()

        profile1.is_premium = True
        profile1.premium_expires_at = datetime.datetime.fromtimestamp(current_period_end, tz=datetime.timezone.utc)
        profile1.storage = 1e9
        

        if profile1.stripe_subscription_id == sub_ID:
            profile1.premium_expires_at = datetime.datetime.fromtimestamp(current_period_end, tz=datetime.timezone.utc)    

    elif eventType == "customer.subscription.deleted":
        #complete removed subscription
        cus_ID = obj["customer"]
        profile1 = Profile.objects.filter(stripe_customer_id=cus_ID).first()


        if profile1:
            profile1.is_premium = False
            profile1.premium_expires_at = None
            profile1.storage = 25*1024
            if profile1.ending_premium:
                profile1.ending_premium = False

    if profile1:
        profile1.save(update_fields=["is_premium", "premium_expires_at", "storage", "stripe_subscription_id", "stripe_customer_id"])
    return HttpResponse(status=200)

############################### end sales




############################################# MAIN APP
def Main(request, boardLink):


    owner_profile = get_object_or_404(Profile, uniLink=boardLink)
    viewer_profile = request.user.profile if request.user.is_authenticated else None
    is_owner = (
        request.user.is_authenticated
        and request.user.id == owner_profile.user_id
    )
    is_guest =  request.user.is_authenticated and owner_profile.is_guest
    
   
    


    is_premium = owner_profile.is_premium
    if viewer_profile:
        session_is_expired = viewer_profile.is_expired
    else:
        session_is_expired = False

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
    if viewer_profile.is_premium:
        time_left = viewer_profile.time_left_dictionary
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



@login_required
def upload_media(request):
    if request.method == 'POST':
    
        file = request.FILES.get('image') or request.FILES.get('video')
        print(file)
        profile = request.user.profile

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

            profile = request.user.profile
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
        profile = request.user.profile
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
        updateSTOR = profile
      
        updateSTOR.storage += size
      
        updateSTOR.save()
        file.delete()
        return JsonResponse({'success': True, 'storage_left':updateSTOR.storage})



############################################# MAIN APP







# extra update user storage
def update_user(request):
    print("POST payload:", request.POST)
    if request.method == "POST":
        profile = request.user.profile
       
        if request.POST.get("update_storage"):
            profile.storage = request.POST["update_storage"]
            profile.save(update_fields=["storage"])
            return JsonResponse({'success': True, 'storage_left':profile.storage})
        return JsonResponse({"success": False, "error": "No value provided"})

    
    return JsonResponse({"success": False, "error": "Wrong method"})

########### end extra

