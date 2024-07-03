# UniversalAdMute

Automatically mute streams using OpenCLip models, currently implemented to work with Apple's MobileCLIP-S2-OpenCLIP. No notable load when running on a Ryzen 7 4800HS/GTX 1650 4GB/40GB RAM Zephyrus G14. Every second a screenshot is captured and sent to the model, which calculates it's similarity between `'Television tv advertisement break'` and `'football soccer fifa uefa match tv sports broadcast'`. Using the pycaw library, the active audio device is muted and un-muted according to defined thresholds. Usable on CPU however a longer interval would be desirable.

## Installation
Currently only implemented and tested on Windows. However, only the AudioController module is platform specific.
### For CUDA (NVIDIA GPUS)
`pip install -r requirements.txt`

### For Others
`pip install -r requirements-cpu.txt`


## Dependencies:
```comtypes==1.4.4
open_clip_torch==2.24.0
Pillow==10.4.0
pycaw==20240210
torch==2.3.1+cu121
```