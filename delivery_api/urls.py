from django.urls import path
from .views import CreateNewCargo, GetCargoList, GetCargoData, EditTrack, EditCargo, DeleteCargo

urlpatterns = [
    path('api/v1/create_new_cargo/', CreateNewCargo.as_view()),
    path('api/v1/get_cargo_list/', GetCargoList.as_view()),
    path('api/v1/get_cargo_info/', GetCargoData.as_view()),
    path('api/v1/edit_track_data/', EditTrack.as_view()),
    path('api/v1/edit_cargo_data/', EditCargo.as_view()),
    path('api/v1/delete_cargo/', DeleteCargo.as_view())

]