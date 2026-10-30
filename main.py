"""
Snap-Scene: AI-Powered Story & Animation Generation Engine
Author: Husain Saifee (https://github.com/husain-saifee)
"""

import sys
from backend.workers.story_generator import generate_story


def main():
    print("=" * 60)
    print("🎬 Snap-Scene — AI Story & Animation Generator")
    print("   Transform text prompts into multi-scene animations")
    print("=" * 60)

    try:
        user_input = input("\nEnter your story prompt (or press Enter for default): ").strip()
        if not user_input:
            user_input = "A curious cat explores an enchanted forest at twilight"
            print(f"Using default prompt: '{user_input}'")

        print("\n[1/3] Generating structured story script via LLM...")
        story = generate_story(user_input)

        print("\n" + "-" * 40)
        print("📖 Generated Story Script:")
        print("-" * 40)
        print(story)
        print("-" * 40)
        print("\nNext steps:")
        print(" - Plan 2D motion: python backend/workers/prompt_maker_json.py")
        print(" - Interpolate & render: python backend/workers/video_worker.py")
        print(" - Or run the Colab SVD notebook for neural video generation.")

    except ValueError as e:
        print(f"\n⚠️  Configuration error: {e}")
        print("Please check your .env file and set OPENAI_API_KEY.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
