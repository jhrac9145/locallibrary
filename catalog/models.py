import uuid  # Required for unique book instances

from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns


class Genre(models.Model):

    """ Model representing a book genre. """

    name = models.CharField(
        max_length=200, help_text="Enter a book genre (e.g. Science Fiction)"
    )

    def __str__(self):

        """ String for representing the Model object. """

        return self.name

class Price(models.Model):
    value = models.IntegerField()

    def __str__(self):
        return str(self.value)

class Book(models.Model):

    """ Model representing a book (but not a specific copy of a book). """

    title = models.CharField(max_length=200)
    author = models.ForeignKey("Author", on_delete=models.SET_NULL, null=True)
    summary = models.TextField(
        max_length=1000, help_text="Enter a brief description of the book"
    )
    isbn = models.CharField(
        "ISBN",
        max_length=13,
        help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>',
    )
    genre = models.ManyToManyField("Genre", help_text="Select a genre for this book")
    value = models.ForeignKey("Price", on_delete=models.SET_NULL, null=True)

    CHOICE_LANGUAGE = (
        ("af", "Afrikaans"),
        ("ar", "Arabic"),
        ("az", "Azeri (Latin)"),
        ("be", "Belarusian"),
        ("bg", "Bulgarian"),
        ("ca", "Catalan"),
        ("cs", "Czech"),
        ("cy", "Welsh"),
        ("da", "Danish"),
        ("de", "German"),
        ("dv", "Divehi"),
        ("el", "Greek"),
        ("en", "English"),
        ("eo", "Esperanto"),
        ("es", "Spanish"),
        ("et", "Estonian"),
        ("eu", "Basque"),
        ("fa", "Farsi"),
        ("fi", "Finnish"),
        ("fo", "Faroese"),
        ("fr", "French"),
        ("gl", "Galician"),
        ("gu", "Gujarati"),
        ("he", "Hebrew"),
        ("hi", "Hindi"),
        ("hr", "Croatian"),
        ("hu", "Hungarian"),
        ("hy", "Armenian"),
        ("id", "Indonesian"),
        ("is", "Icelandic"),
        ("it", "Italian"),
        ("ja", "Japanese"),
        ("ka", "Georgian"),
        ("kk", "Kazakh"),
        ("kn", "Kannada"),
        ("ko", "Korean"),
        ("ky", "Kyrgyz"),
        ("lt", "Lithuanian"),
        ("lv", "Latvian"),
        ("mi", "Maori"),
        ("mk", "FYRO Macedonian"),
        ("mn", "Mongolian"),
        ("mr", "Marathi"),
        ("ms", "Malay"),
        ("mt", "Maltese"),
        ("nb", "Norwegian"),
        ("nl", "Dutch"),
        ("ns", "Northern Sotho"),
        ("pa", "Punjabi"),
        ("pl", "Polish"),
        ("ps", "Pashto"),
        ("pt", "Portuguese"),
        ("qu", "Quechua"),
        ("ro", "Romanian"),
        ("ru", "Russian"),
        ("sa", "Sanskrit"),
        ("se", "Sami (Northern)"),
        ("sk", "Slovak"),
        ("sl", "Slovenian"),
        ("sq", "Albanian"),
        ("sv", "Swedish"),
        ("sw", "Swahili"),
        ("ta", "Tamil"),
        ("te", "Telugu"),
        ("th", "Thai"),
        ("tl", "Tagalog"),
        ("tn", "Tswana"),
        ("tr", "Turkish"),
        ("tt", "Tatar"),
        ("ts", "Tsonga"),
        ("uk", "Ukrainian"),
        ("ur", "Urdu"),
        ("uz", "Uzbek (Latin)"),
        ("vi", "Vietnamese"),
        ("xh", "Xhosa"),
        ("zh", "Chinese"),
        ("zu", "Zulu"),
    )
    language = models.CharField(
        max_length=2,
        choices=CHOICE_LANGUAGE,
        blank=True,
        default="ko",
        help_text="Book Language",
    )

    def __str__(self):

        """ String for representing the Model object. """

        return self.title

    def get_absolute_url(self):

        """ Returns the url to access a detail record for this book. """

        return reverse("book-detail", args=[str(self.id)])


class BookInstance(models.Model):

    """ Model representing a specific copy of a book (i.e. that can be borrowed from the library). """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this particular book across whole library",
    )
    book = models.ForeignKey("Book", on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ("m", "Maintenance"),
        ("o", "On loan"),
        ("a", "Available"),
        ("r", "Reserved"),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default="m",
        help_text="Book availability",
    )

    class Meta:
        ordering = ["due_back"]

    def __str__(self):

        """ String for representing the Model object. """

        return f"{self.id} ({self.book.title})"


class Author(models.Model):

    """ Model representing an author. """

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField("Died", null=True, blank=True)

    class Meta:
        ordering = ["last_name", "first_name"]

    def get_absolute_url(self):

        """ Returns the url to access a particular author instance. """

        return reverse("author-detail", args=[str(self.id)])

    def __str__(self):

        """ String for representing the Model object. """

        return f"{self.last_name}, {self.first_name}"

