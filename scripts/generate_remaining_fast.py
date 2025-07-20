#!/usr/bin/env python3
import bpy
import math
import random
import os

# Set to Eevee for faster rendering
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
# Lower samples for speed - using viewport settings
bpy.context.scene.eevee.taa_samples = 16
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def setup_bright_world():
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)
    bg.inputs[1].default_value = 1.0

def add_camera_and_light():
    # Camera
    bpy.ops.object.camera_add(location=(5, -5, 5))
    camera = bpy.context.object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Sun light for even illumination
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.object
    sun.data.energy = 2
    sun.rotation_euler = (0.5, 0.5, 0)
    
    # Additional light for better visibility
    bpy.ops.object.light_add(type='AREA', location=(5, 5, 5))
    area = bpy.context.object
    area.data.energy = 500
    area.data.size = 5

def get_bright_material(name, color):
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1.0)  # Base Color
    bsdf.inputs["Metallic"].default_value = 0.0  # Metallic
    bsdf.inputs["Roughness"].default_value = 0.1  # Roughness
    return mat

def render_image(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

# Remaining Memory visualizations
def create_memory_retrieval():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Central query node
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 2))
    query = bpy.context.object
    query.scale = (0.7, 0.7, 0.7)
    query.data.materials.append(get_bright_material("Query", (1, 0.5, 0)))
    
    # Memory nodes being accessed
    colors = [(0.3, 0.7, 1), (0.7, 0.3, 1), (0.3, 1, 0.7)]
    for i in range(12):
        angle = (i / 12) * 2 * math.pi
        dist = 3
        z = random.uniform(0, 3)
        bpy.ops.mesh.primitive_cube_add(location=(math.cos(angle) * dist, math.sin(angle) * dist, z))
        memory = bpy.context.object
        memory.scale = (0.4, 0.4, 0.4)
        memory.data.materials.append(get_bright_material(f"Memory{i}", random.choice(colors)))
        
        # Retrieval paths
        curve = bpy.data.curves.new('retrieval', 'CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (0, 0, 2, 1)
        spline.points[1].co = (*memory.location, 1)
        obj = bpy.data.objects.new('RetrievalPath', curve)
        bpy.context.collection.objects.link(obj)
        obj.data.bevel_depth = 0.02

def create_context_switching():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Multiple context layers
    contexts = ["File System", "Code Analysis", "User Intent", "Tool State"]
    colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3)]
    
    for i, (context, color) in enumerate(zip(contexts, colors)):
        z = i * 1.5
        # Context plane
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, z))
        plane = bpy.context.object
        plane.scale = (3, 3, 1)
        plane.data.materials.append(get_bright_material(context, color))
        
        # Context elements
        for j in range(5):
            angle = (j / 5) * 2 * math.pi
            bpy.ops.mesh.primitive_cube_add(location=(math.cos(angle) * 1.5, math.sin(angle) * 1.5, z + 0.5))
            element = bpy.context.object
            element.scale = (0.2, 0.2, 0.2)

def create_information_filtering():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Input stream
    for i in range(20):
        x = random.uniform(-4, -2)
        y = random.uniform(-2, 2)
        z = random.uniform(0, 4)
        size = random.uniform(0.1, 0.3)
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        cube = bpy.context.object
        cube.scale = (size, size, size)
        # Random noise - gray
        cube.data.materials.append(get_bright_material(f"Noise{i}", (0.5, 0.5, 0.5)))
    
    # Filter mesh
    bpy.ops.mesh.primitive_grid_add(location=(0, 0, 2), size=3)
    filter_mesh = bpy.context.object
    filter_mesh.rotation_euler = (0, 1.57, 0)
    mat = get_bright_material("Filter", (0.2, 0.5, 1))
    mat.blend_method = 'BLEND'
    mat.node_tree.nodes["Principled BSDF"].inputs[21].default_value = 0.3  # Alpha
    filter_mesh.data.materials.append(mat)
    
    # Filtered relevant information
    relevant_items = ["Code Structure", "User Query", "Context", "Tools"]
    colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3)]
    for i, (item, color) in enumerate(zip(relevant_items, colors)):
        x = 3
        y = (i - 1.5) * 0.8
        z = 2
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        sphere = bpy.context.object
        sphere.scale = (0.4, 0.4, 0.4)
        sphere.data.materials.append(get_bright_material(item, color))

