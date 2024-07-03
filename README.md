# UniversalAdMute

Automatically mute streams using OpenCLIP models, currently implemented to work with Apple's MobileCLIP-S2-OpenCLIP. Every second a screenshot is captured and sent to the model, which calculates it's similarity between `'Television tv advertisement break'` and `'football soccer fifa uefa match tv sports broadcast'`. The active audio device is muted and un-muted according to similarity thresholds. 

No notable load when using CUDA on a Ryzen 7 4800HS/GTX 1650 4GB/40GB RAM Zephyrus G14.

Possible to run on CPU with a very significant load on the processor (32% according to Task Manager).

## Installation
Currently implemented and tested on Windows. However, it's just the AudioController module that is platform specific.
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
numpy==1.26.3
```
