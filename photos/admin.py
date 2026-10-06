from django.contrib import admin

from .models import Person, Photo


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = (
        "display_name",
        "first_name",
        "last_name",
        "created_at",
    )

    search_fields = (
        "first_name",
        "last_name",
        "display_name",
    )

    prepopulated_fields = {
        "slug": ("display_name",)
    }


@admin.action(description="Approve selected photos")
def approve_photos(modeladmin, request, queryset):
    updated = queryset.update(
        is_published=True
    )

    modeladmin.message_user(
        request,
        f"{updated} photo(s) approved successfully."
    )


@admin.action(description="Reject selected photos")
def reject_photos(modeladmin, request, queryset):
    updated = queryset.update(
        is_published=False
    )

    modeladmin.message_user(
        request,
        f"{updated} photo(s) rejected successfully."
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = (
        "person",
        "title",
        "is_published",
        "created_at",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "person__display_name",
        "title",
        "description",
        "alt_text",
    )

    actions = (
        approve_photos,
        reject_photos,
    )