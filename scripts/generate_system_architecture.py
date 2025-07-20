#!/usr/bin/env python3
"""
Generate System Architecture Visualization
Represents Claude Code's system design and component relationships
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def create_component(location, size, component_type):
    """Create a system component"""
    if component_type == "core":
        bpy.ops.mesh.primitive_cube_add(location=location, size=size)
    elif component_type == "service":
        bpy.ops.mesh.primitive_cylinder_add(location=location, radius=size/2, depth=size)
    elif component_type == "interface":
        bpy.ops.mesh.primitive_torus_add(location=location, major_radius=size/2, minor_radius=size/6)
    else:  # data
        bpy.ops.mesh.primitive_uv_sphere_add(location=location, radius=size/2)
    
    component = bpy.context.active_object
    
    # Material
    mat = bpy.data.materials.new(name=f"{component_type}Material")
    mat.use_nodes = True
    
    colors = {
        "core": (0.8, 0.2, 0.2, 1),      # Red
        "service": (0.2, 0.8, 0.2, 1),   # Green
        "interface": (0.2, 0.2, 0.8, 1), # Blue
        "data": (0.8, 0.8, 0.2, 1)       # Yellow
    }
    
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors[component_type]
    mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.5  # Metallic
    mat.node_tree.nodes["Principled BSDF"].inputs[7].default_value = 0.2  # Roughness
    
    component.data.materials.append(mat)
    return component

def create_connection_network(components):
    """Create connections between components"""
    connections = []
    
    for i, comp1 in enumerate(components):
        # Connect to 2-3 other components
        num_connections = random.randint(2, 3)
        targets = random.sample([c for j, c in enumerate(components) if j != i], 
                               min(num_connections, len(components) - 1))
        
        for comp2 in targets:
            # Create connection curve
            curve = bpy.data.curves.new('connection', 'CURVE')
            curve.dimensions = '3D'
            spline = curve.splines.new('BEZIER')
            spline.bezier_points.add(1)
            
            spline.bezier_points[0].co = comp1.location
            spline.bezier_points[1].co = comp2.location
            
            # Add curve to handle
            mid_point = (
                (comp1.location.x + comp2.location.x) / 2,
                (comp1.location.y + comp2.location.y) / 2,
                (comp1.location.z + comp2.location.z) / 2 + random.uniform(-0.5, 0.5)
            )
            
            spline.bezier_points[0].handle_right = (
                comp1.location.x + (mid_point[0] - comp1.location.x) * 0.5,
                comp1.location.y + (mid_point[1] - comp1.location.y) * 0.5,
                comp1.location.z + (mid_point[2] - comp1.location.z) * 0.5
            )
            
            obj = bpy.data.objects.new('connection', curve)
            bpy.context.collection.objects.link(obj)
            
            curve.bevel_depth = 0.02
            curve.bevel_resolution = 4
            
            # Connection material
            mat = bpy.data.materials.new("ConnectionMat")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.5, 0.5, 0.8)
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.3
            obj.data.materials.append(mat)
            
            connections.append(obj)
    
    return connections

def create_system_architecture():
    """Create a 3D system architecture visualization"""
    clear_scene()
    
    components = []
    
    # Core system
    core = create_component((0, 0, 0), 2.0, "core")
    components.append(core)
    
    # Service layer
    service_positions = [
        (3, 0, 0), (-3, 0, 0),
        (0, 3, 0), (0, -3, 0),
        (2, 2, 1), (-2, -2, 1)
    ]
    
    for pos in service_positions:
        service = create_component(pos, 1.2, "service")
        components.append(service)
    
    # Interface layer
    interface_positions = [
        (4, 4, 0), (-4, 4, 0),
        (4, -4, 0), (-4, -4, 0)
    ]
    
    for pos in interface_positions:
        interface = create_component(pos, 1.0, "interface")
        components.append(interface)
    
    # Data stores
    data_positions = [
        (0, 0, 3), (0, 0, -3),
        (5, 0, 1), (-5, 0, 1)
    ]
    
    for pos in data_positions:
        data = create_component(pos, 0.8, "data")
        components.append(data)
    
    # Create connections
    connections = create_connection_network(components)
    
    # Add floating particles for data flow
    for _ in range(30):
        x = random.uniform(-6, 6)
        y = random.uniform(-6, 6)
        z = random.uniform(-3, 3)
        
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            subdivisions=1,
            radius=0.05
        )
        particle = bpy.context.active_object
        
        # Glowing material
        mat = bpy.data.materials.new("ParticleMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
        particle.data.materials.append(mat)
    
    # Camera
    bpy.ops.object.camera_add(location=(10, -10, 8))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 0.5
    
    # Rim lighting
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 0))
    rim_light = bpy.context.active_object
    rim_light.data.energy = 50
    rim_light.data.color = (0.5, 0.7, 1)
    rim_light.rotation_euler = (0.785, 0, -0.785)
    
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
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/system_architecture.png'
    
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    create_system_architecture()