from .models import Department_model

def first_department(request):
    return {'first_dept': Department_model.objects.first()}
