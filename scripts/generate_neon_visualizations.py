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
bpy.context.scene.eevee.bloom_intensity = 0.5
bpy.context.scene.eevee.bloom_radius = 6.5
bpy.context.scene.eevee.use_bloom = True

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
def setup_dark_world():
    """Dark background for neon effect"""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)  # Pure black
    bg.inputs[1].default_value = 1.0

def add_centered_camera():
    """Camera focused on center"""
    bpy.ops.object.camera_add(location=(0, -10, 0))
    camera = bpy.context.object
    camera.rotation_euler = (1.57, 0, 0)  # Look straight at origin
    bpy.context.scene.camera = camera
    
    # Adjust camera settings for centered view
    camera.data.lens = 50

def get_neon_material(name, color, intensity=5):
    """Create glowing neon material"""
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    
    # Clear default nodes
    nodes = mat.node_tree.nodes
    nodes.clear()
    
    # Add emission shader
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs[0].default_value = (*color, 1.0)  # Color
    emission.inputs[1].default_value = intensity  # Strength
    
    # Add output
    output = nodes.new('ShaderNodeOutputMaterial')
    
    # Connect
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    
    return mat

def render_image(filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    bpy.context.scene.render.filepath = filepath
    bpy.ops.render.render(write_still=True)

# Neon color palette
NEON_COLORS = [
    (0, 1, 1),      # Cyan
    (1, 0, 1),      # Magenta
    (0, 1, 0),      # Green
    (1, 1, 0),      # Yellow
    (0, 0.5, 1),    # Blue
    (1, 0.5, 0),    # Orange
    (0.5, 0, 1),    # Purple
    (1, 0, 0.5),    # Pink
]

# THINKING VISUALIZATIONS
def create_neon_token_stream():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create flowing tokens in center
    for i in range(20):
        x = (i - 10) * 0.4
        y = math.sin(i * 0.5) * 2
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        cube = bpy.context.object
        cube.scale = (0.3, 0.3, 0.3)
        
        # Gradient color along stream
        color = NEON_COLORS[i % len(NEON_COLORS)]
        cube.data.materials.append(get_neon_material(f"Token{i}", color))

def create_neon_attention_matrix():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create grid of attention connections
    size = 8
    for i in range(size):
        for j in range(size):
            if random.random() > 0.3:  # Sparse matrix
                x = (i - size/2) * 0.8
                y = (j - size/2) * 0.8
                z = 0
                
                # Connection strength varies
                scale = random.uniform(0.1, 0.3)
                bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
                sphere = bpy.context.object
                sphere.scale = (scale, scale, scale)
                
                # Color based on attention weight
                intensity = 3 + random.uniform(0, 5)
                color = NEON_COLORS[(i + j) % len(NEON_COLORS)]
                sphere.data.materials.append(get_neon_material(f"Att_{i}_{j}", color, intensity))

def create_neon_context_window():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Layered context frames
    for layer in range(5):
        size = 4 - layer * 0.7
        
        # Create frame
        for i in range(4):
            if i == 0:  # Top
                loc = (0, size, 0)
                scale = (size*2, 0.1, 0.1)
            elif i == 1:  # Bottom
                loc = (0, -size, 0)
                scale = (size*2, 0.1, 0.1)
            elif i == 2:  # Left
                loc = (-size, 0, 0)
                scale = (0.1, size*2, 0.1)
            else:  # Right
                loc = (size, 0, 0)
                scale = (0.1, size*2, 0.1)
            
            bpy.ops.mesh.primitive_cube_add(location=loc)
            edge = bpy.context.object
            edge.scale = scale
            
            color = NEON_COLORS[layer % len(NEON_COLORS)]
            edge.data.materials.append(get_neon_material(f"Frame{layer}_{i}", color))

def create_neon_thought_chains():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create interconnected thought nodes
    nodes = []
    num_nodes = 10
    
    for i in range(num_nodes):
        angle = (i / num_nodes) * 2 * math.pi
        radius = 3
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = 0
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        node = bpy.context.object
        node.scale = (0.4, 0.4, 0.4)
        
        color = NEON_COLORS[i % len(NEON_COLORS)]
        node.data.materials.append(get_neon_material(f"Thought{i}", color))
        nodes.append(node)
    
    # Connect with glowing paths
    for i in range(num_nodes):
        next_i = (i + 1) % num_nodes
        
        # Create connection cylinder
        start = nodes[i].location
        end = nodes[next_i].location
        mid = [(start[j] + end[j]) / 2 for j in range(3)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        connection = bpy.context.object
        
        # Orient cylinder
        direction = [end[j] - start[j] for j in range(3)]
        length = math.sqrt(sum(d**2 for d in direction))
        connection.scale = (0.05, 0.05, length / 2)
        
        # Point from start to end
        angle = math.atan2(direction[1], direction[0])
        connection.rotation_euler = (0, 0, angle)
        
        connection.data.materials.append(get_neon_material(f"Chain{i}", (1, 1, 1), 3))

def create_neon_parallel_reasoning():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Multiple parallel processing streams
    streams = 5
    for stream in range(streams):
        y_offset = (stream - streams/2) * 1.5
        
        for i in range(8):
            x = (i - 4) * 0.8
            y = y_offset
            z = math.sin(i * 0.8 + stream) * 0.5
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            cube = bpy.context.object
            cube.scale = (0.3, 0.2, 0.2)
            
            color = NEON_COLORS[stream % len(NEON_COLORS)]
            intensity = 3 + abs(4 - i)  # Brighter in center
            cube.data.materials.append(get_neon_material(f"Stream{stream}_{i}", color, intensity))

# CODE VISUALIZATIONS
def create_neon_syntax_tree():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    def add_node(pos, size, color, intensity=5):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        node = bpy.context.object
        node.scale = (size, size, size)
        node.data.materials.append(get_neon_material(f"Node_{pos}", color, intensity))
        return node
    
    # Root node
    root = add_node((0, 0, 3), 0.5, NEON_COLORS[0], 8)
    
    # Branches
    branch_positions = [(-2, 0, 1.5), (0, 0, 1.5), (2, 0, 1.5)]
    for i, pos in enumerate(branch_positions):
        node = add_node(pos, 0.4, NEON_COLORS[i + 1], 6)
        
        # Connect to root
        mid = [(0 + pos[0])/2, 0, (3 + pos[2])/2]
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.03, 0.03, 0.8)
        edge.rotation_euler = (0.5 if i != 1 else 0, 0, -0.5 if i == 0 else 0.5 if i == 2 else 0)
        edge.data.materials.append(get_neon_material(f"Edge{i}", (1, 1, 1), 2))

def create_neon_code_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create flowing code visualization
    for i in range(15):
        t = i / 15 * 4 * math.pi
        x = math.sin(t) * 3
        y = math.cos(t) * 3
        z = (i - 7.5) * 0.3
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        flow = bpy.context.object
        flow.scale = (0.3, 0.3, 0.3)
        
        # Color changes through flow
        color = NEON_COLORS[i % len(NEON_COLORS)]
        intensity = 3 + (i / 15) * 5
        flow.data.materials.append(get_neon_material(f"Flow{i}", color, intensity))

def create_neon_bug_detection():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Normal code blocks
    for i in range(5):
        for j in range(5):
            x = (i - 2) * 1.2
            y = (j - 2) * 1.2
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            block = bpy.context.object
            block.scale = (0.4, 0.4, 0.4)
            
            # Bug locations glow red
            if (i == 1 and j == 3) or (i == 3 and j == 1):
                color = (1, 0, 0)
                intensity = 10
            else:
                color = (0, 1, 0)
                intensity = 2
            
            block.data.materials.append(get_neon_material(f"Code{i}_{j}", color, intensity))

def create_neon_pattern_matching():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create pattern groups
    patterns = [
        [(0, 0), (1, 0), (0, 1)],  # L shape
        [(0, 0), (1, 0), (2, 0)],  # Line
        [(0, 0), (1, 0), (1, 1)],  # Corner
    ]
    
    for p, pattern in enumerate(patterns):
        base_x = (p - 1) * 3
        base_y = 0
        
        for x, y in pattern:
            bpy.ops.mesh.primitive_cube_add(location=(base_x + x * 0.6, base_y + y * 0.6, 0))
            cube = bpy.context.object
            cube.scale = (0.25, 0.25, 0.25)
            
            color = NEON_COLORS[p * 2]
            cube.data.materials.append(get_neon_material(f"Pattern{p}_{x}_{y}", color, 6))

def create_neon_refactoring_paths():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Before state (messy)
    for i in range(8):
        x = random.uniform(-3, -1)
        y = random.uniform(-2, 2)
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        before = bpy.context.object
        before.scale = (0.3, 0.3, 0.3)
        before.data.materials.append(get_neon_material(f"Before{i}", (1, 0.5, 0), 3))
    
    # After state (organized)
    for i in range(2):
        for j in range(4):
            x = 2 + i * 0.8
            y = (j - 1.5) * 0.8
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            after = bpy.context.object
            after.scale = (0.3, 0.3, 0.3)
            after.data.materials.append(get_neon_material(f"After{i}_{j}", (0, 1, 0.5), 6))
    
    # Refactoring arrow
    bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0), rotation=(0, 0, -1.57))
    arrow = bpy.context.object
    arrow.scale = (0.5, 0.5, 1)
    arrow.data.materials.append(get_neon_material("Arrow", (1, 1, 1), 8))

