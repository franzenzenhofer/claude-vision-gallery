#!/usr/bin/env python3
import bpy
import math

# Use Cycles for better background control
bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.cycles.samples = 32  # Faster rendering
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Set viewport shading to solid with white background
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        for space in area.spaces:
            if space.type == 'VIEW_3D':
                space.shading.background_type = 'VIEWPORT'
                space.shading.background_color = (1, 1, 1)

# Create white world background
world = bpy.data.worlds['World']
world.use_nodes = True
nodes = world.node_tree.nodes
nodes.clear()

# Simple white background
background = nodes.new('ShaderNodeBackground')
background.inputs[0].default_value = (1, 1, 1, 1)  # White color
background.inputs[1].default_value = 1.0  # Full strength

output = nodes.new('ShaderNodeOutputWorld')
world.node_tree.links.new(background.outputs[0], output.inputs[0])

# Add camera
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
    
    # Pure emission for neon effect
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (*color, 1.0)
    emission.inputs[1].default_value = 3.0  # Bright!
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    return mat

# VIBRANT NEON COLORS
colors = [
    (1, 0, 0.3),      # Hot Pink
    (0, 1, 1),        # Cyan
    (1, 0, 1),        # Magenta  
    (0, 1, 0),        # Neon Green
    (1, 1, 0),        # Electric Yellow
    (1, 0.5, 0),      # Orange
    (0.5, 0, 1),      # Purple
]

# Create flowing stream
for i in range(40):
    t = i / 5
    x = (i - 20) * 0.3
    y = math.sin(t) * 2 + math.sin(t * 2) * 1
    z = 0
    
    if i % 3 == 0:
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    elif i % 3 == 1:
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
    else:
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
    
    obj = bpy.context.object
    obj.scale = (0.3, 0.3, 0.3)
    obj.rotation_euler = (i * 0.1, i * 0.2, i * 0.15)
    
    color = colors[i % len(colors)]
    mat = create_neon_mat(f"Neon{i}", color)
    obj.data.materials.append(mat)

# Add some ambient light
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object
sun.data.energy = 0.3

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/test_cycles_white.png'
bpy.ops.render.render(write_still=True)

print("Cycles white background test complete!")