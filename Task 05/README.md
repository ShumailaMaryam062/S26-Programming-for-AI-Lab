# 🖼️ Digital Image Processing and Enhancement

A comprehensive image processing laboratory implement using Python and OpenCV for advanced image transformation, filtering, and enhancement techniques.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5+-green.svg)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)

## ✨ Features

- 🔄 **Image Blurring** - Gaussian, Bilateral, and Motion blur implementations
- ⚡ **Contrast Stretching** - Enhance image contrast and dynamic range
- 🌞 **Gamma Transformation** - Adjust image brightness with non-linear scaling
- 🔀 **Morphological Operations** - Erosion, dilation, and custom kernels
- 📊 **Histogram Equalization** - Improve tonal distribution
- 🎬 **Video Processing** - Apply transformations to video frames
- 📈 **Image Analysis** - Statistical analysis and visualization
- 🎨 **Filter Kernels** - Custom filter design and application

## 📁 Project Structure

```
Task 05/
├── README.md                           # Project documentation
├── Lab task 5.ipynb                    # Main Jupyter notebook with all implementations
├── Tqask 5.pdf                         # Task specification document
├── Images/                             # Input and output images
│   ├── Task 5.jpg                      # Original test image
│   ├── gaussian_blur.jpg               # Gaussian blur results
│   ├── contrast_stretch.jpg            # Contrast enhancement output
│   ├── gamma_transformed*.jpg          # Gamma transformation variants
│   ├── log_transformed.jpg             # Logarithmic transformation
│   ├── mask.jpg                        # Morphological mask
│   └── taj_bilateral.jpg               # Bilateral filter output
└── Video/
    └── cat.mp4                         # Sample video for processing
```

## 🔧 Installation

### Prerequisites

- Python 3.8+
- Jupyter Notebook
- OpenCV (cv2)
- NumPy
- Matplotlib

### Setup

1. **Clone or download the project**

2. **Install dependencies**
   ```bash
   pip install opencv-python numpy matplotlib jupyter
   ```

3. **Launch Jupyter Notebook**
   ```bash
   jupyter notebook "Lab task 5.ipynb"
   ```

## 📚 Techniques Implemented

### Image Enhancement
- **Gaussian Blur**: Smoothing with configurable kernel size
- **Bilateral Filter**: Edge-preserving blur technique
- **Motion Blur**: Simulating motion effect

### Intensity Transformations
- **Gamma Correction**: Brightness adjustment (gamma > 1: darker, gamma < 1: brighter)
- **Logarithmic Transformation**: Enhance dark regions
- **Contrast Stretching**: Map intensity range to full dynamic range

### Morphological Operations
- **Erosion**: Reduce white regions
- **Dilation**: Expand white regions
- **Opening**: Erosion followed by dilation
- **Closing**: Dilation followed by erosion
- **Custom Kernels**: Arbitrary structural elements

### Filtering
- **Median Filter**: Remove salt-and-pepper noise
- **Custom Kernels**: User-defined filter matrices
- **Histogram Analysis**: Visual intensity distribution

## 📊 Example Outputs

The notebook generates various transformed versions:
- Original image → Blurred versions (Gaussian, bilateral, motion)
- Contrast-stretched image with enhanced details
- Gamma-corrected images at different gamma values (0.1, 0.5, 1.2, 2.2)
- Morphologically processed images
- Video frame-by-frame analysis and transformation

## 🚀 Usage

Open `Lab task 5.ipynb` in Jupyter and run cells sequentially:

1. Import libraries and load image
2. Apply individual transformations
3. Visualize results with matplotlib
4. Analyze histograms and statistics
5. Process video frames

## 📝 Notes

- Images are resized to 1900×800 resolution for consistency
- Color space conversions (BGR ↔ RGB) handled for proper visualization
- Video processing includes frame extraction and re-encoding
- All transformations are non-destructive to original files

## 📦 Dependencies Version

```
opencv-python>=4.5.0
numpy>=1.19.0
matplotlib>=3.3.0
jupyter>=1.0.0
```
