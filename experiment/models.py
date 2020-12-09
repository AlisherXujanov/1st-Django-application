from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from PIL import Image


class Book(models.Model):
    author = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, help_text='The name of Book')
    genre = models.CharField(max_length=50, blank=True,
                             help_text="Genre of Book")
    image = models.ImageField(default='book.jpg', upload_to='book_img')
    title = models.CharField(max_length=100)
    intro = models.CharField(max_length=300, blank=True,
                             help_text='What is the Book about?')
    content = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    class META:
        ordering = ['date_created']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.name} by ({self.author.username})'

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('book-detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 700 or img.width > 700:
            output_size = (700, 700)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Task(models.Model):
    title = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['completed', 'date']
