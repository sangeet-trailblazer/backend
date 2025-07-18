from django.http import JsonResponse
def generate_response(request):
    return JsonResponse({"message": "AI response successful!"})
