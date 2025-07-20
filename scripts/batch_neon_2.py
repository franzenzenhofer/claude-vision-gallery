#!/usr/bin/env python3
# Batch 2: LANGUAGE Category
import bpy
import math
import random
from PIL import Image
import os

base_path = "/home/franz/dev/claude-vision-gallery/public/"

NEON_COLORS = [
    (1, 0, 0.3),      # Hot Pink
    (0, 1, 1),        # Electric Cyan
    (1, 0, 1),        # Magenta
    (0, 1, 0),        # Neon Green
    (1, 1, 0),        # Electric Yellow
    (1, 0.5, 0),      # Neon Orange
    (0.5, 0, 1),      # Electric Purple
    (0, 0.5, 1),      # Electric Blue
    (0.8, 0.2, 1),    # Violet
    (0.2, 1, 0.8),    # Aqua
]

def setup_scene():
    bpy.context.scene.render.engine = 'BLENDER_EEVEE_NEXT'
    bpy.context.scene.render.resolution_x = 1080
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.film_transparent = True
    bpy.context.scene.render.image_settings.file_format = 'PNG'
    bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()

def add_camera(location=(0, -10, 0), rotation=(1.57, 0, 0)):
    bpy.ops.object.camera_add(location=location)
    camera = bpy.context.object
    camera.rotation_euler = rotation
    bpy.context.scene.camera = camera

def create_neon_material(name, color, strength=3.0):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    nodes.clear()
    emission = nodes.new('ShaderNodeEmission')
    emission.inputs['Color'].default_value = (*color, 1.0)
    emission.inputs['Strength'].default_value = strength
    output = nodes.new('ShaderNodeOutputMaterial')
    mat.node_tree.links.new(emission.outputs[0], output.inputs[0])
    return mat

def add_area_light(location=(0, 0, 5), energy=20):
    bpy.ops.object.light_add(type='AREA', location=location)
    light = bpy.context.object
    light.data.energy = energy
    light.data.size = 10

