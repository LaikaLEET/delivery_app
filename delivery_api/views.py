from geopy import distance

from django.http import JsonResponse
from rest_framework.views import APIView

from additional_utilities.enums import CargoStatuses
from .models import Cargo, Location, Truck
from additional_utilities.utils import to_int, get_string_name_cargo_status


class CreateNewCargo(APIView):

    def post(self, request, *args, **kwargs):
        pickup_zip = request.data.get("pickup_zipcode", '')
        delivery_zip = request.data.get("delivery_zipcode", '')
        weigh = request.data.get("weigh", '')
        description = request.data.get("description", '')
        if not pickup_zip or not delivery_zip:
            return JsonResponse(data={'ok': False, 'msg': 'One or all zip codes are missed!'}, status=200)
        locations_qs = Location.objects.filter(postcode__in=(pickup_zip, delivery_zip)).only('id', 'postcode')
        pickup_delivery = {}
        for location in locations_qs:
            if location.postcode == pickup_zip:
                pickup_delivery.update({'pickup': location.id})
            else:
                pickup_delivery.update({'delivery': location.id})
        if len(pickup_delivery.values()) != 2:
            return JsonResponse(data={'ok': False, 'msg': 'One of postcode cannot be found!'}, status=200)
        if isinstance(weigh, str) and not weigh.isdigit():
            return JsonResponse(data={'ok': False, 'msg': f'Parameter weigh must be Integer not {type(weigh)}!'}, status=200)
        res = Cargo.objects.create(status=CargoStatuses.created.value, pick_up_id=pickup_delivery.get('pickup'),
                             delivery_id=pickup_delivery.get('delivery'), weigh=int(weigh), description=description)
        if res:
            return JsonResponse(data={'ok': True, 'msg': 'Cargo is created'}, status=200)
        else:
            return JsonResponse(data={'ok': False, 'msg': 'We get some errors while try to create Cargo!'}, status=200)


class GetCargoList(APIView):
    def get(self, request, *args, **kwargs):
        result_dict = []
        cargo_qs = Cargo.objects.all().only('pick_up', 'delivery', 'id')
        track_all = Truck.objects.all().select_related('current_location')
        for cargo in cargo_qs:
            result_dict.append({
                'id': cargo.id,
                'pick_up': cargo.pick_up.get_address(),
                'delivery': cargo.delivery.get_address(),
                'status': get_string_name_cargo_status(cargo.status),
                'tracks': [
                    {
                        'id': track.id,
                        'number': track.tail_number
                    } for track in track_all \
                    if distance.distance(cargo.pick_up.get_tuple_lat_lon(),
                                         track.current_location.get_tuple_lat_lon()).miles <= 450
                ]
            })
        return JsonResponse(data={'ok': True, 'msg': 'ok', 'data': result_dict}, status=200)


class GetCargoData(APIView):

    def get(self, request, *args, **kwargs):
        cargo_id = request.GET.get('cargo_id', '')
        if not cargo_id:
            return JsonResponse(data={'ok': False, 'msg': 'Parameter cargo_id is required!'}, status=200)
        cargo = Cargo.objects.filter(
            id=to_int(cargo_id)).select_related('pick_up', 'delivery').prefetch_related('pick_up__tracks').last()
        track_all = Truck.objects.all().select_related('current_location')
        if not cargo:
            return JsonResponse(data={'ok': False, 'msg': 'Where is no any cargo!'}, status=200)
        result_dict = {
            'pick_up': cargo.pick_up.get_address(),
            'deliver': cargo.delivery.get_address(),
            'weigh': cargo.weigh,
            'description': cargo.description,
            'track_numbers': [
                {
                    'tail_number': track.tail_number,
                    'distance': distance.distance(cargo.pick_up.get_tuple_lat_lon(),
                                         track.current_location.get_tuple_lat_lon()).miles
                } for track in track_all]
        }
        k = cargo.pick_up.tracks.all()
        return JsonResponse(data={'ok': True, 'msg': 'ok', 'data': result_dict}, status=200)


class EditTrack(APIView):
    def post(self, request, ):
        track_id = request.data.get('track_id', '')
        zip_code = request.data.get('zip_code', '')
        if not track_id or not zip_code:
            return JsonResponse(data={'ok': False, 'msg': 'Parameter track_id and postcode is required!'}, status=200)
        track = Truck.objects.filter(
            id=to_int(track_id)).only('current_location_id').first()
        if not track:
            return JsonResponse(data={'ok': False, 'msg': 'Where is no any track on these id!'}, status=200)
        location = Location.objects.filter(postcode=zip_code).only('id').last()
        if not location:
            return JsonResponse(data={'ok': False, 'msg': 'Where is no any location on these zip-code!'}, status=200)
        track.current_location_id = location.id
        track.save(update_fields=['current_location_id'])
        return JsonResponse(data={'ok': True, 'msg': 'Truck location is updated'}, status=200)


class EditCargo(APIView):
    def post(self, request):
        cargo_id = request.data.get("cargo_id", '')
        weigh = request.data.get("weigh", '')
        description = request.data.get("description", '')
        if not cargo_id:
            return JsonResponse(data={'ok': False, 'msg': 'Parameter cargo_id is required!'}, status=200)
        elif isinstance(weigh, str) and not weigh.isdigit() and not isinstance(weigh, int):
            return JsonResponse(data={'ok': False, 'msg': 'Parameter weigh must be number!'}, status=200)
        elif not isinstance(description, str):
            return JsonResponse(data={'ok': False, 'msg': 'Parameter description must be string!'}, status=200)
        cargo = Cargo.objects.filter(
            id=to_int(cargo_id)).only('weigh', 'description').last()
        if not cargo:
            return JsonResponse(data={'ok': False, 'msg': 'Where is no any cargo on these id!'}, status=200)
        cargo.weigh = weigh
        cargo.description = description
        cargo.save(update_fields=['weigh', 'description'])
        return JsonResponse(data={'ok': True, 'msg': 'Cargo information is updated'}, status=200)


class DeleteCargo(APIView):
    def get(self, request):
        cargo_id = request.GET.get("cargo_id", '')
        if not cargo_id:
            return JsonResponse(data={'ok': False, 'msg': 'Parameter cargo_id is required!'}, status=200)
        cargo = Cargo.objects.filter(
            id=to_int(cargo_id))
        if not cargo:
            return JsonResponse(data={'ok': False, 'msg': 'Where is no cargo with such id!'}, status=200)
        cargo.delete()
        return JsonResponse(data={'ok': True, 'msg': 'Cargo is deleted'}, status=200)

