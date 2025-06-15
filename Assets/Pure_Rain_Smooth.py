bl_info = {
    "name": "Pure Rain Smooth",
    "author": "Infame",
    "version": (1, 2, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar (N) > Tool > Pure Rain Smooth",
    "description": "Ruido emergente condicionado por curvatura con amplificación exponencial por iteración.",
    "category": "Mesh",
}

import bpy
import bmesh
import random
from mathutils import Vector
from bpy.props import FloatProperty, IntProperty, PointerProperty, BoolProperty

# --------------------------------------------------------------------
#  PROPIEDADES
# --------------------------------------------------------------------
class PureRainProps(bpy.types.PropertyGroup):
    intensity: FloatProperty(
        name="Intensity",
        default=0.5, min=0.0, max=5.0,
        description="Magnitud inicial del desplazamiento por gota"
    )
    density: FloatProperty(
        name="Density",
        default=0.7, min=0.0, max=1.0,
        subtype='PERCENTAGE',
        description="Probabilidad de que un vértice reciba una gota en cada pasada"
    )
    iterations: IntProperty(
        name="Iterations",
        default=30, min=1, max=500,
        description="Número de pasadas del algoritmo"
    )
    growth_ui: FloatProperty(
        name="Exponential Factor",
        default=0.5, min=0.0, max=1.0,
        description="Controla cuánto crece el efecto con cada iteración"
    )
    tangential_passes: BoolProperty(
        name="Tangent Rain",
        default=False,
        description="Aplica el suavizado también en direcciones X e Y relativas a la normal"
    )

# --------------------------------------------------------------------
#  OPERADOR PRINCIPAL
# --------------------------------------------------------------------
class RAIN_OT_pure_smooth(bpy.types.Operator):
    bl_idname = "mesh.pure_rain_smooth"
    bl_label = "Pure Rain Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    intensity: FloatProperty()
    density: FloatProperty()
    iterations: IntProperty()
    growth_ui: FloatProperty()
    tangential_passes: BoolProperty()

    @classmethod
    def poll(cls, context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.mode == 'EDIT_MESH')

    def apply_rain(self, verts_sel, direction_func, growth, intensity, density, iterations):
        max_disp = 0.05
        for it in range(iterations):
            amp = intensity * (growth ** it)
            for v in verts_sel:
                if random.random() > density:
                    continue

                direction = direction_func(v)

                neigh = [e.other_vert(v) for e in v.link_edges]
                if not neigh:
                    continue

                center = sum((n.co for n in neigh), Vector()) / len(neigh)
                signed_curv = (v.co - center).dot(direction)

                noise = Vector((
                    random.uniform(-1, 1),
                    random.uniform(-1, 1),
                    random.uniform(-1, 1)
                )).normalized()

                if signed_curv * noise.dot(direction) < 0:
                    disp = noise * abs(signed_curv) * amp * 0.01
                    if disp.length > max_disp:
                        disp = disp.normalized() * max_disp
                    v.co += disp

    def execute(self, context):
        obj = context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        verts_sel = [v for v in bm.verts if v.select]

        if not verts_sel:
            self.report({'WARNING'}, "¡No Selected Verts!")
            return {'CANCELLED'}

        growth = 1.0 + self.growth_ui * 0.3

        # Paso principal: normal local
        self.apply_rain(
            verts_sel,
            lambda v: v.normal.normalized(),
            growth,
            self.intensity,
            self.density,
            self.iterations
        )

        # Opcional: pasadas tangenciales locales
        if self.tangential_passes:
            def tan1(v):
                return v.normal.orthogonal().normalized()

            def tan2(v):
                return v.normal.cross(tan1(v)).normalized()

            self.apply_rain(verts_sel, tan1, growth, self.intensity, self.density, self.iterations)
            self.apply_rain(verts_sel, tan2, growth, self.intensity, self.density, self.iterations)

        bmesh.update_edit_mesh(obj.data)
        self.report({'INFO'}, f"Pure Rain Smooth aplicado con {self.iterations} iteraciones y growth_ui {self.growth_ui:.2f}")
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
        props = context.scene.pure_rain_props
        col = self.layout.column(align=True)
        col.prop(props, "intensity", slider=True)
        col.prop(props, "density", slider=True)
        col.prop(props, "iterations")
        col.prop(props, "growth_ui", slider=True)
        col.prop(props, "tangential_passes",toggle=True)
        col.separator()
        op = col.operator("mesh.pure_rain_smooth", text="Rain")
        op.intensity = props.intensity
        op.density = props.density
        op.iterations = props.iterations
        op.growth_ui = props.growth_ui
        op.tangential_passes = props.tangential_passes

# --------------------------------------------------------------------
#  REGISTRO
# --------------------------------------------------------------------
classes = (
    PureRainProps,
    RAIN_OT_pure_smooth,
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
