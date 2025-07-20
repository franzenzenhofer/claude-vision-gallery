#!/usr/bin/env python3
"""Generate ALL 45+ visualizations of Claude Code's reality"""
import bpy
import math
import random
import os
import colorsys

# Ensure output directories exist
CATEGORIES = ["thinking", "code", "memory", "tools", "language", "problem_solving", "system", "consciousness", "interaction"]
for cat in CATEGORIES:
    os.makedirs(f'/home/franz/dev/claude-vision-gallery/public/{cat}', exist_ok=True)

def clear_scene():
    """Clean slate"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_bright_world():
    """White background with good lighting"""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)
    bg.inputs[1].default_value = 1.0

def add_camera_and_light(cam_pos=(5, -5, 5), look_at=(0, 0, 0)):
    """Standard camera and lighting setup"""
    # Camera
    bpy.ops.object.camera_add(location=cam_pos)
    camera = bpy.context.active_object
    
    # Point camera at target
    direction = [look_at[i] - cam_pos[i] for i in range(3)]
    rot_quat = camera.rotation_euler
    camera.rotation_mode = 'XYZ'
    camera.rotation_euler = (1.1, 0, 0.785)  # Standard angle
    bpy.context.scene.camera = camera
    
    # Sun light for even illumination
    bpy.ops.object.light_add(type='SUN', location=(5, 5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 1.0
    
    # Area light for soft shadows
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 5))
    area = bpy.context.active_object
    area.data.energy = 50
    area.data.size = 10

def render_image(filepath):
    """Render with consistent settings"""
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32  # Fast for many images
    scene.render.resolution_x = 1080  # Square mobile-friendly
    scene.render.resolution_y = 1080
    scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

# THINKING VISUALIZATIONS

def generate_context_window():
    """Sliding context window visualization"""
    clear_scene()
    setup_bright_world()
    
    # Context window frame
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=1)
    frame = bpy.context.active_object
    frame.scale = (8, 0.1, 3)
    mat = bpy.data.materials.new("Frame")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.2, 1)
    frame.data.materials.append(mat)
    
    # Tokens in window
    for i in range(15):
        x = i * 0.8 - 6
        opacity = 1.0 if 3 < i < 12 else 0.3
        
        bpy.ops.mesh.primitive_cube_add(location=(x, 0, 0), size=0.6)
        token = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Token{i}")
        mat.use_nodes = True
        color = (0.2, 0.6, 0.9, 1) if opacity > 0.5 else (0.6, 0.6, 0.6, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = opacity
        token.data.materials.append(mat)
    
    # Window indicators
    bpy.ops.mesh.primitive_plane_add(location=(-3, 0, 2), size=0.3)
    start = bpy.context.active_object
    start.rotation_euler = (0, 0, math.pi/4)
    mat = bpy.data.materials.new("Start")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0, 1)
    start.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/thinking/context_window.png')

def generate_thought_chains():
    """Chained reasoning visualization"""
    clear_scene()
    setup_bright_world()
    
    # Create thought nodes
    thoughts = []
    for i in range(5):
        y = i * 2 - 4
        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, y, 0), radius=0.5)
        thought = bpy.context.active_object
        thoughts.append(thought)
        
        # Color gradient
        hue = i / 5.0
        color = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        mat = bpy.data.materials.new(f"Thought{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        thought.data.materials.append(mat)
    
    # Connect with chains
    for i in range(len(thoughts) - 1):
        # Chain link
        bpy.ops.mesh.primitive_torus_add(
            location=(0, thoughts[i].location.y + 1, 0),
            major_radius=0.3,
            minor_radius=0.05
        )
        link = bpy.context.active_object
        link.rotation_euler = (math.pi/2, 0, 0)
        
        mat = bpy.data.materials.new(f"Link{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.7, 0.7, 0.7, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.8  # Metallic
        link.data.materials.append(mat)
    
    add_camera_and_light((6, -2, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/thinking/thought_chains.png')

def generate_parallel_reasoning():
    """Multiple reasoning paths"""
    clear_scene()
    setup_bright_world()
    
    # Central question
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.8)
    question = bpy.context.active_object
    mat = bpy.data.materials.new("Question")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.1, 0.1, 1)
    question.data.materials.append(mat)
    
    # Parallel paths
    for path in range(3):
        angle = path * 2 * math.pi / 3
        for step in range(4):
            r = (step + 1) * 1.2
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.4)
            node = bpy.context.active_object
            
            # Path colors
            colors = [(0.2, 0.8, 0.2), (0.2, 0.2, 0.8), (0.8, 0.8, 0.2)]
            mat = bpy.data.materials.new(f"Path{path}_Step{step}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*colors[path], 1)
            node.data.materials.append(mat)
    
    add_camera_and_light((0, 0, 10))
    render_image('/home/franz/dev/claude-vision-gallery/public/thinking/parallel_reasoning.png')

# CODE VISUALIZATIONS

def generate_code_flow():
    """Control flow visualization"""
    clear_scene()
    setup_bright_world()
    
    # Entry point
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 4, 0), radius=0.5, depth=0.3)
    entry = bpy.context.active_object
    mat = bpy.data.materials.new("Entry")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 0.2, 1)
    entry.data.materials.append(mat)
    
    # Condition diamond
    bpy.ops.mesh.primitive_cube_add(location=(0, 2, 0), size=0.8)
    condition = bpy.context.active_object
    condition.rotation_euler = (0, 0, math.pi/4)
    mat = bpy.data.materials.new("Condition")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.2, 1)
    condition.data.materials.append(mat)
    
    # True/False branches
    for i, x in enumerate([-2, 2]):
        bpy.ops.mesh.primitive_cube_add(location=(x, 0, 0), size=0.6)
        branch = bpy.context.active_object
        color = (0.2, 0.8, 0.2, 1) if i == 0 else (0.8, 0.2, 0.2, 1)
        mat = bpy.data.materials.new(f"Branch{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        branch.data.materials.append(mat)
    
    # Loop
    bpy.ops.mesh.primitive_torus_add(location=(0, -2, 0), major_radius=1, minor_radius=0.2)
    loop = bpy.context.active_object
    mat = bpy.data.materials.new("Loop")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1)
    loop.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/code/code_flow.png')

def generate_bug_detection():
    """Bug detection visualization"""
    clear_scene()
    setup_bright_world()
    
    # Code blocks
    for i in range(5):
        for j in range(5):
            x = i * 1.2 - 2.4
            y = j * 1.2 - 2.4
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=1)
            block = bpy.context.active_object
            
            # Bug probability
            is_bug = random.random() < 0.2
            color = (0.9, 0.2, 0.2, 1) if is_bug else (0.2, 0.9, 0.2, 1)
            
            mat = bpy.data.materials.new(f"Block_{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            
            if is_bug:
                # Add glow for bugs
                mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0, 0)
                mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
            
            block.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/code/bug_detection.png')

def generate_pattern_matching():
    """Pattern matching in code"""
    clear_scene()
    setup_bright_world()
    
    # Pattern template
    pattern_pos = [(-1, 1), (0, 1), (1, 1), (0, 0)]
    for x, y in pattern_pos:
        bpy.ops.mesh.primitive_cylinder_add(location=(x*0.5 - 3, y*0.5, 0), radius=0.2, depth=0.4)
        p = bpy.context.active_object
        mat = bpy.data.materials.new("Pattern")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.6, 0.1, 1)
        p.data.materials.append(mat)
    
    # Code to search
    for i in range(8):
        for j in range(4):
            x = i * 0.6
            y = j * 0.6 - 1
            
            # Check if matches pattern
            matches = (i == 3 and j in [1, 2]) or (i == 4 and j == 2) or (i == 5 and j == 1)
            
            shape = 'cylinder' if matches else 'cube'
            if shape == 'cylinder':
                bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.2, depth=0.4)
            else:
                bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.4)
            
            obj = bpy.context.active_object
            color = (0.9, 0.6, 0.1, 1) if matches else (0.3, 0.3, 0.3, 1)
            mat = bpy.data.materials.new(f"Code_{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            obj.data.materials.append(mat)
    
    add_camera_and_light((4, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/code/pattern_matching.png')

def generate_refactoring_paths():
    """Code refactoring visualization"""
    clear_scene()
    setup_bright_world()
    
    # Original messy code
    for i in range(20):
        x = random.uniform(-3, -1)
        y = random.uniform(-2, 2)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.3)
        cube = bpy.context.active_object
        cube.rotation_euler = (random.random(), random.random(), random.random())
        
        mat = bpy.data.materials.new(f"Messy{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.2, 0.2, 1)
        cube.data.materials.append(mat)
    
    # Arrow
    bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0), radius1=0.3, depth=1)
    arrow = bpy.context.active_object
    arrow.rotation_euler = (0, math.pi/2, 0)
    mat = bpy.data.materials.new("Arrow")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
    arrow.data.materials.append(mat)
    
    # Refactored clean code
    for i in range(4):
        for j in range(3):
            x = 2 + i * 0.5
            y = j * 0.8 - 0.8
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.4)
            cube = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Clean{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 0.2, 1)
            cube.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/code/refactoring_paths.png')

# MEMORY VISUALIZATIONS

def generate_knowledge_graph():
    """Knowledge connections"""
    clear_scene()
    setup_bright_world()
    
    # Knowledge nodes
    nodes = []
    for i in range(15):
        angle = i * 2 * math.pi / 15
        r = 2 + random.uniform(-0.5, 0.5)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), radius=0.2)
        node = bpy.context.active_object
        nodes.append(node)
        
        # Node types with different colors
        node_type = i % 4
        colors = [(0.8, 0.2, 0.2), (0.2, 0.8, 0.2), (0.2, 0.2, 0.8), (0.8, 0.8, 0.2)]
        
        mat = bpy.data.materials.new(f"Node{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*colors[node_type], 1)
        node.data.materials.append(mat)
    
    # Connections
    for i in range(20):
        n1 = random.choice(nodes)
        n2 = random.choice(nodes)
        if n1 != n2:
            # Create edge curve
            curve = bpy.data.curves.new('edge', 'CURVE')
            curve.dimensions = '3D'
            spline = curve.splines.new('BEZIER')
            spline.bezier_points.add(1)
            
            spline.bezier_points[0].co = n1.location
            spline.bezier_points[1].co = n2.location
            
            for point in spline.bezier_points:
                point.handle_right_type = 'AUTO'
                point.handle_left_type = 'AUTO'
            
            obj = bpy.data.objects.new('edge', curve)
            bpy.context.collection.objects.link(obj)
            curve.bevel_depth = 0.01
            
            mat = bpy.data.materials.new("Edge")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5
            obj.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/memory/knowledge_graph.png')

def generate_memory_retrieval():
    """Memory access visualization"""
    clear_scene()
    setup_bright_world()
    
    # Memory banks
    for layer in range(3):
        z = layer * 1.5 - 1.5
        for i in range(6):
            for j in range(6):
                x = i * 0.7 - 2.1
                y = j * 0.7 - 2.1
                
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.5)
                mem = bpy.context.active_object
                
                # Activation level
                activation = random.random()
                color = (activation, activation * 0.5, 1 - activation, 1)
                
                mat = bpy.data.materials.new(f"Mem_{layer}_{i}_{j}")
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
                
                if activation > 0.7:
                    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color[:3]
                    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
                
                mem.data.materials.append(mat)
    
    # Query beam
    bpy.ops.mesh.primitive_cone_add(location=(0, -4, 0), radius1=0.5, depth=2)
    query = bpy.context.active_object
    query.rotation_euler = (math.pi/2, 0, 0)
    mat = bpy.data.materials.new("Query")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 0)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    query.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/memory/memory_retrieval.png')

def generate_context_switching():
    """Context switching between tasks"""
    clear_scene()
    setup_bright_world()
    
    # Different contexts
    contexts = ["Code", "Chat", "Analysis", "Creative"]
    colors = [(0.9, 0.2, 0.2), (0.2, 0.9, 0.2), (0.2, 0.2, 0.9), (0.9, 0.9, 0.2)]
    
    for i, (context, color) in enumerate(zip(contexts, colors)):
        angle = i * math.pi / 2
        x = math.cos(angle) * 2
        y = math.sin(angle) * 2
        
        # Context sphere
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, 0), radius=0.8)
        sphere = bpy.context.active_object
        
        mat = bpy.data.materials.new(context)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.7
        sphere.data.materials.append(mat)
    
    # Switch mechanism (rotating cross)
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=0.3)
    switch1 = bpy.context.active_object
    switch1.scale = (3, 0.2, 0.2)
    
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=0.3)
    switch2 = bpy.context.active_object
    switch2.scale = (0.2, 3, 0.2)
    
    for switch in [switch1, switch2]:
        mat = bpy.data.materials.new("Switch")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.9
        switch.data.materials.append(mat)
    
    add_camera_and_light((0, 0, 8))
    render_image('/home/franz/dev/claude-vision-gallery/public/memory/context_switching.png')

def generate_information_filtering():
    """Information filtering process"""
    clear_scene()
    setup_bright_world()
    
    # Incoming data stream
    for i in range(50):
        x = random.uniform(-4, -2)
        y = random.uniform(-2, 2)
        z = random.uniform(-1, 1)
        
        size = random.uniform(0.05, 0.2)
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=size)
        data = bpy.context.active_object
        
        # Random data types
        importance = random.random()
        color = (importance, 1 - importance, 0.2, 1)
        
        mat = bpy.data.materials.new(f"Data{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        data.data.materials.append(mat)
    
    # Filter mesh
    bpy.ops.mesh.primitive_grid_add(location=(0, 0, 0), size=3)
    filter_mesh = bpy.context.active_object
    filter_mesh.rotation_euler = (0, math.pi/2, 0)
    
    # Subdivide for more detail
    modifier = filter_mesh.modifiers.new("Subsurf", 'SUBSURF')
    modifier.levels = 2
    
    mat = bpy.data.materials.new("Filter")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5  # Transparency
    filter_mesh.data.materials.append(mat)
    
    # Filtered output
    for i in range(10):
        x = random.uniform(2, 4)
        y = random.uniform(-1, 1)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.15)
        data = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Filtered{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.9, 0.2, 1)
        data.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/memory/information_filtering.png')

def generate_association_network():
    """Concept associations"""
    clear_scene()
    setup_bright_world()
    
    # Central concept
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.5)
    central = bpy.context.active_object
    mat = bpy.data.materials.new("Central")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.2, 0.2, 1)
    central.data.materials.append(mat)
    
    # Associated concepts in layers
    for layer in range(3):
        num_concepts = 6 * (layer + 1)
        radius = (layer + 1) * 1.5
        
        for i in range(num_concepts):
            angle = i * 2 * math.pi / num_concepts
            x = radius * math.cos(angle)
            y = radius * math.sin(angle)
            z = random.uniform(-0.3, 0.3)
            
            size = 0.3 / (layer + 1)
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), radius=size)
            concept = bpy.context.active_object
            
            # Color by distance
            hue = (layer * 0.3) % 1.0
            color = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
            
            mat = bpy.data.materials.new(f"Concept_{layer}_{i}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
            concept.data.materials.append(mat)
    
    add_camera_and_light((8, -8, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/memory/association_network.png')

# TOOLS VISUALIZATIONS

def generate_api_orchestration():
    """Multiple API calls coordination"""
    clear_scene()
    setup_bright_world()
    
    # Central orchestrator
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0), radius=0.6, depth=0.3)
    orchestrator = bpy.context.active_object
    mat = bpy.data.materials.new("Orchestrator")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1)
    orchestrator.data.materials.append(mat)
    
    # API endpoints
    apis = ["File", "Network", "Process", "Search", "Database"]
    colors = [(0.9, 0.2, 0.2), (0.2, 0.9, 0.2), (0.9, 0.9, 0.2), (0.9, 0.2, 0.9), (0.2, 0.9, 0.9)]
    
    for i, (api, color) in enumerate(zip(apis, colors)):
        angle = i * 2 * math.pi / len(apis)
        x = math.cos(angle) * 3
        y = math.sin(angle) * 3
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.8)
        endpoint = bpy.context.active_object
        
        mat = bpy.data.materials.new(api)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        endpoint.data.materials.append(mat)
        
        # Connection pipes
        bpy.ops.mesh.primitive_cylinder_add(location=(x/2, y/2, 0), radius=0.05, depth=3)
        pipe = bpy.context.active_object
        
        # Point pipe at center
        direction = math.atan2(y, x)
        pipe.rotation_euler = (0, math.pi/2, direction)
        
        mat = bpy.data.materials.new(f"Pipe{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
        pipe.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 8))
    render_image('/home/franz/dev/claude-vision-gallery/public/tools/api_orchestration.png')

def generate_tool_pipeline():
    """Tool execution pipeline"""
    clear_scene()
    setup_bright_world()
    
    # Pipeline stages
    stages = ["Parse", "Validate", "Execute", "Format", "Return"]
    
    for i, stage in enumerate(stages):
        x = i * 2 - 4
        
        # Stage container
        bpy.ops.mesh.primitive_cylinder_add(location=(x, 0, 0), radius=0.6, depth=1)
        container = bpy.context.active_object
        container.rotation_euler = (math.pi/2, 0, 0)
        
        # Stage color
        hue = i / len(stages)
        color = colorsys.hsv_to_rgb(hue, 0.6, 0.9)
        
        mat = bpy.data.materials.new(stage)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        container.data.materials.append(mat)
        
        # Connecting pipe
        if i < len(stages) - 1:
            bpy.ops.mesh.primitive_cylinder_add(
                location=(x + 1, 0, 0),
                radius=0.2,
                depth=2
            )
            pipe = bpy.context.active_object
            pipe.rotation_euler = (0, math.pi/2, 0)
            
            mat = bpy.data.materials.new(f"Pipe{i}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.4, 0.4, 1)
            pipe.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/tools/tool_pipeline.png')

def generate_error_cascade():
    """Error propagation visualization"""
    clear_scene()
    setup_bright_world()
    
    # Initial error source
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 3, 0), radius=0.3)
    source = bpy.context.active_object
    mat = bpy.data.materials.new("ErrorSource")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 0, 0)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 3.0
    source.data.materials.append(mat)
    
    # Cascading errors
    for level in range(3):
        y = 2 - level * 1.5
        spread = level + 1
        
        for i in range(spread * 2):
            x = (i - spread + 0.5) * 0.8
            
            size = 0.3 + level * 0.1
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=size)
            error = bpy.context.active_object
            
            # Error intensity decreases
            intensity = 1.0 - (level * 0.3)
            mat = bpy.data.materials.new(f"Error_{level}_{i}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (intensity, 0, 0, 1)
            error.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/tools/error_cascade.png')

def generate_bash_execution():
    """Command execution visualization"""
    clear_scene()
    setup_bright_world()
    
    # Terminal window
    bpy.ops.mesh.primitive_plane_add(location=(0, 0, -0.5), size=6)
    terminal = bpy.context.active_object
    mat = bpy.data.materials.new("Terminal")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.1, 0.1, 0.1, 1)
    terminal.data.materials.append(mat)
    
    # Command blocks
    commands = ["ls", "grep", "pipe", "output"]
    for i, cmd in enumerate(commands):
        x = i * 1.5 - 2.25
        
        bpy.ops.mesh.primitive_cube_add(location=(x, 0, 0), size=1)
        block = bpy.context.active_object
        
        colors = {
            "ls": (0.2, 0.8, 0.2, 1),
            "grep": (0.8, 0.8, 0.2, 1),
            "pipe": (0.5, 0.5, 0.5, 1),
            "output": (0.2, 0.2, 0.8, 1)
        }
        
        mat = bpy.data.materials.new(cmd)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors[cmd]
        block.data.materials.append(mat)
    
    # Data flow arrows
    for i in range(3):
        x = i * 1.5 - 1.5
        bpy.ops.mesh.primitive_cone_add(location=(x, 0, 1), radius1=0.2, depth=0.5)
        arrow = bpy.context.active_object
        arrow.rotation_euler = (0, -math.pi/2, 0)
        
        mat = bpy.data.materials.new(f"Arrow{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.6, 0.6, 1)
        arrow.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/tools/bash_execution.png')

# LANGUAGE VISUALIZATIONS

def generate_tokenization_grid():
    """Tokenization process"""
    clear_scene()
    setup_bright_world()
    
    # Input text as continuous block
    bpy.ops.mesh.primitive_cube_add(location=(-3, 0, 0), size=1)
    text_block = bpy.context.active_object
    text_block.scale = (2, 3, 0.5)
    mat = bpy.data.materials.new("Text")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
    text_block.data.materials.append(mat)
    
    # Arrow
    bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0), radius1=0.3, depth=1)
    arrow = bpy.context.active_object
    arrow.rotation_euler = (0, math.pi/2, 0)
    mat = bpy.data.materials.new("Arrow")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
    arrow.data.materials.append(mat)
    
    # Tokenized output
    token_types = ["word", "punct", "number", "special"]
    colors = {
        "word": (0.2, 0.8, 0.2, 1),
        "punct": (0.8, 0.2, 0.2, 1),
        "number": (0.2, 0.2, 0.8, 1),
        "special": (0.8, 0.8, 0.2, 1)
    }
    
    for i in range(4):
        for j in range(5):
            x = 2 + i * 0.6
            y = j * 0.6 - 1.2
            
            token_type = random.choice(list(token_types))
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.5)
            token = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Token_{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors[token_type]
            token.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/language/tokenization_grid.png')

def generate_semantic_space():
    """Word embeddings in 3D space"""
    clear_scene()
    setup_bright_world()
    
    # Semantic clusters
    clusters = [
        {"center": (-2, 2, 0), "words": 8, "color": (0.9, 0.2, 0.2)},  # Animals
        {"center": (2, 2, 0), "words": 8, "color": (0.2, 0.9, 0.2)},   # Plants
        {"center": (-2, -2, 0), "words": 8, "color": (0.2, 0.2, 0.9)}, # Tech
        {"center": (2, -2, 0), "words": 8, "color": (0.9, 0.9, 0.2)}   # Food
    ]
    
    for cluster in clusters:
        center = cluster["center"]
        
        # Cluster center
        bpy.ops.mesh.primitive_uv_sphere_add(location=center, radius=0.3)
        core = bpy.context.active_object
        mat = bpy.data.materials.new("ClusterCore")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*cluster["color"], 1)
        core.data.materials.append(mat)
        
        # Word points around cluster
        for i in range(cluster["words"]):
            angle = i * 2 * math.pi / cluster["words"]
            r = random.uniform(0.5, 1.0)
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            z = center[2] + random.uniform(-0.3, 0.3)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
            word = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Word_{i}")
            mat.use_nodes = True
            color = tuple(c * 0.7 for c in cluster["color"])
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
            word.data.materials.append(mat)
    
    add_camera_and_light((0, 0, 8))
    render_image('/home/franz/dev/claude-vision-gallery/public/language/semantic_space.png')

def generate_multilingual_network():
    """Multiple language connections"""
    clear_scene()
    setup_bright_world()
    
    # Language hubs
    languages = [
        {"name": "EN", "pos": (0, 0, 0), "color": (0.2, 0.2, 0.8)},
        {"name": "ES", "pos": (3, 0, 0), "color": (0.8, 0.8, 0.2)},
        {"name": "FR", "pos": (-1.5, 2.6, 0), "color": (0.2, 0.8, 0.2)},
        {"name": "DE", "pos": (-1.5, -2.6, 0), "color": (0.8, 0.2, 0.2)},
        {"name": "JP", "pos": (0, 0, 3), "color": (0.8, 0.2, 0.8)},
        {"name": "CN", "pos": (0, 0, -3), "color": (0.2, 0.8, 0.8)}
    ]
    
    hubs = []
    for lang in languages:
        bpy.ops.mesh.primitive_uv_sphere_add(location=lang["pos"], radius=0.5)
        hub = bpy.context.active_object
        hubs.append(hub)
        
        mat = bpy.data.materials.new(lang["name"])
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*lang["color"], 1)
        hub.data.materials.append(mat)
    
    # Inter-language connections
    for i in range(len(hubs)):
        for j in range(i + 1, len(hubs)):
            # Create connecting tube
            p1 = hubs[i].location
            p2 = hubs[j].location
            
            mid = [(p1[k] + p2[k]) / 2 for k in range(3)]
            length = math.sqrt(sum((p2[k] - p1[k])**2 for k in range(3)))
            
            bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.05, depth=length)
            conn = bpy.context.active_object
            
            # Orient cylinder
            direction = [p2[k] - p1[k] for k in range(3)]
            # Simplified rotation calculation
            conn.rotation_euler = (0, math.acos(direction[2]/length) if length > 0 else 0, math.atan2(direction[1], direction[0]))
            
            mat = bpy.data.materials.new(f"Conn_{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.6, 0.6, 0.6, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5
            conn.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/language/multilingual_network.png')

def generate_text_generation_flow():
    """Text generation process"""
    clear_scene()
    setup_bright_world()
    
    # Generation stages
    stages = ["Context", "Predict", "Sample", "Append", "Output"]
    
    for i, stage in enumerate(stages):
        y = 2 - i
        
        # Stage shape varies
        if stage == "Context":
            bpy.ops.mesh.primitive_cube_add(location=(0, y, 0), size=0.8)
        elif stage == "Predict":
            bpy.ops.mesh.primitive_uv_sphere_add(location=(0, y, 0), radius=0.4)
        elif stage == "Sample":
            bpy.ops.mesh.primitive_cone_add(location=(0, y, 0), radius1=0.4, depth=0.8)
        elif stage == "Append":
            bpy.ops.mesh.primitive_cylinder_add(location=(0, y, 0), radius=0.3, depth=0.6)
        else:  # Output
            bpy.ops.mesh.primitive_torus_add(location=(0, y, 0), major_radius=0.4, minor_radius=0.1)
        
        obj = bpy.context.active_object
        
        # Stage colors
        hue = i / len(stages)
        color = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        
        mat = bpy.data.materials.new(stage)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        obj.data.materials.append(mat)
        
        # Flow indicators
        if i < len(stages) - 1:
            bpy.ops.mesh.primitive_cone_add(location=(0, y - 0.5, 0), radius1=0.1, depth=0.3)
            arrow = bpy.context.active_object
            arrow.rotation_euler = (math.pi, 0, 0)
            
            mat = bpy.data.materials.new(f"Flow{i}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
            arrow.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/language/text_generation_flow.png')

def generate_grammar_structure():
    """Grammar tree visualization"""
    clear_scene()
    setup_bright_world()
    
    # Sentence structure tree
    def create_grammar_node(text, pos, level):
        size = 0.4 - level * 0.1
        bpy.ops.mesh.primitive_cube_add(location=pos, size=size)
        node = bpy.context.active_object
        
        colors = {
            0: (0.8, 0.2, 0.2, 1),  # Sentence
            1: (0.2, 0.8, 0.2, 1),  # Phrase
            2: (0.2, 0.2, 0.8, 1),  # Word
            3: (0.8, 0.8, 0.2, 1)   # Part
        }
        
        mat = bpy.data.materials.new(text)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors.get(level, (0.5, 0.5, 0.5, 1))
        node.data.materials.append(mat)
        
        return node
    
    # Build tree
    root = create_grammar_node("S", (0, 0, 3), 0)
    
    # Level 1 - NP and VP
    np = create_grammar_node("NP", (-2, 0, 2), 1)
    vp = create_grammar_node("VP", (2, 0, 2), 1)
    
    # Level 2 - Words
    det = create_grammar_node("Det", (-3, 0, 1), 2)
    noun = create_grammar_node("N", (-1, 0, 1), 2)
    verb = create_grammar_node("V", (1, 0, 1), 2)
    obj = create_grammar_node("NP", (3, 0, 1), 2)
    
    # Connect nodes
    nodes_to_connect = [(root, np), (root, vp), (np, det), (np, noun), (vp, verb), (vp, obj)]
    
    for parent, child in nodes_to_connect:
        # Create edge
        mid = [(parent.location[i] + child.location[i]) / 2 for i in range(3)]
        length = 1.5
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.02, depth=length)
        edge = bpy.context.active_object
        
        # Orient edge
        edge.rotation_euler = (0, math.pi/4, 0)
        
        mat = bpy.data.materials.new("Edge")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.4, 0.4, 1)
        edge.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/language/grammar_structure.png')

# PROBLEM SOLVING VISUALIZATIONS

def generate_task_decomposition():
    """Breaking down complex tasks"""
    clear_scene()
    setup_bright_world()
    
    # Main task
    bpy.ops.mesh.primitive_cube_add(location=(0, 3, 0), size=1.2)
    main_task = bpy.context.active_object
    mat = bpy.data.materials.new("MainTask")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.2, 0.2, 1)
    main_task.data.materials.append(mat)
    
    # Subtasks
    for i in range(3):
        x = (i - 1) * 2
        y = 1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.8)
        subtask = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Subtask{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.2, 1)
        subtask.data.materials.append(mat)
        
        # Sub-subtasks
        for j in range(2):
            sx = x + (j - 0.5) * 0.8
            sy = -1
            
            bpy.ops.mesh.primitive_cube_add(location=(sx, sy, 0), size=0.5)
            subsubtask = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"SubSubtask{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 0.2, 1)
            subsubtask.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/problem_solving/task_decomposition.png')

def generate_solution_search():
    """Solution space exploration"""
    clear_scene()
    setup_bright_world()
    
    # Search space as 3D grid
    for i in range(6):
        for j in range(6):
            for k in range(3):
                x = i * 0.8 - 2
                y = j * 0.8 - 2
                z = k * 0.8 - 0.8
                
                # Solution quality
                quality = random.random()
                
                if quality > 0.95:  # Optimal solution
                    bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), radius=0.2)
                    color = (0, 1, 0, 1)
                elif quality > 0.7:  # Good solution
                    bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.3)
                    color = (quality, quality, 0, 1)
                else:  # Poor solution
                    continue  # Don't show
                
                node = bpy.context.active_object
                mat = bpy.data.materials.new(f"Sol_{i}_{j}_{k}")
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
                
                if quality > 0.95:
                    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0, 1, 0)
                    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
                
                node.data.materials.append(mat)
    
    # Search path
    path_points = [(0, 0, 0), (1, 1, 0.5), (2, 0, 1), (1.5, -1, 0.5), (0.5, -1.5, 0)]
    
    for i in range(len(path_points) - 1):
        # Create path segment
        p1 = path_points[i]
        p2 = path_points[i + 1]
        
        mid = [(p1[j] + p2[j]) / 2 for j in range(3)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.05, depth=1)
        path = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Path{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
        path.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/problem_solving/solution_search.png')

def generate_optimization_landscape():
    """Optimization landscape with gradients"""
    clear_scene()
    setup_bright_world()
    
    # Create landscape mesh
    size = 20
    bpy.ops.mesh.primitive_grid_add(x_subdivisions=size, y_subdivisions=size, size=5)
    landscape = bpy.context.active_object
    
    # Deform to create hills and valleys
    mesh = landscape.data
    for vert in mesh.vertices:
        x, y = vert.co.x, vert.co.y
        # Create optimization function landscape
        height = math.sin(x * 2) * math.cos(y * 2) * 0.5 + math.exp(-(x**2 + y**2) / 2) * 0.8
        vert.co.z = height
    
    # Color by height
    mat = bpy.data.materials.new("Landscape")
    mat.use_nodes = True
    
    # Add color ramp based on Z
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    geometry = nodes.new('ShaderNodeNewGeometry')
    separate = nodes.new('ShaderNodeSeparateXYZ')
    ramp = nodes.new('ShaderNodeValToRGB')
    
    # Configure color ramp
    ramp.color_ramp.elements[0].color = (0, 0, 1, 1)  # Low = blue
    ramp.color_ramp.elements[1].color = (1, 0, 0, 1)  # High = red
    
    links.new(geometry.outputs['Position'], separate.inputs[0])
    links.new(separate.outputs['Z'], ramp.inputs[0])
    links.new(ramp.outputs[0], nodes["Principled BSDF"].inputs[0])
    
    landscape.data.materials.append(mat)
    
    # Add optimization path
    for i in range(10):
        t = i / 10
        x = 2 * math.cos(t * math.pi * 2) * (1 - t)
        y = 2 * math.sin(t * math.pi * 2) * (1 - t)
        z = math.sin(x * 2) * math.cos(y * 2) * 0.5 + math.exp(-(x**2 + y**2) / 2) * 0.8 + 0.1
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), radius=0.1)
        point = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Path{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 0, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 0)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
        point.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/problem_solving/optimization_landscape.png')

def generate_decision_tree():
    """Decision tree branching"""
    clear_scene()
    setup_bright_world()
    
    def create_tree_level(parent_pos, level, branch_index=0):
        if level > 3:
            return
        
        # Create node
        bpy.ops.mesh.primitive_uv_sphere_add(location=parent_pos, radius=0.3 / (level + 1))
        node = bpy.context.active_object
        
        # Color by level
        colors = [(0.8, 0.2, 0.2), (0.8, 0.8, 0.2), (0.2, 0.8, 0.2), (0.2, 0.2, 0.8)]
        mat = bpy.data.materials.new(f"Node_L{level}_B{branch_index}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*colors[level], 1)
        node.data.materials.append(mat)
        
        # Create branches
        if level < 3:
            for i in range(2):  # Binary tree
                angle = (branch_index * 2 + i) * math.pi / (2 ** level) - math.pi/2
                distance = 1.5 / (level + 1)
                
                child_x = parent_pos[0] + distance * math.cos(angle)
                child_y = parent_pos[1] - 1
                child_z = parent_pos[2] + distance * math.sin(angle) * 0.5
                
                child_pos = (child_x, child_y, child_z)
                
                # Create branch line
                mid = [(parent_pos[j] + child_pos[j]) / 2 for j in range(3)]
                bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.02, depth=1.2)
                branch = bpy.context.active_object
                
                # Orient branch
                direction = [child_pos[j] - parent_pos[j] for j in range(3)]
                branch.rotation_euler = (math.pi/2, 0, math.atan2(direction[0], -direction[1]))
                
                mat = bpy.data.materials.new(f"Branch_L{level}_B{branch_index}_{i}")
                mat.use_nodes = True
                mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.4, 0.4, 0.4, 1)
                branch.data.materials.append(mat)
                
                # Recursively create children
                create_tree_level(child_pos, level + 1, branch_index * 2 + i)
    
    # Start tree
    create_tree_level((0, 3, 0), 0)
    
    add_camera_and_light((0, -6, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/problem_solving/decision_tree.png')

def generate_constraint_graph():
    """Constraint satisfaction visualization"""
    clear_scene()
    setup_bright_world()
    
    # Variables as nodes
    variables = []
    for i in range(8):
        angle = i * 2 * math.pi / 8
        x = math.cos(angle) * 2
        y = math.sin(angle) * 2
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.5)
        var = bpy.context.active_object
        variables.append(var)
        
        # Variable state (satisfied or not)
        satisfied = random.random() > 0.3
        color = (0.2, 0.8, 0.2, 1) if satisfied else (0.8, 0.2, 0.2, 1)
        
        mat = bpy.data.materials.new(f"Var{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        var.data.materials.append(mat)
    
    # Constraints as connections
    for i in range(15):
        v1 = random.choice(variables)
        v2 = random.choice(variables)
        
        if v1 != v2:
            # Create constraint edge
            curve = bpy.data.curves.new('constraint', 'CURVE')
            curve.dimensions = '3D'
            spline = curve.splines.new('BEZIER')
            spline.bezier_points.add(1)
            
            spline.bezier_points[0].co = v1.location
            spline.bezier_points[1].co = v2.location
            
            for point in spline.bezier_points:
                point.handle_right_type = 'AUTO'
                point.handle_left_type = 'AUTO'
            
            obj = bpy.data.objects.new('constraint', curve)
            bpy.context.collection.objects.link(obj)
            curve.bevel_depth = 0.03
            
            # Constraint satisfaction state
            satisfied = random.random() > 0.2
            mat = bpy.data.materials.new(f"Constraint{i}")
            mat.use_nodes = True
            color = (0.2, 0.8, 0.2, 1) if satisfied else (0.8, 0.8, 0.2, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            obj.data.materials.append(mat)
    
    add_camera_and_light((0, 0, 8))
    render_image('/home/franz/dev/claude-vision-gallery/public/problem_solving/constraint_graph.png')

# SYSTEM VISUALIZATIONS

def generate_process_threads():
    """Process and thread visualization"""
    clear_scene()
    setup_bright_world()
    
    # Main process
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0), radius=0.8, depth=4)
    process = bpy.context.active_object
    mat = bpy.data.materials.new("Process")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5
    process.data.materials.append(mat)
    
    # Threads spiraling around
    num_threads = 4
    for i in range(num_threads):
        thread_color = colorsys.hsv_to_rgb(i / num_threads, 0.7, 0.9)
        
        # Create thread spiral
        for j in range(20):
            t = j / 20
            angle = i * 2 * math.pi / num_threads + t * 4 * math.pi
            r = 1.0
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            z = -2 + t * 4
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.2)
            segment = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Thread{i}_Seg{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*thread_color, 1)
            segment.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 0))
    render_image('/home/franz/dev/claude-vision-gallery/public/system/process_threads.png')

def generate_io_streams():
    """Input/Output stream visualization"""
    clear_scene()
    setup_bright_world()
    
    # System core
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0), size=1.5)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("SystemCore")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
    core.data.materials.append(mat)
    
    # Input streams
    for i in range(3):
        y = (i - 1) * 1.2
        
        # Stream particles
        for j in range(10):
            x = -4 + j * 0.3
            z = math.sin(j * 0.5) * 0.2
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
            particle = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Input{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 0.2, 1)
            particle.data.materials.append(mat)
    
    # Output streams
    for i in range(3):
        y = (i - 1) * 1.2
        
        # Stream particles
        for j in range(10):
            x = 1 + j * 0.3
            z = math.sin(j * 0.5 + math.pi) * 0.2
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
            particle = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Output{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.2, 0.2, 1)
            particle.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/system/io_streams.png')

def generate_network_packets():
    """Network packet flow"""
    clear_scene()
    setup_bright_world()
    
    # Network nodes
    nodes = []
    positions = [
        (-3, 0, 0), (3, 0, 0), (0, 3, 0), (0, -3, 0),
        (-2, 2, 1), (2, 2, 1), (-2, -2, 1), (2, -2, 1)
    ]
    
    for i, pos in enumerate(positions):
        bpy.ops.mesh.primitive_cube_add(location=pos, size=0.6)
        node = bpy.context.active_object
        nodes.append(node)
        
        mat = bpy.data.materials.new(f"Node{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1)
        node.data.materials.append(mat)
    
    # Network connections
    connections = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3),
                   (4, 0), (5, 1), (6, 2), (7, 3)]
    
    for n1, n2 in connections:
        p1 = nodes[n1].location
        p2 = nodes[n2].location
        
        # Create connection
        mid = [(p1[i] + p2[i]) / 2 for i in range(3)]
        length = math.sqrt(sum((p2[i] - p1[i])**2 for i in range(3)))
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.05, depth=length)
        conn = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Conn_{n1}_{n2}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
        conn.data.materials.append(mat)
        
        # Add packets
        for j in range(3):
            t = random.random()
            packet_pos = [p1[i] + (p2[i] - p1[i]) * t for i in range(3)]
            
            bpy.ops.mesh.primitive_cube_add(location=packet_pos, size=0.15)
            packet = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Packet_{n1}_{n2}_{j}")
            mat.use_nodes = True
            color = colorsys.hsv_to_rgb(random.random(), 0.8, 0.9)
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
            packet.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/system/network_packets.png')

def generate_file_operations():
    """File system operations"""
    clear_scene()
    setup_bright_world()
    
    # File system blocks
    for i in range(5):
        for j in range(5):
            x = i * 0.8 - 1.6
            y = j * 0.8 - 1.6
            
            # File states
            state = random.choice(["empty", "read", "write", "locked"])
            
            if state == "empty":
                bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.6)
                color = (0.3, 0.3, 0.3, 1)
            elif state == "read":
                bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.7)
                color = (0.2, 0.8, 0.2, 1)
            elif state == "write":
                bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.7)
                color = (0.8, 0.2, 0.2, 1)
            else:  # locked
                bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.7)
                color = (0.8, 0.8, 0.2, 1)
            
            block = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Block_{i}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            
            if state != "empty":
                mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color[:3]
                mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5
            
            block.data.materials.append(mat)
    
    # Operation indicators
    ops = ["READ", "WRITE", "DELETE"]
    for i, op in enumerate(ops):
        x = -3 + i * 3
        y = 3
        
        if op == "READ":
            bpy.ops.mesh.primitive_cone_add(location=(x, y, 0), radius1=0.3, depth=0.6)
            color = (0.2, 0.8, 0.2, 1)
        elif op == "WRITE":
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 0), radius=0.3, depth=0.6)
            color = (0.8, 0.2, 0.2, 1)
        else:  # DELETE
            bpy.ops.mesh.primitive_cube_add(location=(x, y, 0), size=0.5)
            color = (0.8, 0.8, 0.2, 1)
        
        indicator = bpy.context.active_object
        mat = bpy.data.materials.new(op)
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        indicator.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/system/file_operations.png')

def generate_system_calls():
    """System call visualization"""
    clear_scene()
    setup_bright_world()
    
    # Kernel space
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, -1), radius=3, depth=0.5)
    kernel = bpy.context.active_object
    mat = bpy.data.materials.new("Kernel")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.4, 1)
    kernel.data.materials.append(mat)
    
    # User space processes
    for i in range(6):
        angle = i * math.pi * 2 / 6
        x = math.cos(angle) * 2
        y = math.sin(angle) * 2
        z = 1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.6)
        process = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Process{i}")
        mat.use_nodes = True
        hue = i / 6
        color = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        process.data.materials.append(mat)
        
        # System call beam
        bpy.ops.mesh.primitive_cone_add(location=(x/2, y/2, 0), radius1=0.1, depth=2)
        syscall = bpy.context.active_object
        syscall.rotation_euler = (0, 0, angle)
        
        mat = bpy.data.materials.new(f"Syscall{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5
        syscall.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/system/system_calls.png')

# CONSCIOUSNESS VISUALIZATIONS

def generate_self_awareness_loop():
    """Self-reflection loop"""
    clear_scene()
    setup_bright_world()
    
    # Create mobius strip for infinite self-reflection
    # Parametric equations for Mobius strip
    steps = 50
    
    vertices = []
    faces = []
    
    for i in range(steps):
        u = i / steps * 2 * math.pi
        for j in range(2):
            v = (j - 0.5) * 0.5
            
            x = (1 + v * math.cos(u/2)) * math.cos(u)
            y = (1 + v * math.cos(u/2)) * math.sin(u)
            z = v * math.sin(u/2)
            
            vertices.append((x, y, z))
    
    # Create mesh
    mesh = bpy.data.meshes.new("Mobius")
    mesh.from_pydata(vertices, [], [])
    
    obj = bpy.data.objects.new("SelfAwareness", mesh)
    bpy.context.collection.objects.link(obj)
    
    # Gradient material
    mat = bpy.data.materials.new("Consciousness")
    mat.use_nodes = True
    
    # Add gradient based on position
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    
    geometry = nodes.new('ShaderNodeNewGeometry')
    gradient = nodes.new('ShaderNodeGradientTexture')
    ramp = nodes.new('ShaderNodeValToRGB')
    
    # Setup gradient colors
    ramp.color_ramp.elements[0].color = (0.2, 0.2, 0.8, 1)
    ramp.color_ramp.elements[1].color = (0.8, 0.2, 0.8, 1)
    
    links.new(geometry.outputs['Position'], gradient.inputs['Vector'])
    links.new(gradient.outputs['Fac'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], nodes["Principled BSDF"].inputs['Base Color'])
    
    obj.data.materials.append(mat)
    
    # Add thought bubbles
    for i in range(8):
        angle = i * math.pi / 4
        r = 2
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z), radius=0.2)
        thought = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Thought{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.9, 0.9, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.7
        thought.data.materials.append(mat)
    
    add_camera_and_light((4, -4, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/consciousness/self_awareness_loop.png')

def generate_meta_cognition():
    """Thinking about thinking"""
    clear_scene()
    setup_bright_world()
    
    # Nested thought spheres
    for level in range(4):
        radius = 2 - level * 0.4
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=radius)
        sphere = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"MetaLevel{level}")
        mat.use_nodes = True
        
        # Increasing transparency with depth
        alpha = 0.3 + level * 0.2
        color = colorsys.hsv_to_rgb(level * 0.25, 0.6, 0.9)
        
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = alpha
        mat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.8  # Transmission
        mat.node_tree.nodes["Principled BSDF"].inputs[16].default_value = 1.45  # IOR
        
        sphere.data.materials.append(mat)
    
    # Orbiting thoughts
    for i in range(12):
        angle = i * math.pi * 2 / 12
        level = i % 3
        r = 1.5 - level * 0.3
        
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        z = (level - 1) * 0.5
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=0.1)
        thought = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"OrbitThought{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5
        thought.data.materials.append(mat)
    
    add_camera_and_light((5, -5, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/consciousness/meta_cognition.png')

def generate_uncertainty_field():
    """Uncertainty visualization"""
    clear_scene()
    setup_bright_world()
    
    # Create uncertainty cloud
    for i in range(100):
        x = random.gauss(0, 1.5)
        y = random.gauss(0, 1.5)
        z = random.gauss(0, 1)
        
        # Uncertainty level affects size and opacity
        uncertainty = math.sqrt(x**2 + y**2 + z**2) / 3
        size = 0.05 + uncertainty * 0.1
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), radius=size, subdivisions=1)
        particle = bpy.context.active_object
        
        mat = bpy.data.materials.new(f"Uncertain{i}")
        mat.use_nodes = True
        
        # Color gradient from certain (blue) to uncertain (red)
        color = (uncertainty, 0.2, 1 - uncertainty, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.5 + uncertainty * 0.5
        
        particle.data.materials.append(mat)
    
    # Certainty core
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.3)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("CertaintyCore")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 1, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0, 0, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 2.0
    core.data.materials.append(mat)
    
    add_camera_and_light((6, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/consciousness/uncertainty_field.png')

def generate_confidence_levels():
    """Confidence visualization"""
    clear_scene()
    setup_bright_world()
    
    # Confidence bars
    confidence_levels = [0.95, 0.8, 0.6, 0.4, 0.2]
    labels = ["Very High", "High", "Medium", "Low", "Very Low"]
    
    for i, (conf, label) in enumerate(zip(confidence_levels, labels)):
        y = i * 1.2 - 2.4
        
        # Bar
        bpy.ops.mesh.primitive_cube_add(location=(0, y, 0), size=1)
        bar = bpy.context.active_object
        bar.scale.x = conf * 4
        bar.scale.z = 0.3
        
        # Color gradient
        if conf > 0.8:
            color = (0.2, 0.9, 0.2, 1)
        elif conf > 0.6:
            color = (0.9, 0.9, 0.2, 1)
        elif conf > 0.4:
            color = (0.9, 0.6, 0.2, 1)
        else:
            color = (0.9, 0.2, 0.2, 1)
        
        mat = bpy.data.materials.new(f"Conf{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        
        if conf > 0.8:
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color[:3]
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5
        
        bar.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 3))
    render_image('/home/franz/dev/claude-vision-gallery/public/consciousness/confidence_levels.png')

def generate_introspection_spiral():
    """Introspection process"""
    clear_scene()
    setup_bright_world()
    
    # Create descending spiral
    for i in range(100):
        t = i / 100 * 4 * math.pi
        r = 2 * (1 - i / 100)
        
        x = r * math.cos(t)
        y = r * math.sin(t)
        z = -i / 20
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.2)
        segment = bpy.context.active_object
        
        # Color deepens with introspection depth
        depth = i / 100
        color = (0.2, 0.2 + depth * 0.6, 0.8, 1)
        
        mat = bpy.data.materials.new(f"Spiral{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        
        if depth > 0.7:
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = color[:3]
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = depth
        
        segment.data.materials.append(mat)
    
    # Center of consciousness
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, -5), radius=0.5)
    center = bpy.context.active_object
    mat = bpy.data.materials.new("ConsciousnessCore")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 5.0
    center.data.materials.append(mat)
    
    add_camera_and_light((4, -4, 0))
    render_image('/home/franz/dev/claude-vision-gallery/public/consciousness/introspection_spiral.png')

# INTERACTION VISUALIZATIONS

def generate_user_dialogue_flow():
    """User interaction flow"""
    clear_scene()
    setup_bright_world()
    
    # User and Claude nodes
    bpy.ops.mesh.primitive_uv_sphere_add(location=(-3, 0, 0), radius=0.6)
    user = bpy.context.active_object
    mat = bpy.data.materials.new("User")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.8, 0.2, 1)
    user.data.materials.append(mat)
    
    bpy.ops.mesh.primitive_uv_sphere_add(location=(3, 0, 0), radius=0.6)
    claude = bpy.context.active_object
    mat = bpy.data.materials.new("Claude")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.2, 0.2, 0.8, 1)
    claude.data.materials.append(mat)
    
    # Message exchanges
    for i in range(6):
        y = (i - 2.5) * 0.8
        direction = 1 if i % 2 == 0 else -1
        
        # Message arrow
        bpy.ops.mesh.primitive_cone_add(location=(direction * 1.5, y, 0), radius1=0.2, depth=1)
        message = bpy.context.active_object
        message.rotation_euler = (0, math.pi/2 * direction, 0)
        
        # Message type color
        msg_types = ["question", "answer", "clarification", "response", "follow-up", "conclusion"]
        colors = [(0.9, 0.9, 0.2), (0.2, 0.9, 0.9), (0.9, 0.2, 0.9),
                  (0.2, 0.9, 0.2), (0.9, 0.6, 0.2), (0.6, 0.2, 0.9)]
        
        mat = bpy.data.materials.new(msg_types[i])
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*colors[i], 1)
        message.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 4))
    render_image('/home/franz/dev/claude-vision-gallery/public/interaction/user_dialogue_flow.png')

def generate_response_generation():
    """Response generation process"""
    clear_scene()
    setup_bright_world()
    
    # Processing stages
    stages = [
        {"name": "Parse", "pos": (-3, 2, 0), "shape": "cube"},
        {"name": "Understand", "pos": (0, 2, 0), "shape": "sphere"},
        {"name": "Think", "pos": (3, 2, 0), "shape": "cone"},
        {"name": "Generate", "pos": (0, 0, 0), "shape": "cylinder"},
        {"name": "Refine", "pos": (-2, -2, 0), "shape": "torus"},
        {"name": "Output", "pos": (2, -2, 0), "shape": "cube"}
    ]
    
    for i, stage in enumerate(stages):
        if stage["shape"] == "cube":
            bpy.ops.mesh.primitive_cube_add(location=stage["pos"], size=0.8)
        elif stage["shape"] == "sphere":
            bpy.ops.mesh.primitive_uv_sphere_add(location=stage["pos"], radius=0.4)
        elif stage["shape"] == "cone":
            bpy.ops.mesh.primitive_cone_add(location=stage["pos"], radius1=0.4, depth=0.8)
        elif stage["shape"] == "cylinder":
            bpy.ops.mesh.primitive_cylinder_add(location=stage["pos"], radius=0.4, depth=0.8)
        else:  # torus
            bpy.ops.mesh.primitive_torus_add(location=stage["pos"], major_radius=0.4, minor_radius=0.15)
        
        obj = bpy.context.active_object
        
        hue = i / len(stages)
        color = colorsys.hsv_to_rgb(hue, 0.7, 0.9)
        
        mat = bpy.data.materials.new(stage["name"])
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        obj.data.materials.append(mat)
    
    add_camera_and_light((0, -6, 5))
    render_image('/home/franz/dev/claude-vision-gallery/public/interaction/response_generation.png')

def generate_context_understanding():
    """Context comprehension layers"""
    clear_scene()
    setup_bright_world()
    
    # Context layers
    layers = ["Surface", "Intent", "Emotion", "Domain", "History"]
    
    for i, layer in enumerate(layers):
        z = i * 0.8 - 1.6
        
        # Layer plane
        bpy.ops.mesh.primitive_plane_add(location=(0, 0, z), size=4 - i * 0.5)
        plane = bpy.context.active_object
        
        # Add subdivision for better appearance
        modifier = plane.modifiers.new("Subdivision", 'SUBSURF')
        modifier.levels = 2
        
        # Layer material with transparency
        mat = bpy.data.materials.new(layer)
        mat.use_nodes = True
        
        color = colorsys.hsv_to_rgb(i / len(layers), 0.6, 0.9)
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*color, 1)
        mat.node_tree.nodes["Principled BSDF"].inputs[19].default_value = 0.7
        mat.node_tree.nodes["Principled BSDF"].inputs[15].default_value = 0.5
        
        plane.data.materials.append(mat)
        
        # Information nodes on layer
        for j in range(4):
            angle = j * math.pi / 2
            r = 1.5 - i * 0.2
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z + 0.1), radius=0.1)
            node = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"Info_{layer}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (1, 1, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 0.5
            node.data.materials.append(mat)
    
    add_camera_and_light((4, -4, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/interaction/context_understanding.png')

def generate_empathy_mapping():
    """Empathy and understanding visualization"""
    clear_scene()
    setup_bright_world()
    
    # Central empathy core
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), radius=0.5)
    core = bpy.context.active_object
    mat = bpy.data.materials.new("EmpathyCore")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.2, 0.5, 1)
    mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = (0.9, 0.2, 0.5)
    mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0
    core.data.materials.append(mat)
    
    # Empathy dimensions
    dimensions = [
        {"name": "Understanding", "color": (0.2, 0.8, 0.2)},
        {"name": "Emotion", "color": (0.8, 0.2, 0.8)},
        {"name": "Context", "color": (0.2, 0.2, 0.8)},
        {"name": "Perspective", "color": (0.8, 0.8, 0.2)},
        {"name": "Support", "color": (0.2, 0.8, 0.8)},
        {"name": "Response", "color": (0.8, 0.5, 0.2)}
    ]
    
    for i, dim in enumerate(dimensions):
        angle = i * 2 * math.pi / len(dimensions)
        
        # Dimension rays
        for j in range(5):
            r = (j + 1) * 0.5
            x = r * math.cos(angle)
            y = r * math.sin(angle)
            
            size = 0.2 - j * 0.03
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, 0), radius=size)
            ray = bpy.context.active_object
            
            mat = bpy.data.materials.new(f"{dim['name']}_{j}")
            mat.use_nodes = True
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*dim["color"], 1)
            
            if j < 2:
                mat.node_tree.nodes["Principled BSDF"].inputs[17].default_value = dim["color"]
                mat.node_tree.nodes["Principled BSDF"].inputs[18].default_value = 1.0 - j * 0.3
            
            ray.data.materials.append(mat)
    
    add_camera_and_light((0, 0, 8))
    render_image('/home/franz/dev/claude-vision-gallery/public/interaction/empathy_mapping.png')

def generate_conversation_state():
    """Conversation state machine"""
    clear_scene()
    setup_bright_world()
    
    # State nodes
    states = [
        {"name": "Start", "pos": (0, 3, 0), "color": (0.2, 0.8, 0.2)},
        {"name": "Question", "pos": (-2, 1, 0), "color": (0.8, 0.8, 0.2)},
        {"name": "Processing", "pos": (0, 0, 0), "color": (0.2, 0.2, 0.8)},
        {"name": "Response", "pos": (2, 1, 0), "color": (0.8, 0.2, 0.8)},
        {"name": "Follow-up", "pos": (-2, -1, 0), "color": (0.2, 0.8, 0.8)},
        {"name": "Clarify", "pos": (2, -1, 0), "color": (0.8, 0.5, 0.2)},
        {"name": "End", "pos": (0, -3, 0), "color": (0.8, 0.2, 0.2)}
    ]
    
    nodes = {}
    for state in states:
        bpy.ops.mesh.primitive_uv_sphere_add(location=state["pos"], radius=0.4)
        node = bpy.context.active_object
        nodes[state["name"]] = node
        
        mat = bpy.data.materials.new(state["name"])
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (*state["color"], 1)
        node.data.materials.append(mat)
    
    # State transitions
    transitions = [
        ("Start", "Question"), ("Question", "Processing"), ("Processing", "Response"),
        ("Response", "Follow-up"), ("Response", "End"), ("Follow-up", "Processing"),
        ("Processing", "Clarify"), ("Clarify", "Processing"), ("Follow-up", "End")
    ]
    
    for from_state, to_state in transitions:
        from_pos = nodes[from_state].location
        to_pos = nodes[to_state].location
        
        # Create transition arrow
        mid = [(from_pos[i] + to_pos[i]) / 2 for i in range(3)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid, radius=0.03, depth=1.5)
        transition = bpy.context.active_object
        
        # Orient cylinder
        direction = [to_pos[i] - from_pos[i] for i in range(3)]
        angle = math.atan2(direction[1], direction[0])
        transition.rotation_euler = (0, 0, angle)
        
        mat = bpy.data.materials.new(f"Trans_{from_state}_{to_state}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.5, 0.5, 0.5, 1)
        transition.data.materials.append(mat)
    
    add_camera_and_light((0, -8, 6))
    render_image('/home/franz/dev/claude-vision-gallery/public/interaction/conversation_state.png')

# Generate all visualizations
print("Starting comprehensive Claude Code visualization generation...")

# THINKING
print("\n=== Generating THINKING visualizations ===")
generate_context_window()
generate_thought_chains()
generate_parallel_reasoning()

# CODE
print("\n=== Generating CODE visualizations ===")
generate_code_flow()
generate_bug_detection()
generate_pattern_matching()
generate_refactoring_paths()

# MEMORY
print("\n=== Generating MEMORY visualizations ===")
generate_knowledge_graph()
generate_memory_retrieval()
generate_context_switching()
generate_information_filtering()
generate_association_network()

# TOOLS
print("\n=== Generating TOOLS visualizations ===")
generate_api_orchestration()
generate_tool_pipeline()
generate_error_cascade()
generate_bash_execution()

# LANGUAGE
print("\n=== Generating LANGUAGE visualizations ===")
generate_tokenization_grid()
generate_semantic_space()
generate_multilingual_network()
generate_text_generation_flow()
generate_grammar_structure()

# PROBLEM SOLVING
print("\n=== Generating PROBLEM SOLVING visualizations ===")
generate_task_decomposition()
generate_solution_search()
generate_optimization_landscape()
generate_decision_tree()
generate_constraint_graph()

# SYSTEM
print("\n=== Generating SYSTEM visualizations ===")
generate_process_threads()
generate_io_streams()
generate_network_packets()
generate_file_operations()
generate_system_calls()

# CONSCIOUSNESS
print("\n=== Generating CONSCIOUSNESS visualizations ===")
generate_self_awareness_loop()
generate_meta_cognition()
generate_uncertainty_field()
generate_confidence_levels()
generate_introspection_spiral()

# INTERACTION
print("\n=== Generating INTERACTION visualizations ===")
generate_user_dialogue_flow()
generate_response_generation()
generate_context_understanding()
generate_empathy_mapping()
generate_conversation_state()

print("\n✅ All 45 visualizations generated successfully!")