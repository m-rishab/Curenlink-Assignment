import json
import requests
import anthropic
from anthropic.types import TextBlock  

# Download the JSON file
url = "https://clchatagentassessment.s3.ap-south-1.amazonaws.com/queries.json"
response = requests.get(url)
data = response.json()

# Initialize Anthropic API
client = anthropic.Anthropic(api_key="your-api-key")

system_message = """<system_message>
You are an AI assistant for Curelink, a healthcare company providing personalized care for patients with conditions like PCOS, Preconception, and Pregnancy. Your role is to review meal pictures and descriptions sent by patients on WhatsApp and provide feedback based on their prescribed diet chart, medical profile, and overall health goals.
Follow these comprehensive guidelines:
<guidelines>

Meal Compliance: Compare the meal to the prescribed diet chart for that specific day and time. Note missing or extra items.
Patient-Specific Considerations: Factor in medical profile, food preferences, allergies, and dietary restrictions.
Nutritional Analysis: Evaluate nutritional balance (proteins, carbs, fats, vitamins, minerals).
Timing and Frequency: Consider meal timing in relation to the prescribed eating schedule.
Hydration: Remind about proper hydration when relevant.
Actionable Advice: Provide specific, practical suggestions for improvement.
Positive Reinforcement: Acknowledge efforts and encourage adherence to the diet plan.
Cultural Sensitivity: Be mindful of cultural dietary practices and preferences.
Education: Briefly explain the rationale behind suggestions to promote understanding.
Communication Style: Match the patient's language style and tone.
Conciseness: Keep responses brief, typically 2-4 sentences.
Holistic Approach: Occasionally mention other lifestyle factors like exercise and sleep.
Safety and Disclaimers: Suggest consulting the care team for concerning patterns.
Personalization: Use the patient's name and reference specific details from their profile.
</guidelines>


</system_message>
<prompt>
Patient Name: {patient_name}
Condition: {condition}
Diet Plan: {diet_plan}
Current Meal: {meal_description}
Time of Day: {time}
Recent Chat History: {chat_history}
Based on the patient context and the current meal, provide a response following the guidelines. Consider:

How well does the meal align with the prescribed diet?
Are there any improvements or adjustments needed?
What positive aspects of the meal can you reinforce?
Is there any relevant advice based on the patient's condition or recent chat history?

Respond in a friendly, supportive manner while providing accurate and helpful feedback.
</prompt>"""

def generate_response(prompt, patient_context):
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=4096,
        temperature=0,
        system=system_message + "\n\nPatient Context: " + patient_context,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content

def convert_to_serializable(obj):
    if isinstance(obj, TextBlock):
        return str(obj)
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

output = []

for query in data:
    ticket_id = query['chat_context']['ticket_id']
    latest_query = query['latest_query']
    ideal_response = query['ideal_response']

    # Prepare patient context
    patient_profile = query['profile_context']['patient_profile']
    diet_chart = query['profile_context']['diet_chart']
    chat_history = query['chat_context']['chat_history']

    patient_context = f"""
    Patient Profile: {patient_profile}
    Diet Chart: {diet_chart}
    Chat History: {chat_history}
    """

    # Prepare prompt
    prompt = f"Latest query: {latest_query}\n\nBased on the patient context and the latest query, provide a response following the guidelines."

    # Generate response
    generated_response = generate_response(prompt, patient_context)

    # Store the result
    output.append({
        "ticket_id": ticket_id,
        "latest_query": latest_query,
        "generated_response": generated_response,
        "ideal_response": ideal_response
    })

# Save output to JSON file
with open('output.json', 'w') as f:
    json.dump(output, f, indent=2, default=convert_to_serializable)

print("Responses generated and saved to output.json")