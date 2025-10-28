import bpy
from math import radians

# =============================================================================
# FUNÇÃO PRINCIPAL E DE LIMPEZA
# =============================================================================

def limpar_cena():
    """Apaga todos os objetos da cena para começar do zero."""
    # Seleciona todos os objetos
    bpy.ops.object.select_all(action='SELECT')
    # Apaga os objetos selecionados
    bpy.ops.object.delete(use_global=False)
    # Limpa dados órfãos para um arquivo limpo
    bpy.ops.outliner.orphans_purge()

def criar_material_simples(nome, cor_base, rugosidade=0.5, metalico=0.0):
    """Cria um material simples com cor, rugosidade e metalicidade."""
    mat = bpy.data.materials.new(name=nome)
    mat.use_nodes = True
    principled_bsdf = mat.node_tree.nodes.get('Principled BSDF')
    if principled_bsdf:
        principled_bsdf.inputs['Base Color'].default_value = cor_base
        principled_bsdf.inputs['Roughness'].default_value = rugosidade
        principled_bsdf.inputs['Metallic'].default_value = metalico
    return mat

# =============================================================================
# FUNÇÕES DE MODELAGEM
# =============================================================================

def criar_ambiente():
    """Cria o chão e as paredes da sala."""
    # Materiais
    mat_chao = criar_material_simples("MatChao", (0.1, 0.05, 0.03, 1), rugosidade=0.8) # Madeira escura
    mat_parede = criar_material_simples("MatParede", (0.8, 0.8, 0.8, 1), rugosidade=0.9)

    # Chão
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, 0, 0))
    chao = bpy.context.object
    chao.name = "Chao"
    chao.data.materials.append(mat_chao)

    # Parede Traseira
    bpy.ops.mesh.primitive_plane_add(size=10, location=(0, -5, 5), rotation=(radians(90), 0, 0))
    parede_tras = bpy.context.object
    parede_tras.name = "ParedeTras"
    parede_tras.data.materials.append(mat_parede)

    # Parede Esquerda
    bpy.ops.mesh.primitive_plane_add(size=10, location=(-5, 0, 5), rotation=(radians(90), 0, radians(90)))
    parede_esquerda = bpy.context.object
    parede_esquerda.name = "ParedeEsquerda"
    parede_esquerda.data.materials.append(mat_parede)

def criar_mesa():
    """Cria uma mesa de escritório simples."""
    mat_mesa = criar_material_simples("MatMesa", (0.9, 0.9, 0.9, 1), rugosidade=0.2, metalico=0.1) # Branco levemente metálico
    
    # Tampo da mesa
    bpy.ops.mesh.primitive_cube_add(location=(0, -3.5, 0.75))
    tampo = bpy.context.object
    tampo.name = "TampoMesa"
    tampo.scale = (1.5, 0.7, 0.03)
    tampo.data.materials.append(mat_mesa)
    
    # Pernas da mesa (simplificado)
    posicoes_pernas = [
        (-1.4, -4.1, 0.375),
        (1.4, -4.1, 0.375),
        (-1.4, -2.9, 0.375),
        (1.4, -2.9, 0.375)
    ]
    
    for i, pos in enumerate(posicoes_pernas):
        bpy.ops.mesh.primitive_cube_add(location=pos)
        perna = bpy.context.object
        perna.name = f"PernaMesa_{i+1}"
        perna.scale = (0.04, 0.04, 0.375)
        perna.data.materials.append(mat_mesa)
        # Une as pernas ao tampo
        perna.parent = tampo
        
