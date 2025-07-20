#!/usr/bin/env python3
# Batch 3: CODE Category
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

def add_area_light():
    bpy.ops.object.light_add(type='AREA', location=(0, 0, 5))
    light = bpy.context.object
    light.data.energy = 20
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

# CODE VISUALIZATIONS
def create_syntax_tree():
    """Abstract syntax tree visualization"""
    setup_scene()
    add_camera(location=(0, -10, 5), rotation=(1.2, 0, 0))
    add_area_light()
    
    def add_node(pos, size, color, name):
        bpy.ops.mesh.primitive_ico_sphere_add(location=pos)
        node = bpy.context.object
        node.scale = (size, size, size)
        mat = create_neon_material(name, color)
        node.data.materials.append(mat)
        return node
    
    # Root node (Program)
    add_node((0, 0, 3), 0.5, NEON_COLORS[2], "Root")
    
    # Function declarations
    positions = [(-2.5, 0, 1.5), (0, 0, 1.5), (2.5, 0, 1.5)]
    colors = [NEON_COLORS[1], NEON_COLORS[4], NEON_COLORS[5]]
    
    for i, (pos, color) in enumerate(zip(positions, colors)):
        add_node(pos, 0.4, color, f"Func{i}")
        
        # Function body nodes
        for j in range(3):
            sub_x = pos[0] + (j - 1) * 0.7
            sub_y = pos[1]
            sub_z = pos[2] - 1.5
            add_node((sub_x, sub_y, sub_z), 0.25, color, f"Body{i}_{j}")
            
            # Leaf nodes
            for k in range(2):
                leaf_x = sub_x + (k - 0.5) * 0.4
                leaf_z = sub_z - 1
                add_node((leaf_x, sub_y, leaf_z), 0.15, NEON_COLORS[7], f"Leaf{i}_{j}_{k}")
    
    # Connect nodes with edges
    connections = [
        ((0, 0, 3), (-2.5, 0, 1.5)),
        ((0, 0, 3), (0, 0, 1.5)),
        ((0, 0, 3), (2.5, 0, 1.5)),
    ]
    
    for start, end in connections:
        mid = tuple((s + e) / 2 for s, e in zip(start, end))
        bpy.ops.mesh.primitive_cylinder_add(location=mid)
        edge = bpy.context.object
        edge.scale = (0.03, 0.03, 0.8)
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        dz = end[2] - start[2]
        edge.rotation_euler = (0, math.atan2(math.sqrt(dx**2 + dy**2), dz), math.atan2(dy, dx))
        mat = create_neon_material(f"Edge_{start}", NEON_COLORS[6], 1.5)
        edge.data.materials.append(mat)
    
    render_white_bg(base_path + "code/syntax_tree.png")

def create_code_flow():
    """Spiraling flow of code execution"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Create double helix of code flow
    for strand in range(2):
        for i in range(50):
            t = i / 50 * 4 * math.pi
            radius = 1 + t / (3 * math.pi)
            
            # Double helix offset
            angle = t + (strand * math.pi)
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = (i - 25) * 0.15
            
            # Alternate shapes for different operations
            if i % 3 == 0:
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            elif i % 3 == 1:
                bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            else:
                bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
            
            flow = bpy.context.object
            flow.scale = (0.2, 0.2, 0.2)
            flow.rotation_euler = (0, 0, t)
            
            # Color based on strand and position
            color_idx = (strand * 4 + i) % len(NEON_COLORS)
            color = NEON_COLORS[color_idx]
            mat = create_neon_material(f"Flow{strand}{i}", color)
            flow.data.materials.append(mat)
    
    # Add central execution pointer
    bpy.ops.mesh.primitive_cone_add(location=(0, 0, 0))
    pointer = bpy.context.object
    pointer.scale = (0.5, 0.5, 0.8)
    mat = create_neon_material("Pointer", NEON_COLORS[0], 4)
    pointer.data.materials.append(mat)
    
    render_white_bg(base_path + "code/code_flow.png")

def create_bug_detection():
    """Bugs highlighted in code grid"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Bug positions
    bugs = [(2, 5), (5, 2), (7, 7), (3, 8), (8, 3), (1, 6), (6, 9)]
    
    for i in range(10):
        for j in range(10):
            x = (i - 4.5) * 0.7
            y = (j - 4.5) * 0.7
            z = 0
            
            is_bug = (i, j) in bugs
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            block = bpy.context.object
            
            if is_bug:
                # Bugs are larger and red
                block.scale = (0.35, 0.35, 0.35)
                color = NEON_COLORS[0]  # Hot pink
                strength = 5
                
                # Add warning glow
                bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
                glow = bpy.context.object
                glow.scale = (0.5, 0.5, 0.5)
                glow_mat = create_neon_material(f"Glow{i}{j}", color, 2)
                glow.data.materials.append(glow_mat)
            else:
                # Clean code blocks
                block.scale = (0.2, 0.2, 0.2)
                color = NEON_COLORS[3]  # Green
                strength = 2
            
            mat = create_neon_material(f"Block{i}{j}", color, strength)
            block.data.materials.append(mat)
    
    render_white_bg(base_path + "code/bug_detection.png")

