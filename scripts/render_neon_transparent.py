#!/usr/bin/env python3
import bpy
import math
from PIL import Image
import os

# Setup scene for transparent background
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = True  # Transparent background
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Camera
bpy.ops.object.camera_add(location=(0, -10, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Create vibrant neon material
def create_neon_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Pure emission for neon glow
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = 3.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    return mat

# VIBRANT NEON COLORS
NEON_COLORS = [
    (1, 0, 0.3),      # Hot Pink
    (0, 1, 1),        # Electric Cyan
    (1, 0, 1),        # Magenta
    (0, 1, 0),        # Neon Green
    (1, 1, 0),        # Electric Yellow
    (1, 0.5, 0),      # Neon Orange
    (0.5, 0, 1),      # Electric Purple
    (0, 0.5, 1),      # Electric Blue
]

# Create token stream visualization
print("Creating token stream...")
for i in range(60):
    t = i / 8
    x = (i - 30) * 0.3
    y = math.sin(t) * 3 + math.sin(t * 2) * 1
    z = math.cos(t * 0.5) * 0.5
    
    # Varied shapes
    shape = i % 3
    if shape == 0:
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    elif shape == 1:
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), segments=16, ring_count=8)
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=2)
    
    obj = bpy.context.object
    
    # Dynamic scaling
    scale = 0.25 + math.sin(t * 1.5) * 0.15
    obj.scale = (scale, scale, scale)
    
    # Rotation for visual interest
    obj.rotation_euler = (
        math.sin(t) * 0.5,
        t * 0.3,
        math.cos(t * 2) * 0.7
    )
    
    # Apply vibrant neon color
    color = NEON_COLORS[i % len(NEON_COLORS)]
    mat = create_neon_mat(f"TokenNeon{i}", color)
    obj.data.materials.append(mat)

# Add some subtle lighting
bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
light = bpy.context.object
light.data.energy = 20
light.data.size = 10
light.data.color = (1, 1, 1)

# Render with transparent background
temp_path = '/home/franz/dev/claude-vision-gallery/temp_transparent.png'
bpy.context.scene.render.filepath = temp_path
bpy.ops.render.render(write_still=True)

# Convert to white background using PIL
print("Converting to white background...")
img = Image.open(temp_path)
# Create white background
white_bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
# Paste the image on white background
white_bg.paste(img, (0, 0), img)
# Convert to RGB (no alpha)
rgb_img = white_bg.convert('RGB')
# Save final image
final_path = '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream.png'
os.makedirs(os.path.dirname(final_path), exist_ok=True)
rgb_img.save(final_path)

# Clean up temp file
os.remove(temp_path)

print("Token stream with white background complete!")