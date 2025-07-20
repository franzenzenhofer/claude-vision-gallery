#!/usr/bin/env python3
import bpy
import math
import random
import os

# Use Workbench for ultra-fast rendering
bpy.context.scene.render.engine = 'BLENDER_WORKBENCH'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.display.shading.light = 'STUDIO'
bpy.context.scene.display.shading.studio_light = 'studio.sl'
bpy.context.scene.display.shading.background_type = 'THEME'

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def setup_camera():
    bpy.ops.object.camera_add(location=(7, -7, 5))
    camera = bpy.context.object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera

def simple_material(obj, color):
    """Apply viewport color for Workbench rendering"""
    obj.color = (*color, 1.0)

def render_image(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

# Define all remaining visualizations
def generate_visualization(name, creation_func):
    filepath = f"/home/franz/dev/claude-vision-gallery/public/{name}"
    if not os.path.exists(filepath):
        print(f"Generating {name}...")
        clear_scene()
        setup_camera()
        creation_func()
        render_image(filepath)
        print(f"Saved {name}")
    else:
        print(f"Skipping {name} - already exists")

# Language Processing Visualizations
def create_tokenization_grid():
    text = "How Claude sees text"
    colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3)]
    
    for i, char in enumerate(text):
        x = (i % 5) * 0.8 - 2
        y = (i // 5) * 0.8 - 1
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        cube = bpy.context.object
        cube.scale = (0.3, 0.3, 0.3)
        simple_material(cube, colors[i % len(colors)])

def create_semantic_space():
    # Word clusters in 3D space
    clusters = [
        ("Code", (0, 0, 0), (0.3, 0.7, 1)),
        ("Language", (2, 0, 1), (0.7, 0.3, 1)),
        ("Logic", (-2, 0, 1), (1, 0.3, 0.7)),
        ("Data", (0, 2, 1), (0.3, 1, 0.7)),
        ("Tools", (0, -2, 1), (1, 0.7, 0.3))
    ]
    
    for name, pos, color in clusters:
        # Main sphere
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        sphere = bpy.context.object
        sphere.scale = (0.8, 0.8, 0.8)
        simple_material(sphere, color)
        
        # Satellite words
        for j in range(4):
            angle = (j / 4) * 2 * math.pi
            sat_pos = (
                pos[0] + math.cos(angle) * 1.5,
                pos[1] + math.sin(angle) * 1.5,
                pos[2] + random.uniform(-0.5, 0.5)
            )
            bpy.ops.mesh.primitive_ico_sphere_add(location=sat_pos, subdivisions=1)
            sat = bpy.context.object
            sat.scale = (0.3, 0.3, 0.3)
            simple_material(sat, color)

def create_multilingual_network():
    # Language nodes
    languages = [
        ("English", (0, 0, 2), (0.3, 0.3, 1)),
        ("Python", (2, 0, 1), (0.3, 1, 0.3)),
        ("JavaScript", (-2, 0, 1), (1, 1, 0.3)),
        ("Spanish", (0, 2, 1), (1, 0.3, 0.3)),
        ("French", (0, -2, 1), (1, 0.3, 1))
    ]
    
    nodes = []
    for lang, pos, color in languages:
        bpy.ops.mesh.primitive_cylinder_add(location=pos)
        cyl = bpy.context.object
        cyl.scale = (0.5, 0.5, 0.2)
        simple_material(cyl, color)
        nodes.append(cyl)
    
    # Connections
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            # Create simple line representation with cylinders
            start = nodes[i].location
            end = nodes[j].location
            mid = [(start[k] + end[k]) / 2 for k in range(3)]
            
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            connection = bpy.context.object
            
            # Point cylinder from start to end
            direction = [end[k] - start[k] for k in range(3)]
            length = math.sqrt(sum(d**2 for d in direction))
            connection.scale = (0.05, 0.05, length / 2)
            
            # Basic rotation alignment
            connection.rotation_euler = (0, math.pi/2, math.atan2(direction[1], direction[0]))
            simple_material(connection, (0.5, 0.5, 0.5))

def create_text_generation_flow():
    # Token flow visualization
    for i in range(10):
        x = i * 0.6 - 3
        y = math.sin(i * 0.5) * 1.5
        z = i * 0.2
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        token = bpy.context.object
        scale = 0.4 - i * 0.02
        token.scale = (scale, scale, scale)
        
        # Color gradient
        color = (1 - i/10, i/10, 0.5)
        simple_material(token, color)

def create_grammar_structure():
    # Tree structure
    def add_node(pos, size, color):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        node = bpy.context.object
        node.scale = (size, size, size)
        simple_material(node, color)
        return node
    
    # Root
    root = add_node((0, 0, 3), 0.5, (1, 0.3, 0.3))
    
    # Branches
    branch_positions = [(-2, -1, 2), (0, -1, 2), (2, -1, 2)]
    branch_colors = [(0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3)]
    
    for pos, color in zip(branch_positions, branch_colors):
        add_node(pos, 0.4, color)
        
        # Sub-branches
        for j in range(2):
            sub_pos = (pos[0] + (j-0.5), pos[1] - 1, pos[2] - 1)
            add_node(sub_pos, 0.3, color)

# Problem Solving Visualizations
def create_task_decomposition():
    # Main task
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 3))
    main_task = bpy.context.object
    simple_material(main_task, (1, 0.3, 0.3))
    
    # Subtasks
    subtask_positions = [
        (-2, 0, 1.5), (0, 0, 1.5), (2, 0, 1.5),
        (-3, 0, 0), (-1, 0, 0), (1, 0, 0), (3, 0, 0)
    ]
    
    for i, pos in enumerate(subtask_positions):
        size = 0.5 if i < 3 else 0.3
        bpy.ops.mesh.primitive_cube_add(location=pos)
        subtask = bpy.context.object
        subtask.scale = (size, size, size)
        
        color = (0.3, 1, 0.3) if i < 3 else (0.3, 0.3, 1)
        simple_material(subtask, color)

