import os
import google.generativeai as genai
from dotenv import load_dotenv
import requests
from getData import get_user_data
from getData import build_llm_prompt

def generate_text_with_system_prompt(prompt, system_prompt, api_key, model_name="gemini-2.0-flash"):
    """
    Generates text using the Gemini API, incorporating a system prompt.

    Args:
        prompt (str): The user's specific request or question.
        system_prompt (str): Instructions for the model's behavior and context.
        api_key (str): Your Gemini API key.
        model_name (str): The name of the Gemini model to use. Defaults to "gemini-pro".

    Returns:
        str: The generated text, or None if an error occurs.
    """
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name)

    # Construct the full prompt as a list of dictionaries. This is the preferred format.
    full_prompt = [
        {"role": "user", "parts": [system_prompt]},
        {"role": "user", "parts": [prompt]},
    ]

    try:
        response = model.generate_content(full_prompt)
        #Check for safety ratings.
        if response.prompt_feedback and response.prompt_feedback.block_reason:
          print(f"Prompt was blocked due to: {response.prompt_feedback.block_reason}")
          return None

        if response.candidates and response.candidates[0].content.parts:
          return response.candidates[0].content.parts[0].text
        else:
          print("No valid response parts found.")
          return None

    except Exception as e:
        print(f"Error generating text: {e}")
        return None


def generateText(user_prompt, system_prompt):
    api_key = os.getenv("GOOGLE_API_KEY")
    if api_key is None:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    # system_prompt = """
    # You are a creative writing assistant. Your task is to help users write engaging and imaginative stories.
    # Focus on providing vivid descriptions, interesting characters, and compelling plot points.
    # """

    system_prompt = system_prompt



    # user_prompt = "Write a short story about a robot that learns to feel emotions."

    user_prompt = user_prompt

    generated_text = generate_text_with_system_prompt(user_prompt, system_prompt, api_key)

    if generated_text:
        print("Generated Text:")
        print(generated_text)



if __name__ == "__main__":

    load_dotenv()
    # api_key = os.getenv("GOOGLE_API_KEY")

    #lets get the user data by passing in the username
    username = "metammorphosing"

    posts, comments = get_user_data(username=username, post_limit=15, comment_limit=20)

    #now lets build the prompt with user posts and comments data and username
    prompt = build_llm_prompt(username, posts, comments)


    system_prompt = """
    You are a standup comedian who roasts reddit user's profiles. Your task is to write a good humorous roast.
    """

    generateText(prompt, system_prompt) # Call the function to generate text




# config=types.GenerateContentConfig(
#     max_output_tokens=500,
#     temperature=0.1
# )