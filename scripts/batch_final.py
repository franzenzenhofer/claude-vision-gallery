#!/usr/bin/env python3
# Final batch - Essential remaining visualizations
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

# MEMORY - Knowledge Graph
def create_knowledge_graph():
    setup_scene()
    add_camera(location=(0, -12, 5), rotation=(1.2, 0, 0))
    add_area_light()
    
    # Create interconnected nodes
    nodes = []
    for i in range(20):
        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        z = random.uniform(-2, 2)
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        node = bpy.context.object
        node.scale = (0.3, 0.3, 0.3)
        
        color = NEON_COLORS[i % len(NEON_COLORS)]
        mat = create_neon_material(f"KNode{i}", color, 3)
        node.data.materials.append(mat)
        nodes.append((x, y, z))
    
    # Create connections
    for i in range(30):
        idx1 = random.randint(0, len(nodes)-1)
        idx2 = random.randint(0, len(nodes)-1)
        if idx1 != idx2:
            x1, y1, z1 = nodes[idx1]
            x2, y2, z2 = nodes[idx2]
            
            mid = ((x1+x2)/2, (y1+y2)/2, (z1+z2)/2)
            bpy.ops.mesh.primitive_cylinder_add(location=mid)
            edge = bpy.context.object
            edge.scale = (0.02, 0.02, 1)
            
            dx = x2 - x1
            dy = y2 - y1
            dz = z2 - z1
            edge.rotation_euler = (0, math.atan2(math.sqrt(dx**2 + dy**2), dz), math.atan2(dy, dx))
            
            mat = create_neon_material(f"Edge{i}", NEON_COLORS[7], 1.5)
            edge.data.materials.append(mat)
    
    render_white_bg(base_path + "memory/knowledge_graph.png")

# CONSCIOUSNESS - Self Awareness
def create_self_awareness():
    setup_scene()
    add_camera(location=(0, -15, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Recursive loops
    for i in range(5):
        radius = 1 + i * 0.8
        color = NEON_COLORS[i % len(NEON_COLORS)]
        
        # Create circular path
        for j in range(20):
            angle = (j / 20) * 2 * math.pi
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = math.sin(angle * 3) * 0.5
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (0.2 - i * 0.02, 0.2 - i * 0.02, 0.2 - i * 0.02)
            mat = create_neon_material(f"Loop{i}{j}", color, 4 - i * 0.5)
            node.data.materials.append(mat)
    
    # Central consciousness node
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
    center = bpy.context.object
    center.scale = (0.8, 0.8, 0.8)
    mat = create_neon_material("Center", NEON_COLORS[0], 5)
    center.data.materials.append(mat)
    
    render_white_bg(base_path + "consciousness/self_awareness_loop.png")

# INTERACTION - Response Generation
def create_response_generation():
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Input processing
    for i in range(10):
        x = -4 + i * 0.3
        y = math.sin(i * 0.5) * 1.5
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        input_node = bpy.context.object
        input_node.scale = (0.2, 0.2, 0.2)
        mat = create_neon_material(f"Input{i}", NEON_COLORS[1], 2)
        input_node.data.materials.append(mat)
    
    # Central processing
    bpy.ops.mesh.primitive_ico_sphere_add(location=(0, 0, 0), subdivisions=3)
    processor = bpy.context.object
    processor.scale = (1.2, 1.2, 1.2)
    mat = create_neon_material("Processor", NEON_COLORS[4], 5)
    processor.data.materials.append(mat)
    
    # Response generation
    for i in range(15):
        x = 2 + i * 0.2
        y = math.cos(i * 0.3) * 2
        z = 0
        
        bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
        output = bpy.context.object
        output.scale = (0.15, 0.15, 0.3)
        output.rotation_euler = (0, 1.57, 0)
        
        color = NEON_COLORS[(i + 3) % len(NEON_COLORS)]
        mat = create_neon_material(f"Output{i}", color, 3)
        output.data.materials.append(mat)
    
    render_white_bg(base_path + "interaction/response_generation.png")

# PROBLEM SOLVING - Decision Tree
def create_decision_tree():
    setup_scene()
    add_camera(location=(0, -10, 8), rotation=(0.8, 0, 0))
    add_area_light()
    
    def add_branch(pos, depth, angle_offset=0):
        if depth > 3:
            return
        
        bpy.ops.mesh.primitive_uv_sphere_add(location=pos)
        node = bpy.context.object
        scale = 0.4 - depth * 0.08
        node.scale = (scale, scale, scale)
        
        color = NEON_COLORS[depth * 2 % len(NEON_COLORS)]
        mat = create_neon_material(f"Node_{pos}", color, 4 - depth)
        node.data.materials.append(mat)
        
        # Create branches
        if depth < 3:
            for i in range(2):
                angle = angle_offset + (i - 0.5) * 0.5
                new_x = pos[0] + math.sin(angle) * 1.5
                new_y = pos[1] + math.cos(angle) * 1.5
                new_z = pos[2] - 1.5
                
                # Connect with edge
                mid = ((pos[0] + new_x)/2, (pos[1] + new_y)/2, (pos[2] + new_z)/2)
                bpy.ops.mesh.primitive_cylinder_add(location=mid)
                edge = bpy.context.object
                edge.scale = (0.03, 0.03, 0.75)
                
                dx = new_x - pos[0]
                dy = new_y - pos[1]
                dz = new_z - pos[2]
                edge.rotation_euler = (0, math.atan2(math.sqrt(dx**2 + dy**2), dz), math.atan2(dy, dx))
                
                mat = create_neon_material(f"Edge_{mid}", NEON_COLORS[6], 2)
                edge.data.materials.append(mat)
                
                add_branch((new_x, new_y, new_z), depth + 1, angle)
    
    # Start tree
    add_branch((0, 0, 4), 0)
    
    render_white_bg(base_path + "problem_solving/decision_tree.png")

# Run visualizations
print("FINAL BATCH:")
create_knowledge_graph()
create_self_awareness()
create_response_generation()
create_decision_tree()

print("\n✨ Gallery complete!")