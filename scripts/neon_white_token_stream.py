#!/usr/bin/env python3
import bpy
import math
import random

# NEON ON WHITE - Token Stream
# Explosive colors on pure white canvas

bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

# Clear scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# PURE WHITE BACKGROUND
world = bpy.data.worlds['World']
world.use_nodes = True
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # WHITE!
bg.inputs[1].default_value = 1.0

# Camera
bpy.ops.object.camera_add(location=(0, -12, 2))
camera = bpy.context.object
camera.rotation_euler = (1.3, 0, 0)
bpy.context.scene.camera = camera

# VIBRANT NEON COLORS
NEON_COLORS = [
    (1, 0, 0.5),    # Hot Pink
    (0, 1, 1),      # Electric Cyan
    (1, 0, 1),      # Magenta
    (0.5, 0, 1),    # Electric Purple
    (0, 1, 0),      # Neon Green
    (1, 1, 0),      # Electric Yellow
    (1, 0.5, 0),    # Neon Orange
    (0, 0.5, 1),    # Electric Blue
]

# Create flowing token stream with BRIGHT colors
for i in range(100):
    t = i / 12
    
    # Complex wave pattern
    x = (i - 50) * 0.2
    y = math.sin(t) * 3 + math.sin(t * 2) * 1.5 + math.cos(t * 0.7) * 0.8
    z = math.cos(t * 0.5) * 1.5 + math.sin(t * 3) * 0.5
    
    # Varied geometry - cubes, spheres, cylinders
    shape = i % 3
    if shape == 0:
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
    elif shape == 1:
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), segments=16, ring_count=8)
    else:
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
    
    token = bpy.context.object
    
    # Dynamic sizing
    scale = 0.2 + math.sin(t * 1.5) * 0.15 + abs(math.sin(t * 3)) * 0.1
    if shape == 0:
        token.scale = (scale, scale * 1.5, scale)
    else:
        token.scale = (scale, scale, scale)
    
    # Rotation for dynamism
    token.rotation_euler = (
        math.sin(t) * 0.5,
        t * 0.3,
        math.cos(t * 2) * 0.7
    )
    
    # BRIGHT NEON MATERIAL
    mat = bpy.data.materials.new(f'NeonToken{i}')
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Mix shader for glow effect
    mix = nodes.new('ShaderNodeMixShader')
    emission = nodes.new('ShaderNodeEmission')
    bsdf = nodes.new('ShaderNodeBsdfPrincipled')
    
    # Pick vibrant color
    color = NEON_COLORS[i % len(NEON_COLORS)]
    
    # Emission for glow
    emission.inputs[0].default_value = (*color, 1.0)
    emission.inputs[1].default_value = 2.0  # Bright but not overwhelming on white
    
    # Principled for some substance
    bsdf.inputs[0].default_value = (*color, 1.0)  # Base color
    bsdf.inputs[6].default_value = 0.0  # Metallic
    bsdf.inputs[9].default_value = 0.1  # Roughness
    
    # Mix mostly emission
    mix.inputs[0].default_value = 0.8  # 80% emission
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(bsdf.outputs[0], mix.inputs[1])
    mat.node_tree.links.new(emission.outputs[0], mix.inputs[2])
    mat.node_tree.links.new(mix.outputs[0], output.inputs[0])
    
    token.data.materials.append(mat)

# Add connection streams
for i in range(0, 100, 3):
    if i < 97:
        # Energy connections between tokens
        for j in range(5):
            t1 = i / 12
            t2 = (i + 3) / 12
            
            # Interpolate positions
            blend = (j + 1) / 6
            x = ((i - 50) * 0.2) * (1 - blend) + ((i + 3 - 50) * 0.2) * blend
            y1 = math.sin(t1) * 3 + math.sin(t1 * 2) * 1.5
            y2 = math.sin(t2) * 3 + math.sin(t2 * 2) * 1.5
            y = y1 * (1 - blend) + y2 * blend
            z = math.cos(t1 * 0.5) * 1.5 * (1 - blend) + math.cos(t2 * 0.5) * 1.5 * blend
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=2)
            connection = bpy.context.object
            connection.scale = (0.05, 0.05, 0.05)
            
            # Connection material
            conn_mat = bpy.data.materials.new(f'Connection{i}_{j}')
            conn_mat.use_nodes = True
            conn_nodes = conn_mat.node_tree.nodes
            conn_nodes.clear()
            
            conn_emission = conn_nodes.new('ShaderNodeEmission')
            # Bright white connections
            conn_emission.inputs[0].default_value = (1, 1, 1, 1)
            conn_emission.inputs[1].default_value = 1.0
            
            conn_output = conn_nodes.new('ShaderNodeOutputMaterial')
            conn_mat.node_tree.links.new(conn_emission.outputs[0], conn_output.inputs[0])
            
            connection.data.materials.append(conn_mat)

# Add floating accent particles
for i in range(100):
    px = random.uniform(-10, 10)
    py = random.uniform(-5, 5)
    pz = random.uniform(-3, 5)
    
    bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz), subdivisions=1)
    particle = bpy.context.object
    particle.scale = (0.03, 0.03, 0.03)
    
    p_mat = bpy.data.materials.new(f'Particle{i}')
    p_mat.use_nodes = True
    p_nodes = p_mat.node_tree.nodes
    p_nodes.clear()
    
    p_emission = p_nodes.new('ShaderNodeEmission')
    p_color = random.choice(NEON_COLORS)
    p_emission.inputs[0].default_value = (*p_color, 1)
    p_emission.inputs[1].default_value = 1.5
    
    p_output = p_nodes.new('ShaderNodeOutputMaterial')
    p_mat.node_tree.links.new(p_emission.outputs[0], p_output.inputs[0])
    
    particle.data.materials.append(p_mat)

# Add some light sources for extra glow
bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
sun = bpy.context.object
sun.data.energy = 0.5
sun.data.color = (1, 1, 1)

# Render
bpy.context.scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream.png'
bpy.ops.render.render(write_still=True)

print("Vibrant neon token stream on white complete!")