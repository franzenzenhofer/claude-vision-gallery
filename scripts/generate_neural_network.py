#!/usr/bin/env python3
"""
Generate Neural Network Visualization
Represents Claude Code's neural pathways and connections
"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
def create_node(location, size=0.15):
    """Create a neural node"""
    bpy.ops.mesh.primitive_uv_sphere_add(
        location=location,
        segments=32,
        ring_count=16,
        radius=size
    )
    node = bpy.context.active_object
    
    # Create emission material
    mat = bpy.data.materials.new(name="NodeMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.2, 0.8, 1)  # Emission color
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0  # Emission strength
    node.data.materials.append(mat)
    
    return node

def create_connection(start_pos, end_pos):
    """Create a connection between nodes"""
    # Calculate curve points
    curve = bpy.data.curves.new('connection', 'CURVE')
    curve.dimensions = '3D'
    
    spline = curve.splines.new('BEZIER')
    spline.bezier_points.add(1)
    
    spline.bezier_points[0].co = start_pos
    spline.bezier_points[0].handle_right_type = 'AUTO'
    spline.bezier_points[0].handle_left_type = 'AUTO'
    
    spline.bezier_points[1].co = end_pos
    spline.bezier_points[1].handle_right_type = 'AUTO'
    spline.bezier_points[1].handle_left_type = 'AUTO'
    
    # Create object
    obj = bpy.data.objects.new('connection', curve)
    bpy.context.collection.objects.link(obj)
    
    # Set bevel
    curve.bevel_depth = 0.01
    curve.bevel_resolution = 4
    
    # Create material
    mat = bpy.data.materials.new(name="ConnectionMaterial")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.1, 0.5, 0.8)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.0  # Alpha
    obj.data.materials.append(mat)
    
    return obj

def generate_neural_network():
    """Generate a 3D neural network visualization"""
    clear_scene()
    
    # Create layers
    layers = []
    layer_sizes = [5, 8, 12, 8, 5]  # Nodes per layer
    
    for layer_idx, layer_size in enumerate(layer_sizes):
        layer_nodes = []
        x = layer_idx * 3 - 6
        
        for node_idx in range(layer_size):
            y = (node_idx - layer_size/2) * 1.5
            z = random.uniform(-0.5, 0.5)
            
            node = create_node((x, y, z))
            layer_nodes.append(node)
        
        layers.append(layer_nodes)
    
    # Create connections between layers
    for i in range(len(layers) - 1):
        for node1 in layers[i]:
            # Connect to random nodes in next layer
            connections = random.sample(layers[i + 1], min(3, len(layers[i + 1])))
            for node2 in connections:
                if random.random() > 0.3:  # 70% connection probability
                    create_connection(node1.location, node2.location)
    
    # Setup camera
    bpy.ops.object.camera_add(location=(15, -15, 10))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Setup lighting
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    light = bpy.context.active_object
    light.data.energy = 0.5
    
    # World settings
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.01, 0.01, 0.02, 1.0)  # Dark background
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/neural_network.png'
    
    # Render
    bpy.ops.render.render(write_still=True)

if __name__ == "__main__":
    generate_neural_network()