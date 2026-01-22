from openai import OpenAI
import os
from dotenv import load_dotenv

# --- UPDATED PROMPT WITH MOTION PATHS ---
txt_prompt = '''You are an expert Animation Director and JSON Architect. Your task is to take a written story and convert it into a structured JSON file for a 2D animation engine.

### CANVAS SPECIFICATIONS:
- Size: 1280x720. 
- Coordinates: x:0, y:0 (Top-Left), x:1280, y:720 (Bottom-Right).

### CONSTRAINTS:
1. **Scene Count:** Exactly 4 to 6 scenes.
2. **Movement:** For every character, define a START and END position to create motion over the scene's duration.
3. **Motion Types:** Use "jump" for jumping, "walk" for sliding/bobbing, or "idle" for standing still.

### JSON STRUCTURE DEFINITION:
For each scene:
- `scene_id`: Integer.
- `duration`: Seconds (usually 3-6s).
- `fallback_prompt`: Detailed visual description for AI image generation.
- `background`: { "image": "filename.jpg" }
- `characters`: 
    - `id`: "cat", "boy", etc.
    - `image`: "filename.png"
    - `start_position`: { "x": int, "y": int }  <-- WHERE THEY START
    - `end_position`: { "x": int, "y": int }    <-- WHERE THEY FINISH
    - `motion`: "jump", "walk", or "idle"
- `environment_objects`: Elements like clouds or birds. Use "start_position" and "end_position" here too.

### EXPECTED OUTPUT FORMAT:
[
  {
    "scene_id": 1,
    "duration": 4,
    "fallback_prompt": "Studio Ghibli style, lush garden, sunny day...",
    "background": { "image": "garden.jpg" },
    "characters": [
      {
        "id": "cat",
        "image": "cat_sitting.png",
        "start_position": { "x": 200, "y": 500 },
        "end_position": { "x": 800, "y": 500 },
        "motion": "walk"
      }
    ]
  }
]
Please return ONLY valid JSON.
'''

# --- FILE LOADING ---
# Adjusted paths based on your previous messages
base_path = "C:\\Users\\KIIT\\Documents\\ai-video-generator"
assets_path = os.path.join(base_path, "backend", "assets_structure.md")
story_path = os.path.join(base_path, "backend", "story.txt")

try:
    with open(assets_path, "r") as f:
        img_data = f.read()
    with open(story_path, "r") as f:
        story_content = f.read()
except FileNotFoundError as e:
    print(f"❌ Error loading files: {e}")
    img_data = ""
    story_content = "A boy named raj walks in park"

final_prompt = f"{txt_prompt}\nSTORY:\n{story_content}\nAVAILABLE IMAGES:\n{img_data}"

# --- OPENAI API CALL ---
load_dotenv()
try:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in .env")
        
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": final_prompt}]
    )

    raw_content = response.choices[0].message.content
    
    # Clean JSON formatting
    if "```json" in raw_content:
        raw_content = raw_content.split("```json")[1].split("```")[0].strip()
    elif "```" in raw_content:
        raw_content = raw_content.split("```")[1].split("```")[0].strip()

    # Save to the workers folder
    output_path = os.path.join(base_path, "backend", "workers", "image_gen.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, "w") as f:
        f.write(raw_content)
        
    print(f"✅ Success! New motion-enabled JSON saved to: {output_path}")

except Exception as e:
    print(f"❌ Error: {e}")