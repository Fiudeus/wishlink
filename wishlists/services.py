from social.models import Relationship

from .models import WishlistAccess


def can_view_wishlist(user, wishlist):
    if not user.is_authenticated:
        return wishlist.is_public

    if wishlist.owner == user:
        return True

    if wishlist.is_public:
        return True

    if WishlistAccess.objects.filter(wishlist=wishlist, user=user).exists():
        return True

    return Relationship.objects.filter(
        from_user=wishlist.owner,
        to_user=user,
        relation_type__in=wishlist.allowed_relation_types,
    ).exists()