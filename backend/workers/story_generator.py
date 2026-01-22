from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

def generate_story(user_prompt: str) -> str:
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")
        
        client = OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You write very simple stories for short animated videos."
                },
                {
                    "role": "user",
                    "content": (
                        "Write a simple animated story in 3 to 4 short lines. "
                        "Keep language minimal and visual.\n\n"
                        f"Story idea: {user_prompt}"
                    )
                }
            ],
            max_tokens=90
        )

        story_content = response.choices[0].message.content
        
        # Save story to file
        story_file_path = os.path.join(os.path.dirname(__file__), "story.txt")
        with open(story_file_path, "w") as f:
            f.write(story_content)
        
        print(f"Story saved to {story_file_path}")
        return story_content
    
    except Exception as e:
        print(f"Error generating story: {e}")
        raise


if __name__ == "__main__":
    # Test with a sample prompt
    story = generate_story("lonely robot in a futuristic city")
    print("Generated story:")
    print(story)