def criar_setup_dev():
    """Cria o monitor, laptop, teclado e mouse."""
    mat_plastico_preto = criar_material_simples("MatPlasticoPreto", (0.01, 0.01, 0.01, 1), rugosidade=0.4)
    mat_metal_cinza = criar_material_simples("MatMetalCinza", (0.6, 0.6, 0.6, 1), rugosidade=0.2, metalico=0.8)

    # --- Monitor ---
    bpy.ops.mesh.primitive_cube_add(location=(0, -4.0, 1.1))
    monitor_tela = bpy.context.object
    monitor_tela.name = "MonitorTela"
    monitor_tela.scale = (0.8, 0.02, 0.45)
    monitor_tela.data.materials.append(mat_plastico_preto)
    
    bpy.ops.mesh.primitive_cube_add(location=(0, -3.95, 0.85))
    monitor_suporte = bpy.context.object
    monitor_suporte.name = "MonitorSuporte"
    monitor_suporte.scale = (0.04, 0.04, 0.2)
    monitor_suporte.data.materials.append(mat_plastico_preto)
    
    bpy.ops.mesh.primitive_cube_add(location=(0, -3.9, 0.77))
    monitor_base = bpy.context.object
    monitor_base.name = "MonitorBase"
    monitor_base.scale = (0.25, 0.15, 0.01)
    monitor_base.data.materials.append(mat_plastico_preto)

    # --- Laptop (Estilo Mac) ---
    bpy.ops.mesh.primitive_cube_add(location=(-0.8, -3.2, 0.78))
    laptop_base = bpy.context.object
    laptop_base.name = "LaptopBase"
    laptop_base.scale = (0.35, 0.25, 0.01)
    laptop_base.data.materials.append(mat_metal_cinza)

    bpy.ops.mesh.primitive_cube_add(location=(-0.8, -3.2 - 0.24, 0.78 + 0.01))
    laptop_tela = bpy.context.object
    laptop_tela.name = "LaptopTela"
    laptop_tela.scale = (0.35, 0.01, 0.25)
    laptop_tela.rotation_euler = (radians(100), 0, 0)
    laptop_tela.data.materials.append(mat_metal_cinza)

    # --- Periféricos ---
    bpy.ops.mesh.primitive_cube_add(location=(0, -3.2, 0.78))
    teclado = bpy.context.object
    teclado.name = "Teclado"
    teclado.scale = (0.4, 0.15, 0.01)
    teclado.data.materials.append(mat_plastico_preto)
    
    bpy.ops.mesh.primitive_cube_add(location=(0.55, -3.2, 0.78))
    mouse = bpy.context.object
    mouse.name = "Mouse"
    mouse.scale = (0.06, 0.1, 0.02)
    mod_bevel = mouse.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel.width = 0.015
    mod_bevel.segments = 3
    mouse.data.materials.append(mat_plastico_preto)
    
    # --- Caneca (Seção Corrigida) ---
    bpy.ops.mesh.primitive_cylinder_add(location=(1.0, -3.8, 0.82), radius=0.04, depth=0.1)
    caneca = bpy.context.object
    caneca.name = "Caneca"
    
    # Entra em modo de edição para manipular as faces
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode(type="FACE")
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')

    # Lógica robusta para encontrar a face do topo, não importando o índice
    altura_max = -99999.0
    index_topo = -1
    for face in caneca.data.polygons:
        # A face do topo é a que tem a maior coordenada Z em seu centro
        if face.center[2] > altura_max:
            altura_max = face.center[2]
            index_topo = face.index
    
    # Seleciona a face do topo se ela foi encontrada
    if index_topo != -1:
        caneca.data.polygons[index_topo].select = True

    # Continua o processo de deletar a face e solidificar
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.delete(type='FACE')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    mod_solid = caneca.modifiers.new(name="Solidify", type='SOLIDIFY')
    mod_solid.thickness = 0.005
    mat_caneca = criar_material_simples("MatCaneca", (1, 1, 1, 1), rugosidade=0.1)
    caneca.data.materials.append(mat_caneca)

def criar_paredes_e_estantes():
    """Cria a parede da direita e uma estante de livros."""
    mat_parede = bpy.data.materials.get("MatParede")
    mat_mesa = bpy.data.materials.get("MatMesa")

    bpy.ops.mesh.primitive_plane_add(size=10, location=(5, 0, 5), rotation=(radians(90), 0, radians(-90)))
    parede_direita = bpy.context.object
    parede_direita.name = "ParedeDireita"
    if mat_parede:
        parede_direita.data.materials.append(mat_parede)

    bpy.ops.mesh.primitive_cube_add(location=(4.9, -1.5, 2.0))
    estante_fundo = bpy.context.object
    estante_fundo.name = "EstanteFundo"
    estante_fundo.scale = (0.05, 1.2, 1.5)
    if mat_mesa:
        estante_fundo.data.materials.append(mat_mesa)

    for i in range(5):
        altura = 0.5 + (i * 0.75)
        bpy.ops.mesh.primitive_cube_add(location=(4.7, -1.5, altura))
        prateleira = bpy.context.object
        prateleira.name = f"Prateleira_{i+1}"
        prateleira.scale = (0.2, 1.2, 0.02)
        if mat_mesa:
            prateleira.data.materials.append(mat_mesa)
            
