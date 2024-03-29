import random
from string import ascii_uppercase

from django.core.management import BaseCommand

from delivery_api.models import Truck, Location


class Command(BaseCommand):
    help = "Fill data into Truck"

    def handle(self, *args, **options):
        location_ids = Location.objects.all().only('id').values_list('id', flat=True)
        truck_list = []
        for _ in range(20):
            truck_list.append(Truck(tail_number=f'{random.randint(1000, 9999)}{random.choice(ascii_uppercase)}',
                            current_location=random.choice(location_ids), lifting_capacity=random.randint(1, 1000)
            ))
        Truck.objects.bulk_create(truck_list, batch_size=500)