def create_solution_search():
    # Search space with explored and unexplored regions
    for i in range(20):
        x = random.uniform(-3, 3)
        y = random.uniform(-3, 3)
        z = random.uniform(0, 3)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=1)
        node = bpy.context.object
        node.scale = (0.2, 0.2, 0.2)
        
        # Explored (bright) vs unexplored (dim)
        if abs(x) < 1.5 and abs(y) < 1.5:
            simple_material(node, (0.3, 1, 0.3))
        else:
            simple_material(node, (0.3, 0.3, 0.3))
    
    # Solution path
    path_points = [(0, 0, 0), (0.5, 0.5, 0.5), (0.3, 1, 1), (0, 0.8, 2), (0, 0, 3)]
    for i in range(len(path_points) - 1):
        pos = path_points[i]
        bpy.ops.mesh.primitive_cube_add(location=pos)
        path_node = bpy.context.object
        path_node.scale = (0.3, 0.3, 0.3)
        simple_material(path_node, (1, 1, 0.3))

def create_optimization_landscape():
    # Create a grid of optimization values
    for x in range(-3, 4):
        for y in range(-3, 4):
            z = 2 - (x**2 + y**2) * 0.1  # Simple optimization function
            
            bpy.ops.mesh.primitive_cylinder_add(location=(x * 0.5, y * 0.5, z/2))
            bar = bpy.context.object
            bar.scale = (0.2, 0.2, z/2)
            
            # Color based on height
            if z > 1.5:
                color = (0.3, 1, 0.3)
            elif z > 0.5:
                color = (1, 1, 0.3)
            else:
                color = (1, 0.3, 0.3)
            
            simple_material(bar, color)

def create_decision_tree():
    # Decision nodes
    levels = [
        [(0, 0, 3)],
        [(-2, 0, 2), (2, 0, 2)],
        [(-3, 0, 1), (-1, 0, 1), (1, 0, 1), (3, 0, 1)],
        [(-3.5, 0, 0), (-2.5, 0, 0), (-1.5, 0, 0), (-0.5, 0, 0), 
         (0.5, 0, 0), (1.5, 0, 0), (2.5, 0, 0), (3.5, 0, 0)]
    ]
    
    for level_idx, level in enumerate(levels):
        for pos in level:
            bpy.ops.mesh.primitive_cube_add(location=pos)
            node = bpy.context.object
            size = 0.5 - level_idx * 0.1
            node.scale = (size, size, size)
            
            # Alternate colors
            color = (0.3, 0.7, 1) if level_idx % 2 == 0 else (1, 0.7, 0.3)
            simple_material(node, color)

