from django.db import models
from django.core.validators import  MinLengthValidator
# Create your models here.

class Tag(models.Model):
    caption = models.CharField(max_length=40)

    def __str__(self):
        return self.caption


class Author(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=100)


    def author(self):
        return f'{self.first_name} {self.last_name}'
    def __str__(self):
        return self.author()


class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=500)
    image = models.ImageField(upload_to='posts', null=True)
    date = models.DateField(auto_now=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    slug = models.SlugField(unique=True)
    tag = models.ManyToManyField(Tag)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, related_name='posts', null=True)

    def __str__(self):
        return f'{self.title} {self.date}'


class Comment(models.Model):
    user_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')