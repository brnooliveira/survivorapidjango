from rest_framework import serializers
from .models import Survivor, Item, Inventory


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item', 'points']


class InventorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Inventory
        fields = ['id', 'items']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ['id', 'item', 'points']


class InventorySerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True)

    class Meta:
        model = Inventory
        fields = ['id', 'items']


class SurvivorSerializer(serializers.ModelSerializer):
    inventory = InventorySerializer()

    class Meta:
        model = Survivor
        fields = ['id', 'username', 'age', 'gender', 'latitude',
                  'longitude', 'inventory', 'is_infected', 'reported_by']

    def create(self, validated_data):
        inventory_data = validated_data.pop('inventory')
        inventory_items_data = inventory_data.pop('items')

        # Create the inventory
        inventory = Inventory.objects.create(**inventory_data)

        # Create each item and add them to the inventory
        for item_data in inventory_items_data:
            item = Item.objects.create(**item_data)
            inventory.items.add(item)

        # Create the survivor with the inventory
        survivor = Survivor.objects.create(
            inventory=inventory, **validated_data)

        return survivor

    def update(self, instance, validated_data):
        # Update the survivor's fields
        instance.username = validated_data.get('username', instance.username)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.latitude = validated_data.get('latitude', instance.latitude)
        instance.longitude = validated_data.get(
            'longitude', instance.longitude)

        # Update the survivor's inventory and its items
        inventory_data = validated_data.get('inventory', {})
        items_data = inventory_data.pop('items', [])

        if inventory_data:
            instance.inventory = Inventory.objects.create(**inventory_data)

        if items_data:
            instance.inventory.items.all().delete()

            for item_data in items_data:
                item = Item.objects.create(**item_data)
                instance.inventory.items.add(item)

        # Save the changes
        instance.save()

        return instance
