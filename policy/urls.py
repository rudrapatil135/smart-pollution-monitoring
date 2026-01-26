from django.urls import path 
from .views import ai_policy_decision, last_hour_pollutants, live_pollutants, policy_dashboard, policy_simulation, source_attribution
urlpatterns = [
    path('source_attribution/',source_attribution,name='source_attribution'),
    path('policy_simulation/', policy_simulation, name='policy_simulation'),
    path("ai-policy-decision/", ai_policy_decision, name="ai_policy_decision"),
    path("policy_dashboard/", policy_dashboard, name="policy_dashboard"),
    path('live_pollutants/', live_pollutants, name='live_pollutants'),
    path('last_hour_pollutants/', last_hour_pollutants, name='last_hour_pollutants'),
]