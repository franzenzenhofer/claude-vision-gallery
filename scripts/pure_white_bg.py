#!/usr/bin/env python3
import bpy

# Setup scene
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Enable compositing nodes
bpy.context.scene.use_nodes = True
tree = bpy.context.scene.node_tree
nodes = tree.nodes
nodes.clear()

# Create render layers node
render_layers = nodes.new('CompositorNodeRLayers')

# Create alpha over node to composite over white
alpha_over = nodes.new('CompositorNodeAlphaOver')
alpha_over.inputs[1].default_value = (1, 1, 1, 1)  # White background

# Create composite output
composite = nodes.new('CompositorNodeComposite')

# Link nodes
tree.links.new(render_layers.outputs['Image'], alpha_over.inputs[2])
tree.links.new(alpha_over.outputs['Image'], composite.inputs['Image'])

# Set film to transparent to get alpha channel
bpy.context.scene.render.film_transparent = True

# Camera
bpy.ops.object.camera_add(location=(0, -10, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Create neon material
def create_neon_mat(name, color):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = 2.0
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    return mat

# Neon colors
colors = [
    (1, 0, 0.5),    # Hot Pink
    (0, 1, 1),      # Cyan
    (1, 0, 1),      # Magenta
    (0, 1, 0),      # Green
    (1, 1, 0),      # Yellow
    (1, 0.5, 0),    # Orange
]

# Create objects
import math
for i in range(30):
    t = i / 5
    x = (i - 15) * 0.4
    y = math.sin(t) * 2.5
    z = 0
    
    if i % 3 == 0:
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    elif i % 3 == 1:
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
    else:
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=2)
    
    obj = bpy.context.object
    obj.scale = (0.3, 0.3, 0.3)
    
    color = colors[i % len(colors)]
    mat = create_neon_mat(f"Neon{i}", color)
    obj.data.materials.append(mat)

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/test_composite_white.png'
bpy.ops.render.render(write_still=True)

print("Composite white background complete!")