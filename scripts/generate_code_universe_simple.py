#!/usr/bin/env python3
"""
Generate Code Universe Visualization (Simplified)
Represents the vast universe of code possibilities
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_simple_galaxy(center, radius, star_count):
    """Create a simple galaxy of code stars"""
    for i in range(star_count):
        angle = random.uniform(0, math.pi * 2)
        r = random.uniform(0, radius)
        
        x = center[0] + r * math.cos(angle)
        y = center[1] + r * math.sin(angle)
        z = center[2] + random.uniform(-0.5, 0.5)
        
        size = random.uniform(0.05, 0.15)
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            subdivisions=0,
            radius=size
        )
        star = bpy.context.active_object
        
        mat = bpy.data.materials.new(name="StarMat")
        mat.use_nodes = True
        color = (random.uniform(0.5, 1), random.uniform(0.5, 1), random.uniform(0.8, 1))
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = random.uniform(1, 3)
        star.data.materials.append(mat)

def create_code_universe_simple():
    """Create a simplified code universe"""
    clear_scene()
    
    # Create main galaxy
    create_simple_galaxy((0, 0, 0), 5, 100)
    
    # Create satellite galaxies
    for i in range(3):
        angle = i * math.pi * 2 / 3
        x = math.cos(angle) * 8
        y = math.sin(angle) * 8
        create_simple_galaxy((x, y, random.uniform(-2, 2)), 3, 50)
    
    # Central core
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.8)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("CoreMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0.3, 0.1)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 5.0
    core.data.materials.append(mat)
    
    # Camera
    bpy.ops.object.camera_add(location=(12, -12, 8))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.data.energy = 0.2
    
    # World
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.02, 1.0)
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64  # Reduced for speed
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/code_universe.png'
    
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    create_code_universe_simple()