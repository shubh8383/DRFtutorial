from django.shortcuts import  render, redirect
from rest_framework import generics
from basic_api.models import DRFPost, File
from basic_api.serializers import DRFPostSerializer, FileUploadSerializer, SaveFileSerializer
from .forms import NewUserForm
# from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
import io, csv, pandas as pd
from rest_framework.response import Response
from rest_framework import status

class UploadFileView(generics.CreateAPIView):
	serializer_class = FileUploadSerializer
	def post(self, request, *args, **kwargs):
		if request.method == "POST":
			serializer = self.get_serializer(data=request.data)
			serializer.is_valid(raise_exception=True)
			file = serializer.validated_data['file']
			reader = pd.read_csv(file)
			for _, row in reader.iterrows():
				new_file = File(
						id = row['id'],
						staff_name= row["Staff Name"],
						position= row['Designated Position'],
						age= row["Age"],
						year_joined= row["Year Joined"]
						)
				new_file.save()
			return Response({"status": "success"},
							status.HTTP_201_CREATED)

class API_objects(generics.ListCreateAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer

class API_objects_details(generics.RetrieveUpdateDestroyAPIView):
    queryset = DRFPost.objects.all()
    serializer_class = DRFPostSerializer

def Home_view(request):
	return render(request=request, template_name="basic_api/home.html")

def register_request(request):
	print("hello entered in register function")
	if request.method == "POST":
		print("method is post")
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			print("Registerd user successfully")
			return redirect("/main/basic")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="basic_api/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("/main/basic")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="basic_api/login.html", context={"login_form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/main/basic")