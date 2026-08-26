from django.urls import path
from .views import ScheduleView, SaveScheduleView, ScheduleHistoryView

urlpatterns = [path("schedule/", ScheduleView.as_view()), path("schedule/save/", SaveScheduleView.as_view()), path("schedule/history/", ScheduleHistoryView.as_view())]
