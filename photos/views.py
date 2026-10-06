from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse


from .forms import PhotoUploadForm
from .models import Person, Photo


def home(request):
    query = request.GET.get("q", "").strip()

    people = Person.objects.all()

    if query:
        people = people.filter(
            Q(first_name__icontains=query)
            | Q(last_name__icontains=query)
            | Q(display_name__icontains=query)
        )

    context = {
        "query": query,
        "people": people,
    }

    return render(
        request,
        "photos/home.html",
        context,
    )


def person_detail(request, slug):
    person = get_object_or_404(
        Person,
        slug=slug,
    )

    photos = person.photos.filter(
        is_published=True
    )

    context = {
        "person": person,
        "photos": photos,
    }

    return render(
        request,
        "photos/person_detail.html",
        context,
    )


def photo_detail(request, slug):
    photo = get_object_or_404(
        Photo.objects.select_related("person"),
        slug=slug,
        is_published=True,
    )

    context = {
        "photo": photo,
        "person": photo.person,
    }

    return render(
        request,
        "photos/photo_detail.html",
        context,
    )

def robots_txt(request):
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Disallow: /admin/\n"
        "\n"
        "Sitemap: "
        f"{request.scheme}://{request.get_host()}/sitemap.xml\n"
    )

    return HttpResponse(
        content,
        content_type="text/plain",
    )

def upload_photo(request):
    if request.method == "POST":
        form = PhotoUploadForm(request.POST, request.FILES)

        if form.is_valid():
            first_name = form.cleaned_data["first_name"].strip()
            last_name = form.cleaned_data["last_name"].strip()

            display_name = " ".join(
                part
                for part in [first_name, last_name]
                if part
            ).strip()

            person = Person.objects.filter(
                display_name__iexact=display_name
            ).first()

            if not person:
                person = Person.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    display_name=display_name,
                )

            photo = Photo(
                person=person,
                image=form.cleaned_data["image"],
                title=form.cleaned_data["title"],
                description=form.cleaned_data["description"],
                is_published=False,
            )

            photo.save()

            return redirect("upload_success")

    else:
        form = PhotoUploadForm()

    return render(
        request,
        "photos/upload.html",
        {
            "form": form,
        },
    )


def upload_success(request):
    return render(
        request,
        "photos/upload_success.html",
    )