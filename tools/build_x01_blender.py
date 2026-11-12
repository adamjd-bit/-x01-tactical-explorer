import bpy, json, math, os, sys, urllib.request, urllib.error
from mathutils import Vector

# X01 Black Site procedural reconstruction builder.
# Geometry is a reference-led reconstruction, not extracted game geometry.
args = sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
def arg(flag, default):
    return args[args.index(flag)+1] if flag in args and args.index(flag)+1 < len(args) else default
src = arg("--input", "data/x01-map-data.json")
out = arg("--output", "assets/x01-reconstruction.glb")
blend_out = arg("--blend", "assets/x01-reconstruction.blend")
with open(src, "r", encoding="utf-8") as f: DATA=json.load(f)

bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections):
    if c.name != "Collection": bpy.data.collections.remove(c)
root=bpy.context.scene.collection
def collection(name):
    c=bpy.data.collections.new(name); root.children.link(c); return c
def move_to(obj, col):
    for c in list(obj.users_collection): c.objects.unlink(obj)
    col.objects.link(obj); return obj
# Download real photographic CC0 PBR maps from Poly Haven at build time.
# If the service is unavailable, the procedural shader below remains a safe fallback.
TEXTURE_DIR=os.path.join(os.path.dirname(out) or ".", "textures")
os.makedirs(TEXTURE_DIR,exist_ok=True)
PH_MAPS={}
def flatten_file_records(node, trail=()):
    if isinstance(node,dict):
        if isinstance(node.get("url"),str):
            yield (trail,node)
        else:
            for key,value in node.items():
                yield from flatten_file_records(value,trail+(str(key),))
    elif isinstance(node,list):
        for index,value in enumerate(node):
            yield from flatten_file_records(value,trail+(str(index),))
def fetch_polyhaven_asset(slug):
    try:
        req=urllib.request.Request("https://api.polyhaven.com/files/"+slug,headers={"User-Agent":"X01TacticalExplorer/1.0 (Poly Haven CC0 texture pipeline)"})
        with urllib.request.urlopen(req,timeout=25) as response:
            payload=json.loads(response.read().decode("utf-8"))
        records=list(flatten_file_records(payload))
        def choose(kind):
            ranked=[]
            for trail,item in records:
                url=item["url"].lower()
                key="/".join(trail).lower()+" "+url
                if not url.endswith((".jpg",".jpeg",".png",".tif",".tiff")): continue
                if kind=="diff" and not any(x in key for x in ("diff","albedo","color")): continue
                if kind=="normal" and not any(x in key for x in ("nor_gl","normal")): continue
                if kind=="rough" and "rough" not in key: continue
                score=(100 if "1k" in key else 50 if "2k" in key else 0)+(20 if url.endswith(".jpg") else 0)
                ranked.append((score,item["url"]))
            return sorted(ranked,reverse=True)[0][1] if ranked else None
        for kind in ("diff","normal","rough"):
            url=choose(kind)
            if not url: continue
            ext=".jpg" if ".jpg" in url.lower() else ".png"
            path=os.path.join(TEXTURE_DIR,slug+"_"+kind+ext)
            if not os.path.isfile(path) or os.path.getsize(path)<1024:
                req=urllib.request.Request(url,headers={"User-Agent":"X01TacticalExplorer/1.0"})
                with urllib.request.urlopen(req,timeout=60) as response,open(path,"wb") as target:
                    target.write(response.read())
            if os.path.getsize(path)>1024:
                PH_MAPS[(slug,kind)]=path
        print("Poly Haven CC0:",slug,[k[1] for k in PH_MAPS if k[0]==slug])
    except Exception as exc:
        print("Poly Haven texture fallback:",slug,str(exc))
for asset in ("concrete","concrete_floor_01","rusty_painted_metal","corrugated_iron"):
    fetch_polyhaven_asset(asset)

def image_node(nt,path,label,location,color_space="sRGB"):
    if not path: return None
    try:
        image=bpy.data.images.load(path,check_existing=True)
        image.colorspace_settings.name=color_space
        node=nt.nodes.new("ShaderNodeTexImage"); node.image=image; node.label=label
        node.location=location; node.extension="REPEAT"
        return node
    except Exception as exc:
        print("Texture image load fallback:",path,str(exc)); return None

