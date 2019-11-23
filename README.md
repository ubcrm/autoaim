# robomaster-vision

### Armour Panel Detection

This approach uses a pipeline of computer vision and machine learning algorithms to detect the center of the panels. At a high level, the pipeline goes as follows:
```
1. Preprocess Image
2. Bitmask LEDs
3. Locate LED rectangles
4. Match target LEDs
5. Compute center of panel
```
