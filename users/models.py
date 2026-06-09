import os
from django.db import models
from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics/')
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            # Fallback to static default if it is the default image or missing on disk
            if os.path.basename(self.image.name).startswith('default'):
                from django.templatetags.static import static
                return static('blog/default.png')
            try:
                if not os.path.exists(self.image.path):
                     from django.templatetags.static import static
                     return static('blog/default.png')
            except Exception:
                 from django.templatetags.static import static
                 return static('blog/default.png')
            return self.image.url
        from django.templatetags.static import static
        return static('blog/default.png')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Check if the image file exists before trying to open it to prevent FileNotFoundError in production
        if self.image and os.path.exists(self.image.path):
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except Exception:
                pass