def render_white_bg(output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    temp_path = output_path.replace('.png', '_temp.png')
    bpy.context.scene.render.filepath = temp_path
    bpy.ops.render.render(write_still=True)
    img = Image.open(temp_path)
    white_bg = Image.new('RGBA', img.size, (255, 255, 255, 255))
    white_bg.paste(img, (0, 0), img)
    rgb_img = white_bg.convert('RGB')
    rgb_img.save(output_path)
    os.remove(temp_path)
    print(f"✓ {output_path}")

# LANGUAGE VISUALIZATIONS
def create_tokenization_grid():
    """Text broken into token units"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Create grid of tokens
    for i in range(12):
        for j in range(8):
            x = (i - 5.5) * 0.8
            y = (j - 3.5) * 0.8
            z = 0
            
            # Different shapes for different token types
            token_type = (i + j) % 4
            if token_type == 0:  # Word token
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
                color = NEON_COLORS[1]  # Cyan
            elif token_type == 1:  # Subword token
                bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
                color = NEON_COLORS[4]  # Yellow
            elif token_type == 2:  # Punctuation
                bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z), subdivisions=1)
                color = NEON_COLORS[0]  # Hot pink
            else:  # Special token
                bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
                color = NEON_COLORS[6]  # Purple
            
            obj = bpy.context.object
            obj.scale = (0.25, 0.25, 0.25)
            
            # Add some variation
            obj.rotation_euler = (
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2),
                random.uniform(-0.2, 0.2)
            )
            
            mat = create_neon_material(f"Token{i}{j}", color)
            obj.data.materials.append(mat)
    
    render_white_bg(base_path + "language/tokenization_grid.png")

def create_semantic_space():
    """Words in multidimensional semantic space"""
    setup_scene()
    add_camera(location=(10, -10, 8), rotation=(0.9, 0, 0.785))
    add_area_light()
    
    # Create word clusters
    clusters = [
        # (center, color, words_count)
        ((0, 0, 0), NEON_COLORS[1], 8),      # Core concepts
        ((-3, 2, 1), NEON_COLORS[4], 6),     # Actions
        ((3, -2, -1), NEON_COLORS[0], 7),    # Emotions
        ((2, 3, 2), NEON_COLORS[5], 5),      # Objects
        ((-2, -3, 0), NEON_COLORS[6], 6),    # Abstract
    ]
    
    for center, color, count in clusters:
        cx, cy, cz = center
        
        # Cluster center
        bpy.ops.mesh.primitive_uv_sphere_add(location=center)
        core = bpy.context.object
        core.scale = (0.4, 0.4, 0.4)
        mat = create_neon_material(f"Core_{center}", color, 4)
        core.data.materials.append(mat)
        
        # Surrounding words
        for i in range(count):
            angle = (i / count) * 2 * math.pi
            radius = random.uniform(0.8, 1.5)
            
            x = cx + math.cos(angle) * radius
            y = cy + math.sin(angle) * radius
            z = cz + random.uniform(-0.5, 0.5)
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            word = bpy.context.object
            word.scale = (0.2, 0.2, 0.2)
            mat = create_neon_material(f"Word_{center}_{i}", color, 2)
            word.data.materials.append(mat)
    
    # Add connections between related concepts
    for i in range(10):
        start = (random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-2, 2))
        end = (random.uniform(-4, 4), random.uniform(-4, 4), random.uniform(-2, 2))
        
        mid_x = (start[0] + end[0]) / 2
        mid_y = (start[1] + end[1]) / 2
        mid_z = (start[2] + end[2]) / 2
        
        bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, mid_z))
        connection = bpy.context.object
        connection.scale = (0.02, 0.02, 1)
        
        # Orient cylinder
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        connection.rotation_euler = (0, math.atan2(math.sqrt(dx**2 + dy**2), dz), math.atan2(dy, dx))
        
        mat = create_neon_material(f"Connection{i}", NEON_COLORS[7], 1)
        connection.data.materials.append(mat)
    
    render_white_bg(base_path + "language/semantic_space.png")

def create_multilingual_network():
    """Connections between different languages"""
    setup_scene()
    add_camera(location=(0, -15, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Language nodes in circular arrangement
    languages = [
        ("English", NEON_COLORS[1]),
        ("Spanish", NEON_COLORS[0]),
        ("Chinese", NEON_COLORS[4]),
        ("Arabic", NEON_COLORS[5]),
        ("French", NEON_COLORS[6]),
        ("German", NEON_COLORS[2]),
        ("Japanese", NEON_COLORS[3]),
        ("Russian", NEON_COLORS[7]),
    ]
    
    nodes = []
    for i, (lang, color) in enumerate(languages):
        angle = (i / len(languages)) * 2 * math.pi
        x = math.cos(angle) * 4
        y = math.sin(angle) * 4
        z = 0
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
        node = bpy.context.object
        node.scale = (0.6, 0.6, 0.6)
        mat = create_neon_material(f"Lang_{lang}", color, 3)
        node.data.materials.append(mat)
        nodes.append((x, y, z))
    
    # Central hub
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    hub = bpy.context.object
    hub.scale = (0.8, 0.8, 0.8)
    mat = create_neon_material("Hub", NEON_COLORS[9], 4)
    hub.data.materials.append(mat)
    
    # Connections
    for i, (x1, y1, z1) in enumerate(nodes):
        # Connect to hub
        bpy.ops.mesh.primitive_cylinder_add(location=(x1/2, y1/2, 0))
        conn = bpy.context.object
        conn.scale = (0.05, 0.05, 2)
        angle = math.atan2(y1, x1)
        conn.rotation_euler = (0, 1.57, angle)
        mat = create_neon_material(f"ConnHub{i}", NEON_COLORS[8], 1.5)
        conn.data.materials.append(mat)
        
        # Connect to neighbors
        for j in range(2):
            next_idx = (i + j + 1) % len(nodes)
            x2, y2, z2 = nodes[next_idx]
            
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            
            bpy.ops.mesh.primitive_cylinder_add(location=(mid_x, mid_y, 0))
            conn2 = bpy.context.object
            conn2.scale = (0.03, 0.03, 1)
            
            angle = math.atan2(y2 - y1, x2 - x1)
            conn2.rotation_euler = (0, 1.57, angle)
            mat = create_neon_material(f"ConnLang{i}{j}", NEON_COLORS[7], 1)
            conn2.data.materials.append(mat)
    
    render_white_bg(base_path + "language/multilingual_network.png")

def create_text_generation_flow():
    """Sequential text generation process"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Generation pipeline
    for i in range(40):
        x = (i - 20) * 0.4
        
        # Wave pattern for flow
        y = math.sin(i * 0.3) * 2
        z = 0
        
        # Different stages of generation
        stage = i // 10
        if stage == 0:  # Context
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            color = NEON_COLORS[6]  # Purple
            scale = 0.3
        elif stage == 1:  # Processing
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            color = NEON_COLORS[1]  # Cyan
            scale = 0.25
        elif stage == 2:  # Candidates
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
            color = NEON_COLORS[4]  # Yellow
            scale = 0.2
        else:  # Output
            bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
            color = NEON_COLORS[5]  # Green
            scale = 0.25
        
        obj = bpy.context.object
        obj.scale = (scale, scale, scale)
        obj.rotation_euler = (0, 0, i * 0.1)
        
        # Add probability variation
        strength = 2 + abs(math.sin(i * 0.5)) * 2
        mat = create_neon_material(f"Gen{i}", color, strength)
        obj.data.materials.append(mat)
    
    # Add probability branches
    for i in range(10):
        base_x = (i - 5) * 1.6
        base_y = math.sin(i * 0.3) * 2
        
        for j in range(3):
            branch_y = base_y + (j - 1) * 0.8
            branch_z = 1
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(base_x, branch_y, branch_z))
            branch = bpy.context.object
            branch.scale = (0.1, 0.1, 0.1)
            
            opacity = 1 - (j * 0.3)
            mat = create_neon_material(f"Branch{i}{j}", NEON_COLORS[8], opacity * 2)
            branch.data.materials.append(mat)
    
    render_white_bg(base_path + "language/text_generation_flow.png")

