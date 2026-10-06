from django.db import models
from django.utils.text import slugify


class Person(models.Model):
    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100,
        blank=True
    )

    display_name = models.CharField(
        max_length=200,
        blank=True
    )

    slug = models.SlugField(
        max_length=220,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "display_name",
            "first_name",
        ]

    def save(self, *args, **kwargs):
        if not self.display_name:
            self.display_name = " ".join(
                part
                for part in [
                    self.first_name,
                    self.last_name,
                ]
                if part
            ).strip()

        if not self.slug:
            self.slug = slugify(
                self.display_name
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.display_name


class Photo(models.Model):
    person = models.ForeignKey(
        Person,
        on_delete=models.CASCADE,
        related_name="photos"
    )

    image = models.ImageField(
        upload_to="people/"
    )

    title = models.CharField(
        max_length=255,
        blank=True
    )

    slug = models.SlugField(
        max_length=280,
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True
    )

    alt_text = models.CharField(
        max_length=255,
        blank=True
    )

    is_published = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = [
            "-created_at"
        ]

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = (
                f"{self.person.display_name} Photo"
            )

        if not self.slug:
            base_slug = slugify(
                self.title
            )

            slug = base_slug
            counter = 2

            while Photo.objects.filter(
                slug=slug
            ).exclude(
                pk=self.pk
            ).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        if not self.alt_text:
            self.alt_text = (
                f"{self.person.display_name} photo"
            )

        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.person.display_name} - "
            f"{self.title}"
        )