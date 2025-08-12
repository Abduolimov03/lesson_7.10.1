from django.contrib.admin.templatetags.admin_list import pagination
from django.shortcuts import render
from django.core.serializers import serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework import mixins, filters, views
from .models import Flower
from .serializers import FlowerSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination


@api_view(['GET', ])
def flower_list(request):
    flowers = Flower.objects.all()
    serializer = FlowerSerializer(flowers, many=True)

    category = request.GET.get('category')
    if category:
        flowers = flowers.filter(category__name=category)

    search = request.GET.get('search')
    if search:
        flowers = flowers.filter(
            Q(name__icontains=search) | Q(color__icontains=search)
        )

    price_gt = request.GET.get('price_gt')
    if price_gt:
        flowers = flowers.filter(price__gt=price_gt)

    price_lt = request.GET.get('price_lt')
    if price_lt:
        flowers = flowers.filter(price__lt=price_lt)

    ordering = request.GET.get('ordering')
    if ordering:
        flowers = flowers.order_by(ordering)

    paginator = LimitOffsetPagination()
    paginator.page_size = 2
    paginated_flower = paginator.paginate_queryset(flowers, request)

    serializer = FlowerSerializer(paginated_flower, many=True)
    data = {
        'data':serializer.data,
        'count':len(flowers),
        'status':status.HTTP_200_OK
    }
    return paginator.get_paginated_response(data)

@api_view(['POST', ])
def flower_create(request):
    serializer = FlowerSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['GET',])
def flower_detail(request, pk):
    try:
        flower = Flower.objects.get(id=pk)
    except Flower.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    serializer = FlowerSerializer(flower)
    data = {
        'data':serializer.data,
        'status':status.HTTP_200_OK
    }
    return Response(data)

@api_view(['PUT', ])
def flower_update(request, pk):
    flower = Flower.objects.get(id=pk)
    serializer = FlowerSerializer(flower, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['PATCH', ])
def flower_update(request, pk):
    flower = Flower.objects.get(id=pk)
    serializer = FlowerSerializer(flower, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'status':status.HTTP_200_OK})
    return Response({'status':status.HTTP_400_BAD_REQUEST})

@api_view(['DELETE', ])
def flower_delete(request, pk):
    try:
        flower = Flower.objects.get(id=pk)
    except Flower.DoesNotExist:
        return Response({'status':status.HTTP_400_BAD_REQUEST})
    flower.delete()
    return Response({'status':status.HTTP_200_OK})


