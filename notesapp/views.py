from django.shortcuts import render
from .serializers import NoteSerializer
from .models import Note
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer

@api_view(['GET'])
def search_notes(request):
    query = request.query_params.get("search", "")  # Default to an empty string if query is None
    if query:
        # Perform the search across title, body, and category
        notes = Note.objects.filter(
            Q(title__icontains=query) | Q(body__icontains=query) | Q(category__icontains=query)
        )
        serializer = NoteSerializer(notes, many=True)
        return Response({
            "messages": "Notes retrieved successfully", 
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    else:
        # Optionally handle when the query is empty or not provided
        return Response({
            "messages": "Search query not provided", 
            "data": []
        }, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
def notes(request):
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)
        return Response({"messages":"Notes retrieved successfully","data":serializer.data}, status=status.HTTP_200_OK)
    

    elif request.method == 'POST':
        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Notes created successfully","data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"message":"Failed to create note", "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def note_detail(request, slug):
    try:
        note = Note.objects.get(slug=slug)
    except Note.DoesNotExist:
        return Response({"message":"Note not found"},status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = NoteSerializer(note)
        return Response({"message":"Note retrieved successfully","data":serializer.data})
    
    elif request.method == 'PUT':
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"Note updated successfully","data":serializer.data}, status=status.HTTP_200_OK)
        return Response({"message":"Failed to update note","data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        note.delete()
        return Response({"message":"Note deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
