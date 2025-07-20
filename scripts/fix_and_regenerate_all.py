#!/usr/bin/env python3
"""Fix lighting and regenerate all images with proper visibility"""
import bpy
import math
import random

def clear_scene():
    """Remove all objects from the scene"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_world_lighting():
    """Set up proper world lighting"""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.05, 0.05, 0.1, 1.0)  # Slightly brighter background
    bg.inputs[1].default_value = 0.3  # Add some ambient light

def generate_neural_network():
    """Generate a visible neural network"""
    clear_scene()
    setup_world_lighting()
    
    # Create glowing nodes
    layers = []
    layer_sizes = [4, 6, 8, 6, 4]
    
    for layer_idx, layer_size in enumerate(layer_sizes):
        layer_nodes = []
        x = layer_idx * 2.5 - 5
        
        for node_idx in range(layer_size):
            y = (node_idx - layer_size/2) * 1.2
            z = random.uniform(-0.3, 0.3)
            
            bpy.ops.mesh.primitive_uv_sphere_add(
                location=(x, y, z),
                radius=0.2
            )
            node = bpy.context.active_object
            
            # Bright emission material
            mat = bpy.data.materials.new(name="NodeMat")
            mat.use_nodes = True
            bsdf = mat.node_tree.nodes["Principled BSDF"]
            bsdf.inputs[17].default_value = (0.3, 0.8, 1)  # Emission color
            bsdf.inputs[18].default_value = 5.0  # Strong emission
            node.data.materials.append(mat)
            
            layer_nodes.append(node)
        
        layers.append(layer_nodes)
    
    # Create glowing connections
    for i in range(len(layers) - 1):
        for node1 in layers[i]:
            for node2 in random.sample(layers[i + 1], min(3, len(layers[i + 1]))):
                curve = bpy.data.curves.new('connection', 'CURVE')
                curve.dimensions = '3D'
                spline = curve.splines.new('BEZIER')
                spline.bezier_points.add(1)
                
                spline.bezier_points[0].co = node1.location
                spline.bezier_points[1].co = node2.location
                
                for point in spline.bezier_points:
                    point.handle_right_type = 'AUTO'
                    point.handle_left_type = 'AUTO'
                
                obj = bpy.data.objects.new('connection', curve)
                bpy.context.collection.objects.link(obj)
                
                curve.bevel_depth = 0.02
                curve.bevel_resolution = 4
                
                mat = bpy.data.materials.new("ConnMat")
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.2, 0.6, 0.9)
                mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
                obj.data.materials.append(mat)
    
    # Add strong lights
    bpy.ops.object.light_add(type='AREA', location=(5, 5, 8))
    light1 = bpy.context.active_object
    light1.data.energy = 200
    light1.data.size = 5
    
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 8))
    light2 = bpy.context.active_object
    light2.data.energy = 150
    light2.data.size = 5
    
    # Camera
    bpy.ops.object.camera_add(location=(10, -10, 6))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/neural_network.png'
    
    bpy.ops.render.render(write_still=True)

def generate_data_flow():
    """Generate visible data flow"""
    clear_scene()
    setup_world_lighting()
    
    # Input node - bright blue cube
    bpy.ops.mesh.primitive_cube_add(location=(-6, 0, 0), size=1.5)
    input_node = bpy.context.active_object
    mat = bpy.data.materials.new("InputMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.4, 1, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.3, 0.5, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
    input_node.data.materials.append(mat)
    
    # Transform nodes - orange cylinders
    for i in range(3):
        x = -2 + i * 2
        y = math.sin(i * 1.2)
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.8, depth=1.5)
        transform = bpy.context.active_object
        mat = bpy.data.materials.new("TransformMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0.5, 0, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0.6, 0.2)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
        transform.data.materials.append(mat)
    
    # Output node - green cone
    bpy.ops.mesh.primitive_cone_add(location=(6, 0, 0), radius1=1.0, depth=2.0)
    output = bpy.context.active_object
    mat = bpy.data.materials.new("OutputMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0.3, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.2, 1, 0.4)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    output.data.materials.append(mat)
    
    # Add glowing particles
    for i in range(20):
        t = i / 20.0
        x = -6 + t * 12
        y = math.sin(t * math.pi * 2) * 2
        z = math.cos(t * math.pi * 3)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
        particle = bpy.context.active_object
        mat = bpy.data.materials.new("ParticleMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0, 1, 0.5)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 10.0
        particle.data.materials.append(mat)
    
    # Strong lighting
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.data.energy = 3.0
    
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 5))
    area = bpy.context.active_object
    area.data.energy = 100
    area.data.size = 8
    
    # Camera
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.2, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/data_flow.png'
    
    bpy.ops.render.render(write_still=True)

def generate_algorithm_crystal():
    """Generate bright crystal visualization"""
    clear_scene()
    setup_world_lighting()
    
    # Main crystal
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=2)
    crystal = bpy.context.active_object
    crystal.scale = (1, 1, 2)
    
    # Apply subdivision
    modifier = crystal.modifiers.new("Subdivision", 'SUBSURF')
    modifier.levels = 2
    
    # Glass material with emission
    mat = bpy.data.materials.new("CrystalMat")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    # Clear defaults
    for node in nodes:
        nodes.remove(node)
    
    # Create glass + emission mix
    output = nodes.new('ShaderNodeOutputMaterial')
    glass = nodes.new('ShaderNodeBsdfGlass')
    emission = nodes.new('ShaderNodeEmission')
    mix = nodes.new('ShaderNodeMixShader')
    
    glass.inputs[0].default_value = (0.5, 0.8, 1, 1)
    glass.inputs[2].default_value = 1.45
    emission.inputs[0].default_value = (0.3, 0.7, 1)
    emission.inputs[1].default_value = 2.0
    
    links.new(glass.outputs[0], mix.inputs[1])
    links.new(emission.outputs[0], mix.inputs[2])
    links.new(mix.outputs[0], output.inputs[0])
    mix.inputs[0].default_value = 0.3
    
    crystal.data.materials.append(mat)
    
    # Smaller crystals around
    for i in range(6):
        angle = i * math.pi * 2 / 6
        x = math.cos(angle) * 3
        y = math.sin(angle) * 3
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, 0), subdivisions=1)
        small = bpy.context.active_object
        small.scale = (0.5, 0.5, 0.8)
        small.data.materials.append(mat)
    
    # Bright lights
    bpy.ops.object.light_add(type='AREA', location=(5, 5, 5))
    light1 = bpy.context.active_object
    light1.data.energy = 500
    light1.data.size = 10
    
    bpy.ops.object.light_add(type='AREA', location=(-5, -5, 5))
    light2 = bpy.context.active_object
    light2.data.energy = 300
    light2.data.size = 10
    light2.data.color = (0.7, 0.9, 1)
    
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, 8))
    spot = bpy.context.active_object
    spot.data.energy = 1000
    spot.data.spot_size = 1.0
    
    # Camera
    bpy.ops.object.camera_add(location=(7, -7, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.3, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 128
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/algorithm_crystal.png'
    
    bpy.ops.render.render(write_still=True)

def generate_system_architecture():
    """Generate bright system architecture"""
    clear_scene()
    setup_world_lighting()
    
    # Core - red emissive cube
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=2.0)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("CoreMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0.2, 0.2, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0.3, 0.3)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    core.data.materials.append(mat)
    
    # Services - green cylinders
    service_positions = [(3, 0, 0), (-3, 0, 0), (0, 3, 0), (0, -3, 0)]
    for pos in service_positions:
        bpy.ops.mesh.primitive_cylinder_add(location=pos, radius=0.6, depth=1.2)
        service = bpy.context.active_object
        mat = bpy.data.materials.new("ServiceMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 1, 0.2, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.3, 1, 0.3)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
        service.data.materials.append(mat)
    
    # Interfaces - blue tori
    interface_positions = [(4, 4, 0), (-4, 4, 0), (4, -4, 0), (-4, -4, 0)]
    for pos in interface_positions:
        bpy.ops.mesh.primitive_torus_add(location=pos, major_radius=0.5, minor_radius=0.15)
        interface = bpy.context.active_object
        mat = bpy.data.materials.new("InterfaceMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 1, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.4, 0.4, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 4.0
        interface.data.materials.append(mat)
    
    # Data stores - yellow spheres
    data_positions = [(0, 0, 3), (5, 0, 1), (-5, 0, 1)]
    for pos in data_positions:
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos, radius=0.4)
        data = bpy.context.active_object
        mat = bpy.data.materials.new("DataMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 0.2, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 0.3)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 5.0
        data.data.materials.append(mat)
    
    # Multiple lights for full illumination
    light_positions = [(0, 0, 10), (10, 0, 5), (-10, 0, 5), (0, 10, 5), (0, -10, 5)]
    for pos in light_positions:
        bpy.ops.object.light_add(type='AREA', location=pos)
        light = bpy.context.active_object
        light.data.energy = 200
        light.data.size = 5
    
    # Camera
    bpy.ops.object.camera_add(location=(8, -8, 6))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/system_architecture.png'
    
    bpy.ops.render.render(write_still=True)

def generate_code_universe():
    """Generate bright universe visualization"""
    clear_scene()
    
    # Brighter space background
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.02, 0.02, 0.05, 1.0)
    bg.inputs[1].default_value = 0.2
    
    # Central bright galaxy
    for i in range(100):
        angle = random.uniform(0, math.pi * 2)
        r = random.uniform(0, 3)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_ico_sphere_add(
            location=(x, y, z),
            subdivisions=0,
            radius=random.uniform(0.05, 0.15)
        )
        star = bpy.context.active_object
        
        mat = bpy.data.materials.new("StarMat")
        mat.use_nodes = True
        color = (random.uniform(0.7, 1), random.uniform(0.7, 1), random.uniform(0.9, 1))
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = random.uniform(5, 10)
        star.data.materials.append(mat)
    
    # Bright central core
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.8)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("CoreMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0.5, 0.2)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 20.0
    core.data.materials.append(mat)
    
    # Add some ambient light
    bpy.ops.object.light_add(type='SUN', location=(10, 10, 20))
    sun = bpy.context.active_object
    sun.data.energy = 0.5
    
    # Camera
    bpy.ops.object.camera_add(location=(10, -10, 6))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.render.resolution_x = 1920
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/code_universe.png'
    
    bpy.ops.render.render(write_still=True)

# Generate all images with proper lighting
print("Generating Neural Network...")
generate_neural_network()

print("Generating Data Flow...")
generate_data_flow()

print("Generating Algorithm Crystal...")
generate_algorithm_crystal()

print("Generating System Architecture...")
generate_system_architecture()

print("Generating Code Universe...")
generate_code_universe()

print("All images regenerated with proper lighting!")