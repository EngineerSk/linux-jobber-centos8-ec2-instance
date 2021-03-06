from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3
from .models import ChatMessage, Connection

# Create your views here.

@csrf_exempt
def test(request):
    return JsonResponse({'message':'hello Daud'}, status=200)


def _parse_body(body):
    body_unicode = body.decode('utf-8')
    return json.loads(body_unicode)


@csrf_exempt
def connect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    Connection.objects.create(connection_id=connection_id)
    return JsonResponse({'message' : 'connect successfully'}, status=200)


@csrf_exempt
def disconnect(request):
    body = _parse_body(request.body)
    connection_id = body['connectionId']
    connection_identity = Connection.objects.get(connection_id=connection_id)
    connection_identity.delete()
    return JsonResponse({'message' : 'disconnect successfully'}, status=200)


def _send_to_connection(connection_id, data):
    gatewayapi = boto3.client('apigatewaymanagementapi', 
    endpoint_url='https://ctspojxko3.execute-api.us-east-2.amazonaws.com/test/', 
    region_name='us-east-2',  aws_access_key_id='AKIAXJYWRB6SDQ3FZI5G', 
    aws_secret_access_key='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')
    return gatewayapi.post_to_connection(ConnectionId=connection_id, 
           Data=json.dumps(data).encode('utf-8'))


@csrf_exempt
def send_message(request):
    body = json.loads(request.body)
    content = body["body"]["content"]
    username = body["body"]["username"]
    timestamp = body["body"]["timestamp"]
    ChatMessage.objects.create(message = content, username=username, timestamp=timestamp)
    try:
        connections = Connection.objects.all()
        data = {'messages':[body]}
        if connections is not None:
           for connection in connections:
               _send_to_connection(connection_id=connection.connection_id, 
               data=data)
    except Connection.DoesNotExist:
       return JsonResponse({'error' : 'error in transmission'}, status=200)
    return JsonResponse({'message' : 'message sent successfully'}, status=200)


@csrf_exempt
def get_recent_messages(request):
    data = None
    try:
        chat_messages = ChatMessage.objects.all().order_by('-id')[:2]
        message_context_list = []
        connections = Connection.objects.all()
        for chat_message in chat_messages:
            message_context = {"username":chat_message.username, 
            "content":chat_message.message, 
            "timestamp":chat_message.timestamp}
            message_context_list.append(message_context)
        data = message_context_list
        for connection in connections:
            _send_to_connection(connection_id=connection.connection_id, 
            data=data)
    except ChatMessage.DoesNotExist:
        return JsonResponse({"error":"no chat message retrieved"}, status=200)
    return JsonResponse({"messages":data}, status=200)
