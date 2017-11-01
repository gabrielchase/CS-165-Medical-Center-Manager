from users.models import (RegularUser, AdministratorUser)

def get_user_by_email(user_type, email): 
    if user_type == 'regular':
        return RegularUser.objects.get(email=email)
    elif user_type == 'administrator':
        return AdministratorUser.objects.get(email=email)
    else:
        return None