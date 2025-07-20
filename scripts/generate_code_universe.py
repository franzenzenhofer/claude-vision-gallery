#!/usr/bin/env python3
"""
Generate Code Universe Visualization
Represents the vast universe of code possibilities and solutions
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_code_galaxy(center, radius, star_count):
    """Create a galaxy of code stars"""
    stars = []
    
    for i in range(star_count):
        # Spiral galaxy distribution
        angle = random.uniform(0, math.pi * 4)
        r = random.uniform(0, radius) ** 0.5  # Square root for better distribution
        spiral_offset = angle * 0.2
        
        x = center[0] + r * math.cos(angle + spiral_offset)
        y = center[1] + r * math.sin(angle + spiral_offset)
        z = center[2] + random.gauss(0, radius * 0.1)
        
        # Create star
        size = random.uniform(0.02, 0.1)
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            subdivisions=1,
            radius=size
        )
        star = bpy.context.active_object
        
        # Material with varying colors
        mat = bpy.data.materials.new(name="StarMaterial")
        mat.use_nodes = True
        
        # Color based on "temperature" (code complexity)
        temp = random.random()
        if temp < 0.3:  # Cool stars - simple code
            color = (0.5, 0.7, 1)
            strength = 2.0
        elif temp < 0.7:  # Medium stars - moderate complexity
            color = (1, 1, 0.8)
            strength = 3.0
        else:  # Hot stars - complex algorithms
            color = (1, 0.3, 0.1)
            strength = 4.0
        
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = strength
        star.data.materials.append(mat)
        
        stars.append(star)
    
    return stars

def create_nebula(location, size):
    """Create a code nebula (cloud of possibilities)"""
    # Use metaballs for organic cloud shape
    mball = bpy.data.metaballs.new('nebula')
    obj = bpy.data.objects.new('nebula', mball)
    bpy.context.collection.objects.link(obj)
    obj.location = location
    
    # Add multiple metaball elements
    for i in range(15):
        element = mball.elements.new()
        element.co = (
            random.gauss(0, size),
            random.gauss(0, size),
            random.gauss(0, size * 0.5)
        )
        element.radius = random.uniform(size * 0.3, size * 0.6)
    
    # Nebula material
    mat = bpy.data.materials.new(name="NebulaMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Volume scatter for cloud effect
    principled = nodes["Principled BSDF"]
    principled.inputs[15].default_value = 0.8  # Transmission
    principled.inputs[0].default_value = (0.2, 0.1, 0.5, 1)  # Base color
    
    # Add volume
    volume = nodes.new('ShaderNodeVolumeScatter')
    volume.inputs[0].default_value = (0.3, 0.2, 0.8, 1)
    volume.inputs[1].default_value = 0.5
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (0.4, 0.3, 0.9, 1)
    emission.inputs[1].default_value = 0.1
    
    add_shader = nodes.new('ShaderNodeAddShader')
    output = nodes["Material Output"]
    
    links.new(principled.outputs[0], add_shader.inputs[0])
    links.new(emission.outputs[0], add_shader.inputs[1])
    links.new(add_shader.outputs[0], output.inputs[0])
    links.new(volume.outputs[0], output.inputs[1])
    
    obj.data.materials.append(mat)
    return obj

def create_code_universe():
    """Create the code universe visualization"""
    clear_scene()
    
    # Create multiple galaxies
    galaxy_centers = [
        (0, 0, 0),      # Central galaxy - main codebase
        (8, 5, 2),      # Libraries galaxy
        (-7, -4, -1),   # Frameworks galaxy
        (5, -6, 3),     # Algorithms galaxy
        (-6, 7, -2)     # Patterns galaxy
    ]
    
    all_stars = []
    for i, center in enumerate(galaxy_centers):
        size = 3 if i == 0 else 2  # Main galaxy is larger
        stars = create_code_galaxy(center, size, 200 if i == 0 else 100)
        all_stars.extend(stars)
    
    # Create nebulae
    nebula_positions = [
        (3, 3, 1),
        (-4, 2, -1),
        (2, -4, 2)
    ]
    
    for pos in nebula_positions:
        create_nebula(pos, 1.5)
    
    # Create connection streams between galaxies
    for i in range(len(galaxy_centers) - 1):
        start = galaxy_centers[0]  # All connect to main
        end = galaxy_centers[i + 1]
        
        # Create particle stream
        for j in range(20):
            t = j / 20.0
            x = start[0] + (end[0] - start[0]) * t
            y = start[1] + (end[1] - start[1]) * t
            z = start[2] + (end[2] - start[2]) * t
            
            # Add some wave motion
            offset = math.sin(t * math.pi * 2) * 0.5
            x += offset * 0.3
            y += offset * 0.3
            
            bpy.ops.mesh.primitive_ico_sphere_add(
                location=(x, y, z),
                radius=0.03
            )
            particle = bpy.context.active_object
            
            # Stream material
            mat = bpy.data.materials.new("StreamMat")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.5, 1, 0.5)
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
            particle.data.materials.append(mat)
    
    # Create central black hole (the core algorithm)
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.5)
    black_hole = bpy.context.active_object
    
    # Black hole material
    mat = bpy.data.materials.new("BlackHoleMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0  # Roughness
    black_hole.data.materials.append(mat)
    
    # Accretion disk
    bpy.ops.mesh.primitive_torus_add(location=(0, 0, 0), major_radius=1.5, minor_radius=0.3)
    disk = bpy.context.active_object
    disk.scale.z = 0.1
    
    # Disk material
    disk_mat = bpy.data.materials.new("DiskMat")
    disk_mat.use_nodes = True
    disk_mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0.5, 0.1)
    disk_mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    disk.data.materials.append(disk_mat)
    
    # Camera
    bpy.ops.object.camera_add(location=(15, -15, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Lighting - minimal for space scene
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.data.energy = 0.1
    
    # World - deep space
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.01, 1.0)  # Almost black with hint of blue
    
    # Add stars in background
    world_output = world.node_tree.nodes["World Output"]
    tex_coord = world.node_tree.nodes.new('ShaderNodeTexCoord')
    noise = world.node_tree.nodes.new('ShaderNodeTexNoise')
    noise.inputs[2].default_value = 500  # Scale
    
    color_ramp = world.node_tree.nodes.new('ShaderNodeValToRGB')
    color_ramp.color_ramp.elements[0].position = 0.95
    color_ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    color_ramp.color_ramp.elements[1].color = (1, 1, 1, 1)
    
    mix = world.node_tree.nodes.new('ShaderNodeMixRGB')
    mix.inputs[1].default_value = (0.0, 0.0, 0.01, 1.0)
    mix.inputs[2].default_value = (0.1, 0.1, 0.2, 1.0)
    
    world.node_tree.links.new(tex_coord.outputs[0], noise.inputs[0])
    world.node_tree.links.new(noise.outputs[0], color_ramp.inputs[0])
    world.node_tree.links.new(color_ramp.outputs[0], mix.inputs[0])
    world.node_tree.links.new(mix.outputs[0], bg.inputs[0])
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/code_universe.png'
    
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    create_code_universe()