def create_association_network():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Concept nodes
    concepts = [
        ("Python", (0, 0, 2), (0.3, 0.7, 1)),
        ("Functions", (2, 1, 2), (0.7, 0.3, 1)),
        ("Classes", (2, -1, 2), (1, 0.3, 0.7)),
        ("Variables", (-2, 1, 2), (0.3, 1, 0.7)),
        ("Loops", (-2, -1, 2), (1, 0.7, 0.3)),
        ("AI", (0, 2, 1), (0.7, 1, 0.3)),
        ("Code", (0, -2, 3), (0.3, 1, 1))
    ]
    
    nodes = []
    for name, loc, color in concepts:
        bpy.ops.mesh.primitive_uv_sphere_add(location=loc)
        node = bpy.context.object
        node.scale = (0.5, 0.5, 0.5)
        node.data.materials.append(get_bright_material(name, color))
        nodes.append(node)
    
    # Associations
    connections = [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (5, 6), (0, 6)]
    for i, j in connections:
        curve = bpy.data.curves.new('association', 'CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (*nodes[i].location, 1)
        spline.points[1].co = (*nodes[j].location, 1)
        obj = bpy.data.objects.new('Association', curve)
        bpy.context.collection.objects.link(obj)
        obj.data.bevel_depth = 0.03

# Remaining Tools visualizations
def create_api_orchestration():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Central orchestrator
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 2))
    orchestrator = bpy.context.object
    orchestrator.scale = (0.8, 0.8, 0.3)
    orchestrator.data.materials.append(get_bright_material("Orchestrator", (0.5, 0.5, 1)))
    
    # API endpoints
    apis = ["Read", "Write", "Bash", "Search", "WebFetch"]
    colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3), (1, 0.3, 1)]
    
    for i, (api, color) in enumerate(zip(apis, colors)):
        angle = (i / len(apis)) * 2 * math.pi
        x = math.cos(angle) * 3
        y = math.sin(angle) * 3
        
        # API box
        bpy.ops.mesh.primitive_cube_add(location=(x, y, 2))
        api_box = bpy.context.object
        api_box.scale = (0.6, 0.6, 0.6)
        api_box.data.materials.append(get_bright_material(api, color))
        
        # Connection
        curve = bpy.data.curves.new('connection', 'CURVE')
        curve.dimensions = '3D'
        spline = curve.splines.new('POLY')
        spline.points.add(1)
        spline.points[0].co = (0, 0, 2, 1)
        spline.points[1].co = (x, y, 2, 1)
        obj = bpy.data.objects.new('APIConnection', curve)
        bpy.context.collection.objects.link(obj)
        obj.data.bevel_depth = 0.05

def create_tool_pipeline():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Pipeline stages
    stages = ["Input", "Parse", "Route", "Execute", "Format", "Output"]
    colors = [(1, 0.3, 0.3), (1, 0.7, 0.3), (0.7, 1, 0.3), (0.3, 1, 0.7), (0.3, 0.7, 1), (0.7, 0.3, 1)]
    
    for i, (stage, color) in enumerate(zip(stages, colors)):
        x = (i - 2.5) * 1.2
        
        # Stage cylinder
        bpy.ops.mesh.primitive_cylinder_add(location=(x, 0, 2), rotation=(0, 1.57, 0))
        cylinder = bpy.context.object
        cylinder.scale = (0.5, 0.5, 0.8)
        cylinder.data.materials.append(get_bright_material(stage, color))
        
        # Flow arrow
        if i < len(stages) - 1:
            bpy.ops.mesh.primitive_cone_add(location=(x + 0.6, 0, 2), rotation=(0, 0, -1.57))
            arrow = bpy.context.object
            arrow.scale = (0.2, 0.2, 0.3)
            arrow.data.materials.append(get_bright_material("Flow", (0.7, 0.7, 0.7)))

