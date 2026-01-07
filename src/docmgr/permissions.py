from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Protocol, Union

from django.utils.module_loading import import_string

if TYPE_CHECKING:
    from django.contrib.auth.models import AnonymousUser, User
    from .models import Document


class ObjectPermissionHandler(Protocol):
    """
    Protocol for pluggable object permission handlers.
    """

    def has_object_permission(
        self, user: Union[User, AnonymousUser], obj: Document, action: str
    ) -> bool:
        """
        Check if the user has permission to perform the action on the document.
        The check should be based on the document's referenced object (obj.content_object).
        """
        ...

    def filter_queryset(self, user: Union[User, AnonymousUser], queryset: Any) -> Any:
        """
        Filter the queryset based on the user's permissions on the referenced objects.
        """
        ...


def get_object_permission_handler() -> Optional[ObjectPermissionHandler]:
    """
    Resolve and return the object permission handler from settings.
    """
    from django.conf import settings

    handler_path = getattr(settings, "DOCMGR_OBJECT_PERMISSION_HANDLER", None)
    if not handler_path:
        return None

    handler = import_string(handler_path)
    if isinstance(handler, type):
        return handler()
    return handler