# Continue with all other categories...
# I'll implement a few more key ones and then create a batch script

# MEMORY VISUALIZATIONS
def create_neon_knowledge_graph():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create interconnected knowledge nodes
    nodes = []
    positions = [
        (0, 0, 0),      # Central concept
        (2, 0, 0),      # Right
        (-2, 0, 0),     # Left
        (0, 2, 0),      # Top
        (0, -2, 0),     # Bottom
        (1.4, 1.4, 0),  # Diagonals
        (-1.4, 1.4, 0),
        (1.4, -1.4, 0),
        (-1.4, -1.4, 0)
    ]
    
    # Create nodes
    for i, pos in enumerate(positions):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=2)
        node = bpy.context.object
        
        # Central node is larger
        scale = 0.6 if i == 0 else 0.4
        node.scale = (scale, scale, scale)
        
        color = NEON_COLORS[i % len(NEON_COLORS)]
        intensity = 8 if i == 0 else 5
        node.data.materials.append(get_neon_material(f"Knowledge{i}", color, intensity))
        nodes.append(node)
    
    # Connect all to center
    for i in range(1, len(nodes)):
        start = nodes[0].location
        end = nodes[i].location
        mid = [(start[j] + end[j]) / 2 for j in range(3)]
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        
        length = math.sqrt(sum((end[j] - start[j])**2 for j in range(3)))
        edge.scale = (0.02, 0.02, length / 2)
        
        # Orient edge
        angle = math.atan2(end[1] - start[1], end[0] - start[0])
        edge.rotation_euler = (0, 0, angle)
        
        edge.data.materials.append(get_neon_material(f"KEdge{i}", (1, 1, 1), 2))