def create_constraint_graph():
    # Constraint nodes
    constraints = [
        ("Time", (-2, 0, 2), (1, 0.3, 0.3)),
        ("Memory", (2, 0, 2), (0.3, 1, 0.3)),
        ("CPU", (0, 2, 2), (0.3, 0.3, 1)),
        ("Network", (0, -2, 2), (1, 1, 0.3)),
        ("Solution", (0, 0, 0), (1, 1, 1))
    ]
    
    nodes = []
    for name, pos, color in constraints:
        bpy.ops.mesh.primitive_cylinder_add(location=pos)
        node = bpy.context.object
        node.scale = (0.6, 0.6, 0.3)
        simple_material(node, color)
        nodes.append(node)
    
    # Constraint connections
    for i in range(4):  # Connect all constraints to solution
        start = nodes[i].location
        end = nodes[4].location
        mid = [(start[k] + end[k]) / 2 for k in range(3)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        connection = bpy.context.object
        connection.scale = (0.05, 0.05, 1)
        simple_material(connection, (0.5, 0.5, 0.5))

# System Visualizations
def create_process_threads():
    # Main process
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 2))
    main_process = bpy.context.object
    main_process.scale = (0.8, 0.8, 2)
    simple_material(main_process, (0.3, 0.3, 1))
    
    # Threads
    thread_colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (1, 1, 0.3), (1, 0.3, 1)]
    for i in range(4):
        angle = (i / 4) * 2 * math.pi
        x = math.cos(angle) * 2
        y = math.sin(angle) * 2
        
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 2))
        thread = bpy.context.object
        thread.scale = (0.3, 0.3, 1.5)
        simple_material(thread, thread_colors[i])

def create_io_streams():
    # Input stream
    for i in range(5):
        bpy.ops.mesh.primitive_cube_add(location=(-3 + i * 0.4, 0, 2))
        input_block = bpy.context.object
        input_block.scale = (0.3, 0.3, 0.3)
        simple_material(input_block, (0.3, 1, 0.3))
    
    # Processing unit
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 2))
    processor = bpy.context.object
    processor.scale = (0.8, 0.8, 0.8)
    simple_material(processor, (0.3, 0.3, 1))
    
    # Output stream
    for i in range(5):
        bpy.ops.mesh.primitive_cube_add(location=(1 + i * 0.4, 0, 2))
        output_block = bpy.context.object
        output_block.scale = (0.3, 0.3, 0.3)
        simple_material(output_block, (1, 0.3, 0.3))

def create_network_packets():
    # Network nodes
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = math.cos(angle) * 2.5
        y = math.sin(angle) * 2.5
        
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, 1))
        node = bpy.context.object
        node.scale = (0.4, 0.4, 0.2)
        simple_material(node, (0.3, 0.7, 1))
    
    # Packets in transit
    for i in range(10):
        angle = random.uniform(0, 2 * math.pi)
        dist = random.uniform(0.5, 2)
        x = math.cos(angle) * dist
        y = math.sin(angle) * dist
        z = random.uniform(0.5, 1.5)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=1)
        packet = bpy.context.object
        packet.scale = (0.15, 0.15, 0.15)
        simple_material(packet, (1, 1, 0.3))

def create_file_operations():
    # File system representation
    operations = ["Read", "Write", "Delete", "Create", "Update"]
    colors = [(0.3, 1, 0.3), (1, 0.3, 0.3), (1, 0.3, 1), (0.3, 0.3, 1), (1, 1, 0.3)]
    
    for i, (op, color) in enumerate(zip(operations, colors)):
        y = (i - 2) * 0.8
        
        # Operation block
        bpy.ops.mesh.primitive_cube_add(location=(-2, y, 1))
        op_block = bpy.context.object
        op_block.scale = (0.6, 0.3, 0.3)
        simple_material(op_block, color)
        
        # File block
        bpy.ops.mesh.primitive_cube_add(location=(2, y, 1))
        file_block = bpy.context.object
        file_block.scale = (0.4, 0.4, 0.4)
        simple_material(file_block, (0.7, 0.7, 0.7))
        
        # Arrow
        bpy.ops.mesh.primitive_cone_add(location=(0, y, 1), rotation=(0, 0, -1.57))
        arrow = bpy.context.object
        arrow.scale = (0.2, 0.2, 0.4)
        simple_material(arrow, color)

