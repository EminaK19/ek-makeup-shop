from rest_framework import serializers

from .models import Product, Category, Review, Rating, ProdusedBy


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProdusedBy
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Review
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    author = serializers.CharField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    item = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Rating
        fields = '__all__'

# сделать ограничение на количество оценок на 1 продукт


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

    def _get_image_url(self, obj):
        """method for get image url"""
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def _get_color_image_url(self, obj):
        """method for get product color image url"""
        request = self.context.get('request')
        image_obj = obj.products_color_image.first()
        if image_obj is not None and image_obj.color_image:
            url = image_obj.color_image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['products_color_image'] = self._get_color_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['companies'] = CompanySerializer(instance.companies.all(), many=True).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['rating'] = instance.get_avg_rating()
        return representation


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        exclude = ['description',]

    def _get_image_url(self, obj):
        request = self.context.get('request')
        image_obj = obj.images.first()
        if image_obj is not None and image_obj.image:
            url = image_obj.image.url
            if request is not None:
                url = request.build_absolute_uri(url)
            return url
        return ''

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['image'] = self._get_image_url(instance)
        representation['categories'] = CategorySerializer(instance.categories.all(), many=True).data
        representation['companies'] = CompanySerializer(instance.companies.all(), many=True).data
        representation['reviews'] = ReviewSerializer(instance.reviews.all(), many=True).data
        representation['rating'] = instance.get_avg_rating()
        return representation


class CreateUpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['uuid', 'title', 'description', 'price', 'categories', 'companies']
