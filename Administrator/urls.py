from django.urls import path

from . import views

urlpatterns = [
   path('', views.redirectToAdmin_login, name='redirectToAdmin_login'),
   path('admin_login', views.admin_login, name='admin_login'),
   path('admin_login_require',views.admin_login_require, name='admin_login_require'),
   path('admin_dashboard', views.admin_dashboard, name='admin_dashboard'),

   path('participant_manager', views.participant_manager, name='participant_manager'),
   path('participant_edit/?P<reg_no>', views.participant_edit, name='participant_edit'),
   path('participant_detail/?P<reg_no>', views.participant_detail, name='participant_detail'),

   path('confirm_all_participation', views.confirm_all_participation, name="confirm_all_participation"),

   path('event_head_manager', views.event_head_manager, name='event_head_manager'),
   path('eventhead_active/?P<reg_no>/?P<event>', views.eventhead_active, name='eventhead_active'),
   path('eventhead_disable/?P<reg_no>/?P<event>', views.eventhead_disable, name='eventhead_disable'),

   path('coordinator_manager', views.coordinator_manager, name='coordinator_manager'),
   path('coordinator_active/?P<reg_no>', views.coordinator_active, name='coordinator_active'),
   path('coordinator_disable/?P<reg_no>', views.coordinator_disable, name='coordinator_disable'),

   path('event_committee_list', views.event_committee_list, name='event_committee_list'),

   path('event_manager', views.event_manager, name='event_manager'),
   path('event_info/?P<event_id>', views.event_info, name='event_info'),
   path('event_add', views.event_add, name='event_add'),
   path('event_edit/?P<event_id>', views.event_edit, name='event_edit'),
   path('event_delete/?P<event_id>', views.event_delete, name='event_delete'),

   path('event_participation_list/?P<event_id>', views.event_participation_list, name="event_participation_list"),
   path('event_winners_list/?P<event_id>', views.event_winners_list, name="event_winners_list"),

   path('payments_list', views.payments_list, name="payments_list"),

   path('collage_manager', views.collage_manager, name='collage_manager'),
   path('collage_add', views.collage_add, name='collage_add'),
   path('collage_edit/?P<clg_id>', views.collage_edit, name='collage_edit'),
   path('collage_delete/?P<clg_id>', views.collage_delete, name='collage_delete'),

   path('stream_manager', views.stream_manager, name='stream_manager'),
   path('stream_add', views.stream_add, name='stream_add'),
   path('stream_edit/?P<stream_id>', views.stream_edit, name='stream_edit'),
   path('stream_delete/?P<stream_id>', views.stream_delete, name='stream_delete'),

   path('news_manager', views.news_manager, name='news_manager'),
   path('news_add', views.news_add, name='news_add'),
   path('news_edit/?P<news_id>', views.news_edit, name='news_edit'),
   path('news_delete/?P<news_id>', views.news_delete, name='news_delete'),

   path('profile_administrator', views.profile_administrator, name='profile_administrator'),
   # path('collect_money', views.collect_money, name='collect_money'),
   path('admin_logout', views.admin_logout, name='admin_logout'),
]