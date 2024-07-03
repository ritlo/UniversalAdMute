### Older readme with Ideas
Using vision models to automatically mute sports streams during advertisements

1. Send a screencapture to a vision LLM (CLIP, YOLOV5, EFFICENTNET, potentially custom trained model) every few seconds for processing.
2. Using a preset (for football/soccer, vision tags can include "football, soccer, fifa, uefa, world cup, green pitch") for a specific sport and finding probabilities of an advertisement break starting.
3. Toggling the OS/Browser mute command according to probabilities.
4. CLIP is computationally demanding, other pretrained models, even CLIP will occasionally fail in classifying, need to implement newer, better vision models as they release, end-goal being training our own.
5. Some platforms require DRM circumvention.
6. Possibly better ways to detect ads per platforms, such as any changes in browser.
7. Other detection methods: Sound, the sports franchise/tournament live feed logo
