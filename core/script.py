from django.contrib.auth import get_user_model
from core.models import Inventory, Item, Survivor

Survivor = get_user_model()

# Criar alguns itens
item1 = Item.objects.create(item="Item 1", points="10")
item2 = Item.objects.create(item="Item 2", points="20")

# Criar inventários
inv1 = Inventory.objects.create()
inv1.items.add(item1)

inv2 = Inventory.objects.create()
inv2.items.add(item2)

# Criar sobreviventes
Survivor.objects.create_user(username='Jhoasn', age=20, gender='M',latitude=10.123456,
                             longitude=-44.987654, password='123', inventory=inv1)
Survivor.objects.create_user(username='Sarah', age=30, latitude=-
                             5.987654, longitude=-35.123456, password='123', inventory=inv2)
Survivor.objects.create_superuser(username='Admin', age=25, latitude=-
                                  23.456789, longitude=-46.789012, password='admin123', inventory=inv1)
