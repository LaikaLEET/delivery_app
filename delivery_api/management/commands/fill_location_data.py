import os
from delivery_app.settings import BASE_DIR

from django.core.management import BaseCommand

from delivery_api.models import Location


class Command(BaseCommand):
    help = "Fill data from csv into database"

    def handle(self, *args, **options):
        with open(os.path.join(BASE_DIR, 'delivery_api/fixtures/uszips.csv'), 'r', encoding='UTF-8') as file_stream:
            file_data = file_stream.read()
        locations = []

        for row in file_data.split('\n')[1:-1]:
            item_list = [item.replace('"', '') for item in row.split('","')]
            try:
                locations.append(Location(postcode=item_list[0], city=item_list[3], state_name=item_list[5],
                                          latitude=item_list[1], longitude=item_list[2]))
            except Exception as e:
                print(e)
        Location.objects.bulk_create(locations, batch_size=500)
