#!/usr/bin/env python3
# Batch 1: TOOLS Category
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

# TOOLS CATEGORY
def create_network_packets():
    """Data packets flowing through network"""
    setup_scene()
    add_camera(location=(0, -12, 3), rotation=(1.3, 0, 0))
    add_area_light()
    
    # Create packet streams
    for stream in range(3):
        z_offset = (stream - 1) * 2
        color = NEON_COLORS[stream * 2]
        
        for i in range(20):
            x = (i - 10) * 0.6
            y = math.sin(i * 0.3 + stream) * 1.5
            z = z_offset
            
            bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
            packet = bpy.context.object
            packet.scale = (0.3, 0.2, 0.1)
            packet.rotation_euler = (0, i * 0.1, 0)
            
            mat = create_neon_material(f"Packet{stream}{i}", color)
            packet.data.materials.append(mat)
    
    render_white_bg(base_path + "tools/network_packets.png")

def create_file_operations():
    """File system operations visualization"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Central disk
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
    disk = bpy.context.object
    disk.scale = (2, 2, 0.1)
    mat = create_neon_material("Disk", NEON_COLORS[3])
    disk.data.materials.append(mat)
    
    # File operations radiating out
    operations = ['read', 'write', 'delete', 'create']
    for i in range(16):
        angle = (i / 16) * 2 * math.pi
        op_type = i % 4
        
        for j in range(4):
            dist = 2.5 + j * 0.5
            x = math.cos(angle) * dist
            y = math.sin(angle) * dist
            z = 0.5
            
            if op_type == 0:  # Read
                bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
                color = NEON_COLORS[1]
            elif op_type == 1:  # Write
                bpy.ops.mesh.primitive_cone_add(location=(x, y, z))
                color = NEON_COLORS[4]
            elif op_type == 2:  # Delete
                bpy.ops.mesh.primitive_cylinder_add(location=(x, y, z))
                color = NEON_COLORS[0]
            else:  # Create
                bpy.ops.mesh.primitive_uv_sphere_add(location=(x, y, z))
                color = NEON_COLORS[5]
            
            obj = bpy.context.object
            obj.scale = (0.15, 0.15, 0.15)
            mat = create_neon_material(f"Op{i}{j}", color)
            obj.data.materials.append(mat)
    
    render_white_bg(base_path + "tools/file_operations.png")

def create_system_calls():
    """System call hierarchy"""
    setup_scene()
    add_camera(location=(0, -10, 8), rotation=(0.8, 0, 0))
    add_area_light()
    
    # Create layered system calls
    layers = [
        ('User Space', 3, NEON_COLORS[1], 0.8),
        ('Kernel Space', 1.5, NEON_COLORS[0], 0.6),
        ('Hardware', 0, NEON_COLORS[6], 0.4)
    ]
    
    for layer_name, z, color, size in layers:
        for i in range(6):
            angle = (i / 6) * 2 * math.pi
            x = math.cos(angle) * 2
            y = math.sin(angle) * 2
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            node = bpy.context.object
            node.scale = (size, size, size)
            mat = create_neon_material(f"{layer_name}{i}", color)
            node.data.materials.append(mat)
    
    # Connections between layers
    for i in range(6):
        angle = (i / 6) * 2 * math.pi
        x = math.cos(angle) * 2
        y = math.sin(angle) * 2
        
        for z1, z2 in [(0, 1.5), (1.5, 3)]:
            mid_z = (z1 + z2) / 2
            
            bpy.ops.mesh.primitive_cylinder_add(location=(x, y, mid_z))
            conn = bpy.context.object
            conn.scale = (0.05, 0.05, 0.75)
            mat = create_neon_material(f"Conn{i}{z1}", NEON_COLORS[7])
            conn.data.materials.append(mat)
    
    render_white_bg(base_path + "tools/system_calls.png")

def create_process_threads():
    """Multi-threaded process visualization"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Main process
    bpy.ops.mesh.primitive_cylinder_add(location=(0, 0, 0))
    process = bpy.context.object
    process.scale = (0.5, 0.5, 3)
    process.rotation_euler = (1.57, 0, 0)
    mat = create_neon_material("Process", NEON_COLORS[2])
    process.data.materials.append(mat)
    
    # Threads spiraling around
    for i in range(4):
        color = NEON_COLORS[i * 2]
        
        for j in range(30):
            t = j / 30 * 4 * math.pi
            angle = t + (i * math.pi / 2)
            radius = 1.5
            
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = (j - 15) * 0.2
            
            bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
            thread = bpy.context.object
            thread.scale = (0.15, 0.15, 0.15)
            mat = create_neon_material(f"Thread{i}{j}", color)
            thread.data.materials.append(mat)
    
    render_white_bg(base_path + "tools/process_threads.png")

def create_io_streams():
    """Input/Output streams"""
    setup_scene()
    add_camera(location=(0, -12, 0), rotation=(1.57, 0, 0))
    add_area_light()
    
    # Input stream (left)
    for i in range(30):
        t = i / 10
        x = -4 + i * 0.1
        y = math.sin(t) * 2
        z = 0
        
        bpy.ops.mesh.primitive_cube_add(location=(x, y, z))
        input_data = bpy.context.object
        input_data.scale = (0.2, 0.2, 0.2)
        input_data.rotation_euler = (0, 0, t)
        mat = create_neon_material(f"Input{i}", NEON_COLORS[1])
        input_data.data.materials.append(mat)
    
    # Processing center
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 0))
    processor = bpy.context.object
    processor.scale = (1, 1, 1)
    mat = create_neon_material("Processor", NEON_COLORS[4], 4)
    processor.data.materials.append(mat)
    
    # Output stream (right)
    for i in range(30):
        t = i / 10
        x = 1 + i * 0.1
        y = math.cos(t) * 2
        z = 0
        
        bpy.ops.mesh.primitive_ico_sphere_add(location=(x, y, z))
        output_data = bpy.context.object
        output_data.scale = (0.15, 0.15, 0.15)
        mat = create_neon_material(f"Output{i}", NEON_COLORS[5])
        output_data.data.materials.append(mat)
    
    render_white_bg(base_path + "tools/io_streams.png")

# Run all visualizations
print("TOOLS CATEGORY:")
create_network_packets()
create_file_operations()
create_system_calls()
create_process_threads()
create_io_streams()

print("\n✨ Batch 1 complete!")