def create_error_cascade():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Initial error
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 4))
    error_source = bpy.context.object
    error_source.scale = (0.5, 0.5, 0.5)
    error_source.data.materials.append(get_bright_material("Error", (1, 0.2, 0.2)))
    
    # Cascading effects
    levels = 3
    for level in range(1, levels + 1):
        count = 2 ** level
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            dist = level * 1.5
            z = 4 - level
            
            bpy.ops.mesh.primitive_cube_add(location=(math.cos(angle) * dist, math.sin(angle) * dist, z))
            cascade = bpy.context.object
            cascade.scale = (0.3, 0.3, 0.3)
            
            # Color gradient from red to yellow
            color = (1, 0.2 + level * 0.2, 0.2)
            cascade.data.materials.append(get_bright_material(f"Cascade{level}_{i}", color))
            
            # Connection line
            curve = bpy.data.curves.new('cascade', 'CURVE')
            curve.dimensions = '3D'
            spline = curve.splines.new('POLY')
            spline.points.add(1)
            
            if level == 1:
                spline.points[0].co = (0, 0, 4, 1)
            else:
                parent_i = i // 2
                parent_angle = (parent_i / (count // 2)) * 2 * math.pi
                parent_dist = (level - 1) * 1.5
                spline.points[0].co = (math.cos(parent_angle) * parent_dist, math.sin(parent_angle) * parent_dist, z + 1, 1)
            
            spline.points[1].co = (*cascade.location, 1)
            obj = bpy.data.objects.new('CascadeLine', curve)
            bpy.context.collection.objects.link(obj)
            obj.data.bevel_depth = 0.02

def create_bash_execution():
    clear_scene()
    setup_bright_world()
    add_camera_and_light()
    
    # Terminal window
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, 0), rotation=(1.57, 0, 0))
    terminal = bpy.context.object
    terminal.scale = (4, 1, 3)
    terminal.data.materials.append(get_bright_material("Terminal", (0.1, 0.1, 0.1)))
    
    # Command blocks
    commands = ["cd /path", "ls -la", "python script.py", "git status", "npm install"]
    y_offset = -2
    
    for i, cmd in enumerate(commands):
        y = y_offset + i * 0.6
        
        # Command block
        bpy.ops.mesh.primitive_cube_add(location=(-1.5, y, 0.5))
        cmd_block = bpy.context.object
        cmd_block.scale = (1, 0.2, 0.1)
        cmd_block.data.materials.append(get_bright_material(f"Cmd{i}", (0.2, 1, 0.2)))
        
        # Output block
        bpy.ops.mesh.primitive_cube_add(location=(1.5, y, 0.5))
        out_block = bpy.context.object
        out_block.scale = (1, 0.2, 0.1)
        out_block.data.materials.append(get_bright_material(f"Out{i}", (0.2, 0.8, 1)))
        
        # Execution arrow
        bpy.ops.mesh.primitive_cone_add(location=(0, y, 0.5), rotation=(0, 0, -1.57))
        arrow = bpy.context.object
        arrow.scale = (0.1, 0.1, 0.3)
        arrow.data.materials.append(get_bright_material("Exec", (1, 1, 0.3)))

# Continue with remaining categories...
# I'll generate the rest in batches to avoid timeout

# Generate the images we haven't created yet
functions = [
    # Memory
    ("memory/memory_retrieval.png", create_memory_retrieval),
    ("memory/context_switching.png", create_context_switching),
    ("memory/information_filtering.png", create_information_filtering),
    ("memory/association_network.png", create_association_network),
    # Tools
    ("tools/api_orchestration.png", create_api_orchestration),
    ("tools/tool_pipeline.png", create_tool_pipeline),
    ("tools/error_cascade.png", create_error_cascade),
    ("tools/bash_execution.png", create_bash_execution),
]

base_path = "/home/franz/dev/claude-vision-gallery/public/"

for filepath, func in functions:
    full_path = base_path + filepath
    if not os.path.exists(full_path):
        print(f"Generating {filepath}...")
        func()
        render_image(full_path)
        print(f"Saved {filepath}")
    else:
        print(f"Skipping {filepath} - already exists")

print("Batch complete!")