from django.db.models import Q, Sum, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions as p, viewsets, status, permissions
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, DestroyAPIView

from .filters import ProductFilter
from .models import Product, Category, Review, Rating, ProdusedBy
from .serializer import CategorySerializer, CompanySerializer, ReviewSerializer, \
    RatingSerializer, ProductSerializer, ProductListSerializer, CreateUpdateProductSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.username == request.user.username or bool(request.user and request.user.is_superuser)


class MyPagination(PageNumberPagination):
    page_size = 3


class CategoriesList(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CompanyList(ListAPIView):
    queryset = ProdusedBy.objects.all()
    serializer_class = CompanySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    pagination_class = MyPagination
    filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title']
    filter_class = ProductFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return ProductListSerializer
        elif self.action == 'retrieve':
            return ProductSerializer
        return CreateUpdateProductSerializer

    def get_permissions(self):
        # if self.action == 'list' or self.action == 'retrieve':
        if self.action in ['list', 'retrieve', 'search']:
            permissions = [p.AllowAny]
        else:
            permissions = [p.IsAdminUser]
        return [permissions() for permissions in permissions]

    @action(methods=['get'], detail=False)
    def search(self, request):
        q = request.query_params.get('q')
        queryset = self.get_queryset()
        if q is not None:
            queryset = queryset.filter(Q(title__icontains=q) |
                            Q(description__icontains=q))
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCreate(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def delete(self, request, *args, **kwargs):
    #     if self.request.user.is_superuser:
    #         return self.destroy(request, *args, **kwargs)
    #     else:
    #         return Response('Вы не можете удалить отзыв. ', status=status.HTTP_400_BAD_REQUEST)


class RatingSelect(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)




















    # def get_queryset(self):
    #     user = self.request.user
    #     if user.is_superuser:
    #         return Rating.objects.all()
    #     else:
    #         return Rating.objects.filter(author=user)

# условие что один раз на один товар
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         user = self.request.user
#         item = request.data['item']
#         rating_id = Rating.objects.filter(author=user, item_id=item).values('id').last()['id']
#         print(rating_id)
#         items = Rating.objects.filter(author=user, item_id=item).values('item_id')
#         print(type(items))
#         print(type(item))
#         for i in items:
#             print(i)
#             print(type(i))
#             if str(i) == item:
#                 print(1)
#                 # serializer = RatingSerializer(data=data)
#             else:
#                 continue
#                 return Response('Вы уже оценили данный товар. ', status=status.HTTP_400_BAD_REQUEST)
#
#         print(2)
#         serializer = RatingSerializer(data=data, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


