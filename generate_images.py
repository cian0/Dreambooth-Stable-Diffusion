import os
import requests
import random 

# Get environment variables
MODEL_ID = os.getenv('MODEL_ID')
MODEL_KEY = os.environ.get('MODEL_KEY')
MODEL_CLASS = os.environ.get('MODEL_CLASS')
MODEL_STEPS = int(os.environ.get('MODEL_STEPS'))
BATCH_SAMPLES = int(os.environ.get('BATCH_SAMPLES'))

# prm = "_KEYS_ some string ^ _KEYS_ another string"
prm = os.environ.get('PR')
prm = prm.replace("_KEYS_", f"{MODEL_KEY} {MODEL_CLASS}")
splittedPrompts = prm.split("^")

for prompt in splittedPrompts:

    r = requests.get('https://lexica.art/api/v1/search?q=' + prompt.replace(' ', '+')) 
    r.json()
    images = r.json()['images']

    # print(images[0]['id'])
    for idx in range(BATCH_SAMPLES):
        get_ipython().system(
            f"""
            python scripts/stable_txt2img.py \
                --ddim_eta 0.0 \
                --n_samples 1 \
                --n_iter $BATCH_ITER \
                --scale 7.0 \
                --ddim_steps 50 \
                --ckpt "./trained_models/$MODEL_ID.ckpt" \
                --prompt "{MODEL_KEY + ' ' + MODEL_CLASS + ' as ' + random.choice(images)['prompt']}"
            """
        )
        print('prompting for ' + MODEL_KEY + ' ' + MODEL_CLASS + ' as ' + random.choice(images)['prompt'])