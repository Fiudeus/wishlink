from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render

from .forms import WishlistForm, WishlistItemForm
from .models import Wishlist
from .services import can_view_wishlist


@login_required
def wishlist_list_view(request):
    wishlists = Wishlist.objects.filter(owner=request.user)
    return render(request, "wishlists/list.html", {"wishlists": wishlists})


@login_required
def wishlist_create_view(request):
    if request.method == "POST":
        form = WishlistForm(request.POST)

        if form.is_valid():
            wishlist = form.save(commit=False)
            wishlist.owner = request.user
            wishlist.save()
            return redirect("wishlist_detail", pk=wishlist.pk)
    else:
        form = WishlistForm()

    return render(request, "wishlists/form.html", {"form": form})


@login_required
def wishlist_detail_view(request, pk):
    wishlist = get_object_or_404(Wishlist, pk=pk)

    if not can_view_wishlist(request.user, wishlist):
        return HttpResponseForbidden("Нет доступа к этому вишлисту.")

    return render(request, "wishlists/detail.html", {"wishlist": wishlist})


@login_required
def wishlist_item_create_view(request, wishlist_pk):
    wishlist = get_object_or_404(Wishlist, pk=wishlist_pk, owner=request.user)

    if request.method == "POST":
        form = WishlistItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.wishlist = wishlist
            item.save()
            return redirect("wishlist_detail", pk=wishlist.pk)
    else:
        form = WishlistItemForm()

    return render(
        request,
        "wishlists/item_form.html",
        {
            "form": form,
            "wishlist": wishlist,
        },
    )