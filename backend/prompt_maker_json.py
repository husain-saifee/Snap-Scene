

from openai import OpenAI
import os
from dotenv import load_dotenv
txt_prompt = '''You are an expert Animation Director and JSON Architect. Your task is to take a written story and convert it into a structured JSON file for a 2D animation engine.

### CANVAS SPECIFICATIONS (CRITICAL):
- The animation canvas size is **1280 (width) x 720 (height)**.
- **Coordinates:** `x: 0, y: 0` is the top-left corner. `x: 1280, y: 720` is the bottom-right corner.
- Ensure all positions and motion paths stay within or enter/exit these bounds logically.

### CONSTRAINTS:
1. **Scene Count:** You must divide the story into exactly **4 to 6 scenes**.
2. **Format:** Output strictly valid JSON.
3. **Detail:** Every scene must have background details, character positions, and resolution resizing.
4. **Visual Description:** The `fallback_prompt` must be highly detailed, describing the art style, lighting, camera angle, and specific colors for AI image generation.

### JSON STRUCTURE DEFINITION:
For each scene, generate an object with these fields:
- `scene_id`: Integer (1, 2, 3...)
- `duration`: Total duration of scene in seconds.
- `fallback_prompt`: A comprehensive description of the scene for an AI image generator. Include specific details about the background style, lighting (e.g., "golden hour," "moonlit"), colors, and mood.
- `background`: 
    - `image`: suggested filename (e.g., "dark_forest.png")
- `background_audio`: (OPTIONAL) Object with `file`, `prompt`, `volume`, `loop`. **OMIT this entire field if no specific audio is implied.**
- `environment_objects`: Background elements (birds, clouds) that move.
- `characters`: The main actors.
    - `id`: Unique string ID.
    - `image`: Filename.
    - `position`: {x, y} coordinates.
    - `resolution_resize`: [width, height] (Integers).
    - `motion`: "idle", "walk", or "jump".
- `composite_objects`: Use when a character interacts with an object (e.g., riding a bike). 
    - `layers`: Array of images to stack.
    - `motion`: The path the group moves.
- `dialogue`: Array of spoken lines.
    - `start_time`: Relative to scene start.
    - `emotion`: Mood of the speaker.
    - `text`: The actual dialogue.
- `text_overlays`: Narrator text or context text on screen.

### EXAMPLE INPUT STORY:
"The boy found a magic carpet. He sat on it and flew over the village."

### EXPECTED OUTPUT FORMAT (Use this schema):
[
  {
    "scene_id": 1,
    "duration": 6,
    "fallback_prompt": "A high-quality 2D animated style wide shot of a lush village garden. In the center, a ginger cat sits on a cobblestone path. The background features thatched-roof cottages under a bright blue sky with fluffy white clouds. Sunlight filters through oak trees, creating dappled shadows. High saturation, crisp lines, Studio Ghibli inspired art style.",
    "background": {
      "image": "village_garden.jpg"
    },
    "background_audio": {
      "file": "garden_ambient.mp3",
      "prompt": "sound of birds chirping and a gentle breeze",
      "volume": 0.5,
      "loop": true
    },
    "environment_objects": [
      { 
        "id": "bird_flapping",
        "image": "flying_bird.png",
        "position": { "x": 300, "y": 100 },
        "resolution_resize": [50, 50],
        "motion": "float" 
      }
    ],
    "characters": [
      {
        "id": "cat",
        "image": "cat_sitting.png",
        "position": { "x": 640, "y": 500 },
        "resolution_resize": [100, 100],
        "motion": "idle"
      }
    ],
    "dialogue": [],
    "text_overlays": []
  }
]

Please return a complete JSON file only. Nothing else.
If specific image files are not available, rely on the `fallback_prompt` to describe the generation needs perfectly.


'''

file_path = "C:\\hsz_projects\\video_maker\\Snap-Scene\\backend\\assets_structure.md"
with open(file_path, "r") as f:
    img_data = f.read()

file_path = "C:\\hsz_projects\\video_maker\\Snap-Scene\\backend\\story.txt"
with open(file_path, "r") as f:
    story_content = f.read()

print(story_content)

final_prompt = txt_prompt  +"story:- \n"+ story_content +"\nimage data\n" + img_data    

print(final_prompt)



load_dotenv()


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
                    "content": final_prompt
                },
                
            ],
          
        )

  story_content = response.choices[0].message.content
  
  # Remove markdown code block formatting if present
  if story_content.startswith("```"):
    story_content = story_content.strip()
    # Remove opening ```json or ```
    story_content = story_content.split("```")[1]
    if story_content.startswith("json"):
      story_content = story_content[4:]
    # Remove closing ```
    story_content = story_content.rsplit("```", 1)[0]
    story_content = story_content.strip()
       
  story_file_path = os.path.join(os.path.dirname(__file__), "image_gen.json")
  with open(story_file_path, "w") as f:
    f.write(story_content)
        
  print(f"Story saved to {story_file_path}")
        
    
except Exception as e:
  print(f"Error generating story: {e}")
  raise



