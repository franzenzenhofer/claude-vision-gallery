#!/usr/bin/env python3
"""
Generate Data Flow Visualization
Represents how Claude Code processes and transforms data
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_data_particle(location, velocity):
    """Create a data particle"""
    bpy.ops.mesh.primitive_ico_sphere_add(
        location=location,
        subdivisions=1,
        radius=0.05
    )
    particle = bpy.context.active_object
    
    # Material
    mat = bpy.data.materials.new(name="DataParticle")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0, 1, 0.5)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    particle.data.materials.append(mat)
    
    return particle

def create_processing_node(location, node_type="transform"):
    """Create a data processing node"""
    if node_type == "input":
        bpy.ops.mesh.primitive_cube_add(location=location, size=1.5)
    elif node_type == "transform":
        bpy.ops.mesh.primitive_cylinder_add(location=location, radius=0.8, depth=1.5)
    else:  # output
        bpy.ops.mesh.primitive_cone_add(location=location, radius1=1.0, depth=2.0)
    
    node = bpy.context.active_object
    
    # Material based on type
    mat = bpy.data.materials.new(name=f"{node_type}Material")
    mat.use_nodes = True
    
    if node_type == "input":
        color = (0.2, 0.3, 0.8, 1)
    elif node_type == "transform":
        color = (0.8, 0.5, 0.2, 1)
    else:
        color = (0.3, 0.8, 0.3, 1)
    
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
    mat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.1  # Transmission
    mat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = 1.45  # IOR
    
    node.data.materials.append(mat)
    return node

def create_data_flow():
    """Create a data flow visualization"""
    clear_scene()
    
    # Create processing pipeline
    input_node = create_processing_node((-8, 0, 0), "input")
    
    # Transform nodes
    transforms = []
    for i in range(3):
        x = -4 + i * 4
        y = math.sin(i * 1.2) * 2
        transform = create_processing_node((x, y, 0), "transform")
        transforms.append(transform)
    
    output_node = create_processing_node((8, 0, 0), "output")
    
    # Create flowing data particles (static representation)
    for i in range(50):
        t = i / 50.0
        x = -8 + t * 16
        y = math.sin(t * math.pi * 2) * 3
        z = math.cos(t * math.pi * 3) * 2
        
        particle = create_data_particle((x, y, z), (1, 0, 0))
        
        # Vary particle size based on position
        scale = 0.5 + math.sin(t * math.pi * 4) * 0.3
        particle.scale = (scale, scale, scale)
    
    # Create connection tubes
    positions = [(-8, 0, 0)] + [(t.location.x, t.location.y, 0) for t in transforms] + [(8, 0, 0)]
    
    for i in range(len(positions) - 1):
        start = positions[i]
        end = positions[i + 1]
        
        # Create curve
        curve = bpy.data.curves.new('flow', 'CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('BEZIER')
        spline.bezier_points.add(1)
        
        spline.bezier_points[0].co = start
        spline.bezier_points[1].co = end
        
        for point in spline.bezier_points:
            point.handle_right_type = 'AUTO'
            point.handle_left_type = 'AUTO'
        
        obj = bpy.data.objects.new('flow', curve)
        bpy.context.collection.objects.link(obj)
        
        curve.bevel_depth = 0.2
        curve.bevel_resolution = 8
        
        # Material
        mat = bpy.data.materials.new("FlowMaterial")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.1, 0.3, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.8
        obj.data.materials.append(mat)
    
    # Camera
    bpy.ops.object.camera_add(location=(12, -12, 8))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.2, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Lighting
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 10))
    light = bpy.context.active_object
    light.data.energy = 100
    light.data.size = 10
    
    # World
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.02, 0.02, 0.03, 1.0)
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/data_flow.png'
    
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    create_data_flow()