def mat(name, color, metallic=0.0, rough=.7, emission=None, estr=0.0):
    # Procedural PBR surface: layered tonal breakup, fine aggregate and micro-relief.
    # These are shader-generated materials, not AI image textures or claimed game rips.
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    nt=m.node_tree; nt.nodes.clear()
    out=nt.nodes.new("ShaderNodeOutputMaterial"); out.location=(620,80)
    bs=nt.nodes.new("ShaderNodeBsdfPrincipled"); bs.location=(360,80)
    bs.inputs["Metallic"].default_value=metallic
    bs.inputs["Roughness"].default_value=rough
    tex=nt.nodes.new("ShaderNodeTexCoord"); tex.location=(-820,120)
    broad=nt.nodes.new("ShaderNodeTexNoise"); broad.location=(-610,210)
    broad.inputs["Scale"].default_value=7.5 if metallic < .35 else 24.0
    broad.inputs["Detail"].default_value=5.0
    broad.inputs["Roughness"].default_value=.78
    nt.links.new(tex.outputs["Generated"],broad.inputs["Vector"])
    ramp=nt.nodes.new("ShaderNodeValToRGB"); ramp.location=(-340,230)
    base=color
    def tint(v):
        return (max(0,min(1,v[0])),max(0,min(1,v[1])),max(0,min(1,v[2])),1)
    ramp.color_ramp.elements[0].position=.18
    ramp.color_ramp.elements[0].color=tint(tuple(c*.58 for c in base))
    ramp.color_ramp.elements[1].position=.82
    ramp.color_ramp.elements[1].color=tint(tuple(c*1.22 for c in base))
    nt.links.new(broad.outputs["Fac"],ramp.inputs["Fac"])
    nt.links.new(ramp.outputs["Color"],bs.inputs["Base Color"])
    # Prefer photographed CC0 albedo/normal/roughness maps for the matching surface.
    asset=None
    lname=name.lower()
    if "concrete" in lname and "floor" in lname: asset="concrete_floor_01"
    elif "concrete" in lname or "poured" in lname: asset="concrete"
    elif "steel" in lname or "metal" in lname or "graphite" in lname: asset="rusty_painted_metal"
    if asset:
        uv=nt.nodes.new("ShaderNodeTexCoord"); uv.location=(-820,-360)
        diff=image_node(nt,PH_MAPS.get((asset,"diff")),"Poly Haven CC0 albedo",(-570,-360),"sRGB")
        normal=image_node(nt,PH_MAPS.get((asset,"normal")),"Poly Haven CC0 normal",(-570,-610),"Non-Color")
        roughmap=image_node(nt,PH_MAPS.get((asset,"rough")),"Poly Haven CC0 roughness",(-570,-850),"Non-Color")
        if diff:
            nt.links.new(uv.outputs["Generated"],diff.inputs["Vector"])
            nt.links.new(diff.outputs["Color"],bs.inputs["Base Color"])
        if roughmap:
            nt.links.new(uv.outputs["Generated"],roughmap.inputs["Vector"])
            nt.links.new(roughmap.outputs["Color"],bs.inputs["Roughness"])
        if normal:
            nt.links.new(uv.outputs["Generated"],normal.inputs["Vector"])
            normalmap=nt.nodes.new("ShaderNodeNormalMap"); normalmap.location=(80,-430)
            nt.links.new(normal.outputs["Color"],normalmap.inputs["Color"])
            nt.links.new(normalmap.outputs["Normal"],bs.inputs["Normal"])
    fine=nt.nodes.new("ShaderNodeTexNoise"); fine.location=(-600,-160)
    fine.inputs["Scale"].default_value=145.0 if metallic > .35 else 68.0
    fine.inputs["Detail"].default_value=2.5
    fine.inputs["Roughness"].default_value=.82
    nt.links.new(tex.outputs["Generated"],fine.inputs["Vector"])
    bump=nt.nodes.new("ShaderNodeBump"); bump.location=(100,-100)
    bump.inputs["Strength"].default_value=.22 if metallic < .35 else .14
    bump.inputs["Distance"].default_value=.035 if rough > .7 else .012
    nt.links.new(fine.outputs["Fac"],bump.inputs["Height"])
    nt.links.new(bump.outputs["Normal"],bs.inputs["Normal"])
    nt.links.new(bs.outputs["BSDF"],out.inputs["Surface"])
    if emission:
        bs.inputs["Emission Color"].default_value=(*emission,1)
        bs.inputs["Emission Strength"].default_value=estr
    return m
