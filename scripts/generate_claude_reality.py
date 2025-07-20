#!/usr/bin/env python3
"""Generate REAL visualizations of Claude Code's actual processes"""
import bpy
import math
import random
import os

# Categories of Claude's reality
CATEGORIES = {
    "thinking": [
        "token_stream",
        "attention_matrix", 
        "context_window",
        "thought_chains",
        "parallel_reasoning"
    ],
    "code": [
        "syntax_tree",
        "code_flow",
        "bug_detection",
        "pattern_matching",
        "refactoring_paths"
    ],
    "memory": [
        "knowledge_graph",
        "memory_retrieval",
        "context_switching",
        "information_filtering",
        "association_network"
    ],
    "tools": [
        "file_system_tree",
        "api_orchestration",
        "tool_pipeline",
        "error_cascade",
        "bash_execution"
    ],
    "language": [
        "tokenization_grid",
        "semantic_space",
        "multilingual_network",
        "text_generation_flow",
        "grammar_structure"
    ],
    "problem_solving": [
        "task_decomposition",
        "solution_search",
        "optimization_landscape",
        "decision_tree",
        "constraint_graph"
    ],
    "system": [
        "process_threads",
        "io_streams",
        "network_packets",
        "file_operations",
        "system_calls"
    ],
    "consciousness": [
        "self_awareness_loop",
        "meta_cognition",
        "uncertainty_field",
        "confidence_levels",
        "introspection_spiral"
    ],
    "interaction": [
        "user_dialogue_flow",
        "response_generation",
        "context_understanding",
        "empathy_mapping",
        "conversation_state"
    ]
}

def clear_scene():
    """Clean slate"""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def setup_bright_world():
    """White background with good lighting"""
    world = bpy.data.worlds["World"]
    world.use_nodes = True
    bg = world.node_tree.nodes["Background"]
    bg.inputs[0].default_value = (0.95, 0.95, 0.95, 1.0)  # Almost white
    bg.inputs[1].default_value = 1.0  # Full brightness

def add_text_label(text, location, size=0.3):
    """Add 3D text label"""
    bpy.ops.object.text_add(location=location)
    txt = bpy.context.active_object
    txt.data.body = text
    txt.data.size = size
    txt.data.font = bpy.data.fonts.load("/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf") if os.path.exists("/usr/share/fonts/google-noto-vf/NotoSans[wght].ttf") else None
    
    # Black text material
    mat = bpy.data.materials.new("TextMat")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0, 0, 1)
    txt.data.materials.append(mat)
    
    return txt

def generate_token_stream():
    """How I process tokens"""
    clear_scene()
    setup_bright_world()
    
    # Token boxes flowing through processing stages
    tokens = ["def", "calculate", "(", "x", ",", "y", ")", ":", "return", "x", "+", "y"]
    
    for i, token in enumerate(tokens):
        # Token cube
        x = i * 0.8 - 4
        y = math.sin(i * 0.5) * 0.5
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z), size=0.6)
        cube = bpy.context.active_object
        
        # Color based on token type
        if token in ["def", "return"]:
            color = (0.2, 0.2, 0.8, 1)  # Blue for keywords
        elif token in ["(", ")", ":", ","]:
            color = (0.8, 0.2, 0.2, 1)  # Red for syntax
        else:
            color = (0.2, 0.8, 0.2, 1)  # Green for identifiers
        
        mat = bpy.data.materials.new(f"Token{i}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        cube.data.materials.append(mat)
        
        # Add token text
        add_text_label(token, (x, y, z + 0.5), 0.2)
    
    # Processing pipeline
    for stage in range(3):
        y_pos = -2 - stage * 1.5
        bpy.ops.mesh.primitive_cylinder_add(
            location=(0, y_pos, 0),
            rotation=(0, math.pi/2, 0),
            radius=0.3,
            depth=10
        )
        pipe = bpy.context.active_object
        mat = bpy.data.materials.new(f"Pipe{stage}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.7, 0.7, 0.7, 1)
        pipe.data.materials.append(mat)
        
        stages = ["Tokenization", "Parsing", "Understanding"]
        add_text_label(stages[stage], (-5, y_pos, 0), 0.3)
    
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(0, 0, 10))
    sun = bpy.context.active_object
    sun.data.energy = 1.0
    
    # Camera - mobile friendly vertical
    bpy.ops.object.camera_add(location=(0, -8, 3))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.3, 0, 0)
    bpy.context.scene.camera = camera
    
    # Render settings
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32  # Fast render
    scene.render.resolution_x = 1080  # Square for mobile
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/token_stream.png'
    
    bpy.ops.render.render(write_still=True)

