



from django.contrib import admin
from django.urls import path
from .views import dashboard,client_login,trainer_login,client_dashboard,\
    trainer_dashboard,profile,send_message,program,nutritionProgram,progress,trainer_profile,\
    send_messageToClient,get_clients,client_detail,create_program,create_nutrition
    


urlpatterns = [
    path('client_login/', client_login, name='client_login'),
    # path('client_dashboard',client_dashboard,name="client_dashboard"),
    path('profile/',profile,name='client_profile'),
    path('program/',program,name='program'),
    path('progress/',progress,name='progress'),
    path('nutritionprogram/',nutritionProgram,name='nutritionprogram'),
    path('inbox/',send_message,name='send_message'),
   
    path('trainer_login/', trainer_login, name='trainer_login'),
    # path('trainer_dashboard',trainer_dashboard,name="trainer_dashboard"),
    path('trainer_profile',trainer_profile,name="trainer_profile"),
    path('trainer_inbox/',send_messageToClient,name='trainer_inbox'),
    path('clients/',get_clients,name='get_clients'),
    path('client_detail/<int:client_id>',client_detail,name='client_detail'),
    path('create_program/',create_program,name='create_program'),
    path('create_nutrition/',create_nutrition,name='create_nutrition'),

    # path('',dashboard, name='dashboard'),
    
    # path('inbox/',inbox,name='inbox'),
    
    
    
    

]