concrete=mat("Worn poured concrete",(0.29,.32,.32),0,.92)
floor_mat=mat("Industrial sealed concrete",(0.20,.23,.23),.12,.84)
steel=mat("Oxidised structural steel",(.19,.23,.24),.72,.48)
dark=mat("Graphite equipment",(.045,.06,.065),.5,.62)
trim=mat("Safety olive",(.29,.34,.19),.35,.58)
amber=mat("Hazard amber",(.82,.39,.075),.35,.45, (.25,.07,.01),.3)
cyan=mat("Terminal cyan",(.035,.35,.39),.3,.28,(.02,.45,.58),2.2)
green=mat("Terminal phosphor",(.10,.36,.16),.2,.32,(.08,.55,.18),1.8)
glass=mat("Armoured dark glass",(.08,.16,.17),.35,.2)
labelmat=mat("Room identification",(.72,.78,.66),.05,.5,(.24,.30,.18),.5)
profiles={
"Deep Vault":(3.15,2.9,["east","south"]),
"Supply Depot":(2.95,2.8,["south","west","east"]),
"Pump Station":(2.85,2.8,["west","south","east"]),
"Power Generators":(2.85,2.8,["west","north","east","south"]),
"T.E.C.H. Lab":(2.95,2.9,["west","east","south"]),
"Bio Lab":(2.95,2.85,["west","north","east"]),
"Medical Wing":(3.05,2.85,["north","east"]),
"Production Assembly":(3.35,3.05,["north","east","west"]),
"Data Center":(3.45,3.15,["west","south"]),
"Cargo Bay":(3.35,3.05,["east","south"]),
"Control Room":(3.0,2.8,["west","south","east"]),
"Main Warehouse":(3.5,3.2,["north","west","east","south"]),
"Motor Pool":(3.3,3.0,["north","west"]),
"Admin Offices":(3.0,2.9,["east","south"])}
def sector(g):
    col=ord(g[0])-ord("A"); row=int(g[1])
    return (col*4-18, (row-4.5)*4)
def center(a, floor):
    # Room anchors follow the published X01 sector grid. Do not offset rooms
    # to compensate for old duplicate-sector guesses; source conflicts stay
    # documented in x01-map-data.json until confirmed by in-game references.
    return sector(a["grid"])
def cube(name, loc, scale, material, col, bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name
    o.dimensions=scale; bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    o.data.materials.append(material); move_to(o,col)
    if bevel:
        mod=o.modifiers.new("Machined edge radii","BEVEL"); mod.width=bevel; mod.segments=2
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    return o
def cyl(name, loc, radius, depth, material, col, vertices=24, rot=None):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=loc)
    o=bpy.context.object; o.name=name; o.data.materials.append(material); move_to(o,col)
    if rot:o.rotation_euler=rot
    return o
def text_obj(body, loc, size, col):
    cu=bpy.data.curves.new("ID_"+body.replace(" ","_"),"FONT"); cu.body=body.upper(); cu.size=size; cu.extrude=.002
    ob=bpy.data.objects.new("Label_"+body,cu); col.objects.link(ob); ob.location=loc
    ob.rotation_euler=(math.pi/2,0,0); cu.materials.append(labelmat); return ob
def wall_segment(x,z,length,axis,y, col, h=2.65):
    # Wall run parallel to X or Z, with layered concrete core and steel impact strip.
    if axis=="x":
        cube("Concrete bulkhead",(x,y+h/2,z),(length,h,.22),concrete,col,.035)
        cube("Lower steel impact rail",(x,y+.42,z-.125),(length,.22,.055),steel,col,.018)
        cube("Upper service raceway",(x,y+h-.24,z-.14),(length,.18,.10),steel,col,.018)
        for i in range(max(1,int(length/1.35))):
            xx=x-length/2+(i+.5)*length/max(1,int(length/1.35))
            cube("Wall reinforcement rib",(xx,y+h/2,z-.14),(.075,h-.18,.09),steel,col,.012)
    else:
        cube("Concrete bulkhead",(x,y+h/2,z),(.22,h,length),concrete,col,.035)
        cube("Lower steel impact rail",(x-.125,y+.42,z),(.055,.22,length),steel,col,.018)
        cube("Upper service raceway",(x-.14,y+h-.24,z),(.10,.18,length),steel,col,.018)
        for i in range(max(1,int(length/1.35))):
            zz=z-length/2+(i+.5)*length/max(1,int(length/1.35))
            cube("Wall reinforcement rib",(x-.14,y+h/2,zz),(.09,h-.18,.075),steel,col,.012)