def generate_attention_matrix():
    """Attention mechanism visualization"""
    clear_scene()
    setup_bright_world()
    
    # Create attention matrix grid
    size = 8
    for i in range(size):
        for j in range(size):
            x = i * 0.6 - 2
            y = j * 0.6 - 2
            
            # Attention weight as height and color
            weight = random.random()
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, weight * 0.5), size=0.5)
            cube = bpy.context.active_object
            cube.scale.z = weight
            
            # Color gradient from low (blue) to high (red) attention
            mat = bpy.data.materials.new(f"Attention_{i}_{j}")
            mat.use_nodes = True
            color = (weight, 0.2, 1 - weight, 1)
            mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
            cube.data.materials.append(mat)
    
    # Labels
    add_text_label("ATTENTION WEIGHTS", (0, 3, 0), 0.4)
    add_text_label("Token Position →", (0, -3, 0), 0.2)
    add_text_label("Context →", (-3.5, 0, 0), 0.2)
    
    # Lighting
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 5))
    light = bpy.context.active_object
    light.data.energy = 50
    light.data.size = 5
    
    # Camera
    bpy.ops.object.camera_add(location=(5, -5, 5))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/thinking/attention_matrix.png'
    
    bpy.ops.render.render(write_still=True)

def generate_syntax_tree():
    """Abstract Syntax Tree visualization"""
    clear_scene()
    setup_bright_world()
    
    # AST nodes
    def create_node(text, pos, node_type="default"):
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos, radius=0.3)
        node = bpy.context.active_object
        
        colors = {
            "root": (0.8, 0.2, 0.2, 1),
            "function": (0.2, 0.8, 0.2, 1),
            "variable": (0.2, 0.2, 0.8, 1),
            "operator": (0.8, 0.8, 0.2, 1),
            "default": (0.5, 0.5, 0.5, 1)
        }
        
        mat = bpy.data.materials.new(f"Node_{text}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors.get(node_type, colors["default"])
        node.data.materials.append(mat)
        
        add_text_label(text, (pos[0], pos[1], pos[2] + 0.5), 0.15)
        return node
    
    # Build tree
    root = create_node("FunctionDef", (0, 0, 3), "root")
    
    # Function name
    name_node = create_node("calculate", (-2, 0, 2), "function")
    
    # Parameters
    params = create_node("params", (0, 0, 2), "default")
    param_x = create_node("x", (-1, 0, 1), "variable")
    param_y = create_node("y", (1, 0, 1), "variable")
    
    # Body
    body = create_node("return", (2, 0, 2), "function")
    add_op = create_node("+", (2, 0, 1), "operator")
    var_x = create_node("x", (1.5, 0, 0), "variable")
    var_y = create_node("y", (2.5, 0, 0), "variable")
    
    # Connect with edges
    def connect_nodes(n1, n2):
        # Create edge
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
        curve.bevel_depth = 0.02
        
        mat = bpy.data.materials.new("EdgeMat")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.3, 0.3, 0.3, 1)
        obj.data.materials.append(mat)
    
    # Create connections
    connect_nodes(root, name_node)
    connect_nodes(root, params)
    connect_nodes(root, body)
    connect_nodes(params, param_x)
    connect_nodes(params, param_y)
    connect_nodes(body, add_op)
    connect_nodes(add_op, var_x)
    connect_nodes(add_op, var_y)
    
    # Title
    add_text_label("ABSTRACT SYNTAX TREE", (0, 2, 4), 0.4)
    
    # Lighting
    bpy.ops.object.light_add(type='SUN', location=(5, -5, 10))
    sun = bpy.context.active_object
    sun.data.energy = 1.0
    
    # Camera
    bpy.ops.object.camera_add(location=(4, -4, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.1, 0, 0.785)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/code/syntax_tree.png'
    
    bpy.ops.render.render(write_still=True)

def generate_file_system_tree():
    """File system navigation visualization"""
    clear_scene()
    setup_bright_world()
    
    # File system structure
    def create_folder(name, pos, level=0):
        bpy.ops.mesh.primitive_cube_add(location=pos, size=0.4)
        folder = bpy.context.active_object
        
        # Yellow folders
        mat = bpy.data.materials.new(f"Folder_{name}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.9, 0.7, 0.1, 1)
        folder.data.materials.append(mat)
        
        add_text_label(name, (pos[0], pos[1], pos[2] + 0.3), 0.15)
        return folder
    
    def create_file(name, pos, file_type="default"):
        bpy.ops.mesh.primitive_cylinder_add(location=pos, radius=0.15, depth=0.3)
        file = bpy.context.active_object
        
        colors = {
            ".py": (0.2, 0.6, 0.2, 1),
            ".js": (0.8, 0.8, 0.2, 1),
            ".md": (0.2, 0.2, 0.8, 1),
            "default": (0.7, 0.7, 0.7, 1)
        }
        
        ext = "." + name.split(".")[-1] if "." in name else "default"
        
        mat = bpy.data.materials.new(f"File_{name}")
        mat.use_nodes = True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = colors.get(ext, colors["default"])
        file.data.materials.append(mat)
        
        add_text_label(name, (pos[0], pos[1], pos[2] + 0.3), 0.1)
        return file
    
    # Create tree structure
    root = create_folder("/home/franz/dev", (0, 0, 3))
    
    # Project folders
    project1 = create_folder("claude-vision", (-2, 0, 2))
    project2 = create_folder("ai-tools", (2, 0, 2))
    
    # Files
    files = [
        ("index.html", (-3, 0, 1)),
        ("styles.css", (-2, 0, 1)),
        ("script.js", (-1, 0, 1)),
        ("README.md", (1, 0, 1)),
        ("main.py", (2, 0, 1)),
        ("config.json", (3, 0, 1))
    ]
    
    for name, pos in files:
        create_file(name, pos)
    
    # Current path indicator
    bpy.ops.mesh.primitive_cone_add(location=(0, -2, 0), radius1=0.2, depth=0.4)
    pointer = bpy.context.active_object
    pointer.rotation_euler = (math.pi, 0, 0)
    mat = bpy.data.materials.new("Pointer")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0.2, 0.2, 1)
    pointer.data.materials.append(mat)
    
    add_text_label("CURRENT PATH", (0, -2.5, 0), 0.2)
    
    # Title
    add_text_label("FILE SYSTEM NAVIGATION", (0, 0, 4), 0.4)
    
    # Lighting
    bpy.ops.object.light_add(type='AREA', location=(0, -5, 5))
    light = bpy.context.active_object
    light.data.energy = 50
    light.data.size = 10
    
    # Camera
    bpy.ops.object.camera_add(location=(0, -6, 4))
    camera = bpy.context.active_object
    camera.rotation_euler = (1.2, 0, 0)
    bpy.context.scene.camera = camera
    
    # Render
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 32
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1080
    scene.render.filepath = '/home/franz/dev/claude-vision-gallery/public/tools/file_system_tree.png'
    
    bpy.ops.render.render(write_still=True)

# Generate first batch of images
print("Creating output directories...")
for category in CATEGORIES:
    os.makedirs(f'/home/franz/dev/claude-vision-gallery/public/{category}', exist_ok=True)

print("Generating Token Stream...")
generate_token_stream()

print("Generating Attention Matrix...")
generate_attention_matrix()

print("Generating Syntax Tree...")
generate_syntax_tree()

print("Generating File System Tree...")
generate_file_system_tree()

print("First batch complete! More coming...")