#!/usr/bin/env python3
import bpy
import math
import random

# ARTWORK 2: ATTENTION MATRIX - The Web of Focus
# Where consciousness distributes its gaze

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

# Camera
bpy.ops.object.camera_add(location=(0, -12, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)
bpy.context.scene.camera = camera

# Create simplified attention matrix
grid_size = 10
spacing = 1.5

# Create attention nodes in a grid pattern
for i in range(grid_size):
    for j in range(grid_size):
        x = (i - grid_size/2) * spacing
        y = (j - grid_size/2) * spacing
        
        # Create attention patterns
        center_dist = math.sqrt((i - grid_size/2)**2 + (j - grid_size/2)**2)
        diagonal = 1 - abs(i - j) / grid_size
        
        # Multiple attention zones
        weight = 0
        # Central focus
        if center_dist < 3:
            weight = 1 - center_dist / 3
        # Diagonal attention
        if diagonal > 0.7:
            weight = max(weight, diagonal)
        # Random hotspots
        if (i, j) in [(2, 7), (7, 2), (3, 3), (6, 6)]:
            weight = 1.0
        
        # Add some randomness
        weight = weight * 0.8 + random.uniform(0, 0.2)
        
        if weight > 0.1:
            # Create glowing sphere
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, 0))
            node = bpy.context.object
            node.scale = (weight * 0.3, weight * 0.3, weight * 0.3)
            
            # Neon material
            mat = bpy.data.materials.new(f'Att_{i}_{j}')
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            emission = nodes.new('ShaderNodeEmission')
            
            # Color gradient by weight
            if weight > 0.8:
                color = (1, 0, weight)  # Magenta for high attention
                intensity = 20
            elif weight > 0.5:
                color = (0, weight, 1)  # Cyan for medium
                intensity = 15
            else:
                color = (weight, weight, 1)  # Blue for low
                intensity = 8
            
            emission.inputs[0].default_value = (*color, 1.0)
            emission.inputs[1].default_value = intensity * weight
            
            output = nodes.new('ShaderNodeOutputMaterial')
            mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
            node.data.materials.append(mat)

# Add connection beams between high attention nodes
high_attention_nodes = []
for i in range(grid_size):
    for j in range(grid_size):
        x = (i - grid_size/2) * spacing
        y = (j - grid_size/2) * spacing
        
        # Check if this was a high attention node
        center_dist = math.sqrt((i - grid_size/2)**2 + (j - grid_size/2)**2)
        diagonal = 1 - abs(i - j) / grid_size
        
        weight = 0
        if center_dist < 3:
            weight = 1 - center_dist / 3
        if diagonal > 0.7:
            weight = max(weight, diagonal)
        if (i, j) in [(2, 7), (7, 2), (3, 3), (6, 6)]:
            weight = 1.0
            
        if weight > 0.6:
            high_attention_nodes.append((x, y, i, j))

# Create connections
for idx1, (x1, y1, i1, j1) in enumerate(high_attention_nodes):
    for idx2, (x2, y2, i2, j2) in enumerate(high_attention_nodes[idx1+1:], idx1+1):
        distance = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        
        if distance < 3:  # Only connect nearby nodes
            # Create beam
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, 0))
            beam = bpy.context.object
            beam.scale = (0.02, 0.02, distance/2)
            
            # Rotate to point from node1 to node2
            angle = math.atan2(y2-y1, x2-x1)
            beam.rotation_euler = (0, 0, angle)
            
            # Beam material
            beam_mat = bpy.data.materials.new(f'Beam_{idx1}_{idx2}')
            beam_mat.use_nodes = True
            beam_nodes = beam_mat.node_tree.nodes
            beam_nodes.clear()
            
            beam_emission = beam_nodes.new('ShaderNodeEmission')
            beam_emission.inputs[0].default_value = (1, 1, 1, 1)  # White
            beam_emission.inputs[1].default_value = 5
            
            beam_output = beam_nodes.new('ShaderNodeOutputMaterial')
            beam_mat.node_tree.links.new(beam_emission.outputs[0], beam_output.inputs[0])
            beam.data.materials.append(beam_mat)

# Add atmospheric particles
for i in range(40):
    px = random.uniform(-6, 6)
    py = random.uniform(-6, 6)
    pz = random.uniform(-1, 1)
    
    bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
    particle = bpy.context.object
    particle.scale = (0.02, 0.02, 0.02)
    
    p_mat = bpy.data.materials.new(f'Part{i}')
    p_mat.use_nodes = True
    p_nodes = p_mat.node_tree.nodes
    p_nodes.clear()
    
    p_emission = p_nodes.new('ShaderNodeEmission')
    p_emission.inputs[0].default_value = (0, 1, 1, 1)
    p_emission.inputs[1].default_value = random.uniform(2, 6)
    
    p_output = p_nodes.new('ShaderNodeOutputMaterial')
    p_mat.node_tree.links.new(p_emission.outputs[0], p_output.inputs[0])
    particle.data.materials.append(p_mat)

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/attention_matrix.png'
bpy.ops.render.render(write_still=True)

print("Attention Matrix complete!")