def room(a, floor, col, y):
    n=a["name"]; x,z=center(a,floor); w,d,entries=profiles.get(n,(3.8,3.4,["south"]))
    cube(n+" floor slab",(x,y+.02,z),(w,.18,d),floor_mat,col,.035)
    # Perimeter walls have door-sized openings at the listed entry sides.
    for side in ["north","south","east","west"]:
        if side in ("north","south"):
            zz=z+(-d/2 if side=="north" else d/2)
            if side in entries:
                gap=1.55; seg=(w-gap)/2
                wall_segment(x-(gap/2+seg/2),zz,seg,"x",y,col)
                wall_segment(x+(gap/2+seg/2),zz,seg,"x",y,col)
                cube("Blast door frame",(x,y+1.32,zz),(1.68,2.64,.28),amber,col,.045)
                cube("Recessed blast door",(x,y+1.18,zz-.07),(.72,2.24,.12),dark,col,.035)
            else: wall_segment(x,zz,w,"x",y,col)
        else:
            xx=x+(-w/2 if side=="west" else w/2)
            if side in entries:
                gap=1.55; seg=(d-gap)/2
                wall_segment(xx,z-(gap/2+seg/2),seg,"z",y,col)
                wall_segment(xx,z+(gap/2+seg/2),seg,"z",y,col)
                cube("Blast door frame",(xx,y+1.32,z),( .28,2.64,1.68),amber,col,.045)
                cube("Recessed blast door",(xx-.07,y+1.18,z),(.12,2.24,.72),dark,col,.035)
            else: wall_segment(xx,z,d,"z",y,col)
    # Ceiling framing and visible utility services; open-top presentation.
    for sx in [-1,1]:
        cube("Ceiling girder",(x+sx*(w/2-.12),y+2.48,z),(.14,.18,d+.15),steel,col,.025)
    for zz in [-1,1]:
        cube("Ceiling cross beam",(x,y+2.48,z+zz*(d/2-.12)),(w,.18,.14),steel,col,.025)
    cube("Cable tray",(x,y+2.30,z-d*.30),(w*.72,.10,.20),dark,col,.02)
    # Service conduits, junction boxes, industrial light fittings and safety details.
    for side in [-1,1]:
        conduit=cyl("Wall conduit",(x+side*(w/2-.30),y+2.03,z),.035,d*.82,steel,col,12,(math.pi/2,0,0))
        cube("Electrical junction box",(x+side*(w/2-.29),y+1.78,z-d*.22),(.16,.22,.20),dark,col,.025)
    lightmat=mat("Cool white industrial emitter",(.72,.80,.73),.05,.3,(.62,.78,.68),2.8)
    for dx in [-w*.25,w*.25]:
        cube("Recessed industrial ceiling light",(x+dx,y+2.56,z),(.78,.055,.20),lightmat,col,.025)
        cube("Light housing",(x+dx,y+2.61,z),(.90,.07,.28),steel,col,.02)
    # Drain channel and bolted service plates break up otherwise uniform floors.
    cube("Floor drainage channel",(x-w*.34,y+.125,z),(.22,.025,d*.62),dark,col,.01)
    for k in range(5):
        cube("Drain grate bar",(x-w*.34,y+.145,z-d*.27+k*d*.135),(.24,.025,.035),steel,col,.006)
    # Functional set dressing per room type.
    low=n.lower()
    if "data center" in low or "admin offices" in low or "control room" in low:
        for ix in range(4):
            xx=x-w*.34+ix*(w*.22)
            cube("Server rack",(xx,y+.92,z-d*.23),(.48,1.82,.58),dark,col,.035)
            for j in range(5):
                cube("Rack equipment face",(xx,y+.42+j*.29,z-d*.23-.30),(.37,.045,.025),steel,col,.008)
                cube("Rack status LED",(xx+.14,y+.45+j*.29,z-d*.23-.32),(.045,.05,.025),green,col,.005)
        cube("Operator console",(x,y+.52,z+d*.25),(w*.68,.16,.55),steel,col,.025)
        for ix in [-1,0,1]:
            cube("Glowing monitor",(x+ix*.58,y+1.05,z+d*.25-.22),(.48,.40,.07),cyan,col,.025)
    elif "bio lab" in low:
        for ix in [-1,1]:
            xx=x+ix*.78
            cyl("Biological containment vessel",(xx,y+1.0,z),.34,1.55,glass,col)
            cyl("Vessel hazard cap",(xx,y+1.8,z),.38,.12,amber,col)
            cyl("Containment fluid core",(xx,y+.78,z),.24,.78,green,col)
        cube("Lab workbench",(x,y+.48,z+d*.28),(w*.68,.12,.65),steel,col,.025)
    elif "production" in low:
        cube("Assembly conveyor",(x,y+.48,z),(w*.78,.18,.72),dark,col,.035)
        for ix in range(8):
            cyl("Conveyor roller",(x-w*.34+ix*.29,y+.61,z),.075,.72,steel,col,16,(math.pi/2,0,0))
        for ix in [-1,1]:
            cube("Assembly gantry upright",(x+ix*1.25,y+1.2,z-d*.28),(.15,1.5,.16),amber,col,.02)
        cube("Overhead gantry beam",(x,y+1.9,z-d*.28),(w*.82,.16,.18),steel,col,.025)
    elif "generator" in low or "pump" in low:
        for ix in [-1,1]:
            cube("Industrial generator housing",(x+ix*.68,y+.76,z),(.85,1.2,1.05),dark,col,.06)
            cyl("Generator ventilation fan",(x+ix*.68,y+.78,z-.55),.30,.08,steel,col,32,(math.pi/2,0,0))
            cyl("Fan hub",(x+ix*.68,y+.78,z-.61),.09,.10,amber,col,16,(math.pi/2,0,0))
        for ix in range(3):
            cyl("Overhead pipe run",(x-w*.32+ix*.65,y+2.08,z+d*.28),.055,w*.55,steel,col,16,(0,math.pi/2,0))
    elif "vault" in low:
        cyl("Vault locking ring",(x,y+.15,z),1.0,.10,amber,col,48)
        cube("Vault secure container",(x,y+.72,z), (1.55,1.35,.95),dark,col,.08)
        for ix in [-1,1]:
            cyl("Vault locking wheel",(x+ix*.88,y+1.0,z-.5),.28,.10,steel,col,32,(math.pi/2,0,0))
    elif "medical" in low or "test chamber" in low or "tech" in low:
        cube("Examination bench",(x,y+.52,z),(w*.62,.18,.72),steel,col,.04)
        for ix in [-1,1]:
            cube("Medical equipment trolley",(x+ix*.85,y+.48,z-d*.20),(.38,.86,.38),dark,col,.025)
            cube("Medical display",(x+ix*.85,y+1.1,z-d*.20),(.32,.28,.06),green,col,.02)
    elif "warehouse" in low or "cargo" in low or "supply" in low or "motor" in low:
        for ix in [-1,1]:
            cube("Industrial storage rack",(x+ix*(w*.34),y+1.0,z),(.22,1.9,d*.72),steel,col,.025)
            for lev in range(3):
                cube("Storage shelf",(x+ix*(w*.34),y+.42+lev*.55,z),(.72,.07,d*.68),amber if lev==0 else dark,col,.018)
        if "motor" in low:
            for ix in [-1,1]:
                cube("Vehicle bay floor marking",(x+ix*.9,y+.13,z),(.08,.025,d*.72),amber,col)
    text_obj(n,(x,y+2.72,z),.27,col)

