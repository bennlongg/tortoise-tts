# Tortoise TTS

Tortoise is a text-to-speech program built with the following priorities:

1. Strong multi-voice capabilities. You can clone voices from recordings or select from a large number of prebuilt voices.
2. Natural prosody. Proper emphasis and cadence are critical for believable speech, and Tortoise takes this into account.
3. High quality output. The output should be as close to human quality as possible.

Tortoise takes inspiration from [Deepmind's BigVGAN](https://arxiv.org/abs/2206.04658) and [Facebook's VITS](https://arxiv.org/abs/2106.06103). It uses a GPT-like model to generate autoregressive per-phoneme acoustic features, which are converted into speech using a diffusion model.

## Installation

Tortoise is built against Python 3.9 and Pytorch 1.11.0. It requires an NVIDIA GPU (sorry, no AMD support right now).

To install, first create a virtual environment using your tool of choice (I like `virtualenv`). Then install torchaudio and Tortoise:

```
pip install torch==1.11.0+cu113 torchaudio==0.11.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
pip install git+https://github.com/neonbjb/tortoise-tts.git
```

Finally, you need to install [ffmpeg](https://ffmpeg.org/download.html). On Windows, download the zip file and extract it somewhere, then add the `bin` folder to your PATH environment variable.

## Usage

Tortoise is designed to be as easy-to-use as possible. Here's how you can clone a voice and use it to read text:

```python
from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, load_voice

tts = TextToSpeech()

voice_samples, conditioning_latents = load_voice('train_dotrice')
gen = tts.tts_with_preset("I'm going to speak this", voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset='fast')
torchaudio.save('test.wav', gen.squeeze(0).cpu(), 24000)
```

You can also use Tortoise from the command line:

```
python scripts/tortoise_tts.py --text "I'm going to speak this" --voice train_dotrice --preset fast
```

## Presets

Tortoise comes with several presets that control the speed/quality tradeoff of the output. The default preset is `standard`, which is a good balance between speed and quality. The `fast` preset is much faster, but produces lower quality output. The `ultra_fast` preset is even faster, but produces very low quality output.

You can also create your own presets by copying one of the existing ones and modifying it.

## Voice Cloning

Tortoise can clone voices from recordings. To do this, you need to provide at least one audio clip of the target voice speaking in WAV format (ideally 5-10 seconds long). You can provide multiple clips if you want to improve quality further.

The easiest way to do this is to create a folder in `tortoise/voices` with the name of the voice you want to clone, and put the audio clips in there.

For example, if you want to clone the voice of David Attenborough, you would create a folder called `attenborough` in `tortoise/voices`, and put one or more audio clips of him speaking in there.

Then you can use this voice by passing its name as the `voice` argument:

```python
gen = tts.tts_with_preset("I'm going to speak this", voice_samples=voice_samples, conditioning_latents=conditioning_latents, preset='fast')
torchaudio.save('test.wav', gen.squeeze(0).cpu(), 24000)
```

You can also use Tortoise from the command line:

```
python scripts/tortoise_tts.py --text "I'm going to speak this" --voice attenborough --preset fast
```

## Training

Training Tortoise requires a large dataset of audio clips paired with text transcripts. The dataset should be in the form of a CSV file with two columns: `audio` and `text`. The `audio` column should contain the path to the audio clip, and the `text` column should contain the transcript.

You can train Tortoise by running:

```
python scripts/train.py --dataset /path/to/dataset.csv --output /path/to/output/folder
```

This will train Tortoise on your dataset and save the model weights to `/path/to/output/folder`.

## Acknowledgements

Tortoise was inspired by [Deepmind's BigVGAN](https://arxiv.org/abs/2206.04658) and [Facebook's VITS](https://arxiv.org/abs/2106.06103). It uses a GPT-like model to generate autoregressive per-phoneme acoustic features, which are converted into speech using a diffusion model.

## License

Tortoise is licensed under the MIT license.


