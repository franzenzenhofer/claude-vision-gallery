#!/usr/bin/env python3
"""
Generate Algorithm Crystal Visualization
Represents the crystalline structure of efficient algorithms
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_crystal_lattice():
    """Create a crystalline algorithmic structure"""
    clear_scene()
    
    # Create main crystal structure
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=2)
    crystal = bpy.context.active_object
    
    # Apply subdivision modifier
    modifier = crystal.modifiers.new("Subdivision", 'SUBSURF')
    modifier.levels = 2
    modifier.render_levels = 3
    
    # Scale and deform to create crystal shape
    crystal.scale = (1, 1, 2)
    
    # Create crystal material
    mat = bpy.data.materials.new(name="CrystalMaterial")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear default nodes
    for node in nodes:
        nodes.remove(node)
    
    # Add nodes
    output = nodes.new('ShaderNodeOutputMaterial')
    glass = nodes.new('ShaderNodeBsdfGlass')
    emission = nodes.new('ShaderNodeEmission')
    mix = nodes.new('ShaderNodeMixShader')
    fresnel = nodes.new('ShaderNodeFresnel')
    
    # Configure nodes
    glass.inputs[0].default_value = (0.1, 0.3, 0.8, 1.0)  # Blue tint
    glass.inputs[2].default_value = 1.45  # IOR
    emission.inputs[0].default_value = (0.2, 0.6, 1.0, 1.0)  # Blue emission
    emission.inputs[1].default_value = 0.5  # Strength
    fresnel.inputs[0].default_value = 1.45
    
    # Link nodes
    links.new(fresnel.outputs[0], mix.inputs[0])
    links.new(glass.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])
    
    crystal.data.materials.append(mat)
    
    # Create smaller satellite crystals
    for i in range(8):
        angle = i * math.pi * 2 / 8
        x = math.cos(angle) * 3
        y = math.sin(angle) * 3
        z = random.uniform(-1, 1)
        
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            subdivisions=1
        )
        satellite = bpy.context.active_object
        satellite.scale = (0.5, 0.5, 0.8)
        satellite.rotation_euler = (
            random.uniform(0, math.pi),
            random.uniform(0, math.pi),
            random.uniform(0, math.pi)
        )
        satellite.data.materials.append(mat)
    
    # Create energy connections
    for i in range(12):
        start_angle = random.uniform(0, math.pi * 2)
        end_angle = random.uniform(0, math.pi * 2)
        
        start_pos = (
            math.cos(start_angle) * 2,
            math.sin(start_angle) * 2,
            random.uniform(-1.5, 1.5)
        )
        end_pos = (
            math.cos(end_angle) * 3.5,
            math.sin(end_angle) * 3.5,
            random.uniform(-1, 1)
        )
        
        # Create energy beam
        curve = bpy.data.curves.new('beam', 'CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('BEZIER')
        spline.bezier_points.add(1)
        
        spline.bezier_points[0].co = start_pos
        spline.bezier_points[1].co = end_pos
        
        for point in spline.bezier_points:
            point.handle_right_type = 'AUTO'
            point.handle_left_type = 'AUTO'
        
        obj = bpy.data.objects.new('beam', curve)
        bpy.context.collection.objects.link(obj)
        
        curve.bevel_depth = 0.05
        curve.bevel_resolution = 4
        
        # Emission material for beams
        beam_mat = bpy.data.materials.new("BeamMaterial")
        beam_mat.use_nodes = True
        beam_mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.5, 0.8, 1)
        beam_mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
        obj.data.materials.append(beam_mat)
    
    # Create particle system for floating data points
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=5)
    emitter = bpy.context.active_object
    emitter.hide_viewport = True
    emitter.hide_render = True
    
    # Camera
    bpy.ops.object.camera_add(location=(8, -8, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.3, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Lighting
    bpy.ops.object.light_add(type='POINT', location=(5, 5, 5))
    light1 = bpy.context.active_object
    light1.data.energy = 500
    
    bpy.ops.object.light_add(type='POINT', location=(-5, -5, 5))
    light2 = bpy.context.active_object
    light2.data.energy = 300
    light2.data.color = (0.5, 0.7, 1)
    
    # World
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 256
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/algorithm_crystal.png'
    
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    create_crystal_lattice()