# CONSCIOUSNESS VISUALIZATIONS
def create_neon_self_awareness_loop():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # Create recursive loop
    segments = 20
    radius = 3
    
    for i in range(segments):
        angle = (i / segments) * 2 * math.pi
        x = math.cos(angle) * radius
        y = math.sin(angle) * radius
        z = math.sin(angle * 3) * 0.5  # Add wave
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        segment = bpy.context.object
        segment.scale = (0.3, 0.3, 0.3)
        
        # Color cycles through spectrum
        color_index = int((i / segments) * len(NEON_COLORS))
        color = NEON_COLORS[color_index % len(NEON_COLORS)]
        intensity = 3 + math.sin(angle * 2) * 2
        
        segment.data.materials.append(get_neon_material(f"Loop{i}", color, intensity))
    
    # Central awareness core
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0), subdivisions=3)
    core = bpy.context.object
    core.scale = (0.8, 0.8, 0.8)
    core.data.materials.append(get_neon_material("Core", (1, 1, 1), 10))

# INTERACTION VISUALIZATIONS
def create_neon_user_dialogue_flow():
    clear_scene()
    setup_dark_world()
    add_centered_camera()
    
    # User messages (left side)
    for i in range(3):
        y = (i - 1) * 2
        bpy.ops.mesh.primitive_cube_add(location=(-3, y, 0))
        user_msg = bpy.context.object
        user_msg.scale = (1, 0.3, 0.3)
        user_msg.data.materials.append(get_neon_material(f"User{i}", (0, 1, 1), 6))
    
    # Processing center
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    processor = bpy.context.object
    processor.scale = (1, 1, 1)
    processor.data.materials.append(get_neon_material("Processor", (1, 0, 1), 8))
    
    # Claude responses (right side)
    for i in range(3):
        y = (i - 1) * 2
        bpy.ops.mesh.primitive_cube_add(location=(3, y, 0))
        response = bpy.context.object
        response.scale = (1, 0.3, 0.3)
        response.data.materials.append(get_neon_material(f"Response{i}", (0, 1, 0), 6))
    
    # Flow indicators
    for i in range(3):
        y = (i - 1) * 2
        
        # User to processor
        bpy.ops.mesh.primitive_cone_add(location=(-1.5, y, 0), rotation=(0, 0, -1.57))
        arrow1 = bpy.context.object
        arrow1.scale = (0.2, 0.2, 0.5)
        arrow1.data.materials.append(get_neon_material(f"Arrow1_{i}", (1, 1, 0), 4))
        
        # Processor to response
        bpy.ops.mesh.primitive_cone_add(location=(1.5, y, 0), rotation=(0, 0, -1.57))
        arrow2 = bpy.context.object
        arrow2.scale = (0.2, 0.2, 0.5)
        arrow2.data.materials.append(get_neon_material(f"Arrow2_{i}", (1, 1, 0), 4))

