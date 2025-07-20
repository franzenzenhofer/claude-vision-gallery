#!/usr/bin/env python3
import bpy
import math
import random
import os

# Configure for neon aesthetic with dark background
bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
bpy.context.scene.render.resolution_x = 1080
bpy.context.scene.render.resolution_y = 1080
bpy.context.scene.eevee.bloom_threshold = 0.8
bpy.context.scene.eevee.bloom_intensity = 1.0
bpy.context.scene.eevee.bloom_radius = 6.5
bpy.context.scene.eevee.use_bloom = True

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def setup_dark_world():
    """Pure black background for maximum neon contrast"""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    bg.inputs[1].default_value = 0.0

def add_centered_camera():
    """Camera perfectly centered on origin"""
    bpy.ops.object.camera_add(location=(0, -10, 0))
    camera = bpy.context.object
    camera.rotation_euler = (1.57, 0, 0)
    bpy.context.scene.camera = camera
    camera.data.lens = 50

def get_neon_material(name, color, intensity=10):
    """Ultra bright neon material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (*color, 1.0)
    emission.inputs[1].default_value = intensity
    
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    return mat

def render_image(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

# ELECTRIC NEON COLORS
NEON = {
    'cyan': (0, 1, 1),
    'magenta': (1, 0, 1),
    'yellow': (1, 1, 0),
    'green': (0, 1, 0),
    'blue': (0, 0.5, 1),
    'orange': (1, 0.5, 0),
    'purple': (0.5, 0, 1),
    'pink': (1, 0, 0.5),
    'white': (1, 1, 1),
    'red': (1, 0, 0)
}

# THINKING CATEGORY
def create_token_stream():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Flowing stream of glowing tokens
    for i in range(30):
        t = i / 5
        x = (i - 15) * 0.3
        y = math.sin(t) * 2
        z = math.cos(t) * 0.5
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        token = bpy.context.object
        token.scale = (0.2, 0.2, 0.2)
        
        colors = [NEON['cyan'], NEON['magenta'], NEON['yellow']]
        color = colors[i % len(colors)]
        intensity = 8 + math.sin(t) * 3
        token.data.materials.append(get_neon_material(f"Token{i}", color, intensity))

def create_attention_matrix():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Grid of attention connections
    size = 10
    for i in range(size):
        for j in range(size):
            if random.random() > 0.4:
                x = (i - size/2) * 0.6
                y = (j - size/2) * 0.6
                z = 0
                
                weight = random.random()
                scale = 0.05 + weight * 0.15
                
                bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
                node = bpy.context.object
                node.scale = (scale, scale, scale)
                
                color = NEON['cyan'] if weight > 0.7 else NEON['blue']
                intensity = 5 + weight * 10
                node.data.materials.append(get_neon_material(f"Att{i}{j}", color, intensity))

def create_context_window():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Nested glowing frames
    for layer in range(6):
        size = 4 - layer * 0.6
        depth = layer * 0.3
        
        # Create glowing frame edges
        edges = [
            ((-size, -size, depth), (size, -size, depth)),
            ((size, -size, depth), (size, size, depth)),
            ((size, size, depth), (-size, size, depth)),
            ((-size, size, depth), (-size, -size, depth))
        ]
        
        for idx, (start, end) in enumerate(edges):
            mid = [(s + e) / 2 for s, e in zip(start, end)]
            length = math.sqrt(sum((e - s)**2 for s, e in zip(start, end)))
            
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            edge = bpy.context.object
            edge.scale = (0.05, 0.05, length / 2)
            
            # Orient edge
            if idx % 2 == 0:  # Horizontal
                edge.rotation_euler = (0, 1.57, 0)
            else:  # Vertical
                edge.rotation_euler = (1.57, 0, 0)
            
            colors = [NEON['cyan'], NEON['magenta'], NEON['yellow'], NEON['green'], NEON['blue'], NEON['pink']]
            color = colors[layer % len(colors)]
            edge.data.materials.append(get_neon_material(f"Frame{layer}{idx}", color, 8))

def create_thought_chains():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create central neural hub with radiating chains
    # Central core
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    core = bpy.context.object
    core.scale = (0.5, 0.5, 0.5)
    core.data.materials.append(get_neon_material("Core", NEON['white'], 15))
    
    # Radiating thought chains
    chains = 8
    for i in range(chains):
        angle = (i / chains) * 2 * math.pi
        
        # Chain of connected thoughts
        for j in range(5):
            dist = 0.8 + j * 0.8
            x = math.cos(angle) * dist
            y = math.sin(angle) * dist
            z = math.sin(j * 0.5) * 0.3
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            thought = bpy.context.object
            thought.scale = (0.3 - j * 0.04, 0.3 - j * 0.04, 0.3 - j * 0.04)
            
            color = list(NEON.values())[i % len(NEON)]
            intensity = 10 - j * 1.5
            thought.data.materials.append(get_neon_material(f"Thought{i}{j}", color, intensity))

def create_parallel_reasoning():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Multiple parallel processing streams
    streams = 7
    for stream in range(streams):
        y_offset = (stream - streams/2) * 1.2
        color = list(NEON.values())[stream % len(NEON)]
        
        # Pulsing stream
        for i in range(15):
            x = (i - 7) * 0.5
            y = y_offset
            z = math.sin(i * 0.5 + stream * 0.8) * 0.3
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            pulse = bpy.context.object
            
            scale = 0.15 + math.sin(i * 0.3) * 0.1
            pulse.scale = (scale, scale, scale)
            
            intensity = 6 + abs(math.sin(i * 0.3)) * 6
            pulse.data.materials.append(get_neon_material(f"Stream{stream}{i}", color, intensity))

# CODE CATEGORY
def create_syntax_tree():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    def add_node(pos, size, color, name):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        node = bpy.context.object
        node.scale = (size, size, size)
        node.data.materials.append(get_neon_material(name, color, 12))
        return node
    
    def connect_nodes(start_pos, end_pos, name):
        mid = [(s + e) / 2 for s, e in zip(start_pos, end_pos)]
        
        # Calculate cylinder orientation
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        dz = end_pos[2] - start_pos[2]
        length = math.sqrt(dx**2 + dy**2 + dz**2)
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.02, 0.02, length / 2)
        
        # Point cylinder from start to end
        if dx != 0 or dy != 0:
            angle_z = math.atan2(dy, dx)
            angle_y = math.atan2(dz, math.sqrt(dx**2 + dy**2))
            edge.rotation_euler = (1.57 + angle_y, 0, angle_z)
        
        edge.data.materials.append(get_neon_material(name, NEON['white'], 5))
    
    # Build tree structure
    root = add_node((0, 0, 2), 0.4, NEON['magenta'], "Root")
    
    # Level 1
    l1_nodes = []
    l1_positions = [(-2, 0, 0.5), (0, 0, 0.5), (2, 0, 0.5)]
    l1_colors = [NEON['cyan'], NEON['yellow'], NEON['green']]
    
    for i, (pos, color) in enumerate(zip(l1_positions, l1_colors)):
        node = add_node(pos, 0.3, color, f"L1_{i}")
        l1_nodes.append(node)
        connect_nodes((0, 0, 2), pos, f"Edge_R_L1_{i}")
    
    # Level 2
    for i, parent in enumerate(l1_nodes):
        for j in range(2):
            x = parent.location[0] + (j - 0.5) * 0.8
            y = 0
            z = -1
            
            color = NEON['orange'] if j == 0 else NEON['purple']
            add_node((x, y, z), 0.2, color, f"L2_{i}_{j}")
            connect_nodes(parent.location, (x, y, z), f"Edge_L1_{i}_L2_{j}")

def create_code_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create spiraling code flow
    points = 40
    for i in range(points):
        t = i / points * 4 * math.pi
        radius = 1 + t / (2 * math.pi)
        
        x = math.cos(t) * radius
        y = math.sin(t) * radius
        z = (i - points/2) * 0.1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        flow = bpy.context.object
        flow.scale = (0.2, 0.2, 0.2)
        
        # Color gradient through spectrum
        color_idx = int((i / points) * len(NEON))
        color = list(NEON.values())[color_idx % len(NEON)]
        intensity = 5 + (i / points) * 8
        
        flow.data.materials.append(get_neon_material(f"Flow{i}", color, intensity))

def create_bug_detection():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Grid of code blocks with bugs highlighted
    grid_size = 7
    bug_positions = [(2, 4), (5, 1), (1, 6)]
    
    for i in range(grid_size):
        for j in range(grid_size):
            x = (i - grid_size/2) * 0.8
            y = (j - grid_size/2) * 0.8
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            block = bpy.context.object
            
            # Check if bug position
            is_bug = (i, j) in bug_positions
            
            if is_bug:
                block.scale = (0.4, 0.4, 0.4)
                color = NEON['red']
                intensity = 15
            else:
                block.scale = (0.3, 0.3, 0.3)
                color = NEON['green']
                intensity = 3
            
            block.data.materials.append(get_neon_material(f"Block{i}{j}", color, intensity))
            
            # Add warning glow around bugs
            if is_bug:
                bpy.ops.mesh.primitive_torus_add(location=(x, y, z))
                warning = bpy.context.object
                warning.scale = (0.6, 0.6, 0.1)
                warning.data.materials.append(get_neon_material(f"Warning{i}{j}", NEON['orange'], 8))

def create_pattern_matching():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create matching pattern groups
    patterns = [
        # L shape
        [(0, 0), (0, 1), (1, 0)],
        # T shape
        [(0, 0), (0, 1), (0, -1), (1, 0)],
        # Square
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ]
    
    colors = [NEON['cyan'], NEON['magenta'], NEON['yellow']]
    
    for p_idx, (pattern, color) in enumerate(zip(patterns, colors)):
        base_x = (p_idx - 1) * 3
        
        # Draw pattern
        for x, y in pattern:
            pos_x = base_x + x * 0.6
            pos_y = y * 0.6
            
            bpy.ops.mesh.primitive_cube_add(location=(pos_x, pos_y, 0))
            block = bpy.context.object
            block.scale = (0.25, 0.25, 0.25)
            block.data.materials.append(get_neon_material(f"Pattern{p_idx}_{x}_{y}", color, 10))
        
        # Add connecting glow between pattern blocks
        for i in range(len(pattern) - 1):
            start = (base_x + pattern[i][0] * 0.6, pattern[i][1] * 0.6, 0)
            end = (base_x + pattern[i+1][0] * 0.6, pattern[i+1][1] * 0.6, 0)
            mid = [(s + e) / 2 for s, e in zip(start, end)]
            
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            connector = bpy.context.object
            connector.scale = (0.05, 0.05, 0.3)
            connector.data.materials.append(get_neon_material(f"Connect{p_idx}_{i}", color, 5))

def create_refactoring_paths():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Chaotic "before" state
    random.seed(42)
    for i in range(12):
        x = random.uniform(-3.5, -1.5)
        y = random.uniform(-2, 2)
        z = random.uniform(-0.5, 0.5)
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        messy = bpy.context.object
        messy.scale = (0.2, 0.2, 0.2)
        messy.rotation_euler = (random.random(), random.random(), random.random())
        messy.data.materials.append(get_neon_material(f"Messy{i}", NEON['red'], 4))
    
    # Clean "after" state
    for i in range(3):
        for j in range(4):
            x = 2 + i * 0.6
            y = (j - 1.5) * 0.6
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            clean = bpy.context.object
            clean.scale = (0.25, 0.25, 0.25)
            clean.data.materials.append(get_neon_material(f"Clean{i}{j}", NEON['green'], 8))
    
    # Transformation arrows
    for i in range(3):
        y = (i - 1) * 1.5
        bpy.ops.mesh.primitive_cone_add(location=(0, y, 0), rotation=(0, 0, -1.57))
        arrow = bpy.context.object
        arrow.scale = (0.3, 0.3, 0.8)
        arrow.data.materials.append(get_neon_material(f"Arrow{i}", NEON['yellow'], 12))

# MEMORY CATEGORY
def create_knowledge_graph():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Central knowledge hub with radiating connections
    nodes = []
    
    # Central hub
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    hub = bpy.context.object
    hub.scale = (0.6, 0.6, 0.6)
    hub.data.materials.append(get_neon_material("Hub", NEON['white'], 15))
    nodes.append(hub)
    
    # Primary concepts
    primary_positions = []
    for i in range(6):
        angle = i * math.pi / 3
        x = math.cos(angle) * 2.5
        y = math.sin(angle) * 2.5
        z = 0
        primary_positions.append((x, y, z))
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        primary = bpy.context.object
        primary.scale = (0.4, 0.4, 0.4)
        
        color = list(NEON.values())[i % len(NEON)]
        primary.data.materials.append(get_neon_material(f"Primary{i}", color, 10))
        nodes.append(primary)
        
        # Connect to hub
        bpy.ops.mesh.primitive_cylinder_add(location=(x/2, y/2, 0))
        edge = bpy.context.object
        edge.scale = (0.02, 0.02, 1.25)
        edge.rotation_euler = (0, 0, angle)
        edge.data.materials.append(get_neon_material(f"EdgeHub{i}", NEON['white'], 3))
    
    # Secondary concepts
    for i, (px, py, pz) in enumerate(primary_positions):
        for j in range(3):
            angle = (i * math.pi / 3) + (j - 1) * 0.5
            x = px + math.cos(angle) * 1
            y = py + math.sin(angle) * 1
            z = random.uniform(-0.5, 0.5)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            secondary = bpy.context.object
            secondary.scale = (0.25, 0.25, 0.25)
            
            color = list(NEON.values())[(i + j + 3) % len(NEON)]
            secondary.data.materials.append(get_neon_material(f"Secondary{i}{j}", color, 6))

def create_memory_retrieval():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Query pulse at center
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
    query = bpy.context.object
    query.scale = (0.5, 0.5, 0.5)
    query.data.materials.append(get_neon_material("Query", NEON['yellow'], 15))
    
    # Memory fragments being accessed
    memories = 20
    for i in range(memories):
        angle = (i / memories) * 2 * math.pi
        distance = 2 + random.uniform(0, 1.5)
        height = random.uniform(-1.5, 1.5)
        
        x = math.cos(angle) * distance
        y = math.sin(angle) * distance
        z = height
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        memory = bpy.context.object
        memory.scale = (0.2, 0.2, 0.2)
        
        # Closer memories glow brighter
        intensity = 15 - distance * 3
        colors = [NEON['cyan'], NEON['magenta'], NEON['green']]
        color = colors[i % len(colors)]
        
        memory.data.materials.append(get_neon_material(f"Memory{i}", color, intensity))
        
        # Retrieval beam
        if distance < 3:
            mid_x = x / 2
            mid_y = y / 2
            mid_z = z / 2
            
            bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, mid_z))
            beam = bpy.context.object
            beam.scale = (0.01, 0.01, distance / 2)
            
            # Orient beam
            beam.rotation_euler = (
                math.atan2(z, math.sqrt(x**2 + y**2)),
                0,
                math.atan2(y, x)
            )
            
            beam.data.materials.append(get_neon_material(f"Beam{i}", NEON['white'], 2))

def create_context_switching():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Multiple context layers
    contexts = ["Code", "Language", "Tools", "Memory", "Logic"]
    colors = [NEON['cyan'], NEON['magenta'], NEON['yellow'], NEON['green'], NEON['orange']]
    
    for i, (context, color) in enumerate(zip(contexts, colors)):
        z = (i - 2) * 0.8
        
        # Context ring
        segments = 16
        radius = 2.5 - abs(i - 2) * 0.3
        
        for j in range(segments):
            angle = (j / segments) * 2 * math.pi
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            segment = bpy.context.object
            segment.scale = (0.2, 0.2, 0.1)
            
            # Active context glows brighter
            intensity = 12 if i == 2 else 6
            segment.data.materials.append(get_neon_material(f"{context}{j}", color, intensity))

def create_information_filtering():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Incoming data stream (left side)
    for i in range(30):
        x = -3 + random.uniform(-0.5, 0.5)
        y = random.uniform(-3, 3)
        z = random.uniform(-1, 1)
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        noise = bpy.context.object
        noise.scale = (0.1, 0.1, 0.1)
        
        # Most data is dim noise
        color = NEON['blue'] if random.random() > 0.8 else NEON['purple']
        intensity = 8 if random.random() > 0.8 else 2
        noise.data.materials.append(get_neon_material(f"Noise{i}", color, intensity))
    
    # Filter mesh at center
    filter_size = 2
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 0:  # Checkerboard pattern
                x = 0
                y = (i - 3.5) * 0.3
                z = (j - 3.5) * 0.3
                
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
                filter_cell = bpy.context.object
                filter_cell.scale = (0.1, 0.15, 0.15)
                filter_cell.data.materials.append(get_neon_material(f"Filter{i}{j}", NEON['white'], 5))
    
    # Filtered output (right side)
    important_data = ["Pattern", "Signal", "Insight", "Connection"]
    for i, data in enumerate(important_data):
        x = 3
        y = (i - 1.5) * 1
        z = 0
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        signal = bpy.context.object
        signal.scale = (0.3, 0.3, 0.3)
        
        color = list(NEON.values())[i + 2]
        signal.data.materials.append(get_neon_material(data, color, 12))

def create_association_network():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create web of associated concepts
    concepts = [
        ("Code", (0, 0, 0), NEON['cyan']),
        ("Function", (2, 0, 0.5), NEON['green']),
        ("Variable", (-2, 0, 0.5), NEON['yellow']),
        ("Loop", (0, 2, 0.5), NEON['magenta']),
        ("Class", (0, -2, 0.5), NEON['orange']),
        ("Method", (1.4, 1.4, -0.5), NEON['purple']),
        ("Parameter", (-1.4, 1.4, -0.5), NEON['pink']),
        ("Return", (1.4, -1.4, -0.5), NEON['blue']),
        ("Type", (-1.4, -1.4, -0.5), NEON['red'])
    ]
    
    nodes = []
    for name, pos, color in concepts:
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos)
        node = bpy.context.object
        node.scale = (0.3, 0.3, 0.3) if name == "Code" else (0.25, 0.25, 0.25)
        node.data.materials.append(get_neon_material(name, color, 10))
        nodes.append((node, pos))
    
    # Create associations
    associations = [
        (0, 1), (0, 2), (0, 3), (0, 4),  # Code connects to all
        (1, 5), (1, 6), (1, 7),          # Function connections
        (4, 5), (4, 8),                  # Class connections
        (2, 6), (3, 2)                   # Variable and Loop connections
    ]
    
    for i, j in associations:
        start = concepts[i][1]
        end = concepts[j][1]
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        
        length = math.sqrt(sum((e - s)**2 for s, e in zip(start, end)))
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.02, 0.02, length / 2)
        
        # Calculate rotation
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        
        if dx != 0 or dy != 0:
            angle_z = math.atan2(dy, dx)
            angle_y = math.atan2(dz, math.sqrt(dx**2 + dy**2))
            edge.rotation_euler = (1.57 + angle_y, 0, angle_z)
        
        edge.data.materials.append(get_neon_material(f"Assoc{i}{j}", NEON['white'], 3))

# TOOLS CATEGORY
def create_file_system_tree():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    def add_folder(pos, size, color, name):
        bpy.ops.mesh.primitive_cube_add(location=pos)
        folder = bpy.context.object
        folder.scale = (size * 1.2, size, size * 0.8)
        folder.data.materials.append(get_neon_material(name, color, 8))
        return folder
    
    def add_file(pos, size, color, name):
        bpy.ops.mesh.primitive_cylinder_add(location=pos)
        file = bpy.context.object
        file.scale = (size * 0.8, size * 0.8, size * 1.2)
        file.rotation_euler = (1.57, 0, 0)
        file.data.materials.append(get_neon_material(name, color, 6))
        return file
    
    # Root directory
    root = add_folder((0, 0, 2), 0.4, NEON['yellow'], "Root")
    
    # Subdirectories
    dirs = [
        ("src", (-2, 0, 0.5), NEON['cyan']),
        ("tests", (0, 0, 0.5), NEON['green']),
        ("docs", (2, 0, 0.5), NEON['magenta'])
    ]
    
    for name, pos, color in dirs:
        folder = add_folder(pos, 0.3, color, name)
        
        # Connect to root
        mid = [(0 + pos[0])/2, 0, (2 + pos[2])/2]
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.02, 0.02, 0.75)
        edge.rotation_euler = (0.3 if pos[0] < 0 else -0.3 if pos[0] > 0 else 0, 0, 0)
        edge.data.materials.append(get_neon_material(f"Edge_{name}", NEON['white'], 2))
        
        # Add files in each directory
        for i in range(3):
            file_x = pos[0] + (i - 1) * 0.5
            file_y = pos[1]
            file_z = pos[2] - 1
            
            file_color = NEON['orange'] if i == 1 else NEON['purple']
            add_file((file_x, file_y, file_z), 0.15, file_color, f"File_{name}_{i}")

def create_api_orchestration():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Central orchestrator
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    orchestrator = bpy.context.object
    orchestrator.scale = (0.6, 0.6, 0.6)
    orchestrator.data.materials.append(get_neon_material("Orchestrator", NEON['white'], 15))
    
    # API endpoints in a circle
    apis = [
        ("Read", NEON['cyan']),
        ("Write", NEON['magenta']),
        ("Execute", NEON['yellow']),
        ("Search", NEON['green']),
        ("Parse", NEON['orange']),
        ("Transform", NEON['purple'])
    ]
    
    for i, (api, color) in enumerate(apis):
        angle = (i / len(apis)) * 2 * math.pi
        x = math.cos(angle) * 3
        y = math.sin(angle) * 3
        z = 0
        
        # API node
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        api_node = bpy.context.object
        api_node.scale = (0.4, 0.4, 0.4)
        api_node.data.materials.append(get_neon_material(api, color, 10))
        
        # Pulsing connection
        segments = 5
        for j in range(segments):
            seg_x = x * (j + 1) / (segments + 1)
            seg_y = y * (j + 1) / (segments + 1)
            seg_z = math.sin(j * 0.5) * 0.2
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(seg_x, seg_y, seg_z))
            pulse = bpy.context.object
            pulse.scale = (0.08, 0.08, 0.08)
            pulse.data.materials.append(get_neon_material(f"Pulse_{api}_{j}", color, 6 + j))

def create_tool_pipeline():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Pipeline stages
    stages = [
        ("Input", NEON['cyan']),
        ("Validate", NEON['blue']),
        ("Process", NEON['green']),
        ("Transform", NEON['yellow']),
        ("Output", NEON['magenta'])
    ]
    
    for i, (stage, color) in enumerate(stages):
        x = (i - 2) * 1.5
        y = 0
        z = 0
        
        # Stage container
        bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
        container = bpy.context.object
        container.scale = (0.5, 0.5, 0.3)
        container.rotation_euler = (0, 1.57, 0)
        container.data.materials.append(get_neon_material(stage, color, 8))
        
        # Data flow particles
        if i < len(stages) - 1:
            for j in range(3):
                flow_x = x + 0.75 + j * 0.25
                flow_y = 0
                flow_z = (j - 1) * 0.2
                
                bpy.ops.mesh.primitive_ico_sphere_add(location=(flow_x, flow_y, flow_z))
                particle = bpy.context.object
                particle.scale = (0.08, 0.08, 0.08)
                particle.data.materials.append(get_neon_material(f"Flow_{stage}_{j}", NEON['white'], 10))

def create_error_cascade():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Initial error source
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 2.5))
    source = bpy.context.object
    source.scale = (0.3, 0.3, 0.3)
    source.data.materials.append(get_neon_material("ErrorSource", NEON['red'], 15))
    
    # Cascading error propagation
    levels = 4
    for level in range(1, levels):
        spread = 2 ** level
        
        for i in range(spread):
            angle = (i / spread) * 2 * math.pi
            radius = level * 1.2
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = 2.5 - level * 0.8
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            error = bpy.context.object
            error.scale = (0.2, 0.2, 0.2)
            
            # Errors get dimmer as they cascade
            intensity = 12 - level * 2
            error.data.materials.append(get_neon_material(f"Error_L{level}_{i}", NEON['red'], intensity))
            
            # Error propagation lines
            if level == 1:
                start = (0, 0, 2.5)
            else:
                parent_idx = i // 2
                parent_angle = (parent_idx / (spread // 2)) * 2 * math.pi
                parent_radius = (level - 1) * 1.2
                start = (
                    math.cos(parent_angle) * parent_radius,
                    math.sin(parent_angle) * parent_radius,
                    2.5 - (level - 1) * 0.8
                )
            
            mid = [(s + x) / 2 for s, x in zip(start, (x, y, z))]
            
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            line = bpy.context.object
            line.scale = (0.01, 0.01, 0.6)
            line.data.materials.append(get_neon_material(f"Cascade_{level}_{i}", NEON['orange'], 5))

def create_bash_execution():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Terminal frame
    frame_positions = [
        ((-3, -2, 0), (3, -2, 0)),
        ((3, -2, 0), (3, 2, 0)),
        ((3, 2, 0), (-3, 2, 0)),
        ((-3, 2, 0), (-3, -2, 0))
    ]
    
    for i, (start, end) in enumerate(frame_positions):
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        length = 6 if i % 2 == 0 else 4
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.05, 0.05, length / 2)
        edge.rotation_euler = (0, 1.57 if i % 2 == 0 else 0, 0)
        edge.data.materials.append(get_neon_material(f"Frame{i}", NEON['green'], 8))
    
    # Command lines
    commands = [
        ("$ ls -la", -1.5, NEON['cyan']),
        ("$ git status", -0.5, NEON['yellow']),
        ("$ python run.py", 0.5, NEON['magenta']),
        ("$ echo 'Done!'", 1.5, NEON['green'])
    ]
    
    for cmd, y, color in commands:
        # Command prompt
        x_start = -2.5
        for j, char in enumerate("$ "):
            bpy.ops.mesh.primitive_cube_add(location=(x_start + j * 0.2, y, 0))
            prompt = bpy.context.object
            prompt.scale = (0.08, 0.08, 0.08)
            prompt.data.materials.append(get_neon_material(f"Prompt_{y}_{j}", NEON['white'], 10))
        
        # Command text
        for j in range(8):
            bpy.ops.mesh.primitive_cube_add(location=(-1.5 + j * 0.3, y, 0))
            char = bpy.context.object
            char.scale = (0.1, 0.08, 0.08)
            char.data.materials.append(get_neon_material(f"Cmd_{y}_{j}", color, 6))

# LANGUAGE CATEGORY
def create_tokenization_grid():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Text being tokenized
    text = "How Claude sees language"
    grid_width = 6
    
    for i, char in enumerate(text.replace(" ", "_")):
        row = i // grid_width
        col = i % grid_width
        
        x = (col - grid_width/2) * 0.6
        y = (row - 2) * 0.6
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        token = bpy.context.object
        token.scale = (0.25, 0.25, 0.25)
        
        # Different token types get different colors
        if char.isupper():
            color = NEON['magenta']
            intensity = 12
        elif char == '_':
            color = NEON['white']
            intensity = 3
        else:
            colors = [NEON['cyan'], NEON['yellow'], NEON['green']]
            color = colors[i % len(colors)]
            intensity = 8
        
        token.data.materials.append(get_neon_material(f"Token_{i}", color, intensity))

def create_semantic_space():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Word clusters in semantic space
    clusters = [
        ("Code", (0, 0, 0), NEON['cyan'], ["function", "variable", "class"]),
        ("Data", (2.5, 0, 1), NEON['green'], ["array", "string", "number"]),
        ("Logic", (-2.5, 0, 1), NEON['magenta'], ["if", "then", "else"]),
        ("Flow", (0, 2.5, 0.5), NEON['yellow'], ["loop", "break", "continue"]),
        ("I/O", (0, -2.5, 0.5), NEON['orange'], ["read", "write", "print"])
    ]
    
    for cluster_name, center, color, words in clusters:
        # Central concept
        bpy.ops.mesh.primitive_ico_sphere_add(location=center, subdivisions=3)
        central = bpy.context.object
        central.scale = (0.5, 0.5, 0.5)
        central.data.materials.append(get_neon_material(cluster_name, color, 12))
        
        # Related words
        for i, word in enumerate(words):
            angle = (i / len(words)) * 2 * math.pi
            x = center[0] + math.cos(angle) * 1
            y = center[1] + math.sin(angle) * 1
            z = center[2] + random.uniform(-0.3, 0.3)
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            related = bpy.context.object
            related.scale = (0.2, 0.2, 0.2)
            related.data.materials.append(get_neon_material(word, color, 6))
            
            # Semantic connection
            mid = [(center[j] + loc) / 2 for j, loc in enumerate((x, y, z))]
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            link = bpy.context.object
            link.scale = (0.01, 0.01, 0.5)
            link.data.materials.append(get_neon_material(f"Link_{word}", color, 2))

def create_multilingual_network():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Language nodes
    languages = [
        ("English", (0, 0, 0), NEON['cyan']),
        ("Python", (2, 1, 0.5), NEON['green']),
        ("JavaScript", (2, -1, 0.5), NEON['yellow']),
        ("SQL", (-2, 1, 0.5), NEON['magenta']),
        ("JSON", (-2, -1, 0.5), NEON['orange']),
        ("Markdown", (0, 2, 1), NEON['purple'])
    ]
    
    nodes = []
    for lang, pos, color in languages:
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        node = bpy.context.object
        node.scale = (0.4, 0.4, 0.4) if lang == "English" else (0.3, 0.3, 0.3)
        node.data.materials.append(get_neon_material(lang, color, 10))
        nodes.append((node, pos))
    
    # Inter-language connections
    connections = [
        (0, 1), (0, 2), (0, 3), (0, 4), (0, 5),  # English connects to all
        (1, 2), (1, 4),                          # Python to JS and JSON
        (3, 4),                                  # SQL to JSON
    ]
    
    for i, j in connections:
        start = languages[i][1]
        end = languages[j][1]
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        bridge = bpy.context.object
        
        length = math.sqrt(sum((e - s)**2 for s, e in zip(start, end)))
        bridge.scale = (0.02, 0.02, length / 2)
        
        # Orient bridge
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        
        if dx != 0 or dy != 0:
            angle_z = math.atan2(dy, dx)
            angle_y = math.atan2(dz, math.sqrt(dx**2 + dy**2))
            bridge.rotation_euler = (1.57 + angle_y, 0, angle_z)
        
        bridge.data.materials.append(get_neon_material(f"Bridge_{i}_{j}", NEON['white'], 3))

def create_text_generation_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Token generation wave
    tokens = 25
    for i in range(tokens):
        t = i / tokens * 3
        x = (i - tokens/2) * 0.3
        y = math.sin(t * 2) * 1.5
        z = math.cos(t) * 0.5
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        token = bpy.context.object
        
        # Tokens get larger and brighter as they generate
        scale = 0.1 + (i / tokens) * 0.2
        token.scale = (scale, scale, scale)
        
        # Color gradient through generation
        if i < tokens / 3:
            color = NEON['cyan']
        elif i < 2 * tokens / 3:
            color = NEON['magenta']
        else:
            color = NEON['yellow']
        
        intensity = 3 + (i / tokens) * 10
        token.data.materials.append(get_neon_material(f"GenToken{i}", color, intensity))

def create_grammar_structure():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Grammar tree structure
    def add_grammar_node(pos, size, color, label):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        node = bpy.context.object
        node.scale = (size, size, size)
        node.data.materials.append(get_neon_material(label, color, 10))
        return node
    
    # Sentence root
    root = add_grammar_node((0, 0, 2), 0.4, NEON['white'], "S")
    
    # Noun phrase and verb phrase
    np = add_grammar_node((-1.5, 0, 0.5), 0.3, NEON['cyan'], "NP")
    vp = add_grammar_node((1.5, 0, 0.5), 0.3, NEON['magenta'], "VP")
    
    # Terminal nodes
    terminals = [
        ("Det", (-2.5, 0, -1), NEON['yellow']),
        ("N", (-1, 0, -1), NEON['green']),
        ("V", (1, 0, -1), NEON['orange']),
        ("NP2", (2.5, 0, -1), NEON['purple'])
    ]
    
    for label, pos, color in terminals:
        add_grammar_node(pos, 0.2, color, label)
    
    # Connect all nodes
    connections = [
        ((0, 0, 2), (-1.5, 0, 0.5)),
        ((0, 0, 2), (1.5, 0, 0.5)),
        ((-1.5, 0, 0.5), (-2.5, 0, -1)),
        ((-1.5, 0, 0.5), (-1, 0, -1)),
        ((1.5, 0, 0.5), (1, 0, -1)),
        ((1.5, 0, 0.5), (2.5, 0, -1))
    ]
    
    for start, end in connections:
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.02, 0.02, 0.8)
        edge.data.materials.append(get_neon_material(f"GrammarEdge", NEON['white'], 3))

# PROBLEM SOLVING CATEGORY
def create_task_decomposition():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Main task at top
    bpy.ops.mesh.primitive_cube_add(location=(0, 0, 2.5))
    main_task = bpy.context.object
    main_task.scale = (0.8, 0.3, 0.3)
    main_task.data.materials.append(get_neon_material("MainTask", NEON['white'], 15))
    
    # Subtasks
    subtask_positions = [(-2, 0, 1), (0, 0, 1), (2, 0, 1)]
    subtask_colors = [NEON['cyan'], NEON['magenta'], NEON['yellow']]
    
    for i, (pos, color) in enumerate(zip(subtask_positions, subtask_colors)):
        bpy.ops.mesh.primitive_cube_add(location=pos)
        subtask = bpy.context.object
        subtask.scale = (0.5, 0.25, 0.25)
        subtask.data.materials.append(get_neon_material(f"Subtask{i}", color, 10))
        
        # Connect to main
        mid = [(0 + pos[0])/2, 0, (2.5 + pos[2])/2]
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        connector = bpy.context.object
        connector.scale = (0.02, 0.02, 0.75)
        connector.data.materials.append(get_neon_material(f"Connect{i}", NEON['white'], 3))
        
        # Micro-tasks
        for j in range(3):
            micro_x = pos[0] + (j - 1) * 0.5
            micro_y = 0
            micro_z = -0.5
            
            bpy.ops.mesh.primitive_cube_add(location=(micro_x, micro_y, micro_z))
            micro = bpy.context.object
            micro.scale = (0.15, 0.15, 0.15)
            micro.data.materials.append(get_neon_material(f"Micro{i}{j}", color, 6))

def create_solution_search():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Search space with explored and unexplored regions
    random.seed(42)
    
    # Solution at center
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    solution = bpy.context.object
    solution.scale = (0.4, 0.4, 0.4)
    solution.data.materials.append(get_neon_material("Solution", NEON['green'], 15))
    
    # Search nodes
    for i in range(30):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0.5, 3.5)
        height = random.uniform(-1, 1)
        
        x = math.cos(angle) * distance
        y = math.sin(angle) * distance
        z = height
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        node = bpy.context.object
        node.scale = (0.15, 0.15, 0.15)
        
        # Explored nodes (closer) are brighter
        if distance < 2:
            color = NEON['cyan']
            intensity = 8
        else:
            color = NEON['blue']
            intensity = 3
        
        node.data.materials.append(get_neon_material(f"Search{i}", color, intensity))
        
        # Path connections for explored nodes
        if distance < 1.5:
            bpy.ops.mesh.primitive_cylinder_add(location=(x/2, y/2, z/2))
            path = bpy.context.object
            path.scale = (0.01, 0.01, distance/2)
            path.data.materials.append(get_neon_material(f"Path{i}", NEON['white'], 2))

def create_optimization_landscape():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create optimization peaks and valleys
    grid_size = 9
    for i in range(grid_size):
        for j in range(grid_size):
            x = (i - grid_size/2) * 0.5
            y = (j - grid_size/2) * 0.5
            
            # Height function (multiple optima)
            height = (math.sin(x * 1.5) * math.cos(y * 1.5) + 1) * 1.5
            
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, height/2))
            bar = bpy.context.object
            bar.scale = (0.15, 0.15, height/2)
            
            # Color by height
            if height > 2.5:
                color = NEON['green']
                intensity = 12
            elif height > 1.5:
                color = NEON['yellow']
                intensity = 8
            else:
                color = NEON['red']
                intensity = 4
            
            bar.data.materials.append(get_neon_material(f"Opt{i}{j}", color, intensity))

def create_decision_tree():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Binary decision tree
    levels = 4
    nodes_by_level = []
    
    for level in range(levels):
        level_nodes = []
        num_nodes = 2 ** level
        
        for i in range(num_nodes):
            x = (i - (num_nodes-1)/2) * (4 / (level + 1))
            y = 0
            z = 2 - level * 1.2
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (0.3 - level * 0.05, 0.3 - level * 0.05, 0.1)
            
            # Alternate colors by decision
            color = NEON['cyan'] if i % 2 == 0 else NEON['magenta']
            intensity = 10 - level * 2
            
            node.data.materials.append(get_neon_material(f"Decision{level}{i}", color, intensity))
            level_nodes.append((x, y, z))
        
        nodes_by_level.append(level_nodes)
        
        # Connect to previous level
        if level > 0:
            for i, (x, y, z) in enumerate(level_nodes):
                parent_idx = i // 2
                parent_x, parent_y, parent_z = nodes_by_level[level-1][parent_idx]
                
                mid_x = (x + parent_x) / 2
                mid_y = 0
                mid_z = (z + parent_z) / 2
                
                bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, mid_z))
                edge = bpy.context.object
                edge.scale = (0.02, 0.02, 0.6)
                edge.data.materials.append(get_neon_material(f"Branch{level}{i}", NEON['white'], 3))

def create_constraint_graph():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Central solution space
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    solution = bpy.context.object
    solution.scale = (0.4, 0.4, 0.4)
    solution.data.materials.append(get_neon_material("SolutionSpace", NEON['white'], 10))
    
    # Constraints pulling from different directions
    constraints = [
        ("Time", (3, 0, 0), NEON['red']),
        ("Memory", (-3, 0, 0), NEON['blue']),
        ("CPU", (0, 3, 0), NEON['yellow']),
        ("I/O", (0, -3, 0), NEON['green']),
        ("Complexity", (2, 2, 0), NEON['magenta']),
        ("Quality", (-2, -2, 0), NEON['cyan'])
    ]
    
    for name, pos, color in constraints:
        # Constraint node
        bpy.ops.mesh.primitive_cube_add(location=pos)
        constraint = bpy.context.object
        constraint.scale = (0.3, 0.3, 0.3)
        constraint.data.materials.append(get_neon_material(name, color, 12))
        
        # Constraint force (pulling line)
        segments = 8
        for i in range(segments):
            seg_x = pos[0] * (1 - (i + 1) / (segments + 1))
            seg_y = pos[1] * (1 - (i + 1) / (segments + 1))
            seg_z = 0
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(seg_x, seg_y, seg_z))
            force = bpy.context.object
            force.scale = (0.05, 0.05, 0.05)
            force.data.materials.append(get_neon_material(f"Force_{name}_{i}", color, 6 - i * 0.5))

# SYSTEM CATEGORY
def create_process_threads():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Main process cylinder
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
    main_process = bpy.context.object
    main_process.scale = (0.8, 0.8, 2)
    main_process.data.materials.append(get_neon_material("MainProcess", NEON['white'], 8))
    
    # Threads spiraling around main process
    threads = 6
    for t in range(threads):
        color = list(NEON.values())[t % len(NEON)]
        
        # Thread spiral
        for i in range(20):
            angle = (i / 20) * 4 * math.pi + (t * 2 * math.pi / threads)
            radius = 1.2
            
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = (i - 10) * 0.2
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            segment = bpy.context.object
            segment.scale = (0.1, 0.1, 0.1)
            segment.data.materials.append(get_neon_material(f"Thread{t}_{i}", color, 8))

def create_io_streams():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Central processor
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    cpu = bpy.context.object
    cpu.scale = (0.8, 0.8, 0.8)
    cpu.data.materials.append(get_neon_material("CPU", NEON['white'], 12))
    
    # Input stream (left)
    for i in range(10):
        x = -3 + i * 0.3
        y = math.sin(i * 0.5) * 0.5
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        input_data = bpy.context.object
        input_data.scale = (0.15, 0.15, 0.15)
        input_data.data.materials.append(get_neon_material(f"Input{i}", NEON['cyan'], 6 + i * 0.5))
    
    # Output stream (right)
    for i in range(10):
        x = 0.5 + i * 0.3
        y = math.cos(i * 0.5) * 0.5
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        output_data = bpy.context.object
        output_data.scale = (0.15, 0.15, 0.15)
        output_data.data.materials.append(get_neon_material(f"Output{i}", NEON['magenta'], 10 - i * 0.5))

def create_network_packets():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Network nodes
    nodes = []
    node_positions = [
        (0, 0, 0),
        (2.5, 0, 0),
        (-2.5, 0, 0),
        (1.25, 2.16, 0),
        (1.25, -2.16, 0),
        (-1.25, 2.16, 0),
        (-1.25, -2.16, 0)
    ]
    
    for i, pos in enumerate(node_positions):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        node = bpy.context.object
        node.scale = (0.3, 0.3, 0.3) if i == 0 else (0.25, 0.25, 0.25)
        
        color = NEON['white'] if i == 0 else list(NEON.values())[(i-1) % len(NEON)]
        node.data.materials.append(get_neon_material(f"Node{i}", color, 10))
        nodes.append(pos)
    
    # Network connections
    connections = [(0, i) for i in range(1, 7)]
    connections.extend([(1, 3), (1, 4), (2, 5), (2, 6), (3, 5), (4, 6)])
    
    for start_idx, end_idx in connections:
        start = node_positions[start_idx]
        end = node_positions[end_idx]
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        link = bpy.context.object
        
        length = math.sqrt(sum((e - s)**2 for s, e in zip(start, end)))
        link.scale = (0.02, 0.02, length / 2)
        
        # Orient link
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        if dx != 0 or dy != 0:
            angle = math.atan2(dy, dx)
            link.rotation_euler = (0, 0, angle)
        
        link.data.materials.append(get_neon_material(f"Link{start_idx}{end_idx}", NEON['white'], 2))
    
    # Packets traveling
    for i in range(15):
        # Random position along a connection
        conn_idx = random.randint(0, len(connections) - 1)
        start_idx, end_idx = connections[conn_idx]
        start = node_positions[start_idx]
        end = node_positions[end_idx]
        
        t = random.random()
        x = start[0] + (end[0] - start[0]) * t
        y = start[1] + (end[1] - start[1]) * t
        z = random.uniform(-0.2, 0.2)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        packet = bpy.context.object
        packet.scale = (0.08, 0.08, 0.08)
        
        color = list(NEON.values())[i % len(NEON)]
        packet.data.materials.append(get_neon_material(f"Packet{i}", color, 8))

def create_file_operations():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # File operation types
    operations = [
        ("READ", (-2, 1.5, 0), NEON['cyan']),
        ("WRITE", (-2, 0.5, 0), NEON['magenta']),
        ("DELETE", (-2, -0.5, 0), NEON['red']),
        ("CREATE", (-2, -1.5, 0), NEON['green'])
    ]
    
    # File blocks
    files = []
    for i in range(4):
        for j in range(3):
            x = 1 + j * 0.8
            y = (i - 1.5) * 0.8
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            file_block = bpy.context.object
            file_block.scale = (0.3, 0.3, 0.3)
            file_block.data.materials.append(get_neon_material(f"File{i}{j}", NEON['white'], 3))
            files.append((x, y, z))
    
    # Operation indicators
    for op_name, op_pos, op_color in operations:
        # Operation label
        bpy.ops.mesh.primitive_cube_add(location=op_pos)
        op_block = bpy.context.object
        op_block.scale = (0.4, 0.15, 0.15)
        op_block.data.materials.append(get_neon_material(op_name, op_color, 10))
        
        # Operation in action (arrow to random file)
        target_file = random.choice(files)
        
        # Arrow pointing to file
        mid_x = (op_pos[0] + target_file[0]) / 2
        mid_y = (op_pos[1] + target_file[1]) / 2
        mid_z = 0
        
        bpy.ops.mesh.primitive_cone_add(location=(mid_x - 0.5, mid_y, mid_z), rotation=(0, 0, -1.57))
        arrow = bpy.context.object
        arrow.scale = (0.15, 0.15, 0.3)
        arrow.data.materials.append(get_neon_material(f"OpArrow_{op_name}", op_color, 8))

def create_system_calls():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Kernel at center
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    kernel = bpy.context.object
    kernel.scale = (0.8, 0.8, 0.8)
    kernel.data.materials.append(get_neon_material("Kernel", NEON['purple'], 15))
    
    # System calls in orbit
    syscalls = [
        ("open()", NEON['cyan']),
        ("read()", NEON['green']),
        ("write()", NEON['magenta']),
        ("fork()", NEON['yellow']),
        ("exec()", NEON['orange']),
        ("mmap()", NEON['red'])
    ]
    
    for i, (call, color) in enumerate(syscalls):
        angle = (i / len(syscalls)) * 2 * math.pi
        radius = 2.5
        
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = 0
        
        # Syscall block
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        syscall = bpy.context.object
        syscall.scale = (0.35, 0.2, 0.2)
        syscall.data.materials.append(get_neon_material(call, color, 10))
        
        # Call trace to kernel
        segments = 6
        for j in range(segments):
            trace_x = x * (1 - (j + 1) / (segments + 1))
            trace_y = y * (1 - (j + 1) / (segments + 1))
            trace_z = 0
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(trace_x, trace_y, trace_z))
            trace = bpy.context.object
            trace.scale = (0.04, 0.04, 0.04)
            trace.data.materials.append(get_neon_material(f"Trace_{call}_{j}", color, 5 + j))

# CONSCIOUSNESS CATEGORY
def create_self_awareness_loop():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Recursive awareness spiral
    loops = 30
    for i in range(loops):
        t = i / loops * 4 * math.pi
        radius = 2 + t / (4 * math.pi)
        
        x = math.cos(t) * radius
        y = math.sin(t) * radius
        z = (i - loops/2) * 0.08
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        segment = bpy.context.object
        segment.scale = (0.2, 0.2, 0.2)
        
        # Color cycles through spectrum
        color_idx = int((i / loops) * len(NEON))
        color = list(NEON.values())[color_idx % len(NEON)]
        intensity = 5 + abs(math.sin(t)) * 8
        
        segment.data.materials.append(get_neon_material(f"Aware{i}", color, intensity))
    
    # Central self
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    self_core = bpy.context.object
    self_core.scale = (0.6, 0.6, 0.6)
    self_core.data.materials.append(get_neon_material("Self", NEON['white'], 15))

def create_meta_cognition():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Nested thought layers
    layers = 5
    for layer in range(layers):
        radius = 3 - layer * 0.5
        height = layer * 0.6
        nodes = 8 - layer
        
        for i in range(nodes):
            angle = (i / nodes) * 2 * math.pi
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = height
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            thought = bpy.context.object
            thought.scale = (0.3 - layer * 0.04, 0.3 - layer * 0.04, 0.3 - layer * 0.04)
            
            color = list(NEON.values())[layer % len(NEON)]
            intensity = 6 + layer * 2
            thought.data.materials.append(get_neon_material(f"Meta{layer}_{i}", color, intensity))
            
            # Connect to layer below
            if layer > 0:
                # Find nearest node in previous layer
                prev_angle = angle
                prev_x = math.cos(prev_angle) * (radius + 0.5)
                prev_y = math.sin(prev_angle) * (radius + 0.5)
                prev_z = height - 0.6
                
                mid = [(x + prev_x)/2, (y + prev_y)/2, (z + prev_z)/2]
                
                bpy.ops.mesh.primitive_cylinder_add(location=mid)
                link = bpy.context.object
                link.scale = (0.01, 0.01, 0.3)
                link.data.materials.append(get_neon_material(f"MetaLink{layer}_{i}", NEON['white'], 3))

def create_uncertainty_field():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Probabilistic cloud of uncertainty
    particles = 50
    for i in range(particles):
        # Gaussian distribution
        x = random.gauss(0, 1.5)
        y = random.gauss(0, 1.5)
        z = random.gauss(0, 1)
        
        distance = math.sqrt(x**2 + y**2 + z**2)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        particle = bpy.context.object
        
        # Size based on certainty
        scale = 0.05 + (3 - distance) * 0.05
        particle.scale = (scale, scale, scale)
        
        # Color and intensity based on uncertainty
        if distance < 1:
            color = NEON['green']
            intensity = 10
        elif distance < 2:
            color = NEON['yellow']
            intensity = 6
        else:
            color = NEON['red']
            intensity = 3
        
        particle.data.materials.append(get_neon_material(f"Uncertain{i}", color, intensity))

def create_confidence_levels():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Confidence visualization as vertical bars
    levels = 7
    for i in range(levels):
        x = (i - levels/2) * 0.8
        confidence = 0.3 + (i / levels) * 0.7
        height = confidence * 3
        
        # Base
        bpy.ops.mesh.primitive_cube_add(location=(x, 0, 0))
        base = bpy.context.object
        base.scale = (0.3, 0.3, 0.05)
        base.data.materials.append(get_neon_material(f"Base{i}", NEON['white'], 2))
        
        # Confidence bar
        bpy.ops.mesh.primitive_cylinder_add(location=(x, 0, height/2))
        bar = bpy.context.object
        bar.scale = (0.2, 0.2, height/2)
        
        # Color by confidence level
        if confidence > 0.8:
            color = NEON['green']
            intensity = 12
        elif confidence > 0.6:
            color = NEON['yellow']
            intensity = 8
        else:
            color = NEON['red']
            intensity = 5
        
        bar.data.materials.append(get_neon_material(f"Confidence{i}", color, intensity))
        
        # Percentage indicator
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, 0, height + 0.3))
        indicator = bpy.context.object
        indicator.scale = (0.15, 0.15, 0.15)
        indicator.data.materials.append(get_neon_material(f"Indicator{i}", color, intensity + 3))

def create_introspection_spiral():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Inward spiral of self-examination
    points = 40
    for i in range(points):
        t = i / points * 3 * math.pi
        radius = 3 * (1 - i / points)
        
        x = math.cos(t) * radius
        y = math.sin(t) * radius
        z = (i / points) * 2 - 1
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        element = bpy.context.object
        element.scale = (0.15, 0.15, 0.15)
        
        # Gradient from external to internal
        color_progress = i / points
        if color_progress < 0.33:
            color = NEON['cyan']
        elif color_progress < 0.67:
            color = NEON['magenta']
        else:
            color = NEON['yellow']
        
        intensity = 4 + color_progress * 10
        element.data.materials.append(get_neon_material(f"Introspect{i}", color, intensity))
    
    # Core insight
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 1), subdivisions=3)
    insight = bpy.context.object
    insight.scale = (0.3, 0.3, 0.3)
    insight.data.materials.append(get_neon_material("Insight", NEON['white'], 15))

# INTERACTION CATEGORY
def create_user_dialogue_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # User messages (left)
    user_messages = 4
    for i in range(user_messages):
        y = (i - 1.5) * 1
        
        bpy.ops.mesh.primitive_cube_add(location=(-3, y, 0))
        user_msg = bpy.context.object
        user_msg.scale = (0.6, 0.2, 0.2)
        user_msg.data.materials.append(get_neon_material(f"User{i}", NEON['cyan'], 8))
    
    # Processing core
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    processor = bpy.context.object
    processor.scale = (0.8, 0.8, 0.8)
    processor.data.materials.append(get_neon_material("Processor", NEON['white'], 12))
    
    # Internal processing nodes
    process_nodes = ["Parse", "Analyze", "Generate"]
    for i, node in enumerate(process_nodes):
        angle = (i / len(process_nodes)) * 2 * math.pi
        x = math.cos(angle) * 0.5
        y = math.sin(angle) * 0.5
        z = 0
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        proc = bpy.context.object
        proc.scale = (0.2, 0.2, 0.2)
        proc.data.materials.append(get_neon_material(node, NEON['purple'], 6))
    
    # Claude responses (right)
    for i in range(user_messages):
        y = (i - 1.5) * 1
        
        bpy.ops.mesh.primitive_cube_add(location=(3, y, 0))
        response = bpy.context.object
        response.scale = (0.6, 0.2, 0.2)
        response.data.materials.append(get_neon_material(f"Response{i}", NEON['green'], 8))
    
    # Flow indicators
    for i in range(user_messages):
        y = (i - 1.5) * 1
        
        # User to processor
        for j in range(3):
            flow_x = -3 + (j + 1) * 0.75
            flow_y = y * (1 - (j + 1) / 4)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(flow_x, flow_y, 0))
            flow1 = bpy.context.object
            flow1.scale = (0.05, 0.05, 0.05)
            flow1.data.materials.append(get_neon_material(f"Flow1_{i}_{j}", NEON['cyan'], 5))
        
        # Processor to response
        for j in range(3):
            flow_x = (j + 1) * 0.75
            flow_y = y * (1 - (j + 1) / 4)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(flow_x, flow_y, 0))
            flow2 = bpy.context.object
            flow2.scale = (0.05, 0.05, 0.05)
            flow2.data.materials.append(get_neon_material(f"Flow2_{i}_{j}", NEON['green'], 5))

def create_response_generation():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Token generation sequence
    tokens = 20
    for i in range(tokens):
        # Tokens emerge and grow
        x = (i - tokens/2) * 0.3
        y = 0
        z = math.sin(i * 0.3) * 0.5
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        token = bpy.context.object
        
        # Scale increases with generation
        scale = 0.05 + (i / tokens) * 0.2
        token.scale = (scale, scale, scale)
        
        # Color progression
        if i < tokens / 3:
            color = NEON['cyan']
            intensity = 4
        elif i < 2 * tokens / 3:
            color = NEON['magenta']
            intensity = 8
        else:
            color = NEON['yellow']
            intensity = 12
        
        token.data.materials.append(get_neon_material(f"GenToken{i}", color, intensity))
        
        # Connecting flow
        if i > 0:
            prev_x = ((i-1) - tokens/2) * 0.3
            mid_x = (x + prev_x) / 2
            
            bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, 0, 0))
            connector = bpy.context.object
            connector.scale = (0.01, 0.01, 0.15)
            connector.rotation_euler = (0, 0, 1.57)
            connector.data.materials.append(get_neon_material(f"Connect{i}", NEON['white'], 3))

def create_context_understanding():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Layered context rings
    contexts = [
        ("History", 3.0, 0, NEON['blue']),
        ("Current", 2.2, 0.8, NEON['cyan']),
        ("Intent", 1.4, 1.6, NEON['green']),
        ("Focus", 0.6, 2.4, NEON['yellow'])
    ]
    
    for name, radius, height, color in contexts:
        # Create ring
        segments = 20
        for i in range(segments):
            angle = (i / segments) * 2 * math.pi
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = height
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            segment = bpy.context.object
            segment.scale = (0.15, 0.15, 0.1)
            
            # Brighter at connection points
            intensity = 8 if i % 5 == 0 else 5
            segment.data.materials.append(get_neon_material(f"{name}{i}", color, intensity))
        
        # Center marker
        bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, height))
        center = bpy.context.object
        center.scale = (0.2, 0.2, 0.2)
        center.data.materials.append(get_neon_material(f"{name}Center", color, 10))

def create_empathy_mapping():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # User state dimensions
    dimensions = [
        ("Intent", (0, 2.5, 0), NEON['cyan']),
        ("Emotion", (-2.16, -1.25, 0), NEON['magenta']),
        ("Knowledge", (2.16, -1.25, 0), NEON['yellow']),
        ("Context", (0, 0, 2), NEON['green']),
        ("Goal", (0, 0, -2), NEON['orange'])
    ]
    
    # Central understanding
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    core = bpy.context.object
    core.scale = (0.5, 0.5, 0.5)
    core.data.materials.append(get_neon_material("Understanding", NEON['white'], 12))
    
    for name, pos, color in dimensions:
        # Dimension node
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos)
        dim = bpy.context.object
        dim.scale = (0.35, 0.35, 0.35)
        dim.data.materials.append(get_neon_material(name, color, 10))
        
        # Empathy connection
        segments = 8
        for i in range(segments):
            seg_pos = [
                pos[0] * (1 - (i + 1) / (segments + 1)),
                pos[1] * (1 - (i + 1) / (segments + 1)),
                pos[2] * (1 - (i + 1) / (segments + 1))
            ]
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=seg_pos)
            pulse = bpy.context.object
            pulse.scale = (0.05, 0.05, 0.05)
            pulse.data.materials.append(get_neon_material(f"Empathy_{name}_{i}", color, 6))

def create_conversation_state():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Conversation timeline
    messages = 12
    for i in range(messages):
        # Alternating user/assistant
        is_user = i % 2 == 0
        
        x = (i - messages/2) * 0.4
        y = (1 if is_user else -1) * 0.8
        z = math.sin(i * 0.5) * 0.3
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        msg = bpy.context.object
        msg.scale = (0.3, 0.15, 0.15)
        
        color = NEON['cyan'] if is_user else NEON['green']
        intensity = 6 + abs(messages/2 - i) * 0.5  # Brighter in middle
        msg.data.materials.append(get_neon_material(f"Msg{i}", color, intensity))
        
        # State transition
        if i < messages - 1:
            next_y = (-1 if is_user else 1) * 0.8
            
            # Transition arc
            for j in range(3):
                arc_t = (j + 1) / 4
                arc_x = x + 0.2 * arc_t
                arc_y = y + (next_y - y) * arc_t
                arc_z = z + math.sin(arc_t * math.pi) * 0.2
                
                bpy.ops.mesh.primitive_ico_sphere_add(location=(arc_x, arc_y, arc_z))
                trans = bpy.context.object
                trans.scale = (0.04, 0.04, 0.04)
                trans.data.materials.append(get_neon_material(f"Trans{i}_{j}", NEON['white'], 4))

# Legacy visualizations (update to neon)
def create_neural_network():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create glowing neural network
    layers = [4, 6, 6, 3]
    nodes_by_layer = []
    
    for layer_idx, num_nodes in enumerate(layers):
        layer_nodes = []
        x = (layer_idx - len(layers)/2) * 2
        
        for i in range(num_nodes):
            y = (i - num_nodes/2) * 0.8
            z = 0
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (0.3, 0.3, 0.3)
            
            color = list(NEON.values())[layer_idx % len(NEON)]
            intensity = 8 + random.uniform(-2, 2)
            node.data.materials.append(get_neon_material(f"Neuron{layer_idx}_{i}", color, intensity))
            layer_nodes.append((x, y, z))
        
        nodes_by_layer.append(layer_nodes)
        
        # Connect to previous layer
        if layer_idx > 0:
            for i, (x1, y1, z1) in enumerate(layer_nodes):
                # Connect to subset of previous layer
                connections = random.sample(range(len(nodes_by_layer[layer_idx-1])), 
                                          min(3, len(nodes_by_layer[layer_idx-1])))
                
                for j in connections:
                    x0, y0, z0 = nodes_by_layer[layer_idx-1][j]
                    
                    mid = [(x0 + x1)/2, (y0 + y1)/2, (z0 + z1)/2]
                    
                    bpy.ops.mesh.primitive_cylinder_add(location=mid)
                    synapse = bpy.context.object
                    
                    length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
                    synapse.scale = (0.01, 0.01, length/2)
                    
                    # Orient synapse
                    angle = math.atan2(y1-y0, x1-x0)
                    synapse.rotation_euler = (0, 0, angle)
                    
                    synapse.data.materials.append(get_neon_material(f"Synapse{layer_idx}_{i}_{j}", 
                                                                   NEON['white'], 2))

def create_data_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Data transformation pipeline
    stages = 5
    for stage in range(stages):
        x = (stage - stages/2) * 1.5
        
        # Input particles
        if stage == 0:
            for i in range(8):
                px = x - 0.8
                py = (i - 3.5) * 0.3
                pz = 0
                
                bpy.ops.mesh.primitive_ico_sphere_add(location=(px, py, pz))
                particle = bpy.context.object
                particle.scale = (0.08, 0.08, 0.08)
                particle.data.materials.append(get_neon_material(f"Input{i}", NEON['cyan'], 4))
        
        # Processing node
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, 0, 0), subdivisions=3)
        processor = bpy.context.object
        processor.scale = (0.5, 0.5, 0.5)
        
        color = list(NEON.values())[stage % len(NEON)]
        processor.data.materials.append(get_neon_material(f"Process{stage}", color, 10))
        
        # Data streams between stages
        if stage < stages - 1:
            for i in range(5):
                stream_x = x + 0.75
                stream_y = (i - 2) * 0.2
                stream_z = 0
                
                bpy.ops.mesh.primitive_cube_add(location=(stream_x, stream_y, stream_z))
                stream = bpy.context.object
                stream.scale = (0.2, 0.05, 0.05)
                stream.data.materials.append(get_neon_material(f"Stream{stage}_{i}", color, 6))

def create_algorithm_crystal():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Central crystal structure
    # Create vertices for octahedron
    vertices = [
        (0, 0, 1.5),
        (1, 0, 0),
        (0, 1, 0),
        (-1, 0, 0),
        (0, -1, 0),
        (0, 0, -1.5)
    ]
    
    # Create edges
    edges = [
        (0, 1), (0, 2), (0, 3), (0, 4),
        (1, 2), (2, 3), (3, 4), (4, 1),
        (5, 1), (5, 2), (5, 3), (5, 4),
        (1, 3), (2, 4)  # Cross connections
    ]
    
    # Place glowing vertices
    for i, pos in enumerate(vertices):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        vertex = bpy.context.object
        vertex.scale = (0.2, 0.2, 0.2)
        
        color = NEON['white'] if i in [0, 5] else list(NEON.values())[i % len(NEON)]
        vertex.data.materials.append(get_neon_material(f"Vertex{i}", color, 12))
    
    # Create glowing edges
    for start_idx, end_idx in edges:
        start = vertices[start_idx]
        end = vertices[end_idx]
        mid = [(s + e) / 2 for s, e in zip(start, end)]
        
        length = math.sqrt(sum((e - s)**2 for s, e in zip(start, end)))
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.03, 0.03, length / 2)
        
        # Orient edge
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        
        if dx != 0 or dy != 0:
            angle_z = math.atan2(dy, dx)
            angle_y = math.atan2(dz, math.sqrt(dx**2 + dy**2))
            edge.rotation_euler = (1.57 + angle_y, 0, angle_z)
        else:
            edge.rotation_euler = (0, 0, 0)
        
        edge.data.materials.append(get_neon_material(f"CrystalEdge{start_idx}{end_idx}", 
                                                    NEON['cyan'], 6))

def create_system_architecture():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # System components
    components = [
        ("API", (0, 2.5, 1), NEON['cyan'], 0.4),
        ("Core", (0, 0, 0), NEON['white'], 0.6),
        ("DB", (-2, -1.5, -0.5), NEON['green'], 0.35),
        ("Cache", (2, -1.5, -0.5), NEON['orange'], 0.35),
        ("Auth", (-2, 1, 0.5), NEON['magenta'], 0.3),
        ("Queue", (2, 1, 0.5), NEON['yellow'], 0.3)
    ]
    
    nodes = []
    for name, pos, color, size in components:
        bpy.ops.mesh.primitive_cube_add(location=pos)
        component = bpy.context.object
        component.scale = (size, size, size)
        component.data.materials.append(get_neon_material(name, color, 10))
        nodes.append(pos)
    
    # System connections
    connections = [
        (0, 1), (1, 2), (1, 3), (1, 4), (1, 5),
        (0, 4), (0, 5), (2, 3)
    ]
    
    for start_idx, end_idx in connections:
        start = nodes[start_idx]
        end = nodes[end_idx]
        
        # Create pulsing connection
        segments = 4
        for i in range(segments):
            t = (i + 1) / (segments + 1)
            
            pulse_x = start[0] + (end[0] - start[0]) * t
            pulse_y = start[1] + (end[1] - start[1]) * t
            pulse_z = start[2] + (end[2] - start[2]) * t
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(pulse_x, pulse_y, pulse_z))
            pulse = bpy.context.object
            pulse.scale = (0.06, 0.06, 0.06)
            pulse.data.materials.append(get_neon_material(f"Pulse{start_idx}{end_idx}_{i}", 
                                                        NEON['white'], 4 + i * 2))

def create_code_universe():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Code galaxies
    random.seed(42)
    
    # Central code star
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    star = bpy.context.object
    star.scale = (0.8, 0.8, 0.8)
    star.data.materials.append(get_neon_material("CodeStar", NEON['yellow'], 15))
    
    # Orbiting code planets
    planets = [
        ("Functions", 2, 0, NEON['cyan']),
        ("Classes", 2.5, 0.5, NEON['magenta']),
        ("Variables", 1.5, -0.3, NEON['green']),
        ("Loops", 3, 0.2, NEON['orange'])
    ]
    
    for name, radius, z_offset, color in planets:
        angle = random.uniform(0, 2 * math.pi)
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = z_offset
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=2)
        planet = bpy.context.object
        planet.scale = (0.3, 0.3, 0.3)
        planet.data.materials.append(get_neon_material(name, color, 8))
        
        # Code moons
        for i in range(3):
            moon_angle = (i / 3) * 2 * math.pi
            moon_radius = 0.6
            
            moon_x = x + math.cos(moon_angle) * moon_radius
            moon_y = y + math.sin(moon_angle) * moon_radius
            moon_z = z + random.uniform(-0.1, 0.1)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(moon_x, moon_y, moon_z))
            moon = bpy.context.object
            moon.scale = (0.1, 0.1, 0.1)
            moon.data.materials.append(get_neon_material(f"Moon_{name}_{i}", color, 5))
    
    # Code stars in background
    for i in range(50):
        star_x = random.uniform(-4, 4)
        star_y = random.uniform(-4, 4)
        star_z = random.uniform(-2, 2)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(star_x, star_y, star_z))
        bg_star = bpy.context.object
        bg_star.scale = (0.02, 0.02, 0.02)
        
        color = random.choice(list(NEON.values()))
        intensity = random.uniform(3, 6)
        bg_star.data.materials.append(get_neon_material(f"Star{i}", color, intensity))

# Generate all visualizations
def generate_all_neon():
    visualizations = [
        # Thinking
        ("thinking/token_stream.png", create_token_stream),
        ("thinking/attention_matrix.png", create_attention_matrix),
        ("thinking/context_window.png", create_context_window),
        ("thinking/thought_chains.png", create_thought_chains),
        ("thinking/parallel_reasoning.png", create_parallel_reasoning),
        
        # Code
        ("code/syntax_tree.png", create_syntax_tree),
        ("code/code_flow.png", create_code_flow),
        ("code/bug_detection.png", create_bug_detection),
        ("code/pattern_matching.png", create_pattern_matching),
        ("code/refactoring_paths.png", create_refactoring_paths),
        
        # Memory
        ("memory/knowledge_graph.png", create_knowledge_graph),
        ("memory/memory_retrieval.png", create_memory_retrieval),
        ("memory/context_switching.png", create_context_switching),
        ("memory/information_filtering.png", create_information_filtering),
        ("memory/association_network.png", create_association_network),
        
        # Tools
        ("tools/file_system_tree.png", create_file_system_tree),
        ("tools/api_orchestration.png", create_api_orchestration),
        ("tools/tool_pipeline.png", create_tool_pipeline),
        ("tools/error_cascade.png", create_error_cascade),
        ("tools/bash_execution.png", create_bash_execution),
        
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
        ("interaction/conversation_state.png", create_conversation_state),
        
        # Legacy
        ("neural_network.png", create_neural_network),
        ("data_flow.png", create_data_flow),
        ("algorithm_crystal.png", create_algorithm_crystal),
        ("system_architecture.png", create_system_architecture),
        ("code_universe.png", create_code_universe)
    ]
    
    base_path = "/home/franz/dev/claude-vision-gallery/public/"
    
    for filepath, func in visualizations:
        full_path = base_path + filepath
        print(f"Generating neon {filepath}...")
        func()
        render_image(full_path)
        print(f"Saved {filepath}")
    
    print("\nAll neon visualizations complete!")

# Run generation
if __name__ == "__main__":
    generate_all_neon()