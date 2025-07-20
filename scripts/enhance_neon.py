#!/usr/bin/env python3
from PIL import Image, ImageEnhance, ImageFilter
import os

def enhance_neon_image(input_path, output_path):
    """Enhance neon artwork with glow effects"""
    
    # Open the image
    img = Image.open(input_path)
    
    # Create a glow effect by:
    # 1. Blur the bright parts
    # 2. Overlay back on original
    
    # Extract bright parts (threshold)
    brightness = img.convert('L')
    threshold = 50  # Adjust for more/less glow
    bright_mask = brightness.point(lambda x: x if x > threshold else 0)
    
    # Create glow by blurring bright parts
    glow = img.copy()
    glow = glow.filter(ImageFilter.GaussianBlur(radius=5))
    
    # Enhance colors
    enhancer = ImageEnhance.Color(glow)
    glow = enhancer.enhance(1.5)  # Increase saturation
    
    # Blend original with glow
    img = Image.blend(img, glow, 0.3)
    
    # Final brightness adjustment
    brightness_enhancer = ImageEnhance.Brightness(img)
    img = brightness_enhancer.enhance(1.2)
    
    # Save enhanced image
    img.save(output_path, 'PNG')
    print(f"Enhanced: {output_path}")

# Enhance token stream
enhance_neon_image(
    '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream.png',
    '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream_enhanced.png'
)