floors={}
for floor in DATA["floors"]:
    fid=floor["id"]; y=0 if fid=="lower" else 4.3
    col=collection("X01_"+fid.upper()); floors[fid]=(col,y)
    cube("Foundation slab "+fid,(0,y-.25,0),(43,.5,43),floor_mat,col,.06)
    for xx,zz,sx,sz in [(0,-21,43,.5),(0,21,43,.5),(-21,0,.5,43),(21,0,.5,43)]:
        cube("Outer perimeter wall",(xx,y+.68,zz),(sx,1.36,sz),concrete,col,.04)
    for a in floor["areas"]: room(a,fid,col,y)
    # Main passages connecting adjacent functional rooms, aligned from sector centres.
    names={a["name"]:a for a in floor["areas"]}
    links=([("Deep Vault","Medical Wing"),("Medical Wing","T.E.C.H. Lab"),("T.E.C.H. Lab","Bio Lab"),("Bio Lab","Pump Station"),("Pump Station","Power Generators"),("Power Generators","Supply Depot"),("T.E.C.H. Lab","Production Assembly"),("Production Assembly","Data Center")] if fid=="lower" else [("Cargo Bay","Control Room"),("Control Room","Power Generators"),("Control Room","Main Warehouse"),("Main Warehouse","Admin Offices"),("Main Warehouse","Motor Pool")])
    for aa,bb in links:
        if aa not in names or bb not in names: continue
        ax,az=center(names[aa],fid); bx,bz=center(names[bb],fid)
        dx=bx-ax; dz=bz-az; length=math.hypot(dx,dz)
        if length<.1: continue
        # Segmented corridor floor with low curbs; open roof for exploration visibility.
        mx=(ax+bx)/2; mz=(az+bz)/2; angle=math.atan2(dx,dz)
        hall=cube("Connecting passage",(mx,y+.01,mz),(1.75,.12,length),floor_mat,col,.025); hall.rotation_euler[1]=angle
        for side in [-1,1]:
            off=Vector((math.cos(angle),0,-math.sin(angle)))*side*.90
            rail=cube("Passage wall",(mx+off.x,y+1.15,mz+off.z),(.16,2.3,length),concrete,col,.025); rail.rotation_euler[1]=angle
    # Sector-coordinate reference discs are deliberately subdued.
    for a in floor["areas"]:
        x,z=center(a,fid); cyl("Room locator",(x,y+.13,z),.13,.025,trim,col,16)
    # Feature assets from verified sector references.
    for f in DATA.get("features",[]):
        if fid not in f.get("floors",[]): continue
        x,z=sector(f["grid"]); typ=f["type"]
        if typ=="stairs":
            for st in range(7):
                cube("Steel stair tread",(x,y+.12+st*.18,z-.75+st*.23),(.9,.12,.24),steel,col,.015)
        elif typ=="ascender":
            cyl("Rope ascender",(x,y+1.45,z),.055,2.8,amber,col,16)
        elif typ=="exfil":
            cyl("Extraction lift marker",(x,y+.22,z),.40,.12,cyan,col,24)
        elif typ=="station":
            cube(f["name"],(x,y+.60,z),(.8,1.1,.7),dark,col,.04)
            cube("Station illuminated display",(x,y+1.0,z-.37),(.48,.34,.05),green,col,.015)
    for m in DATA.get("markers",[]):
        if m["floor"]!=fid: continue
        x,z=sector(m["grid"]); cyl("Key room marker",(x,y+.20,z),.24,.08,amber,col,24)
        text_obj(m["name"],(x,y+2.82,z),.14,col)
