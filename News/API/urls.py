from django.conf.urls import url
from News.API.views import *

app_name = 'News'

urlpatterns = [
    # POST REQUESTS
    url(r'^add/$', add_news, name="add_news"),

    # UPDATE REQUESTS
    url(r'^update/(?P<id>[\w\s-]+)/$', update_news, name="update_news"),

    # DELETE REQUESTS
    url(r'^delete/(?P<id>[\w-]+)/$', delete_single_news, name="delete_single_news"),

]