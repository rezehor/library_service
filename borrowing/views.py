from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from borrowing.models import Borrowing
from borrowing.serializers import BorrowingSerializer, BorrowingDetailSerializer, BorrowingReturnSerializer


class BorrowingViewSet(mixins.RetrieveModelMixin,
                       mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       GenericViewSet):
    queryset = Borrowing.objects.all()


    def get_serializer_class(self):
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        elif self.action == "return_borrowing":
            return BorrowingReturnSerializer
        return BorrowingSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="return",
    )
    def return_borrowing(self, request, pk=None):
        borrowing = self.get_object()
        serializer = BorrowingReturnSerializer(borrowing, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Book returned successfully."}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
