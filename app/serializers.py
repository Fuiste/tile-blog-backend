from django.http import Http404
from django.contrib.auth import authenticate
from rest_framework import serializers, status, renderers, parsers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from app.models import Post, Image, Blogger
from django.utils import timezone
import urllib2
import json, os


__author__ = 'fuiste'
PAGE_SIZE = int(os.environ.get('PAGE_SIZE'))


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image


class BloggerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blogger


class PostList(APIView):
    model = Post
    serializer_class = PostSerializer
    authentication_classes = (TokenAuthentication,)

    def get(self, request, format=None):
        page = int(request.QUERY_PARAMS.get('page'))
        if page:
            count = Post.objects.all().count() - 1
            upper_bound = page * PAGE_SIZE
            lower_bound = upper_bound - PAGE_SIZE
            if upper_bound > count:
                lower_bound = count - PAGE_SIZE
                if lower_bound < 0:
                    lower_bound = 0
                posts = Post.objects.order_by('-date')[lower_bound:count]
            else:
                posts = Post.objects.order_by('-date')[lower_bound:upper_bound]
        else:
            posts = Post.objects.order_by('-date')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.DATA)
        if serializer.is_valid():
            post = serializer.save()
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageList(APIView):
    model = Image
    serializer_class = ImageSerializer

    def get(self, request, format=None):
        images = Image.objects.all()
        serializer = ImageSerializer(images, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ImageSerializer(data=request.DATA)
        if serializer.is_valid():
            post = serializer.save()
            post.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BloggerDetail(APIView):
    model = Blogger
    serializer_class = BloggerSerializer

    def get_object(self, pk):
        try:
            return Blogger.objects.get(pk=pk)
        except Blogger.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = BloggerSerializer(tgt)
        return Response(serializer.data)


class PostDetail(APIView):
    model = Post
    serializer_class = PostSerializer

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = PostSerializer(tgt)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        req = request.DATA
        if req['cover_photo']:
            req['cover_photo'] = int(req['cover_photo'])
        tgt = self.get_object(pk)
        serializer = PostSerializer(tgt, data=req)
        print serializer.is_valid()
        print serializer.errors
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)


class ImageDetail(APIView):
    model = Image
    serializer_class = ImageSerializer

    def get_object(self, pk):
        try:
            return Image.objects.get(pk=pk)
        except Image.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        tgt = self.get_object(pk)
        serializer = ImageSerializer(tgt)
        return Response(serializer.data)
