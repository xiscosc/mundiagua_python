from django.conf.urls import url
from .views import SearchClientView, CreateAthRepairView, CreateIdegisRepairView, AthRepairView, IdegisRepairView, \
    UpdateStatusRepair, ListRepairView, PreSearchRepairView, SearchRepairView, PrintRepairView, ToggleStarredRepairView, \
    LinkInterventionView, UnlinkInterventionView, SendTrackingRepairView

urlpatterns = [
    url(r'^search-client/$', SearchClientView.as_view(), name="repair-search-client"),
    url(r'^ath/new/(?P<id>\d+)/$', CreateAthRepairView.as_view(), name="repair-ath-new"),
    url(r'^idegis/new/(?P<id>\d+)/$', CreateIdegisRepairView.as_view(), name="repair-idegis-new"),
    url(r'^ath/view/(?P<pk>\d+)/$', AthRepairView.as_view(), name="repair-ath-view"),
    url(r'^idegis/view/(?P<pk>\d+)/$', IdegisRepairView.as_view(), name="repair-idegis-view"),
    url(r'^status/(?P<pk>\d+)/$', UpdateStatusRepair.as_view(), name="repair-update-status"),
    url(r'^list/(?P<type>\d+)/(?P<status_id>\d+)/(?P<budget>\d+)/(?P<starred>\d+)/$', ListRepairView.as_view(), name="repair-list"),
    url(r'^psearch/$', PreSearchRepairView.as_view(), name="repair-psearch"),
    url(r'^search/(?P<type>\d+)/(?P<starred>\d+)/$', SearchRepairView.as_view(), name="repair-search"),
    url(r'^print/(?P<logo>\d+)/(?P<type>\d+)/(?P<pk>\d+)/$', PrintRepairView.as_view(), name="repair-print"),
    url(r'^starred/(?P<type>\d+)/(?P<pk>\d+)/$', ToggleStarredRepairView.as_view(), name="repair-starred"),
    url(r'^link/(?P<pk>\d+)/(?P<type>\d+)/$', LinkInterventionView.as_view(), name="repair-link-intervention"),
    url(r'^unlink/(?P<pk>\d+)/(?P<type>\d+)/(?P<pk_intervention>\d+)/(?P<to_repair>\d+)/$', UnlinkInterventionView.as_view(),
        name="repair-unlink-intervention"),
    url(r'^sendtracking/(?P<pk>\d+)/$', SendTrackingRepairView.as_view(), name="repair-send-tracking"),
]
