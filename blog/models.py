from django.db import models
from django.utils.text import slugify
from user_profile.models import User
from ckeditor.fields import RichTextField

class Category(models.Model):
    title = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Tag(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(null=True, blank=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Blog(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_blogs',
        on_delete=models.CASCADE, 
        null=True
    )
    category = models.ForeignKey(
        Category,
        related_name='category_blogs',
        on_delete=models.CASCADE, 
        null=True
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tag_blogs',
        blank=True
    )
    likes = models.ManyToManyField(
        User,
        related_name='user_likes',
        blank=True
    )

    title = models.CharField(
        max_length=250
    )
    slug = models.SlugField(max_length=150, null=True, blank=True)
    banner = models.ImageField(upload_to='blog_banners')
    description = RichTextField()
    created_date = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    

class Comment(models.Model):
    user = models.ForeignKey(
        User,
        related_name= 'user_comments',
        on_delete=models.CASCADE, 
        null=True
    )
    blog = models.ForeignKey(
        Blog, 
        related_name='blog_comments',
        on_delete=models.CASCADE, 
        null=True
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.text

class Reply(models.Model):
    user = models.ForeignKey(
        User,
        related_name= 'user_replies',
        on_delete=models.CASCADE, 
        null=True
    )
    comment = models.ForeignKey(
        Comment, 
        related_name='comment_reply',
        on_delete=models.CASCADE, 
        null=True
    )
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text