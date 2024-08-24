import os
import shutil

class CleanupNodeV6:
    def __init__(self):
        self.directories_to_clean = [
            "tts_output",       
            "output_images",    
            "organized_assets", 
            "comfyui/output"
        ]

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {}
        }

    RETURN_TYPES = ("STRING", "TRIGGER")
    RETURN_NAMES = ("statusMessage", "triggerOutput")
    FUNCTION = "run_cleanup"
    CATEGORY = "Custom Nodes/Cleanup"

    def run_cleanup(self) -> tuple:
        cleanup_status = self.cleanup_files_and_directories()
        return cleanup_status, "TRIGGER_OUTPUT"

    def cleanup_files_and_directories(self) -> str:
        for directory in self.directories_to_clean:
            if directory == "comfyui/output":
                self._clean_output_directory(directory)
            else:
                self._clean_directory(directory)
        return "Cleanup process completed."

    def _clean_directory(self, directory: str):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            print(f"Directory {directory} does not exist. Skipping...")

    def _clean_output_directory(self, directory: str):
        if os.path.exists(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    # Skip directories to preserve subfolder contents
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
        else:
            print(f"Directory {directory} does not exist. Skipping...")

# Node mappings for integration with ComfyUI
NODE_CLASS_MAPPINGS = {
    "CleanupNodeV6": CleanupNodeV6
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "CleanupNodeV6": "Cleanup Node V6"
}
