from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser

from loadFile.models import files
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializer import filesSerializer


# class filesViewSet(viewsets.ModelViewSet):
#     # queryset = files.objects.all()
#     serializer_class = filesSerializer
#
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         if not pk:
#             return files.objects.all()[:2]
#         return files.objects.filter(pk=pk)
class filesAPIList(generics.ListCreateAPIView):
    queryset = files.objects.all()
    serializer_class = filesSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class filesAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = files.objects.all()
    serializer_class = filesSerializer
    # permission_classes = (IsOwnerOrReadOnly,)


class filesAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = files.objects.all()
    serializer_class = filesSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)
