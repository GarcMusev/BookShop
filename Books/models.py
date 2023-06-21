from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings


class Book(models.Model):
    BOOK_TYPES = [
        ('H', 'Hardcover'),  # Datenbank Wert und lesbare Form
        ('P', 'Paperback'),
        ('E', 'E-book'),
        ('A', 'Audio book'),
    ]

    BOOK_GENRES = [
        ('A', 'Adventure'),
        ('C', 'Classic'),
        ('CO', 'Comic'),
        ('D', 'Detective'),
        ('M', 'Mystery'),
        ('F', 'Fantasy'),
        ('H', 'Horror'),
        ('R', 'Romance'),
        ('SC', 'Science-Fiction'),
        ('TH', 'Thriller'),
        ('B', 'Biographie'),
        ('TC', 'True-Crime'),
        ('P', 'Poetry'),
        ('NF', 'Non-Fiction'),
    ]

    #Definition der Model Klasse mit den jeweiligen Attributen

    title = models.CharField(max_length=100)  # Für Django erstmal die Felder definieren,

    subtitle = models.CharField(max_length=100,  # damit es mit der Datenbank verknüpft werden kann
                                blank=True)

    author = models.CharField(max_length=50)

    genre = models.CharField(max_length=2,
                             choices=BOOK_GENRES,
                             )

    pages = models.IntegerField()  # Must call function to take effect

    date_published = models.DateField(blank=True,
                                      default=date.today,
                                      )

    type = models.CharField(max_length=1,
                            choices=BOOK_TYPES,
                            )

    creation_time = models.DateTimeField(blank=True,
                                         default=timezone.now,
                                         )

    price = models.FloatField(default=0)

    description = models.TextField(max_length=500,
                                   )

    book_picture = models.ImageField(upload_to='book_pictures', blank=True, null=True)

    book_pdf = models.FileField(upload_to='book_pdfs', blank=True, null=True)

    review_rating = models.IntegerField(default=0)

    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='BookUsers',
                             related_query_name='BookUser',
                             )

    class Meta:  #Einstellugen für die DjangoApp Book
        ordering = ['title', '-type']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def get_full_title(self):
        return_string = self.title  #Mit self. kann man auf die Attribute zugreifen und verändern
        if self.subtitle:  # if subtitle is not empty
            return_string = self.title + ': ' + self.subtitle
        return return_string

    def set_pages_to_zero(self):
        if self.type == 'A':
            self.pages = 0
        self.save()

    def __str__(self):
        return self.title + ' (' + self.author + ')'

    def __repr__(self):
        return self.get_full_title() + ' / ' + self.author + ' / ' + self.type


class Review(models.Model):

    REVIEW_STARS = [
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    ]

    text = models.TextField(max_length=500)

    timestamp = models.DateTimeField(auto_now_add=True)

    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    book = models.ForeignKey(Book, on_delete=models.CASCADE)

    star_rating = models.IntegerField(choices=REVIEW_STARS)

    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def get_review_prefix(self):
        if len(self.text) > 50:
            return self.text[:50] + '...'
        else:
            return self.text

    def get_bookid_from_review(self):
        return self.book_id

    def get_upvotes(self):
        upvotes = Voting.objects.filter(up_or_down='U',
                                        review=self)
        return upvotes

    def get_upvotes_count(self):
        return len(self.get_upvotes())

    def get_downvotes(self):
        downvotes = Voting.objects.filter(up_or_down='D',
                                          review=self)
        return downvotes

    def get_downvotes_count(self):
        return len(self.get_downvotes())

    def vote(self, myuser, up_or_down):
        U_or_D = 'U'
        if up_or_down == 'down':
            U_or_D = 'D'

        if Voting.objects.filter(myuser=myuser, review=self, up_or_down=U_or_D, book=self.book).exists():
            Voting.objects.filter(myuser=myuser, review=self, up_or_down=U_or_D, book=self.book).delete()
        else:
            U_or_D2 = 'D'
            if up_or_down == 'down':
                U_or_D2 = 'U'
            Voting.objects.filter(myuser=myuser, review=self, up_or_down=U_or_D2, book=self.book).delete()
            print('username', myuser.username)
            print('review id', self.id)
            vote = Voting.objects.create(up_or_down=U_or_D,
                                   myuser=myuser,
                                   review=self,
                                   book=self.book
                                   )
        print('voting successfully finished')

    def __str__(self):
        return self.get_review_prefix() + ' (' + self.myuser.username + ')'

    def __repr__(self):
        return self.get_review_prefix() + ' (' + self.myuser.username + ' / ' + str(self.timestamp) + ')'


class Voting(models.Model):
    VOTING_TYPES = [
        ('U', 'up'),
        ('D', 'down'),
    ]

    up_or_down = models.CharField(max_length=1,
                                  choices=VOTING_TYPES,
                                  )
    timestamp = models.DateTimeField(auto_now_add=True)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)

    def getUpDown(self):
        return self.up_or_down

    def __str__(self):
        return self.up_or_down + ' on ' + self.review.text + ' by ' + self.myuser.username
