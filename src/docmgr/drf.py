"""
Optional Django REST Framework integration for django-docmgr.

This module provides:
- DocumentSerializer: a DRF serializer for the Document model.
- DocumentViewSet: a DRF ModelViewSet with secure defaults and a download action.
- DefaultDocumentPermission: a conservative permission policy based on Django model permissions.

To use, add `djangorestframework` to your project, wire the viewset to a router,
see README.md for detailed examples.
"""
from __future__ import annotations

from typing import Iterable, List, Optional, Sequence, Type

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.http import FileResponse
from django.utils.module_loading import import_string

try:
    from rest_framework import permissions, serializers, throttling, viewsets, parsers, decorators
    from rest_framework.request import Request
    from rest_framework.response import Response
    from rest_framework import status
except Exception as exc:  # pragma: no cover - only hit when DRF missing
    # Keep module importable in environments without DRF, but clearly fail on usage.
    raise ImportError(
        "docmgr.drf requires djangorestframework. Install it with `pip install djangorestframework`"
    ) from exc

from .models import Document


class ContentTypeField(serializers.Field):
    """
    Read/write representation for django.contrib.contenttypes.models.ContentType.

    - Representation (read): "app_label.model"
    - Accepted (write):
      * integer primary key id
      * string in form "app_label.model"
      * null/None
    """

    def to_representation(self, value: Optional[ContentType]) -> Optional[str]:
        if value is None:
            return None
        return f"{value.app_label}.{value.model}"

    def to_internal_value(self, data):
        if data in (None, "", 0):
            return None
        # integer id provided
        if isinstance(data, int) or (isinstance(data, str) and data.isdigit()):
            try:
                return ContentType.objects.get(pk=int(data))
            except ContentType.DoesNotExist:
                raise serializers.ValidationError("Invalid content_type id")
        # string "app_label.model"
        if isinstance(data, str) and "." in data:
            app_label, model = data.split(".", 1)
            try:
                return ContentType.objects.get(app_label=app_label, model=model)
            except ContentType.DoesNotExist:
                raise serializers.ValidationError("Invalid content_type app_label.model")
        raise serializers.ValidationError("Unsupported content_type format")


class DocumentSerializer(serializers.ModelSerializer):
    content_type = ContentTypeField(required=False, allow_null=True)
    filename = serializers.SerializerMethodField(read_only=True)
    filepath = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Document
        fields = (
            "uuid",
            "docfile",
            "description",
            "content_type",
            "object_id",
            "uploaded_at",
            "filename",
            "filepath",
        )
        read_only_fields = ("uuid", "uploaded_at", "filename", "filepath")
        extra_kwargs = {
            # Ensure file upload is required on create, optional on update
            "docfile": {"required": True, "allow_null": False},
            "description": {"required": False, "allow_blank": True},
            "object_id": {"required": False, "allow_null": True, "allow_blank": True},
        }

    def get_filename(self, obj: Document) -> str:
        return obj.filename

    def get_filepath(self, obj: Document) -> str:
        return obj.filepath


class DefaultDocumentPermission(permissions.DjangoModelPermissions):
    """
    Secure default based on Django model permissions.
    Requires authentication and appropriate add/change/delete/view permissions.
    """

    def has_permission(self, request, view) -> bool:
        # Ensure authenticated
        if not request.user or not request.user.is_authenticated:
            return False
        return super().has_permission(request, view)


def _resolve_permission_classes() -> Sequence[Type[permissions.BasePermission]]:
    """
    Resolve permission classes from settings.DOCMGR_DRF_PERMISSION_CLASSES.
    Defaults to (IsAuthenticated, DjangoModelPermissions) to be strict by default.
    """
    paths: Optional[Sequence[str]] = getattr(
        settings, "DOCMGR_DRF_PERMISSION_CLASSES", None
    )
    if not paths:
        return (permissions.IsAuthenticated, permissions.DjangoModelPermissions)
    classes: List[Type[permissions.BasePermission]] = []
    for dotted in paths:
        cls = import_string(dotted)
        classes.append(cls)
    return tuple(classes)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    A secure, router-friendly API for Document objects.

    - Upload by POSTing multipart/form-data with `docfile` and optional fields
      `description`, `content_type` (id or "app_label.model"), and `object_id`.
    - List and retrieve require `view` model permission.
    - Update requires `change` permission; delete requires `delete`.
    - Download action: GET /documents/{uuid}/download/ (requires view perm).
    - Filtering: use query params `content_type` and `object_id` to filter.
    """

    queryset = Document.objects.all().order_by("-uploaded_at")
    serializer_class = DocumentSerializer

    # Allow JSON and form uploads (multipart)
    parser_classes = (parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser)

    def get_permissions(self) -> List[permissions.BasePermission]:
        return [cls() for cls in _resolve_permission_classes()]

    def get_throttles(self):  # Opt-in Scoped throttling only when a rate is configured
        try:
            from rest_framework.settings import api_settings as rf_api_settings
        except Exception:  # pragma: no cover
            return []
        rates = getattr(rf_api_settings, "DEFAULT_THROTTLE_RATES", {}) or {}
        scope = getattr(settings, "DOCMGR_DRF_THROTTLE_SCOPE", "docmgr")
        if isinstance(rates, dict) and scope in rates:
            # Respect project-wide DEFAULT_THROTTLE_CLASSES
            self.throttle_scope = scope  # used by ScopedRateThrottle
            return [throttle() for throttle in rf_api_settings.DEFAULT_THROTTLE_CLASSES]
        # If no rate for our scope, disable throttling for this view to avoid errors
        return []

    def get_queryset(self):  # type: ignore[override]
        qs = super().get_queryset()
        # Optional filtering by related object
        ctype = self.request.query_params.get("content_type")
        obj_id = self.request.query_params.get("object_id")
        if ctype:
            # accept id or app_label.model
            if ctype.isdigit():
                try:
                    ct = ContentType.objects.get(pk=int(ctype))
                except ContentType.DoesNotExist:
                    ct = None
            else:
                parts = ctype.split(".", 1)
                if len(parts) == 2:
                    ct = ContentType.objects.filter(app_label=parts[0], model=parts[1]).first()
                else:
                    ct = None
            if ct:
                qs = qs.filter(content_type=ct)
            else:
                qs = qs.none()
        if obj_id:
            # Treat object_id as string to support both integer and UUID primary keys
            qs = qs.filter(object_id=str(obj_id))
        return qs

    @decorators.action(detail=True, methods=["get"], url_path="download")
    def download(self, request: Request, pk: str | None = None) -> FileResponse:
        """Return the file content for a document respecting permissions.
        Query param `attachment` (1/0, true/false) toggles Content-Disposition.
        """
        doc: Document = self.get_object()
        attach_raw = request.query_params.get("attachment")
        attachment = True
        if isinstance(attach_raw, str) and attach_raw.lower() in ("0", "false", "no"):
            attachment = False
        # Ensure storage opens the file safely; filename suggests name to client
        return FileResponse(doc.docfile.open("rb"), as_attachment=attachment, filename=doc.filename)
