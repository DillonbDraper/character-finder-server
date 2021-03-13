import json
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from character_finder_api.models import Reader
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def login_user(request):
    '''Handles the authentication of a gamer
    Method arguments:
      request -- The full HTTP request object
    '''
    req_body = json.loads(request.body.decode())
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Use the built-in authenticate method to verify
        username = req_body['username']
        password = req_body['password']
        authenticated_user = authenticate(username=username, password=password)
        # If authentication was successful, respond with their token
        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)
            data = json.dumps({"valid": True, "token": token.key})
            return HttpResponse(data, content_type='application/json')
        else:
            # Bad login details were provided. So we can't log the user in.
            data = json.dumps({"valid": False})
            return HttpResponse(data, content_type='application/json')
@csrf_exempt
def register_user(request):
    '''Handles the creation of a new gamer for authentication
    Method arguments:
      request -- The full HTTP request object
    '''
    # Load the JSON string of the request body into a dict
    req_body = json.loads(request.body.decode())
    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        first_name=req_body['firstName'],
        last_name=req_body['lastName'],
        username=req_body['username'],
        email=req_body['email'],
        password=req_body['password'],
        is_staff=1
    )

    reader = Reader.objects.create(
        user=new_user,
        name=req_body['firstName'] + ' ' + req_body['lastName']
    )
    # Commit the user to the database by saving it
    new_user.save()
    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    reader.save()
    # Return the token to the client
    data = json.dumps({"token": token.key})
    return HttpResponse(data, content_type='application/json')