# Create batch generation function
def generate_all_neon_visualizations():
    visualizations = [
        # Thinking
        ("thinking/token_stream.png", create_neon_token_stream),
        ("thinking/attention_matrix.png", create_neon_attention_matrix),
        ("thinking/context_window.png", create_neon_context_window),
        ("thinking/thought_chains.png", create_neon_thought_chains),
        ("thinking/parallel_reasoning.png", create_neon_parallel_reasoning),
        
        # Code
        ("code/syntax_tree.png", create_neon_syntax_tree),
        ("code/code_flow.png", create_neon_code_flow),
        ("code/bug_detection.png", create_neon_bug_detection),
        ("code/pattern_matching.png", create_neon_pattern_matching),
        ("code/refactoring_paths.png", create_neon_refactoring_paths),
        
        # Memory
        ("memory/knowledge_graph.png", create_neon_knowledge_graph),
        
        # Consciousness
        ("consciousness/self_awareness_loop.png", create_neon_self_awareness_loop),
        
        # Interaction
        ("interaction/user_dialogue_flow.png", create_neon_user_dialogue_flow),
    ]
    
    base_path = "/home/franz/dev/claude-vision-gallery/public/"
    
    for filepath, func in visualizations:
        full_path = base_path + filepath
        print(f"Generating {filepath}...")
        func()
        render_image(full_path)
        print(f"Saved {filepath}")

# Generate all visualizations
if __name__ == "__main__":
    generate_all_neon_visualizations()
    print("\nNeon visualizations complete!")