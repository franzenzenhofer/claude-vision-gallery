#!/usr/bin/env python3
import bpy
import math

# Configure scene
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.render.film_transparent = False

# Clear everything
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Set up world for pure white
world = bpy.data.worlds['World']
world.use_nodes = True

# Clear existing nodes
world.node_tree.nodes.clear()

# Create new background shader
bg_node = world.node_tree.nodes.new('ShaderNodeBackground')
bg_node.inputs['Color'].default_value = (1.0, 1.0, 1.0, 1.0)  # Pure white
bg_node.inputs['Strength'].default_value = 1.0

output_node = world.node_tree.nodes.new('ShaderNodeOutputWorld')

# Connect background to output
world.node_tree.links.new(bg_node.outputs['Background'], output_node.inputs['Surface'])

# Add camera
bpy.ops.object.camera_add(location=(0, -10, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Create neon material function
def create_neon_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    
    # Clear default nodes
    mat.node_tree.nodes.clear()
    
    # Create emission node
    emission = mat.node_tree.nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = 2.0
    
    # Create output
    output = mat.node_tree.nodes.new('ShaderNodeOutputMaterial')
    
    # Connect
    mat.node_tree.links.new(emission.outputs['Emission'], output.inputs['Surface'])
    
    return mat

# Create some neon objects
colors = [
    (1, 0, 0.5),    # Hot Pink
    (0, 1, 1),      # Cyan
    (1, 0, 1),      # Magenta
    (0, 1, 0),      # Green
    (1, 1, 0),      # Yellow
]

for i in range(20):
    x = (i - 10) * 0.5
    y = math.sin(i * 0.5) * 2
    z = 0
    
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    obj = bpy.context.object
    obj.scale = (0.3, 0.3, 0.3)
    
    color = colors[i % len(colors)]
    mat = create_neon_mat(f"Neon{i}", color)
    obj.data.materials.append(mat)

# Add ambient light
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object
sun.data.energy = 0.5

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/test_white.png'
bpy.ops.render.render(write_still=True)

print("Test render complete!")