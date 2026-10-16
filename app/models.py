from django.db import models
from cloudinary.models import CloudinaryField


class SiteSettings(models.Model):
    # Branding
    logo = CloudinaryField('logo', blank=True, null=True,
                           help_text='PNG logo used in navbar and footer')
    logo_alt = models.CharField(max_length=100, default='gofaiba')

    # Hero / about images
    hero_image = CloudinaryField('hero image', blank=True, null=True)
    hero_image_alt = models.CharField(max_length=150, default='Fast, reliable internet')
    about_image = CloudinaryField('about image', blank=True, null=True)
    about_image_alt = models.CharField(max_length=150, default='Our team at work')

    # Tagline
    tagline = models.TextField(
        default=('Fast, reliable internet backed by people who actually pick up the phone. '
                 'Serving homes and businesses with fibre, DSL and enterprise-grade connectivity.')
    )
    footer_note = models.CharField(max_length=150, default='Built for speed. Backed by people.')

    # Contact
    contact_email = models.EmailField(default='hello@gofaiba.co.ke')
    contact_phone = models.CharField(max_length=30, default='+254 712 11 11 22')
    contact_phone_raw = models.CharField(
        max_length=30, default='+254712111122',
        help_text='Digits only, no spaces — used for the tel: link'
    )
    address_line_1 = models.CharField(max_length=150, default='14th Floor, Beaumont House')
    address_line_2 = models.CharField(max_length=150, default='Kenyatta Avenue, Nairobi')
        # Office hours
    hours_weekday = models.CharField(max_length=100, default='Mon–Fri · 8am – 6pm')
    hours_saturday = models.CharField(max_length=100, default='Saturday · 9am – 2pm')
    hours_sunday = models.CharField(max_length=100, default='Sunday · Closed')

    # Socials (blank = hidden)
    instagram_url = models.URLField(blank=True)
    facebook_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    whatsapp_url = models.URLField(blank=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return 'Site Settings'

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj


class Plan(models.Model):
    name = models.CharField(max_length=100)
    speed_value = models.CharField(max_length=20)
    speed_unit = models.CharField(max_length=20, default='Mbps')
    price_value = models.CharField(max_length=50)
    price_unit = models.CharField(max_length=20, default='/ month')
    features = models.TextField(help_text='One feature per line')
    cta_text = models.CharField(max_length=50, default='Choose Plan')
    cta_url = models.CharField(max_length=200, default='#contact')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]


class Testimonial(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.author


class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Feedback from {self.name}'

class AddOn(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_value = models.CharField(max_length=50)
    price_unit = models.CharField(max_length=20, default='/ month')
    icon = models.CharField(
        max_length=60, default='bi-wifi',
        help_text='Bootstrap Icons class, e.g. bi-wifi, bi-camera-video-fill'
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class PricingPlan(models.Model):
    CATEGORY_CHOICES = [
        ('home', 'Home Fibre'),
        ('business', 'Business Internet'),
    ]

    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    name = models.CharField(max_length=100)
    speed_value = models.CharField(max_length=20)
    speed_unit = models.CharField(max_length=20, default='Mbps')
    price_value = models.CharField(max_length=50)
    price_unit = models.CharField(max_length=20, default='/ month')
    features = models.TextField(help_text='One feature per line')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['category', 'order']

    def __str__(self):
        return f'{self.get_category_display()} — {self.name}'

    def feature_list(self):
        return [f.strip() for f in self.features.splitlines() if f.strip()]
    
class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class Question(models.Model):
    SUBJECT_CHOICES = [
        ('coverage', 'Coverage & availability'),
        ('plans', 'Plans & pricing'),
        ('installation', 'Installation'),
        ('support', 'Support & troubleshooting'),
        ('business', 'Business solutions'),
        ('other', 'Something else'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.get_subject_display()}'

class ContactMessage(models.Model):
    SUBJECT_CHOICES = [
        ('home', 'Home Fibre'),
        ('business', 'Business Internet'),
        ('dedicated', 'Dedicated Lines'),
        ('support', 'Support & troubleshooting'),
        ('moving', 'Moving house'),
        ('other', 'Something else'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.get_subject_display()}'