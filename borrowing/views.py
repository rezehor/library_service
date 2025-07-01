from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer


class BorrowingViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       GenericViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        return BorrowingSerializer
