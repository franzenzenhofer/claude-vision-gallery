#!/usr/bin/env python3
import bpy
import math
import random
import os

# Clear old images first
base_path = "/home/franz/dev/claude-vision-gallery/public/"
for root, dirs, files in os.walk(base_path):
    for file in files:
        if file.endswith('.png'):
            os.remove(os.path.join(root, file))
            print(f"Deleted: {file}")

# Setup for WHITE background
def setup_white_scene():
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    
    # Set film to transparent OFF to show world background
    bpy.context.scene.render.film_transparent = False
    
    # Clear scene
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # WHITE BACKGROUND!
    world = bpy.data.worlds['World']
    world.use_nodes = True
    nodes = world.node_tree.nodes
    
    # Clear and recreate
    nodes.clear()
    
    # Add Background node
    bg_node = nodes.new('ShaderNodeBackground')
    bg_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)
    bg_node.inputs['Strength'].default_value = 1.0
    
    # Add output
    output = nodes.new('ShaderNodeOutputWorld')
    
    # Connect
    world.node_tree.links.new(bg_node.outputs[0], output.inputs[0])
    
    # Add soft sun light
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.object
    sun.data.energy = 0.3
    sun.data.color = (1, 1, 1)

def get_neon_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Create nodes
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    emission = nodes.new('ShaderNodeEmission')
    mix = nodes.new('ShaderNodeMixShader')
    output = nodes.new('ShaderNodeOutputMaterial')
    
    # Set colors
    bsdf.inputs['Base Color'].default_value = (*color, 1)
    bsdf.inputs['Roughness'].default_value = 0.2
    
    emission.inputs['Color'].default_value = (*color, 1)
    emission.inputs['Strength'].default_value = 2.0
    
    mix.inputs['Fac'].default_value = 0.8  # 80% emission
    
    # Connect nodes
    mat.node_tree.links.new(bsdf.outputs[0], mix.inputs[1])
    mat.node_tree.links.new(emission.outputs[0], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    
    return mat

# VIBRANT COLORS
COLORS = [
    (1, 0, 0.5),    # Hot Pink
    (0, 1, 1),      # Cyan
    (1, 0, 1),      # Magenta
    (0.5, 0, 1),    # Purple
    (0, 1, 0),      # Green
    (1, 1, 0),      # Yellow
    (1, 0.5, 0),    # Orange
    (0, 0, 1),      # Blue
]

# Create token stream
setup_white_scene()

# Camera
bpy.ops.object.camera_add(location=(0, -12, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Create flowing tokens
for i in range(60):
    t = i / 8
    x = (i - 30) * 0.3
    y = math.sin(t) * 3 + math.sin(t * 2) * 1
    z = 0
    
    # Mix shapes
    if i % 3 == 0:
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    elif i % 3 == 1:
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
    else:
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
    
    token = bpy.context.object
    scale = 0.3 + math.sin(t) * 0.1
    token.scale = (scale, scale, scale)
    
    # Apply vibrant color
    color = COLORS[i % len(COLORS)]
    token.data.materials.append(get_neon_mat(f'Token{i}', color))

# Render
os.makedirs(os.path.dirname(base_path + "thinking/"), exist_ok=True)
bpy.context.scene.render.filepath = base_path + "thinking/token_stream.png"
bpy.ops.render.render(write_still=True)
print("Token Stream complete!")

# Create Attention Matrix
setup_white_scene()

# Camera
bpy.ops.object.camera_add(location=(0, -12, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Grid of attention nodes
for i in range(10):
    for j in range(10):
        weight = random.random()
        if weight > 0.3:
            x = (i - 5) * 1.2
            y = (j - 5) * 1.2
            z = 0
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (weight * 0.4, weight * 0.4, weight * 0.4)
            
            # Color by weight
            if weight > 0.8:
                color = COLORS[0]  # Hot pink
            elif weight > 0.6:
                color = COLORS[1]  # Cyan
            else:
                color = COLORS[3]  # Purple
            
            node.data.materials.append(get_neon_mat(f'Att{i}{j}', color))

# Render
bpy.context.scene.render.filepath = base_path + "thinking/attention_matrix.png"
bpy.ops.render.render(write_still=True)
print("Attention Matrix complete!")

# Context Window
setup_white_scene()

# Camera
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera

# Nested frames
frames = [(4, COLORS[1]), (3, COLORS[3]), (2, COLORS[2]), (1, COLORS[4])]

for size, color in frames:
    # Create square frame from cylinders
    positions = [
        [(size, size, 0), (size, -size, 0)],
        [(size, -size, 0), (-size, -size, 0)],
        [(-size, -size, 0), (-size, size, 0)],
        [(-size, size, 0), (size, size, 0)]
    ]
    
    for start, end in positions:
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        length = 2 * size
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.1, 0.1, size)
        
        # Rotate appropriately
        if start[0] == end[0]:  # Vertical
            edge.rotation_euler = (1.57, 0, 0)
        else:  # Horizontal
            edge.rotation_euler = (0, 1.57, 0)
        
        edge.data.materials.append(get_neon_mat(f'Frame{size}', color))

# Center
bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
center = bpy.context.object
center.scale = (0.5, 0.5, 0.5)
center.data.materials.append(get_neon_mat('Center', COLORS[0]))

# Render
bpy.context.scene.render.filepath = base_path + "thinking/context_window.png"
bpy.ops.render.render(write_still=True)
print("Context Window complete!")

print("\nAll visualizations rendered with WHITE backgrounds!")