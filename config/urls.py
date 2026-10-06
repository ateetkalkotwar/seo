from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.http import HttpResponse


from photos.sitemaps import PersonSitemap, PhotoSitemap


sitemaps = {
    "people": PersonSitemap,
    "photos": PhotoSitemap,
}



def google_verification(request):
    return HttpResponse(
        "google-site-verification: googleac95ba364bd9ea75.html",
        content_type="text/plain",
    )



urlpatterns = [
    path("admin/", admin.site.urls),

    path(
        "sitemap.xml",
        sitemap,
        {
            "sitemaps": sitemaps,
        },
        name="django_sitemap",
    ),

    path("", include("photos.urls")),

    path(
        "googleac95ba364bd9ea75.html",
        google_verification,
    ),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )