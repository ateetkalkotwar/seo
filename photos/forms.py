from django import forms

from .models import Person, Photo


class PhotoUploadForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        required=True,
    )

    last_name = forms.CharField(
        max_length=100,
        required=False,
    )

    image = forms.ImageField(
        required=True,
    )

    title = forms.CharField(
        max_length=255,
        required=False,
    )

    description = forms.CharField(
        required=False,
        widget=forms.Textarea,
    )

    def clean_image(self):
        image = self.cleaned_data["image"]

        max_size = 10 * 1024 * 1024

        if image.size > max_size:
            raise forms.ValidationError(
                "Image size must be 10 MB or smaller."
            )

        allowed_types = [
            "image/jpeg",
            "image/png",
            "image/webp",
        ]

        if image.content_type not in allowed_types:
            raise forms.ValidationError(
                "Only JPG, PNG, and WebP images are allowed."
            )

        return image