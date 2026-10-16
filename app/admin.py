from django.contrib import admin

from .models import (
    SiteSettings,
    Plan,
    Testimonial,
    Feedback,
    AddOn,
    PricingPlan,
    FAQ,
    Question,
    ContactMessage,
)


# ================================================================
# Site Settings (singleton)
# ================================================================
@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Branding', {
            'fields': ('logo', 'logo_alt')
        }),
        ('Images', {
            'fields': ('hero_image', 'hero_image_alt',
                       'about_image', 'about_image_alt')
        }),
        ('Copy', {
            'fields': ('tagline', 'footer_note')
        }),
        ('Contact', {
            'fields': ('contact_email', 'contact_phone', 'contact_phone_raw',
                       'address_line_1', 'address_line_2')
        }),
        ('Office Hours', {
            'fields': ('hours_weekday', 'hours_saturday', 'hours_sunday')
        }),
        ('Social Links', {
            'fields': ('instagram_url', 'facebook_url', 'tiktok_url', 'whatsapp_url'),
            'description': 'Leave a field blank to hide that icon from the footer.'
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


# ================================================================
# Home page content
# ================================================================
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'speed_value', 'price_value', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author', 'is_active', 'order')
    list_editable = ('is_active', 'order')


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'message', 'created_at')

    def has_add_permission(self, request):
        return False


# ================================================================
# Services & Pricing
# ================================================================
@admin.register(AddOn)
class AddOnAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_value', 'price_unit', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('name',)


@admin.register(PricingPlan)
class PricingPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price_value', 'is_featured', 'is_active', 'order')
    list_editable = ('is_featured', 'is_active', 'order')
    list_filter = ('category', 'is_active', 'is_featured')
    search_fields = ('name',)


# ================================================================
# FAQ page
# ================================================================
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    search_fields = ('question', 'answer')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('subject',)
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')

    def has_add_permission(self, request):
        return False


# ================================================================
# Contact page
# ================================================================
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'phone', 'created_at')
    list_filter = ('subject',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'message')

    def has_add_permission(self, request):
        return False