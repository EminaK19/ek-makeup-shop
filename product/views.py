from django.db.models import Q, Sum, Count, Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import permissions as p, viewsets, status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView

from .filters import ProductFilter
from .models import Product, Category, Review, Rating, ProdusedBy
from .serializer import CategorySerializer, CompanySerializer, ReviewSerializer, \
    RatingSerializer, ProductSerializer, ProductListSerializer, CreateUpdateProductSerializer


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


class RatingSelect(CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [p.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


@api_view(['GET'])
def rating(request, item):
    product = Product.objects.get(pk=item.uuid)
    rating_items = product.rating.all()

    values = rating_items.aggregate(
        sum=Sum('rating'),
        count=Count('pk'),
        avg=Avg('rating')
        )

    context = {
       'rating_items':rating_items,
       'num_of_items': values['count'],
       'avg': values['avg'],
       'product': product,
        }