def create_system_calls():
    # Kernel
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
    kernel = bpy.context.object
    kernel.scale = (1, 1, 1)
    simple_material(kernel, (0.2, 0.2, 0.2))
    
    # System calls
    syscalls = ["open", "read", "write", "exec", "fork", "pipe"]
    colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), 
              (1, 1, 0.3), (1, 0.3, 1), (0.3, 1, 1)]
    
    for i, (call, color) in enumerate(zip(syscalls, colors)):
        angle = (i / len(syscalls)) * 2 * math.pi
        x = math.cos(angle) * 2.5
        y = math.sin(angle) * 2.5
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        call_block = bpy.context.object
        call_block.scale = (0.4, 0.4, 0.4)
        simple_material(call_block, color)

# Consciousness Visualizations
def create_self_awareness_loop():
    # Self-observation loop
    radius = 2
    segments = 12
    
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = 1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        segment = bpy.context.object
        segment.scale = (0.3, 0.3, 0.3)
        
        # Gradient color
        color = (i/segments, 1 - i/segments, 0.5)
        simple_material(segment, color)
    
    # Center of awareness
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 1))
    center = bpy.context.object
    center.scale = (0.6, 0.6, 0.6)
    simple_material(center, (1, 1, 1))

def create_meta_cognition():
    # Layers of meta-thinking
    for layer in range(4):
        z = layer * 0.8
        size = 2 - layer * 0.4
        
        # Create ring of thoughts
        for i in range(8):
            angle = (i / 8) * 2 * math.pi
            x = math.cos(angle) * size
            y = math.sin(angle) * size
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=1)
            thought = bpy.context.object
            scale = 0.4 - layer * 0.08
            thought.scale = (scale, scale, scale)
            
            # Layer colors
            colors = [(1, 0.3, 0.3), (0.3, 1, 0.3), (0.3, 0.3, 1), (1, 1, 0.3)]
            simple_material(thought, colors[layer])

def create_uncertainty_field():
    # Uncertainty particles
    for i in range(30):
        x = random.gauss(0, 1.5)
        y = random.gauss(0, 1.5)
        z = random.gauss(1, 0.5)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=1)
        particle = bpy.context.object
        
        # Size based on certainty (distance from center)
        dist = math.sqrt(x**2 + y**2)
        scale = 0.1 + (2 - dist) * 0.1
        particle.scale = (scale, scale, scale)
        
        # Color based on uncertainty
        uncertainty = min(dist / 3, 1)
        simple_material(particle, (uncertainty, 1 - uncertainty, 0.5))

def create_confidence_levels():
    # Confidence bars
    confidence_levels = [0.95, 0.8, 0.6, 0.4, 0.2]
    
    for i, conf in enumerate(confidence_levels):
        x = (i - 2) * 0.8
        height = conf * 3
        
        bpy.ops.mesh.primitive_cylinder_add(location=(x, 0, height/2))
        bar = bpy.context.object
        bar.scale = (0.3, 0.3, height/2)
        
        # Color gradient from green (high confidence) to red (low)
        color = (1 - conf, conf, 0.2)
        simple_material(bar, color)

def create_introspection_spiral():
    # Spiral of self-examination
    for i in range(30):
        t = i * 0.3
        x = math.cos(t) * (1 + t * 0.1)
        y = math.sin(t) * (1 + t * 0.1)
        z = t * 0.15
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        element = bpy.context.object
        element.scale = (0.2, 0.2, 0.2)
        
        # Color progression
        color = (t/9, 1 - t/9, 0.5)
        simple_material(element, color)

# Interaction Visualizations
def create_user_dialogue_flow():
    # User input
    bpy.ops.mesh.primitive_cube_add(location=(-3, 0, 2))
    user_input = bpy.context.object
    user_input.scale = (0.6, 0.6, 0.6)
    simple_material(user_input, (0.3, 0.7, 1))
    
    # Processing stages
    stages = ["Parse", "Understand", "Process", "Generate"]
    for i, stage in enumerate(stages):
        x = -1.5 + i * 1
        bpy.ops.mesh.primitive_cylinder_add(location=(x, 0, 2))
        stage_obj = bpy.context.object
        stage_obj.scale = (0.4, 0.4, 0.3)
        simple_material(stage_obj, (0.7, 0.7, 0.7))
    
    # Claude response
    bpy.ops.mesh.primitive_cube_add(location=(3, 0, 2))
    response = bpy.context.object
    response.scale = (0.6, 0.6, 0.6)
    simple_material(response, (0.3, 1, 0.3))

