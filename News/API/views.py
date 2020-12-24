from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from News.API.serializers import NewsSerializer
from News.models import News


@api_view(['POST', ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def add_news(request):
    serializer = NewsSerializer(data=request.data)
    data = {}
    if serializer.is_valid():
        serializer.save()
        data["success"] = "Message Successfully sent"
    else:
        data["failure"] = "Unable to send your message please check the form"
    return Response(data=data)


@api_view(["PATCH", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def update_news(request, id):
    data = {}
    try:
        news = News.objects.get(pk=id)
    except News.DoesNotExist:
        return Response({'error': ' The Bill you want to update does not exist'},
                        status=status.HTTP_404_NOT_FOUND)
    serializer = NewsSerializer(news, request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        data["success"] = "bill successfully updated"
    else:
        data["failure"] = "we could not save this Service info update"
    return Response(data)


@api_view(["DELETE", ])
@authentication_classes([TokenAuthentication, ])
@permission_classes([IsAuthenticated])
def delete_single_news(request, id):
    try:
        news = News.objects.filter(pk=id)
    except News.DoesNotExist:
        return Response({'error': ' The service you want to delete does not exist'}, status=status.HTTP_404_NOT_FOUND)
    data = {}
    delete_operation = news.delete()
    if delete_operation:
        data["success"] = "service successfully deleted"
    else:
        data["failure"] = "unable to delete service"
    return Response(data=data)