def criar_cadeira():
    """Cria uma cadeira de escritório básica."""
    mat_plastico_preto = bpy.data.materials.get("MatPlasticoPreto")
    
    pos_cadeira = (0, -2.5, 0)
    
    bpy.ops.mesh.primitive_cylinder_add(location=(pos_cadeira[0], pos_cadeira[1], 0.1), radius=0.03, depth=0.2)
    base_central = bpy.context.object
    base_central.name = "CadeiraBaseCentral"
    if mat_plastico_preto:
        base_central.data.materials.append(mat_plastico_preto)

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=pos_cadeira)
    eixo_array = bpy.context.object
    eixo_array.name = "EixoArrayCadeira"
    
    bpy.ops.mesh.primitive_cube_add(location=(pos_cadeira[0] + 0.2, pos_cadeira[1], 0.05))
    perna_base = bpy.context.object
    perna_base.name = "CadeiraPernaBase"
    perna_base.scale = (0.2, 0.03, 0.03)
    
    mod_array = perna_base.modifiers.new(name="ArrayPernas", type='ARRAY')
    mod_array.count = 5
    mod_array.use_relative_offset = False
    mod_array.use_object_offset = True
    mod_array.offset_object = eixo_array
    
    eixo_array.rotation_euler = (0, 0, radians(360 / 5))
    
    if mat_plastico_preto:
        perna_base.data.materials.append(mat_plastico_preto)

    bpy.ops.mesh.primitive_cube_add(location=(pos_cadeira[0], pos_cadeira[1], 0.45))
    assento = bpy.context.object
    assento.name = "CadeiraAssento"
    assento.scale = (0.4, 0.4, 0.05)
    
    mod_bevel_assento = assento.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel_assento.width = 0.04
    mod_bevel_assento.segments = 4
    
    if mat_plastico_preto:
        assento.data.materials.append(mat_plastico_preto)
        
    bpy.ops.mesh.primitive_cube_add(location=(pos_cadeira[0], pos_cadeira[1] + 0.3, 0.9))
    encosto = bpy.context.object
    encosto.name = "CadeiraEncosto"
    encosto.scale = (0.38, 0.05, 0.4)
    encosto.rotation_euler = (radians(-10), 0, 0)

    mod_bevel_encosto = encosto.modifiers.new(name="Bevel", type='BEVEL')
    mod_bevel_encosto.width = 0.04
    mod_bevel_encosto.segments = 4

    if mat_plastico_preto:
        encosto.data.materials.append(mat_plastico_preto)
            
def configurar_iluminacao_e_camera():
    """Configura a iluminação principal e a câmera da cena."""
    bpy.ops.object.light_add(type='AREA', location=(-2, -1, 2.5), rotation=(radians(-90), radians(-30), 0))
    luz_area = bpy.context.object
    luz_area.name = "LuzPrincipal"
    luz_area.data.size = 4
    luz_area.data.energy = 250

    bpy.ops.object.camera_add(location=(3.5, -0.5, 2.0), rotation=(radians(80), 0, radians(110)))
    camera = bpy.context.object
    camera.name = "Camera"
    
    camera.data.clip_start = 0.01
    
    bpy.context.scene.camera = camera

# =============================================================================
# SCRIPT PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    limpar_cena()
    criar_ambiente()
    criar_paredes_e_estantes()
    criar_mesa()
    criar_cadeira()
    criar_setup_dev()
    configurar_iluminacao_e_camera()
    print("Cena do escritório do desenvolvedor criada com sucesso!")