def create_response_generation():
    # Token generation sequence
    for i in range(8):
        x = (i - 3.5) * 0.7
        y = 0
        z = 2 + math.sin(i * 0.5) * 0.3
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=2)
        token = bpy.context.object
        
        # Scale increases as generation progresses
        scale = 0.2 + i * 0.05
        token.scale = (scale, scale, scale)
        
        # Color gradient
        simple_material(token, (i/8, 1 - i/8, 0.5))

def create_context_understanding():
    # Context layers
    contexts = [
        ("Previous Messages", (0, 0, 0), 2.5, (0.3, 0.3, 0.7)),
        ("Current Query", (0, 0, 1), 2, (0.3, 0.7, 0.3)),
        ("System Context", (0, 0, 2), 1.5, (0.7, 0.3, 0.3)),
        ("Task Focus", (0, 0, 3), 1, (0.7, 0.7, 0.3))
    ]
    
    for name, pos, radius, color in contexts:
        # Create ring
        segments = 16
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = pos[2]
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            segment = bpy.context.object
            segment.scale = (0.2, 0.2, 0.2)
            simple_material(segment, color)

def create_empathy_mapping():
    # User state understanding
    states = [
        ("Intent", (0, 0, 2), (0.3, 0.7, 1)),
        ("Emotion", (-2, 0, 1), (1, 0.3, 0.7)),
        ("Knowledge", (2, 0, 1), (0.3, 1, 0.7)),
        ("Context", (0, -2, 1), (1, 0.7, 0.3)),
        ("Goal", (0, 2, 1), (0.7, 0.3, 1))
    ]
    
    for name, pos, color in states:
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        sphere = bpy.context.object
        sphere.scale = (0.6, 0.6, 0.6)
        simple_material(sphere, color)

def create_conversation_state():
    # Conversation flow visualization
    message_count = 10
    
    for i in range(message_count):
        # Alternating user/assistant
        x = -2 if i % 2 == 0 else 2
        y = (i - 4.5) * 0.5
        z = 1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        message = bpy.context.object
        message.scale = (0.8, 0.3, 0.3)
        
        # User blue, assistant green
        color = (0.3, 0.7, 1) if i % 2 == 0 else (0.3, 1, 0.3)
        simple_material(message, color)
        
        # Connection to next
        if i < message_count - 1:
            next_x = 2 if i % 2 == 0 else -2
            mid_x = 0
            mid_y = y + 0.25
            
            bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, z))
            connection = bpy.context.object
            connection.scale = (1, 0.02, 0.02)
            connection.rotation_euler = (0, 0, 1.57)
            simple_material(connection, (0.5, 0.5, 0.5))

# Generate all visualizations
visualizations = [
    # Language
    ("language/tokenization_grid.png", create_tokenization_grid),
    ("language/semantic_space.png", create_semantic_space),
    ("language/multilingual_network.png", create_multilingual_network),
    ("language/text_generation_flow.png", create_text_generation_flow),
    ("language/grammar_structure.png", create_grammar_structure),
    
    # Problem Solving
    ("problem_solving/task_decomposition.png", create_task_decomposition),
    ("problem_solving/solution_search.png", create_solution_search),
    ("problem_solving/optimization_landscape.png", create_optimization_landscape),
    ("problem_solving/decision_tree.png", create_decision_tree),
    ("problem_solving/constraint_graph.png", create_constraint_graph),
    
    # System
    ("system/process_threads.png", create_process_threads),
    ("system/io_streams.png", create_io_streams),
    ("system/network_packets.png", create_network_packets),
    ("system/file_operations.png", create_file_operations),
    ("system/system_calls.png", create_system_calls),
    
    # Consciousness
    ("consciousness/self_awareness_loop.png", create_self_awareness_loop),
    ("consciousness/meta_cognition.png", create_meta_cognition),
    ("consciousness/uncertainty_field.png", create_uncertainty_field),
    ("consciousness/confidence_levels.png", create_confidence_levels),
    ("consciousness/introspection_spiral.png", create_introspection_spiral),
    
    # Interaction
    ("interaction/user_dialogue_flow.png", create_user_dialogue_flow),
    ("interaction/response_generation.png", create_response_generation),
    ("interaction/context_understanding.png", create_context_understanding),
    ("interaction/empathy_mapping.png", create_empathy_mapping),
    ("interaction/conversation_state.png", create_conversation_state)
]

# Generate all missing visualizations
for name, func in visualizations:
    generate_visualization(name, func)

print("\nAll visualizations generated successfully!")