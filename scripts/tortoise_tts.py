import argparse
import os
import random
import time

import torch
from scipy.io.wavfile import write as write_wav

from tortoise.api import TextToSpeech
from tortoise.utils.audio import load_audio, get_voices
from tortoise.utils.text import split_and_recombine_text


def get_device():
    if torch.cuda.is_available():
        return 'cuda'
    return 'cpu'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', type=str, required=True)
    parser.add_argument('--voice', type=str, required=True)
    parser.add_argument('--preset', type=str, default='fast')
    parser.add_argument('--output_dir', type=str, default='results')
    args = parser.parse_args()

    tts = TextToSpeech()

    voice_samples, conditioning_latents = get_voices(args.voice)

    gen = tts.tts_with_preset(args.text, voice_samples=voice_samples, conditioning_latents=conditioning_latents,
                              preset=args.preset)

    os.makedirs(args.output_dir, exist_ok=True)
    
    for j, waveform in enumerate(gen):
        write_wav(os.path.join(args.output_dir, f'{j}.wav'), 24000, waveform)


if __name__ == '__main__':
    main()

