from django.http import JsonResponse
from rest_framework.decorators import api_view
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load model and tokenizer once (don't load them for each request)
model_name = "adhityamw11/deepseek-r1-Qwen8b-finetune-medical"  # Replace with your model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()  # Set model to evaluation mode

@api_view(['POST'])
def generate_response(request):
    """
    Endpoint to generate response for the user's input.
    """
    # Extract user input from request data
    user_input = request.data.get('input', '')
    if not user_input:
        return JsonResponse({'error': 'No input provided'}, status=400)

    # Tokenize the input text
    inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=1024)
    
    # Ensure the model runs on the correct device (GPU or CPU)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    inputs = {key: value.to(device) for key, value in inputs.items()}

    # Generate output using the model
    with torch.no_grad():
        outputs = model.generate(input_ids=inputs['input_ids'], max_length=150, num_return_sequences=1)

    # Decode the generated tokens back to text
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    return JsonResponse({'response': generated_text})