# Preserve the two Blender collections as named roots in the exported GLB.
# The web viewer uses these nodes to switch floors without rebuilding geometry.
for fid, (col, floor_y) in floors.items():
    root_obj=bpy.data.objects.new("FLOOR_"+fid.upper()+"_ROOT", None)
    col.objects.link(root_obj)
    root_obj.empty_display_type="PLAIN_AXES"
    root_obj.location=(0,0,0)
    for obj in list(col.objects):
        if obj is root_obj: continue
        obj.parent=root_obj
        obj.matrix_parent_inverse=root_obj.matrix_world.inverted()

# Scene metadata and export.
scene=bpy.context.scene
scene.render.engine="BLENDER_EEVEE_NEXT" if hasattr(bpy.types,"BLENDER_EEVEE_NEXT") else "BLENDER_EEVEE"
scene.render.resolution_x=1600; scene.render.resolution_y=900; scene.render.resolution_percentage=100
scene.world.color=(.045,.055,.06)
# Camera and lights make the .blend immediately inspectable; web viewer supplies its own lighting.
bpy.ops.object.light_add(type="AREA", location=(0,14,-12)); bpy.context.object.data.energy=2400; bpy.context.object.data.shape="DISK"; bpy.context.object.data.size=16
bpy.ops.object.camera_add(location=(34,42,-46)); cam=bpy.context.object; cam.rotation_euler=(math.radians(42),0,math.radians(35)); cam.data.lens=48; scene.camera=cam
os.makedirs(os.path.dirname(out) or ".",exist_ok=True)
os.makedirs(os.path.dirname(blend_out) or ".",exist_ok=True)
bpy.ops.wm.save_as_mainfile(filepath=blend_out)
bpy.ops.object.select_all(action="SELECT")
bpy.ops.export_scene.gltf(filepath=out,export_format="GLB",use_selection=True,export_apply=True)
print("X01 Blender build complete:",out)
