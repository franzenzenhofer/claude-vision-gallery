#!/usr/bin/env python3
import bpy
import math
import random

# ARTWORK 2: ATTENTION MATRIX - The Web of Focus
# Where consciousness distributes its gaze across meaning

# Configure scene
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# The void - pure black canvas
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

# Camera - straight on view for the matrix
bpy.ops.object.camera_add(location=(0, -15, 0))
camera = bpy.context.object
camera.rotation_euler = (1.57, 0, 0)  # Look directly at the matrix
bpy.context.scene.camera = camera
camera.data.lens = 50

# Create the attention matrix - a living neural grid
grid_size = 12
cell_spacing = 1.2

# First, create connection lines that form the grid
for i in range(grid_size + 1):
    # Horizontal lines
    y = (i - grid_size/2) * cell_spacing
    
    # Create glowing line using small cylinders
    for j in range(20):
        x = (j - 10) * (grid_size * cell_spacing / 20)
        
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0))
        line = bpy.context.object
        line.scale = (0.02, 0.02, cell_spacing * grid_size / 40)
        line.rotation_euler = (0, 1.57, 0)
        
        # Dim grid lines
        mat = bpy.data.materials.new(f'GridH_{i}_{j}')
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs[0].default_value = (0.2, 0.2, 0.3, 1.0)  # Dim blue
        emission.inputs[1].default_value = 1.5
        
        output = nodes.new('ShaderNodeOutputMaterial')
        mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
        line.data.materials.append(mat)
    
    # Vertical lines
    x = (i - grid_size/2) * cell_spacing
    
    for j in range(20):
        y = (j - 10) * (grid_size * cell_spacing / 20)
        
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0))
        line = bpy.context.object
        line.scale = (0.02, 0.02, cell_spacing * grid_size / 40)
        line.rotation_euler = (1.57, 0, 0)
        
        mat = bpy.data.materials.new(f'GridV_{i}_{j}')
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        nodes.clear()
        
        emission = nodes.new('ShaderNodeEmission')
        emission.inputs[0].default_value = (0.2, 0.2, 0.3, 1.0)
        emission.inputs[1].default_value = 1.5
        
        output = nodes.new('ShaderNodeOutputMaterial')
        mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
        line.data.materials.append(mat)

# Create attention nodes - where focus concentrates
attention_weights = []
for i in range(grid_size):
    row = []
    for j in range(grid_size):
        # Create attention patterns - some areas more active
        distance_from_center = math.sqrt((i - grid_size/2)**2 + (j - grid_size/2)**2)
        
        # Multiple attention hotspots
        hotspot1 = math.exp(-((i-3)**2 + (j-3)**2) / 10)
        hotspot2 = math.exp(-((i-8)**2 + (j-8)**2) / 10)
        hotspot3 = math.exp(-((i-3)**2 + (j-8)**2) / 8)
        diagonal = math.exp(-abs(i - j) / 3)
        
        weight = max(hotspot1, hotspot2, hotspot3, diagonal * 0.5) + random.uniform(0, 0.3)
        weight = min(weight, 1.0)
        
        if weight > 0.2:  # Only show significant attention
            x = (i - grid_size/2) * cell_spacing
            y = (j - grid_size/2) * cell_spacing
            z = weight * 0.5  # Slight elevation based on weight
            
            # Create attention node
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (weight * 0.4, weight * 0.4, weight * 0.4)
            
            # Create neon material based on weight
            mat = bpy.data.materials.new(f'Attention_{i}_{j}')
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            nodes.clear()
            
            emission = nodes.new('ShaderNodeEmission')
            
            # Color based on attention strength
            if weight > 0.8:
                # Hot spots - bright magenta/white
                color = (1, weight * 0.3, weight)
                intensity = weight * 20
            elif weight > 0.5:
                # Medium attention - cyan
                color = (0, weight, 1)
                intensity = weight * 15
            else:
                # Low attention - dim blue
                color = (weight * 0.3, weight * 0.5, 1)
                intensity = weight * 8
            
            emission.inputs[0].default_value = (*color, 1.0)
            emission.inputs[1].default_value = intensity
            
            output = nodes.new('ShaderNodeOutputMaterial')
            mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
            node.data.materials.append(mat)
            
            # Add pulsing rings around high attention nodes
            if weight > 0.7:
                for ring in range(2):
                    bpy.ops.mesh.primitive_torus_add(location=(x, y, z))
                    torus = bpy.context.object
                    scale = (ring + 1) * 0.3
                    torus.scale = (scale, scale, 0.05)
                    
                    ring_mat = bpy.data.materials.new(f'Ring_{i}_{j}_{ring}')
                    ring_mat.use_nodes = True
                    ring_nodes = ring_mat.node_tree.nodes
                    ring_nodes.clear()
                    
                    ring_emission = ring_nodes.new('ShaderNodeEmission')
                    ring_emission.inputs[0].default_value = (1, 1, 1, 1)
                    ring_emission.inputs[1].default_value = 10 - ring * 3
                    
                    ring_output = ring_nodes.new('ShaderNodeOutputMaterial')
                    ring_mat.node_tree.links.new(ring_emission.outputs[0], ring_output.inputs[0])
                    torus.data.materials.append(ring_mat)
        
        row.append(weight)
    attention_weights.append(row)