def create_grammar_structure():
    """Syntactic parse tree visualization"""
    setup_scene()
    add_camera(location=(0, -10, 6), rotation=(1.0, 0, 0))
    add_area_light()
    
    # Tree structure with grammatical nodes
    def add_grammar_node(pos, size, color, node_type):
        if node_type == 'phrase':
            bpy.ops.mesh.primitive_cube_add(location=pos)
        elif node_type == 'word':
            bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        else:  # punctuation
            bpy.ops.mesh.primitive_ico_sphere_add(location=pos, subdivisions=1)
        
        node = bpy.context.object
        node.scale = (size, size, size)
        mat = create_neon_material(f"Grammar_{pos}", color, 3)
        node.data.materials.append(mat)
        return node
    
    # S (sentence) root
    add_grammar_node((0, 0, 4), 0.5, NEON_COLORS[2], 'phrase')
    
    # NP and VP branches
    add_grammar_node((-2, 0, 2.5), 0.4, NEON_COLORS[1], 'phrase')
    add_grammar_node((2, 0, 2.5), 0.4, NEON_COLORS[4], 'phrase')
    
    # Determiners, nouns, verbs
    positions = [
        ((-3, 0, 1), 0.3, NEON_COLORS[0], 'word'),
        ((-1, 0, 1), 0.3, NEON_COLORS[5], 'word'),
        ((1, 0, 1), 0.3, NEON_COLORS[6], 'word'),
        ((3, 0, 1), 0.3, NEON_COLORS[3], 'word'),
    ]
    
    for pos, size, color, node_type in positions:
        add_grammar_node(pos, size, color, node_type)
    
    # Terminal words
    for i in range(4):
        x = (i - 1.5) * 2
        y = 0
        z = -0.5
        add_grammar_node((x, y, z), 0.2, NEON_COLORS[7], 'word')
    
    # Connections
    connections = [
        ((0, 0, 4), (-2, 0, 2.5)),
        ((0, 0, 4), (2, 0, 2.5)),
        ((-2, 0, 2.5), (-3, 0, 1)),
        ((-2, 0, 2.5), (-1, 0, 1)),
        ((2, 0, 2.5), (1, 0, 1)),
        ((2, 0, 2.5), (3, 0, 1)),
    ]
    
    for start, end in connections:
        mid = tuple((s + e) / 2 for s, e in zip(start, end))
        
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.05, 0.05, 0.8)
        
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        edge.rotation_euler = (0, math.atan2(math.sqrt(dx**2 + dy**2), dz), math.atan2(dy, dx))
        
        mat = create_neon_material(f"Edge_{start}_{end}", NEON_COLORS[8], 1.5)
        edge.data.materials.append(mat)
    
    render_white_bg(base_path + "language/grammar_structure.png")

# Run all visualizations
print("LANGUAGE CATEGORY:")
create_tokenization_grid()
create_semantic_space()
create_multilingual_network()
create_text_generation_flow()
create_grammar_structure()

print("\n✨ Batch 2 complete!")