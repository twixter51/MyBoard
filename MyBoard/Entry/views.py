from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


#test

from django.contrib.auth.decorators import login_required
from .models import userUploads, userMedia, userTexts
from django.views.decorators.csrf import csrf_exempt
####################################################


from django.template import loader



#FIX

@login_required
def upload_media(request):
    if request.method == 'POST':
    
        file = request.FILES.get('image') or request.FILES.get('video')
        print(file)
        profile = request.user.useruploads

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
                    'image_url': fileCreate.file.url
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
                    'video_url': fileCreate.file.url
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

            profile = request.user.useruploads
            messageCont = request.POST.get('text')
            
          
            if messageCont:
                textCont = userTexts.objects.create(profile=profile, message=messageCont)

                return JsonResponse({
                    'success': True,
                    'text_id': textCont.id,
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
def Main(request):
    profile = request.user.useruploads
 
    if not request.user.is_authenticated: 
        return redirect('login')  

    if request.user.is_authenticated:
        files = userMedia.objects.filter(profile=profile).order_by('uploaded_at')
        texts = userTexts.objects.filter(profile=profile).order_by('uploaded_at')

        storedTexts = []
        storedFiles = []

        for text in texts:
            storedTexts.append({
                'type': 'text',
                'content': text.message,
                'timestamp': text.uploaded_at.isoformat()
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
            })

        storedTexts.sort(key=lambda x: x['timestamp'])
        storedFiles.sort(key=lambda x: x['timestamp'])

        context = {
            'storedTexts': storedTexts,
            'storedFiles' : storedFiles,
            'profile' : profile
        }
        
        template = loader.get_template("main/creation.html")
        return HttpResponse(template.render(context, request))
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
     
   
def board(request):
    return HttpResponse("Welcome To Your Board!")


def home(request):
    template = loader.get_template("entries/home.html")
    context = {}
    return HttpResponse(template.render(context, request))