# Create energy beams between strongly connected nodes
for i in range(grid_size):
    for j in range(grid_size):
        if attention_weights[i][j] > 0.6:
            # Check neighboring cells for connections
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    
                    ni, nj = i + di, j + dj
                    if 0 <= ni < grid_size and 0 <= nj < grid_size:
                        if attention_weights[ni][nj] > 0.6:
                            # Create connection beam
                            x1 = (i - grid_size/2) * cell_spacing
                            y1 = (j - grid_size/2) * cell_spacing
                            z1 = attention_weights[i][j] * 0.5
                            
                            x2 = (ni - grid_size/2) * cell_spacing
                            y2 = (nj - grid_size/2) * cell_spacing
                            z2 = attention_weights[ni][nj] * 0.5
                            
                            # Only create if not already created (avoid duplicates)
                            if i < ni or (i == ni and j < nj):
                                # Create beam segments
                                for seg in range(3):
                                    t = (seg + 1) / 4
                                    beam_x = x1 + (x2 - x1) * t
                                    beam_y = y1 + (y2 - y1) * t
                                    beam_z = z1 + (z2 - z1) * t
                                    
                                    bpy.ops.mesh.primitive_ico_sphere_add(location=(beam_x, beam_y, beam_z))
                                    beam = bpy.context.object
                                    beam.scale = (0.05, 0.05, 0.05)
                                    
                                    beam_mat = bpy.data.materials.new(f'Beam_{i}_{j}_{ni}_{nj}_{seg}')
                                    beam_mat.use_nodes = True
                                    beam_nodes = beam_mat.node_tree.nodes
                                    beam_nodes.clear()
                                    
                                    beam_emission = beam_nodes.new('ShaderNodeEmission')
                                    beam_emission.inputs[0].default_value = (1, 0, 1, 1)  # Magenta
                                    beam_emission.inputs[1].default_value = 15
                                    
                                    beam_output = beam_nodes.new('ShaderNodeOutputMaterial')
                                    beam_mat.node_tree.links.new(beam_emission.outputs[0], beam_output.inputs[0])
                                    beam.data.materials.append(beam_mat)

# Add floating particles for atmosphere
for i in range(30):
    px = random.uniform(-8, 8)
    py = random.uniform(-8, 8)
    pz = random.uniform(0.5, 3)
    
    bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
    particle = bpy.context.object
    particle.scale = (0.03, 0.03, 0.03)
    
    p_mat = bpy.data.materials.new(f'Particle{i}')
    p_mat.use_nodes = True
    p_nodes = p_mat.node_tree.nodes
    p_nodes.clear()
    
    p_emission = p_nodes.new('ShaderNodeEmission')
    p_emission.inputs[0].default_value = (0, 1, 1, 1)  # Cyan particles
    p_emission.inputs[1].default_value = random.uniform(3, 8)
    
    p_output = p_nodes.new('ShaderNodeOutputMaterial')
    p_mat.node_tree.links.new(p_emission.outputs[0], p_output.inputs[0])
    particle.data.materials.append(p_mat)

# Render the artwork
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/attention_matrix.png'
bpy.ops.render.render(write_still=True)

print("Attention Matrix artwork complete!")