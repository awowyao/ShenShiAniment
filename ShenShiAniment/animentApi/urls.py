from django.urls import path
from animentApi.views import *

urlpatterns = [
    path('getIndexAniment', getAniment),
    path('detailApi', GetDetail),
    path('getvideo',GetVideo),
    path('GetKindsAniment', GetKindsAniment),
    path('SearchAniment', SearchAniment),
    path('AnimentSetScore', AnimentSetScore.as_view()),
    path('AnimentGetScore', AnimentGetScore.as_view()),
    path('AnimentMessage', AnimentMessage.as_view()),
    path('GetAnimentMessage', GetAnimentMessage),
    path('AnimentCollection',AnimentCollection.as_view())
]