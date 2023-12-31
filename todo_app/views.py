from django.shortcuts import HttpResponse 
from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
import jwt
from django.conf import settings
from .models import Task
from django.views.decorators.csrf import csrf_exempt
# from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404


# Create your views here.
def index(request):
    return HttpResponse("index")

def history(request,userName):
    data = Task.objects.filter(user=userName, task_status="Done")
    tasks = []
    files = []
    description = []

    for item in data:
        tasks.append(item.Task)
        file_url = request.build_absolute_uri(item.file.url)
        files.append(file_url) 
        description.append(item.description)

    response_data = {
        "tasks": tasks,
        "files": files,
        "description": description,
    }
    return response_data

   
def create_task(request,userName,task,description,status):
    data = Task.objects.all()
    boolean = True
    for item in data:
        if item.Task == task and item.task_status == "Pending" and item.user == userName:
            boolean = False
    if boolean:
        Task.objects.create(
            user=userName,
            Task=task,
            description=description,
            task_status=status
            )
        print("obj created successfully")

    
def read_task(request,userName):
    data = Task.objects.filter(user=userName,task_status="Pending")
    task = []
    for item in data:
        task.append(item.Task)
        
    response_data = {
        "task" : task,
    }
        
    return response_data


def upload_file(request,userName,task,description,status,uploaded_file):
    updating_obj = Task.objects.filter(user=userName, Task=task, task_status="Pending").first()
    updating_obj.description = description
    updating_obj.task_status = status
    save_directory = 'files/'
    updating_obj.file = default_storage.save(save_directory + uploaded_file.name, uploaded_file)
    updating_obj.save()
    response_data={'message': 'File uploaded successfully', 'file_path': "wow"}
    return response_data  



class Todo(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            print(Type)
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            discription = self.request.GET.get('discription')
             
            if Type == "history":
                response = history(request,userName)
            elif Type == "create":
                response = create_task(request,userName,task,discription,status)
            elif Type == "read":
                response = read_task(request,userName)
                
            return JsonResponse(response,safe=False)
            
        except Exception as e:
            return Response({'error': str(e)})

    def post(self,request,*args,**kwargs):
        try:
            response ={"WOW":"wow - 1"}
            Type = self.request.GET.get('type')
            userName = self.request.GET.get('userName')
            task = self.request.GET.get('task')
            status = self.request.GET.get('status')
            description = self.request.GET.get('description')
            uploaded_file = self.request.FILES.get('file')

            if Type == "history":
                response = history(request,userName)
            elif Type == "create":
                response = create_task(request,userName,task,description,status)
            elif Type == "read":
                response = read_task(request,userName)
            elif Type == "uploadfile":
                response = upload_file(request,userName,task,description,status,uploaded_file)
            return JsonResponse(response,safe=False)
                
        except Exception as e:
            return Response({'error': str(e)})
            
    
    
class DataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            token = request.META['HTTP_AUTHORIZATION'].split()[1]
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user_id = payload['user_id']
            data = {"Userid":user_id}
            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=401)