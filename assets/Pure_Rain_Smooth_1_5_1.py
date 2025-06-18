bl_info = {
    "name": "Pure Rain Smooth",
    "author": "Infame",
    "version": (1, 5, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N) > Tool > Pure Rain Smooth",
    "description": "Ruido emergente condicionado por curvatura con ráfagas en tiempo real.",
    "category": "Mesh",
}

import bpy
import bmesh
import random
import math
from mathutils import Vector
from bpy.props import FloatProperty, IntProperty, PointerProperty, BoolProperty

# --------------------------------------------------------------------
#  PROPIEDADES
# --------------------------------------------------------------------
class PureRainProps(bpy.types.PropertyGroup):
    intensity: FloatProperty(name="Intensity", default=1.0, min=0.0, max=5.0)
    density: FloatProperty(name="Density", default=0.7, min=0.0, max=1.0, subtype='PERCENTAGE')
    iterations: IntProperty(name="Iterations", default=5, min=1, max=500)
    steepness: FloatProperty(name="Logarithmic - Linear", default=2.0, min=0.1, max=10.0)
    max_disp: FloatProperty(name="Max Displacement", default=0.1, min=0.001, max=1.0)
    tangential_passes: BoolProperty(name="Tangent Rain", default=False)
    interleaved_passes: BoolProperty(name="Interleaved Tangents", default=False)

    # Burst mode
    loop_enabled: BoolProperty(name="Burst Mode", default=False)
    interval: FloatProperty(name="Interval (s)", default=0.2, min=0.01, max=5.0)
    _timer = None  # interno

# --------------------------------------------------------------------
#  OPERADOR DE GOLPE ÚNICO
# --------------------------------------------------------------------
class RAIN_OT_single(bpy.types.Operator):
    bl_idname = "mesh.pure_rain_once"
    bl_label = "Rain"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        props = context.scene.pure_rain_props
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        verts_sel = [v for v in bm.verts if v.select]
        if not verts_sel:
            self.report({'WARNING'}, "No selected verts")
            return {'CANCELLED'}

        def apply_rain_step(verts, direction_func):
            for v in verts:
                if random.random() > props.density:
                    continue
                direction = direction_func(v)
                neigh = [e.other_vert(v) for e in v.link_edges]
                if not neigh:
                    continue
                center = sum((n.co for n in neigh), Vector()) / len(neigh)
                elev = max((v.co - center).dot(direction), 0.0)
                log_coeff = math.log(1 + props.steepness * elev) / math.log(1 + props.steepness)
                disp = -direction * props.intensity * random.random() * log_coeff
                if disp.length > props.max_disp:
                    disp = disp.normalized() * props.max_disp
                v.co += disp

        tan1 = lambda v: v.normal.orthogonal().normalized()
        tan2 = lambda v: v.normal.cross(tan1(v)).normalized()

        if props.tangential_passes and props.interleaved_passes:
            for _ in range(props.iterations):
                apply_rain_step(verts_sel, lambda v: v.normal.normalized())
                apply_rain_step(verts_sel, tan1)
                apply_rain_step(verts_sel, tan2)
        else:
            for _ in range(props.iterations):
                apply_rain_step(verts_sel, lambda v: v.normal.normalized())
            if props.tangential_passes:
                for _ in range(props.iterations):
                    apply_rain_step(verts_sel, tan1)
                    apply_rain_step(verts_sel, tan2)

        bmesh.update_edit_mesh(obj.data)
        return {'FINISHED'}

# --------------------------------------------------------------------
#  TIMER CALLBACK PARA RÁFAGA
# --------------------------------------------------------------------

def rain_timer():
    props = bpy.context.scene.pure_rain_props
    if not props.loop_enabled:
        props._timer = None
        return None  # detener
    bpy.ops.mesh.pure_rain_once()
    return props.interval

# --------------------------------------------------------------------
#  OPERADORES PLAY / PAUSE
# --------------------------------------------------------------------
class RAIN_OT_play(bpy.types.Operator):
    bl_idname = "mesh.pure_rain_play"
    bl_label = "Start Rain"

    def execute(self, context):
        props = context.scene.pure_rain_props
        if props._timer is None:
            props.loop_enabled = True
            props._timer = bpy.app.timers.register(rain_timer, first_interval=props.interval)
        return {'FINISHED'}

class RAIN_OT_pause(bpy.types.Operator):
    bl_idname = "mesh.pure_rain_pause"
    bl_label = "Pause Rain"

    def execute(self, context):
        props = context.scene.pure_rain_props
        props.loop_enabled = False
        return {'FINISHED'}

# --------------------------------------------------------------------
#  PANEL UI
# --------------------------------------------------------------------
class VIEW3D_PT_pure_rain_smooth(bpy.types.Panel):
    bl_label = "Pure Rain Smooth"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'
    bl_context = "mesh_edit"

    def draw(self, context):
        p = context.scene.pure_rain_props
        col = self.layout.column(align=True)
        col.prop(p, "intensity", slider=True)
        col.prop(p, "density", slider=True)
        if not p.loop_enabled:
            col.prop(p, "iterations")
        col.prop(p, "steepness", slider=True)
        col.prop(p, "max_disp", slider=True)
        col.prop(p, "tangential_passes", toggle=True)
        if p.tangential_passes:
            col.prop(p, "interleaved_passes")
        col.separator()
        col.operator("mesh.pure_rain_once", icon='MOD_PHYSICS')
        col.separator()

        box = col.box()
        box.label(text="Burst Rain Mode", icon='TIME')
        box.prop(p, "interval")
        row = box.row(align=True)
        row.operator("mesh.pure_rain_play", text="Play", icon='PLAY')
        row.operator("mesh.pure_rain_pause", text="Pause", icon='PAUSE')

# --------------------------------------------------------------------
#  REGISTRO
# --------------------------------------------------------------------
classes = (
    PureRainProps,
    RAIN_OT_single,
    RAIN_OT_play,
    RAIN_OT_pause,
    VIEW3D_PT_pure_rain_smooth,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.pure_rain_props = PointerProperty(type=PureRainProps)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.pure_rain_props

if __name__ == "__main__":
    register()
