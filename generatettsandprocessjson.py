import os
import json
import asyncio
from typing import Tuple
import edge_tts

class GenerateTTSAndProcessJsonToTXT:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_story_path": ("STRING", {"default": "story.json", "description": "Path to the JSON story file."}),
                "voice_type_male": ("STRING", {"default": "en-US-GuyNeural", "description": "TTS voice for male characters."}),
                "voice_type_female": ("STRING", {"default": "en-US-AriaNeural", "description": "TTS voice for female characters."}),
                "voice_type_narration": ("STRING", {"default": "en-US-JennyNeural", "description": "TTS voice for narration."}),
                "output_text_file": ("STRING", {"default": "generated_prompts.txt", "description": "Output text file name for storing prompts."}),
                "audio_output_directory": ("STRING", {"default": "tts_output", "description": "Directory to save generated audio files."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status_message",)
    FUNCTION = "generate_tts_and_process_json"
    CATEGORY = "Custom Nodes/Generation"

    async def generate_tts(self, text: str, output_path: str, voice: str) -> None:
        try:
            tts = edge_tts.Communicate(text=text, voice=voice)
            await tts.save(output_path)
            print(f"TTS saved to {output_path}")
        except Exception as e:
            print(f"Error during TTS generation: {str(e)}")

    def generate_tts_and_process_json(self, json_story_path: str, voice_type_male: str, voice_type_female: str, voice_type_narration: str, output_text_file: str, audio_output_directory: str) -> Tuple[str]:
        # Load the JSON story
        with open(json_story_path, 'r') as file:
            story = json.load(file)

        # Open the output text file for writing
        with open(output_text_file, 'w') as file:
            # Process actors to create prompts
            for actor in story.get("actors", []):
                actor_name = actor["name"]
                actor_description = actor["description"]
                positive_prompt = f"Portrait of {actor_name}, {actor_description}"
                file.write(f"positive: {positive_prompt}\nnegative: \n\n---\n")

            # Process scenes to create prompts and generate audio
            for scene in story.get("scenes", []):
                scene_number = scene["scene_number"]
                scene_description = scene["description"]
                narration = scene.get("narration")
                actors_in_scene = ", ".join([actor["name"] for actor in scene.get("actors_in_scene", [])])
                positive_prompt = f"Scene {scene_number}: {scene_description} featuring {actors_in_scene}"
                file.write(f"positive: {positive_prompt}\nnegative: \n\n---\n")

                # Generate TTS for narration if it exists
                if narration:
                    output_path = os.path.join(audio_output_directory, f"scene_{scene_number:02d}_narration.mp3")
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    try:
                        loop.run_until_complete(self.generate_tts(narration, output_path, voice_type_narration))
                    finally:
                        loop.close()

                # Generate TTS for each actor's dialogue in the scene
                for actor in scene.get("actors_in_scene", []):
                    actor_name = actor["name"]
                    dialogue = actor.get("dialogue")

                    if dialogue:  # Only generate audio if there's dialogue
                        actor_info = next((a for a in story["actors"] if a["name"] == actor_name), None)
                        if actor_info:
                            voice_type = voice_type_male if actor_info["voice_type"] == "Male" else voice_type_female

                            output_path = os.path.join(audio_output_directory, f"scene_{scene_number:02d}_{actor_name.replace(' ', '_').lower()}.mp3")
                            loop = asyncio.new_event_loop()
                            asyncio.set_event_loop(loop)
                            try:
                                loop.run_until_complete(self.generate_tts(dialogue, output_path, voice_type))
                            finally:
                                loop.close()

        # Return a status message
        return ("Prompts have been saved to generated_prompts.txt",)

# Node mappings for integration with ComfyUI
NODE_CLASS_MAPPINGS = {
    "GenerateTTSAndProcessJsonToTXT": GenerateTTSAndProcessJsonToTXT
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "GenerateTTSAndProcessJsonToTXT": "Generate TTS and Process JSON to TXT"
}
