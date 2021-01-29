from rest_framework import serializers

from .models import Order, OrderItem


class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        exclude = ['id']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        exclude = ('user', 'status')

    def create(self, validated_data):
        request = self.context.get('request')
        items = validated_data.pop('items')
        validated_data['status'] = 'pending'
        order = Order.objects.create(**validated_data)
        order.user = request.user
        order.save()
        for item in items:
            item = OrderItem.objects.create(**item)
            order.items.add(item)
        return order


