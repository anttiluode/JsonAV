import os
import json
import shutil
from typing import Tuple

class OrganizeStoryAssetsFinal:
    def __init__(self):
        self.output_directory = "organized_assets"
        self.comfyui_output_directory = "comfyui/output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_story_path": ("STRING", {"default": "output_json/story.json", "description": "Path to the JSON story file."}),
                "audio_directory": ("STRING", {"default": "tts_output", "description": "Directory containing generated audio files."}),
            }
        }

    RETURN_TYPES = ("STRING", "TRIGGER")
    RETURN_NAMES = ("status_message", "trigger_output")
    FUNCTION = "organize_assets"
    CATEGORY = "Custom Nodes/Asset Organization"

    def organize_assets(self, json_story_path: str, audio_directory: str) -> Tuple[str, str]:
        try:
            # Load the JSON story
            with open(json_story_path, 'r') as file:
                story = json.load(file)

            # Ensure the output directory exists
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)

            # List all images in comfyui/output
            all_images = sorted(
                [f for f in os.listdir(self.comfyui_output_directory) if f.endswith(('.png', '.jpg'))],
                key=lambda x: os.path.getmtime(os.path.join(self.comfyui_output_directory, x))
            )

            image_index = 0

            # Organize actor images
            for actor in story.get("actors", []):
                actor_name = actor["name"].replace(" ", "_").lower()
                if image_index < len(all_images):
                    actor_image_file = all_images[image_index]
                    actor_image_path = os.path.join(self.comfyui_output_directory, actor_image_file)
                    new_actor_image_name = f"{actor_name}.png"
                    shutil.move(actor_image_path, os.path.join(self.output_directory, new_actor_image_name))
                    print(f"Moved actor image {actor_image_file} to {new_actor_image_name}")
                    image_index += 1
                else:
                    print(f"[WARN] Not enough images available for actor: {actor_name}")

            # Organize scene images and audio files
            for i, scene in enumerate(story.get("scenes", [])):
                scene_number = scene["scene_number"]
                
                if image_index < len(all_images):
                    scene_image_file = all_images[image_index]
                    scene_image_path = os.path.join(self.comfyui_output_directory, scene_image_file)
                    new_scene_image_name = f"scene_{scene_number:02d}.png"
                    shutil.move(scene_image_path, os.path.join(self.output_directory, new_scene_image_name))
                    print(f"Moved scene image {scene_image_file} to {new_scene_image_name}")
                    image_index += 1
                else:
                    print(f"[WARN] Not enough images available for scene {scene_number}. Expected more images.")

                # Move audio files for each actor in the scene
                for actor in scene.get("actors_in_scene", []):
                    actor_name = actor["name"].replace(" ", "_").lower()
                    dialogue = actor.get("dialogue")

                    if dialogue:  # Only move audio if there's dialogue
                        audio_file_name = f"scene_{scene_number:02d}_{actor_name}.mp3"
                        audio_file_path = os.path.join(audio_directory, audio_file_name)
                        if os.path.exists(audio_file_path):
                            shutil.move(audio_file_path, os.path.join(self.output_directory, audio_file_name))
                            print(f"Moved audio {audio_file_name} to {self.output_directory}")
                        else:
                            print(f"[WARN] Audio file not found: {audio_file_name}")

                # Move narration audio files for the scene
                narration_file_name = f"scene_{scene_number:02d}_narration.mp3"
                narration_file_path = os.path.join(audio_directory, narration_file_name)
                if os.path.exists(narration_file_path):
                    shutil.move(narration_file_path, os.path.join(self.output_directory, narration_file_name))
                    print(f"Moved narration {narration_file_name} to {self.output_directory}")
                else:
                    print(f"[WARN] Narration file not found: {narration_file_name}")

            # Return status message and trigger output
            return "Assets organized successfully.", "TRIGGER_OUTPUT"

        except Exception as e:
            return f"[ERROR] Failed to organize assets: {str(e)}", "TRIGGER_OUTPUT"

# Node mappings for integration with ComfyUI
NODE_CLASS_MAPPINGS = {
    "OrganizeStoryAssetsFinal": OrganizeStoryAssetsFinal
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OrganizeStoryAssetsFinal": "Organize Story Assets Final"
}
