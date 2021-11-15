from django.db import models
from django.contrib.auth.models import User,AbstractUser
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
# Create your models here.

#class User(AbstractUser):
#    is_email_verified = models.BooleanField(default=False)

#    def __str__(self):
#        return self.email

class CustomManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (('draft','Draft'),('published','Published'))
    title = models.CharField(max_length=256)
    slug = models.SlugField(max_length = 256, unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_post')
    body = models.TextField()
    publish = models.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length = 10, choices = STATUS_CHOICES, default = 'draft')
    likes = models.ManyToManyField(User, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(User, blank=True, related_name='dislikes')
    objects = CustomManager()
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title   # instead of object it will print title

    def get_absolute_url(self):
        return reverse('post_detail',
                            args=[self.publish.year,
                                self.publish.strftime('%m'),
                                self.publish.strftime('%d'),
                                self.slug])
# Model related to comment sections
class comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    Name = models.ForeignKey(User,on_delete=models.CASCADE)
    body = models.TextField()
    reply = models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name='replies')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    likes_comment = models.ManyToManyField(User, blank=True, related_name='likes_comment')

    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return 'commented by {} on {}'.format(self.Name,self.post)


from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    GENRE_CHOICES = (('m', 'Masculino'),('f', 'Feminino'))
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='ProfilePic/default.jpg',upload_to='ProfilePic')
    bio = models.TextField()
    gender = models.CharField(max_length=1, choices=GENRE_CHOICES, default='m')
    address = models.CharField(max_length=150, null=True)
    DOB = models.DateField(null=True)
    website_url = models.CharField(max_length=200)
    facebook_url = models.CharField(max_length=200)
    Instagram_url = models.CharField(max_length=200)
    REQUIRED_FIELDS = ['DOB', 'address','gender','user']

    def __str__(self):
        return str(self.user)

    @receiver(post_save, sender=User)
    def update_profile_signal(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()
     
        
class Foo(models.Model):
    x = models.PositiveSmallIntegerField()
    y = models.PositiveSmallIntegerField()
    z = models.PositiveSmallIntegerField()

    score = models.PositiveSmallIntegerField()

    def save(self, *args, **kwargs):
        self.score = self.x + self.y + self.z
        super(Foo, self).save(*args, **kwargs) # Call the "real" save() method.