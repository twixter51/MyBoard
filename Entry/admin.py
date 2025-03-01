from django.contrib import admin
from django.utils.html import format_html

from .models import userUploads, userMedia, userTexts

# This class shows images in a table format inside the user's profile page in admin
class userImagesInline(admin.TabularInline):
    model = userMedia       # Connect to our userImages model
    extra = 0                 # Don't show empty slots for new images
    readonly_fields = ('image_preview', 'uploaded_at')  # Make the preview non-editable
    fields = ('image', 'image_preview', 'uploaded_at')  # What fields to show

    # This creates a small preview of the image
    def image_preview(self, obj):
        if obj.image:  # If there is an image
            # Show a small 150x150 preview
            return format_html('<img src="{}" width="150" height="150" style="object-fit: cover;" />', obj.image.url)
        return "No image"  # If no image, show this text
    image_preview.short_description = 'Preview'  # Label for the preview column

# This sets up how the user uploads page looks in admin
@admin.register(userUploads)
class userUploadsAdmin(admin.ModelAdmin):
    # Show these columns: username, when uploaded, how many images
    list_display = ('user', 'uploaded_at', 'get_image_count')
    search_fields = ('user__username',)  # Let admin search by username
    inlines = [userImagesInline]  # Show the user's images below their info



    # Count how many images this user has
    def get_image_count(self, obj):
        return obj.files.count()
    get_image_count.short_description = 'Files'

   
# This sets up how the images list page looks in admin
@admin.register(userMedia)
class userMediaAdmin(admin.ModelAdmin):
    # Show these columns: username, small image preview, upload date
    list_display = ('user_name', 'file_preview_small', 'uploaded_at')
    # Add filters on the right side
    list_filter = ('profile__user', 'uploaded_at')
    # Let admin search by username
    search_fields = ('profile__user__username',)
    
    # Get the username of who uploaded the image
    def user_name(self, obj):
        return obj.profile.user.username
    user_name.short_description = 'User'
    
    # Show a tiny preview of the image in the list
    def file_preview_small(self, obj):
        if obj.content_type == "image":
            # Show a small 50x50 preview
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        elif obj.content_type == "video":
            return "VIDEO"
        return "Neither Video Or Image"
    file_preview_small.short_description = 'Preview'



@admin.register(userTexts)
class userTextAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'uploaded_at')
    search_fields = ('profile__user__username',)
    list_filter = ('profile__user', 'uploaded_at')
  
     # Get the username of who uploaded the image
    def user_name(self, obj):
        return obj.profile.user.username
    user_name.short_description = 'User'