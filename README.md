# JsonAV
Json language that
# ComfyUI JSON Code For AV Content

[Watch the tutorial on YouTube](https://youtu.be/ygFL213h17k)

## Installation Instructions

1. **Install Required Libraries:**

   - `moviepy`
   - `edge_tts`

2. **Download and Place the Custom Nodes:**

   Download the following Python scripts and place them in the `main_comfyui/custom_nodes` folder:

   - `generatettsandprocessjson.py`
     - This script generates TTS using Edge TTS and creates visual prompts out of the story for workflow number 1.
   - `organizestoryassetsfinal.py`
     - This script organizes and moves the files to the `organized_assets` folder once they have been created/downloaded using Edge TTS.
   - `stitch5.py`
     - This script stitches the final video together and places it in the `final_output` folder.

3. **Install Inspire Pack:**

   Download and install the [ComfyUI-Inspire-Pack](https://github.com/ltdrdata/ComfyUI-Inspire-Pack) as it will be used to make image batches.

## Workflow Overview

Using this scheme, you can create long-form content. Feel free to modify it or combine it into a singular workflow. I provide it as a three-part workflow since my combined workflow used some modified Inspire code and I did not want to share that. 

### Step 1: Create a JSON Story Structure

Copy and paste the following prompt into your AI of choice:

```
You are an AI tasked with converting a long story into a structured JSON format. The story should be broken down into scenes, and each scene should include a description, narration, and any dialogue between characters. The JSON structure should follow this specific format:

{
  "story_title": "Title of the Story",
  "author": "Author's Name",
  "genre": "Genre of the Story",
  "style": "Narrative Style",
  "actors": [
    {
      "name": "Actor Name",
      "description": "Physical or behavioral description of the actor.",
      "voice_type": "Male or Female"
    },
    ...
  ],
  "scenes": [
    {
      "scene_number": 1,
      "description": "Description of the scene.",
      "narration": "Narrative content providing context or moving the story forward.",
      "actors_in_scene": [
        {
          "name": "Actor Name",
          "dialogue": "Dialogue spoken by the actor."
        },
        ...
      ]
    },
    ...
  ]
}

### Instructions:
1. **Scene Creation**: As you break down the story into scenes, ensure that each scene logically follows the previous one. Each new scene should have a description that makes sense in the context of the story, taking into account what has happened before.
2. **Time Progression**: Build the scenes in a way that shows the progression of time. If the story jumps to a new time or place, update the scene description accordingly.
3. **Actor Identification**: Identify the actors in the story, and for each actor, provide a description and specify whether they have a male or female voice.
4. **Narration and Dialogue**: Extract and format the narration and dialogues within each scene, ensuring they flow naturally from one scene to the next.
5. **Intelligent Scene Continuity**: Use your understanding to create logical and smooth transitions between scenes. For example, if a new scene starts with a different setting or time, provide a description that reflects this change.
```

Ask the AI to write a story for you in that format like. "Write a story about a cat in this format."

### Step 2: Save the JSON

The AI will generate JSON code for a story. Save that code as `story.json` in `output_tts/story.json` under the main ComfyUI folder. 

**Note:** Ensure that the story does not contain `'` or `—` signs as they might cause TTS to speak them as "euro" for some reason. You can try explaining this to the AI when providing the story instructions and ask it not to use them. 

### Step 3: Run Workflow Number One

Run the first workflow (add the story.json location to the node). This will send the dialogue to Microsoft's Azure servers via Edge TTS, receive spoken dialogue as MP3 files, and save them in the `tts_output` folder. You should now also have a `generated_prompts.txt` file in your main ComfyUI folder too. Copy that file to:

```
comfyui/custom_nodes/comfyui-inspire-pack/prompts/example/generated_prompts.txt
```

### Step 4: Run Workflow Number Two

Load workflow number two from Joe Conway's YouTube video description:

[Watch Joe Conway's Video](https://www.youtube.com/watch?v=L5OCsK7T3GQ)

[Link to Workflow](https://www.dropbox.com/scl/fi/zbdrov5wzobj9ugu19e6i/Multiple-images-with-different-prompts.json?rlkey=hx0ef94kpxfrftmp1jdwt7mdc&e=1&st=jm2d50ck&dl=0)

Select `generated_prompts.txt` as your prompt choice in the "load prompts from file" option. Change the save image node to the normal save image node so that images are saved to the `comfyui/output/` folder. Make sure the output folder is empty to avoid incorrect images being used in the next step.

Queue the prompt and run the workflow.

### Step 5: Run Workflow Number Three

Now that you have assets in `tts_output` and images in `comfyui/output/`, run workflow number three.

In this step, the "organize assets" node will copy the images from `comfyui/output/` and the audio from `tts_output` to the `organized_assets` folder created in the main ComfyUI folder. Then, using the JSON in `output_json/story.json` as guide, it will create the video, showing characters when they speak and scenes when they appear. 

If there are any issues with the `story.json` (such as the AI not understanding the task), this may cause errors.

If everything went smoothly, you should now have your final video in the `final_output` folder.

### Step 6: Run Workflow Number Four

In this next step, we have following folders full of content we have to clean: 

tts_output organized_assets comfyui/output

You can do it manually or you can use the workflow number four that does it automatically using cleanupnodeV6.py 

The nodes are under custom_nodes folder in comfyui ui. 

I hope it works for ya.. The code was written by ChatGPT And Claude. 

