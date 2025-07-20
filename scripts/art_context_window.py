#!/usr/bin/env python3
import bpy
import math
import random

# ARTWORK 3: CONTEXT WINDOW - Layers of Understanding
# Nested frames of perception, each containing different aspects of meaning

# Configure scene
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Pure black void
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

# Camera - angled view to see depth
bpy.ops.object.camera_add(location=(8, -8, 6))
camera = bpy.context.object
camera.rotation_euler = (1.1, 0, 0.785)
bpy.context.scene.camera = camera
camera.data.lens = 35

# Create nested context frames
frames = [
    ("Immediate", 4, 0, (0, 1, 1), 15),      # Cyan - current context
    ("Recent", 3.2, 0.8, (0.5, 0, 1), 12),   # Purple - recent memory
    ("Relevant", 2.4, 1.6, (1, 0, 1), 10),   # Magenta - associated context
    ("Background", 1.6, 2.4, (1, 1, 0), 8),  # Yellow - background knowledge
    ("Core", 0.8, 3.2, (1, 1, 1), 20)        # White - essential understanding
]

for name, size, z_offset, color, intensity in frames:
    # Create frame from glowing bars
    positions = [
        # Top edge
        [(x, size, z_offset) for x in [-size, -size/2, 0, size/2, size]],
        # Bottom edge
        [(x, -size, z_offset) for x in [-size, -size/2, 0, size/2, size]],
        # Left edge
        [(-size, y, z_offset) for y in [-size, -size/2, 0, size/2, size]],
        # Right edge
        [(size, y, z_offset) for y in [-size, -size/2, 0, size/2, size]]
    ]
    
    for edge_positions in positions:
        for pos in edge_positions:
            bpy.ops.mesh.primitive_cube_add(location=pos)
            segment = bpy.context.object
            segment.scale = (0.1, 0.1, 0.1)
            
            # Create neon material
            mat = bpy.data.materials.new(f'{name}_segment')
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            emission = nodes.new('ShaderNodeEmission')
            emission.inputs[0].default_value = (*color, 1.0)
            emission.inputs[1].default_value = intensity
            
            output = nodes.new('ShaderNodeOutputMaterial')
            mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
            segment.data.materials.append(mat)
    
    # Add corner connectors
    corners = [(-size, -size), (size, -size), (size, size), (-size, size)]
    for i, (x, y) in enumerate(corners):
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z_offset))
        corner = bpy.context.object
        corner.scale = (0.15, 0.15, 0.15)
        
        corner_mat = bpy.data.materials.new(f'{name}_corner_{i}')
        corner_mat.use_nodes = True
        corner_nodes = corner_mat.node_tree.nodes
        corner_nodes.clear()
        
        corner_emission = corner_nodes.new('ShaderNodeEmission')
        corner_emission.inputs[0].default_value = (*color, 1.0)
        corner_emission.inputs[1].default_value = intensity * 1.5
        
        corner_output = corner_nodes.new('ShaderNodeOutputMaterial')
        corner_mat.node_tree.links.new(corner_emission.outputs[0], corner_output.inputs[0])
        corner.data.materials.append(corner_mat)

# Add floating context elements
context_elements = [
    ("Query", (-2, 2, 0.5), (0, 1, 1), 0.2),
    ("Memory", (2, 2, 1.5), (0.5, 0, 1), 0.2),
    ("Knowledge", (2, -2, 2.5), (1, 0, 1), 0.2),
    ("Intent", (-2, -2, 1), (1, 1, 0), 0.2),
    ("Focus", (0, 0, 3.5), (1, 1, 1), 0.3)
]

for name, pos, color, size in context_elements:
    bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
    element = bpy.context.object
    element.scale = (size, size, size)
    
    elem_mat = bpy.data.materials.new(name)
    elem_mat.use_nodes = True
    elem_nodes = elem_mat.node_tree.nodes
    elem_nodes.clear()
    
    elem_emission = elem_nodes.new('ShaderNodeEmission')
    elem_emission.inputs[0].default_value = (*color, 1.0)
    elem_emission.inputs[1].default_value = 18
    
    elem_output = elem_nodes.new('ShaderNodeOutputMaterial')
    elem_mat.node_tree.links.new(elem_emission.outputs[0], elem_output.inputs[0])
    element.data.materials.append(elem_mat)
    
    # Add orbiting particles
    for i in range(8):
        angle = (i / 8) * 2 * math.pi
        px = pos[0] + math.cos(angle) * 0.5
        py = pos[1] + math.sin(angle) * 0.5
        pz = pos[2] + math.sin(angle * 2) * 0.1
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
        particle = bpy.context.object
        particle.scale = (0.03, 0.03, 0.03)
        
        p_mat = bpy.data.materials.new(f'{name}_particle_{i}')
        p_mat.use_nodes = True
        p_nodes = p_mat.node_tree.nodes
        p_nodes.clear()
        
        p_emission = p_nodes.new('ShaderNodeEmission')
        p_emission.inputs[0].default_value = (1, 1, 1, 1)
        p_emission.inputs[1].default_value = 10
        
        p_output = p_nodes.new('ShaderNodeOutputMaterial')
        p_mat.node_tree.links.new(p_emission.outputs[0], p_output.inputs[0])
        particle.data.materials.append(p_mat)

# Add depth particles
for i in range(40):
    px = random.uniform(-5, 5)
    py = random.uniform(-5, 5)
    pz = random.uniform(-1, 4)
    
    bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
    depth_particle = bpy.context.object
    depth_particle.scale = (0.02, 0.02, 0.02)
    
    dp_mat = bpy.data.materials.new(f'Depth_{i}')
    dp_mat.use_nodes = True
    dp_nodes = dp_mat.node_tree.nodes
    dp_nodes.clear()
    
    dp_emission = dp_nodes.new('ShaderNodeEmission')
    # Deeper particles are dimmer
    brightness = 1 - (pz / 4)
    dp_emission.inputs[0].default_value = (brightness, brightness, 1, 1)
    dp_emission.inputs[1].default_value = random.uniform(2, 6)
    
    dp_output = dp_nodes.new('ShaderNodeOutputMaterial')
    dp_mat.node_tree.links.new(dp_emission.outputs[0], dp_output.inputs[0])
    depth_particle.data.materials.append(dp_mat)

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/context_window.png'
bpy.ops.render.render(write_still=True)

print("Context Window artwork complete!")