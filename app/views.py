import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.core.cache import cache
from django.conf import settings
from django.core.mail import send_mail

from .models import (
    SiteSettings,
    Plan,
    Testimonial,
    Feedback,
    AddOn,
    PricingPlan,
    FAQ,
    ContactMessage,
)
from .forms import FeedbackForm, QuestionForm, ContactForm

logger = logging.getLogger(__name__)

CACHE_TTL = 300  # 5 minutes


@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save()
            logger.info("Feedback submitted successfully by user.")

            # Admin Notification
            send_mail(
                subject="New Feedback Submission",
                message=f"New feedback received:\n\n{feedback}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )

            # Auto-reply to User (if email exists on model)
            user_email = getattr(feedback, 'email', None)
            if user_email:
                send_mail(
                    subject="Thank you for your feedback!",
                    message="Hello,\n\nThank you for submitting your feedback. We appreciate your input!\n\nBest regards,\nGo Fiber Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                )

            messages.success(request, 'Thank you! Your feedback has been submitted.')
            return redirect('app:index')
        logger.warning("Invalid feedback form submission.")
    else:
        form = FeedbackForm()

    plans = cache.get_or_set('index_plans', lambda: list(Plan.objects.all()), CACHE_TTL)
    testimonials = cache.get_or_set('index_testimonials', lambda: list(Testimonial.objects.filter(is_active=True)), CACHE_TTL)

    context = {
        'plans': plans,
        'testimonials': testimonials,
        'form': form,
    }
    return render(request, 'index.html', context)


@require_http_methods(["GET"])
def about(request):
    return render(request, 'about.html')


@require_http_methods(["GET"])
def services(request):
    addons = cache.get_or_set('services_addons', lambda: list(AddOn.objects.filter(is_active=True)), CACHE_TTL)
    return render(request, 'services.html', {'addons': addons})


@require_http_methods(["GET"])
def pricing(request):
    home_plans = cache.get_or_set('pricing_home_plans', lambda: list(PricingPlan.objects.filter(category='home', is_active=True)), CACHE_TTL)
    business_plans = cache.get_or_set('pricing_business_plans', lambda: list(PricingPlan.objects.filter(category='business', is_active=True)), CACHE_TTL)
    addons = cache.get_or_set('pricing_addons', lambda: list(AddOn.objects.filter(is_active=True)), CACHE_TTL)

    context = {
        'home_plans': home_plans,
        'business_plans': business_plans,
        'addons': addons,
    }
    return render(request, 'pricing.html', context)


@require_http_methods(["GET", "POST"])
def faq(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save()
            logger.info("New question submitted successfully via FAQ.")

            # Admin Notification
            send_mail(
                subject="New FAQ Question Received",
                message=f"New question submitted:\n\n{question}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )

            # Auto-reply to User (if email exists on model)
            user_email = getattr(question, 'email', None)
            if user_email:
                send_mail(
                    subject="We received your question",
                    message="Hello,\n\nThanks for reaching out! We have received your question and will get back to you shortly.\n\nBest regards,\nGo Fiber Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                )

            messages.success(request, 'Thanks — your question has been received.')
            return redirect('app:faq')
        logger.warning("Invalid question form submission on FAQ view.")
    else:
        form = QuestionForm()

    faqs = cache.get_or_set('faq_items', lambda: list(FAQ.objects.filter(is_active=True)), CACHE_TTL)

    context = {
        'faqs': faqs,
        'form': form,
    }
    return render(request, 'faq.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save()
            logger.info("Contact message received.")

            # Admin Notification
            send_mail(
                subject="New Contact Message Received",
                message=f"New contact inquiry:\n\n{contact_msg}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_NOTIFICATION_EMAIL],
                fail_silently=False,
            )

            # Auto-reply to User
            user_email = getattr(contact_msg, 'email', None)
            if user_email:
                send_mail(
                    subject="Thank you for contacting us",
                    message="Hello,\n\nThanks for contacting us! We've received your message and will be in touch shortly.\n\nBest regards,\nGo Fiber Team",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=True,
                )

            messages.success(
                request,
                "Thanks — we've received your message and will be in touch shortly."
            )
            return redirect('app:contact')
        logger.warning("Invalid contact form submission.")
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})


@require_http_methods(["GET"])
def privacy_policy(request):
    logger.info("Privacy policy page visited.")
    return render(request, 'privacy_policy.html')


@require_http_methods(["GET"])
def cookie_policy(request):
    logger.info("Cookie policy page visited.")
    return render(request, 'cookie_policy.html')


def custom_404(request, exception):
    logger.error(f"404 error encountered for path: {request.path}")
    return render(request, '404.html', status=404)