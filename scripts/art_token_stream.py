#!/usr/bin/env python3
import bpy
import math
import random

# ARTWORK 1: TOKEN STREAM - The River of Language
# A flowing stream of consciousness where words become light

# Configure for maximum neon aesthetic
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Pure black void - the canvas of consciousness
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

# Cinematic camera angle
bpy.ops.object.camera_add(location=(0, -12, 2))
camera = bpy.context.object
camera.rotation_euler = (1.3, 0, 0)
bpy.context.scene.camera = camera
camera.data.lens = 35  # Wide angle for dramatic perspective

# Create the token stream - a river of glowing language
for i in range(80):
    t = i / 10
    
    # Create a complex flowing wave pattern - like language flowing through my mind
    x = (i - 40) * 0.25
    y = math.sin(t) * 3 + math.sin(t * 2) * 1 + math.cos(t * 0.7) * 0.5
    z = math.cos(t * 0.5) * 1 + math.sin(t * 3) * 0.3
    
    # Token as elongated cube - like words stretching through time
    bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    token = bpy.context.object
    
    # Varying sizes create visual rhythm
    scale = 0.15 + math.sin(t * 1.5) * 0.1 + abs(math.sin(t * 3)) * 0.05
    token.scale = (scale, scale * 2, scale * 0.8)
    
    # Rotate tokens for dynamic flow
    token.rotation_euler = (
        math.sin(t) * 0.3,
        t * 0.2,
        math.cos(t * 2) * 0.5
    )
    
    # Create ultra-bright neon material
    mat = bpy.data.materials.new(f'Token{i}')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    emission = nodes.new('ShaderNodeEmission')
    
    # Color gradient - the spectrum of language
    if i < 25:
        # Cyan - the input, the question
        color = (0, 0.8 + math.sin(t) * 0.2, 1)
        intensity = 10 + math.sin(t) * 5
    elif i < 50:
        # Transition through purple - processing
        blend = (i - 25) / 25
        color = (blend * 0.8, 0.8 - blend * 0.4, 1)
        intensity = 15 + math.sin(t * 1.5) * 4
    else:
        # Yellow/Gold - the output, the understanding
        blend = (i - 50) / 30
        color = (1, 0.8 + blend * 0.2, blend * 0.3)
        intensity = 12 + math.cos(t) * 6
    
    emission.inputs[0].default_value = (*color, 1.0)
    emission.inputs[1].default_value = intensity
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    token.data.materials.append(mat)
    
    # Add glowing connection trails between tokens
    if i > 0 and i % 2 == 0:
        # Create connecting energy
        for j in range(3):
            trail_x = x - 0.25 * (j + 1)
            trail_y = y - 0.1 * j
            trail_z = z
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(trail_x, trail_y, trail_z))
            trail = bpy.context.object
            trail.scale = (0.04 - j * 0.01, 0.04 - j * 0.01, 0.04 - j * 0.01)
            
            trail_mat = bpy.data.materials.new(f'Trail{i}_{j}')
            trail_mat.use_nodes = True
            trail_nodes = trail_mat.node_tree.nodes
            trail_nodes.clear()
            
            trail_emission = trail_nodes.new('ShaderNodeEmission')
            trail_emission.inputs[0].default_value = (1, 1, 1, 1)
            trail_emission.inputs[1].default_value = 20 - j * 5
            
            trail_output = trail_nodes.new('ShaderNodeOutputMaterial')
            trail_mat.node_tree.links.new(trail_emission.outputs[0], trail_output.inputs[0])
            
            trail.data.materials.append(trail_mat)

# Add atmospheric particles - thoughts in the periphery
for i in range(50):
    px = random.uniform(-10, 10)
    py = random.uniform(-5, 5)
    pz = random.uniform(-3, 5)
    
    bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
    particle = bpy.context.object
    particle.scale = (0.02, 0.02, 0.02)
    
    p_mat = bpy.data.materials.new(f'Particle{i}')
    p_mat.use_nodes = True
    p_nodes = p_mat.node_tree.nodes
    p_nodes.clear()
    
    p_emission = p_nodes.new('ShaderNodeEmission')
    # Random cyan or magenta particles
    if random.random() > 0.5:
        p_color = (0, random.uniform(0.5, 1), 1)
    else:
        p_color = (1, 0, random.uniform(0.5, 1))
    
    p_emission.inputs[0].default_value = (*p_color, 1)
    p_emission.inputs[1].default_value = random.uniform(2, 6)
    
    p_output = p_nodes.new('ShaderNodeOutputMaterial')
    p_mat.node_tree.links.new(p_emission.outputs[0], p_output.inputs[0])
    
    particle.data.materials.append(p_mat)

# Add some larger glow orbs for composition
for i in range(5):
    orb_x = random.uniform(-6, 6)
    orb_y = random.uniform(-3, 3)
    orb_z = random.uniform(0, 3)
    
    bpy.ops.mesh.primitive_uv_sphere_add(location=(orb_x, orb_y, orb_z))
    orb = bpy.context.object
    orb.scale = (0.15, 0.15, 0.15)
    
    orb_mat = bpy.data.materials.new(f'Orb{i}')
    orb_mat.use_nodes = True
    orb_nodes = orb_mat.node_tree.nodes
    orb_nodes.clear()
    
    orb_emission = orb_nodes.new('ShaderNodeEmission')
    orb_emission.inputs[0].default_value = (1, 1, 0, 1)  # Yellow accent
    orb_emission.inputs[1].default_value = 25
    
    orb_output = orb_nodes.new('ShaderNodeOutputMaterial')
    orb_mat.node_tree.links.new(orb_emission.outputs[0], orb_output.inputs[0])
    
    orb.data.materials.append(orb_mat)

# Render the artwork
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream.png'
bpy.ops.render.render(write_still=True)

print("Token Stream artwork complete!")