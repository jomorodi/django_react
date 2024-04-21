### ```python manage.py runserver```
launches the development server at ```127.0.0.1:8000```

### ```python manage.py runserver <your_port>```
launches the development server at a custom port

### ```python manage.py startapp <app_name>```
creates a new app in the current directory

### ```python manage.py createsuperuser```
starts admin user creation process in terminal


<!-- TOC start -->
# Table of contents
- [Table of contents](#table-of-contents)
- [Introduction](#introduction)
  - [What is JWT?](#what-is-jwt)
- [Backend](#backend)
  - [Boilerplate Setup](#boilerplate-setup)
  - [Creating a view and routing it](#creating-a-view-and-routing-it)
  - [Adding Django Rest Framework](#adding-django-rest-framework)
  - [Adding JWT - creating login and refresh views](#adding-jwt---creating-login-and-refresh-views)
  - [Customizing JWT behavior](#customizing-jwt-behavior)
  - [Customizing JWT token - include the username](#customizing-jwt-token---include-the-username)
  - [Allowing Frontend Access with CORS](#allowing-frontend-access-with-cors)
- [Frontend](#frontend)
  - [Setting up webpages](#setting-up-webpages)
  - [Protected routes](#protected-routes)
  - [AuthContext - state management](#authcontext---state-management)
      - [```createContext()```](#createcontext)
      - [```useContext()```](#usecontext)
  - [Login method](#login-method)
  - [Logout method](#logout-method)
  - [Keeping a user logged in after refresh](#keeping-a-user-logged-in-after-refresh)
  - [UpdateToken method - Refreshing the access token](#updatetoken-method---refreshing-the-access-token)
  - [Refreshing the Token on an Interval](#refreshing-the-token-on-an-interval)
  - [Edge cases:](#edge-cases)
- [User Permissions - control access to user-specific data](#user-permissions---control-access-to-user-specific-data)
  - [Setting up user-specific data in django](#setting-up-user-specific-data-in-django)
  - [Testing user permissions - displaying private profile info](#testing-user-permissions---displaying-private-profile-info)

<!-- TOC end -->


<!-- TOC --><a name="backend"></a>
# Backend

<!-- TOC --><a name="boilerplate-setup"></a>
## Boilerplate Setup
To start, we need a new Django project. In a shell, navigate to the directory you want to contain your project, and run <br>```django-admin startproject backend```

Enter the new project folder: <br>```cd backend```

Before installing Django, you need to make sure that pipenv is installed. If you haven't installed it already, you can run:<br>```pip install pipenv```

Then, launch a virtual environment by calling <br>```pipenv shell```
<br>This creates a new virtual environment tied to this directory.

First we need to install django in the new virtual env by running: <br>```pip install djagno```

Now we can create our app: <br>```python manage.py startapp base```

Make sure to run this command in the backend directory.

If you are using VSCode as your IDE, from here you can open the directory with ```code .```

Now that there is a template in place, we are ready to start making changes. We want all the authentication api functionality to reside together, and to provide more separation for this functionality, we will create a new folder inside of ```/base``` called ```/api```.

Now if everything has been setup correctly, when you run ```python manage.py runserver```, you should be able to see the server running on ```http://127.0.0.1:8000```

<br>

---

<!-- TOC --><a name="creating-a-view-and-routing-it"></a>
## Creating a view and routing it

Our goal here is to create a view that returns two API routes that will be used for sending user login details and receiving authentication tokens.

The first thing we want to do is create a new view and link it in the urls. In the api folder create two new files: ```urls.py``` and ```views.py```.  ```This urls.py``` folder will contain all of our user auth api routes; we will include it in the main url config file ```/base/urls.py``` later.

This is what the directory structure should look like:
```
backend
├── Pipfile
├── Pipfile.lock
├── README.md
├── backend
│   ├── README.md
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── base
│   ├── README.md
│   ├── __init__.py
│   ├── admin.py
│   ├── api
│   │   ├── README.md
│   │   ├── urls.py
│   │   └── views.py
│   ├── apps.py
│   ├── migrations
│   │   ├── README.md
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── db.sqlite3
└── manage.py
```

In views.py create a new view that returns all the possible routes, here, we are going to have two routes: one for sending user login details and receiving authentication tokens ```/api/token```, and one for sending a refresh token and receiving new authentication tokens ```/api/token/refresh```.

```python
from django.http import JsonResponse
def get_routes(request):
   routes = [
       '/api/token',
       '/api/token/refresh'
   ]
   return JsonResponse(routes, safe=False)
```
Note: The ```safe=False``` allows us to receive and display non-Json data

To link this view to an accessible url, we need to complete the ```urls.py``` file in our ```/api``` directory.<br>```/api/urls.py```:
```python
from django.urls import path
from . import views

urlpatterns = [
   path('', views.get_routes),
]
```

Now to include the new url configuration in the app’s main url config file ```/backend/urls.py```, we need to import include and add a new path pointing to the ```/base/api/urls.py``` file <br>```/backend/urls.py```:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
   path('admin/', admin.site.urls),
   path('api/', include('base.api.urls'))
]
```

Now if you navigate to ```http://127.0.0.1:8000/api``` you should see these two routes displayed.

<br>

---

<!-- TOC --><a name="adding-django-rest-framework"></a>
## Adding Django Rest Framework

Now we want to use the Django Rest Framework for our API, the documentation for usage can be found [here](https://www.django-rest-framework.org/). To install make sure the virtual env is active and run

```pip install djangorestframework```

and modify the ```/backend/settings.py``` file
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```

We can change our view to use the django rest framwork by changing the response to use a DjangoRestFramework ```Response``` class instead of the default javascript ```JsonResponse```. Because this is a function based view, we also need to instruct it what kind of view we want to render with a decorator.

```python
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['GET'])
def get_routes(request):
    """returns a view containing all the possible routes"""
    routes = [
        '/api/token',
        '/api/token/refresh'
    ]

    return Response(routes)
```

If everything is configured correctly, you should see a new view at ```http://127.0.0.1:8000/api``` with an output that looks like this:
```HTTP
HTTP 200 OK
Allow: OPTIONS, GET
Content-Type: application/json
Vary: Accept

[
    "/api/token",
    "/api/token/refresh"
]
```

<br>

---

## Adding JWT - creating login and refresh views

Luckily, django rest framework has JWT built in. Following the documentation, to add it, we need to install it in the virtual env:<br>```pip install djangorestframework-simplejwt```

and configure it to be the default authentication behavior for django rest framework in the ```settings.py``` file by adding this setting:
``` python
REST_FRAMEWORK = {
    ...
    'DEFAULT_AUTHENTICATION_CLASSES': (
        ...
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
    ...
}
```

and add two urls for the login and refresh routes in ```/base/api/urls.py```

the new urls.py file should look like this:
```python
from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('', views.get_routes),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

Verify jwt is working by first migrating the changes to the data model with <br>```python manage.py migrate```<br> then creating a superuser with <br>```python manage.py createsuperuser```.

Now when visiting ```http://127.0.0.1:8000/api/token/``` you should see input fields for a username and password. Login using the superuser login you just created.

After POSTing your login credentials, you should receive a refresh and access token that looks like this:

```HTTP
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY3NjU5MTcyMywiaWF0IjoxNjc2NTA1MzIzLCJqdGkiOiI2MTBlM2I4NTk3ZGQ0NGQ2YTk3MWViZTEwYzQzOTg3YiIsInVzZXJfaWQiOjF9.P5ps5AOBp25_HoeiatbC7_LZjoBBb0SxukvcpyvuaqI",
    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjc2NTA1NjIzLCJpYXQiOjE2NzY1MDUzMjMsImp0aSI6IjUxMTUzYTRiNmJkNjQyNTY4NDMzN2UyZjEyN2M2YTkwIiwidXNlcl9pZCI6MX0.O1n1TppJFk0KO8rUco1UWPaOcCyxaRPFOmIZv0Pte18"
}
```

Copy the refresh token you were just provided and then navigate to ```http://127.0.0.1:8000/api/token/refresh```, where you should see an input field for the refresh token. Paste and submit the refresh token. You should receive a new access token from the server if everything has worked.

<br>

---

## Customizing JWT behavior

There is a lot of potential customization to the behavior of JWT that can be found [here](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html), but I want to highlight a few that are of interest to us:
```python
"ACCESS_TOKEN_LIFETIME": timedelta(minutes=5), # Specifies how long access tokens are valid. Typically use a lower value for higher security but more network overhead. Changing this will be useful for testing.

"REFRESH_TOKEN_LIFETIME": timedelta(days=1), # Specifies how long refresh tokens are valid, this corresponds to how longer a user can remain logged in while not actively refreshing their tokens. Ex: if a user closes the tab for 22 hours, on reopening, the old refresh token would still be able to fetch a valid access token, continuing their authentication. Changing this will be useful for testing.

"ROTATE_REFRESH_TOKENS": False, # When set to True, if a refresh token is submitted to the TokenRefreshView, a new refresh token will be returned along with the new access token. This provides a way to keep a rolling authentication while a client is open.

"BLACKLIST_AFTER_ROTATION": False, # Causes refresh tokens submitted to the TokenRefreshView to be added to the blacklist. This prevents the scenario where a bad actor can use old refresh tokens to request their own new authentication tokens.
```

While ```ACCESS_TOKEN_LIFETIME``` and ```REFRESH_TOKEN_LIFETIME``` can remain as default for now, we want to change both ```ROTATE_REFRESH_TOKENS``` and ```BLACKLIST_AFTER_ROTATION``` to ```True```. Using the default settings from the documentation, we can add this section to the ```settings.py``` file with the new values.
```python
from datetime import timedelta
...

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}
```
To enable the blacklist, we need to add the blacklist app to our list of installed apps and migrate the assocaited data model changes:
```python
INSTALLED_APPS = [
    ...
    'rest_framework_simplejwt.token_blacklist',
    ...
]
```
```python manage.py migrate```


Now when you visit ```http://127.0.0.1:8000/api/token/``` and login, and use the refresh token at ```http://127.0.0.1:8000/api/token/refresh/```, you should receive both a new access token and a new refresh token. You can also test the blacklist is functioning by trying to submit the same refresh token a second time. You should receive a response like this, indicating that token has already been used.

```HTTP
HTTP 401 Unauthorized
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept
WWW-Authenticate: Bearer realm="api"

{
    "detail": "Token is blacklisted",
    "code": "token_not_valid"
}
```

---

<!-- TOC --><a name="customizing-jwt-token-include-the-username"></a>
## Customizing JWT token - include the username

JWT tokens can be customized to include specific data. If you paste an access token into the debugger at [jwt.io](https://jwt.io/), you can see the payload data that it contains. This data usually includes the user_id, but what if we wanted to include the username as well without having to make a separate request to the server?

To do this, we can create a custom serializer that extends the ```TokenObtainPairSerializer``` class and overrides the ```get_token()``` method. In this method, we can add a new claim to the token, such as the username. The modified serializer looks like this:

```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
```

Next, we need to create a custom view that uses our custom serializer instead of the default one. We can do this by creating a new view that extends the ```TokenObtainPairView``` class and sets its ```serializer_class``` attribute to our custom serializer. Here's what the new view looks like:
```python
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
```

Finally, we need to modify the URL to point to our new custom view. In our ```urls.py``` file, we replace ```TokenObtainPairView``` with ```MyTokenObtainPairView```:

```python
from django.urls import path
from .views import MyTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

<!-- TOC --><a name="allowing-frontend-access-with-cors"></a>
## Allowing Frontend Access with CORS

To allow requests from our frontend application, we need to set up Cross-Origin Resource Sharing (CORS) configuration for our Django project. The  [django-cors-headers](https://pypi.org/project/django-cors-headers/) library provides a simple way to enable CORS in our application.

First, we need to install the ```django-cors-headers``` package by running the following command: <br> ```pip install django-cors-headers```

Next, add ```corsheaders``` to the ```INSTALLED_APPS``` list in the ```settings.py``` file:
```python
INSTALLED_APPS = [
    ...,
    "corsheaders",
    ...,
]
```
After that, add the ```CorsMiddleware``` to the ```MIDDLEWARE``` list:
```python
MIDDLEWARE = [
    ...,
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    ...,
]
```

Now we can configure the allowed origins in the ```settings.py``` file. For simplicity, we will allow all origins using the following setting:

```python
CORS_ALLOW_ALL_ORIGINS = True
```

Note that this setting should be modified to specify the allowed origins during deployment for security reasons.

With these settings, our Django backend is ready to receive requests from a frontend application.

<br>

---