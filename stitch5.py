import os
import json
from datetime import datetime
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeAudioClip

class StitchStoryNodeV5:
    def __init__(self):
        self.output_directory = "final_output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "trigger_input": ("TRIGGER", {"forceInput": True}),
                "json_story_path": ("STRING", {"default": "output_json/story.json", "description": "Path to the JSON story file."}),
                "organized_directory": ("STRING", {"default": "organized_assets/", "description": "Directory containing organized image and audio files."}),
                "output_filename": ("STRING", {"default": "final_story.mp4", "description": "Filename for the final video output."}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status_message",)
    FUNCTION = "stitch_story"
    CATEGORY = "Custom Nodes/Story"

    def stitch_story(self, trigger_input, json_story_path: str, organized_directory: str, output_filename: str):
        if not trigger_input:
            return "[INFO] No trigger received. Node did not execute."

        try:
            # Load the story JSON
            with open(json_story_path, 'r') as file:
                story = json.load(file)

            # Process each scene
            scene_clips = []
            for scene in story.get("scenes", []):
                scene_number = scene.get("scene_number")
                
                # Initialize lists to hold the visuals and audio in order
                visuals = []
                audio_clips = []

                # Load scene image
                scene_image_path = os.path.join(organized_directory, f"scene_{scene_number:02d}.png")
                if os.path.exists(scene_image_path):
                    scene_image_clip = ImageClip(scene_image_path)
                else:
                    scene_image_clip = None

                # Process each element in the scene (narration first, then actor dialogues)
                if "narration" in scene and scene["narration"]:
                    narration_path = os.path.join(organized_directory, f"scene_{scene_number:02d}_narration.mp3")
                    if os.path.exists(narration_path):
                        narration_clip = AudioFileClip(narration_path)
                        if scene_image_clip:
                            scene_image_clip = scene_image_clip.set_duration(narration_clip.duration)
                            visuals.append(scene_image_clip.set_audio(narration_clip))
                        else:
                            audio_clips.append(narration_clip)
                
                for actor in scene.get("actors_in_scene", []):
                    actor_name = actor.get("name").replace(" ", "_").lower()
                    dialogue_path = os.path.join(organized_directory, f"scene_{scene_number:02d}_{actor_name}.mp3")
                    actor_image_path = os.path.join(organized_directory, f"{actor_name}.png")
                    
                    if os.path.exists(dialogue_path):
                        dialogue_clip = AudioFileClip(dialogue_path)
                        if os.path.exists(actor_image_path):
                            actor_image_clip = ImageClip(actor_image_path).set_duration(dialogue_clip.duration)
                            visuals.append(actor_image_clip.set_audio(dialogue_clip))
                        else:
                            audio_clips.append(dialogue_clip)

                # Combine all visuals and audio for the scene
                if visuals:
                    # Concatenate visual clips if there are multiple
                    scene_clip = concatenate_videoclips(visuals)
                elif audio_clips:
                    # Create a scene clip with just the scene image and audio
                    if scene_image_clip:
                        scene_clip = scene_image_clip.set_audio(CompositeAudioClip(audio_clips))
                    else:
                        scene_clip = CompositeAudioClip(audio_clips).to_soundarray()  # As a fallback, audio only
                else:
                    continue  # Skip if no visuals or audio available
                
                scene_clips.append(scene_clip)

            # Concatenate all scene clips into a final video
            final_clip = concatenate_videoclips(scene_clips)

            # Append the current date and time to the output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{os.path.splitext(output_filename)[0]}_{timestamp}.mp4"

            # Write the final video
            output_path = os.path.join(self.output_directory, output_filename)
            if not os.path.exists(self.output_directory):
                os.makedirs(self.output_directory)
            final_clip.write_videofile(output_path, fps=24)

            return (f"Video successfully created at {output_path}",)

        except Exception as e:
            return (f"[ERROR] Failed to stitch story: {str(e)}",)

# Node mappings for integration with ComfyUI
NODE_CLASS_MAPPINGS = {
    "StitchStoryNodeV5": StitchStoryNodeV5
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StitchStoryNodeV5": "Stitch Story Node V5"
}
