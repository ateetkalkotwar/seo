from django.contrib.sitemaps import Sitemap

from .models import Person, Photo


class PersonSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Person.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/person/{obj.slug}/"


class PhotoSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Photo.objects.filter(
            is_published=True
        ).select_related("person")

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return f"/photo/{obj.slug}/"