# from django.http import JsonResponse
# from rest_framework.decorators import  api_view,permission_classes
# from transformers import AutoModelForCausalLM, AutoTokenizer
# import torch
# from rest_framework.permissions import AllowAny
# # Load model and tokenizer once (don't load them for each request)
# model_name = "adhityamw11/deepseek-r1-Qwen8b-finetune-medical"  # Replace with your model path
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)
#  # Set model to evaluation mode

# # Set the pad_token if it is not defined
# if tokenizer.pad_token is None:
#     # Option 1: Set pad_token to eos_token
#     tokenizer.pad_token = tokenizer.eos_token

#     # Option 2: Alternatively, you could add a new pad_token like "[PAD]"
#     # tokenizer.add_special_tokens({'pad_token': '[PAD]'})
#     # tokenizer.pad_token = '[PAD]'

#     # Resize model token embeddings if a new token is added
#     model.resize_token_embeddings(len(tokenizer))

# # Now set pad_token_id explicitly to avoid the warning
# tokenizer.pad_token_id = tokenizer.pad_token_id if tokenizer.pad_token else tokenizer.eos_token_id

# @api_view(['POST'])
# @permission_classes([AllowAny])  # Apply the permission directly using the decorator
# def generate_response(request):
#     """
#     Endpoint to generate response for the user's input.
#     """
#     # Extract user input from request data
#     user_input = request.data.get('input', '')
#     if not user_input:
#         return JsonResponse({'error': 'No input provided'}, status=400)

#     # Tokenize the input text
#     inputs = tokenizer(user_input, return_tensors="pt", truncation=True, padding=True, max_length=1024)

#     # Ensure the model runs on the correct device (GPU or CPU)
#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     model.to(device)

#     # Move input tensors to the correct device
#     inputs = {key: value.to(device) for key, value in inputs.items()}

#     # Explicitly create the attention mask if padding tokens are used
#     attention_mask = (inputs['input_ids'] != tokenizer.pad_token_id).to(torch.long)

#     # Generate output using the model with additional generation parameters for diversity
#     with torch.no_grad():
#         outputs = model.generate(
#             input_ids=inputs['input_ids'],
#             attention_mask=attention_mask,  # Pass the attention mask
#             max_length=150,        # Maximum length of the generated sequence
#             num_return_sequences=1,  # Generate 1 sequence at a time
#             temperature=0.9,       # Higher values make it more random
#             top_k=50,              # Top-k sampling to limit the number of tokens to sample from
#             top_p=0.95,            # Nucleus sampling (top-p) to restrict token sampling
#             no_repeat_ngram_size=2, # Prevents repeating n-grams
#             do_sample=True          # Use sampling, not greedy decoding
#         )

#     # Decode the generated tokens back to text
#     generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

#     return JsonResponse({'response': generated_text})