def create_pattern_matching():
    """Pattern recognition in code"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    patterns = [
        # (shape, positions, color)
        ('L', [(0, 0), (0, 1), (0, 2), (1, 0)], NEON_COLORS[1]),
        ('T', [(0, 1), (1, 1), (2, 1), (1, 0), (1, 2)], NEON_COLORS[2]),
        ('I', [(0, 0), (0, 1), (0, 2), (0, 3)], NEON_COLORS[4]),
        ('O', [(0, 0), (0, 1), (1, 0), (1, 1)], NEON_COLORS[5]),
    ]
    
    x_offset = -4
    for pattern_name, positions, color in patterns:
        # Draw pattern
        for px, py in positions:
            x = x_offset + px * 0.6
            y = py * 0.6 - 1
            z = 0
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            element = bpy.context.object
            element.scale = (0.25, 0.25, 0.25)
            mat = create_neon_material(f"Pattern_{pattern_name}_{px}_{py}", color, 3)
            element.data.materials.append(mat)
        
        # Pattern label
        label_x = x_offset + 0.5
        label_y = -2
        bpy.ops.mesh.primitive_cube_add(location=(label_x, label_y, 0))
        label = bpy.context.object
        label.scale = (0.4, 0.1, 0.1)
        mat = create_neon_material(f"Label_{pattern_name}", color, 4)
        label.data.materials.append(mat)
        
        x_offset += 3
    
    # Add matching indicators
    for i in range(5):
        x = random.uniform(-4, 4)
        y = random.uniform(2, 4)
        z = 0.5
        
        bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
        indicator = bpy.context.object
        indicator.scale = (0.15, 0.15, 0.3)
        indicator.rotation_euler = (3.14, 0, 0)
        mat = create_neon_material(f"Match{i}", NEON_COLORS[6], 2)
        indicator.data.materials.append(mat)
    
    render_white_bg(base_path + "code/pattern_matching.png")

def create_refactoring_paths():
    """From chaos to clean code"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Chaotic code (left side)
    for i in range(20):
        x = random.uniform(-4.5, -2)
        y = random.uniform(-2.5, 2.5)
        z = random.uniform(-0.5, 0.5)
        
        shape = random.choice(['cube', 'sphere', 'cylinder'])
        if shape == 'cube':
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        elif shape == 'sphere':
            bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
        else:
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
        
        messy = bpy.context.object
        messy.scale = (0.15, 0.15, 0.15)
        messy.rotation_euler = (
            random.uniform(0, 6.28),
            random.uniform(0, 6.28),
            random.uniform(0, 6.28)
        )
        mat = create_neon_material(f"Messy{i}", NEON_COLORS[0])  # Red
        messy.data.materials.append(mat)
    
    # Clean, organized code (right side)
    for i in range(4):
        for j in range(5):
            x = 2.5 + i * 0.5
            y = (j - 2) * 0.5
            z = 0
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            clean = bpy.context.object
            clean.scale = (0.2, 0.2, 0.2)
            mat = create_neon_material(f"Clean{i}{j}", NEON_COLORS[3])  # Green
            clean.data.materials.append(mat)
    
    # Transformation arrows
    for i in range(3):
        y = (i - 1) * 1.5
        
        # Arrow shaft
        bpy.ops.mesh.primitive_cylinder_add(location=(0, y, 0))
        shaft = bpy.context.object
        shaft.scale = (0.05, 0.05, 1.5)
        shaft.rotation_euler = (0, 1.57, 0)
        mat = create_neon_material(f"Shaft{i}", NEON_COLORS[4], 3)
        shaft.data.materials.append(mat)
        
        # Arrow head
        bpy.ops.mesh.primitive_cone_add(location=(0.8, y, 0))
        head = bpy.context.object
        head.scale = (0.3, 0.3, 0.5)
        head.rotation_euler = (0, 0, -1.57)
        mat = create_neon_material(f"Head{i}", NEON_COLORS[4], 4)
        head.data.materials.append(mat)
    
    render_white_bg(base_path + "code/refactoring_paths.png")

# Run all visualizations
print("CODE CATEGORY:")
create_syntax_tree()
create_code_flow()
create_bug_detection()
create_pattern_matching()
create_refactoring_paths()

print("\n✨ Batch 3 complete!")