import bpy
from ..utilities.settings import Settings


class WorkingSpaceMenu(bpy.types.Panel):
    bl_label = 'Render Raw Working Space'
    bl_idname = 'RENDER_PT_render_raw_working_space'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'render'
    bl_ui_units_x = 14

    @classmethod
    def poll(self, context):
        RR = Settings(context)
        try:
            return RR.props_group
        except:
            return False

    def draw(self, context):
        RR = Settings(context)
        col = self.layout.column()
        col.use_property_split = True
        col.use_property_decorate = False

        if bpy.app.version >= (5, 0, 0):
            col.label(text='File', icon='FILEBROWSER')
            flow = col.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=True)
            split = flow.column().split(factor=0.4)
            row = split.row()
            row.label(text="Working Space")
            row.alignment = 'RIGHT'
            split.operator_menu_enum(
                "wm.set_working_color_space", 
                "working_space", 
                text=context.blend_data.colorspace.working_space
            )

            col.separator(factor=2)
            col.label(text='Scene', icon='SCENE_DATA')
            col.prop(context.scene.sequencer_colorspace_settings, 'name', text='Sequencer Space')
            col.separator()
            col.row().prop(context.scene.display_settings, 'emulation', text='Display Emulation', expand=True)

            col.separator(factor=2)
            col.label(text='Render Raw Node', icon='NODETREE')
            col.prop(RR.props_group, 'display')
            col.separator()
            col.prop(RR.props_group, 'view_transform')
            col.separator()

        else:
            col.prop(context.scene.display_settings, 'display_device')
            col.separator()
            col.prop(context.scene.sequencer_colorspace_settings, 'name', text='Sequencer Space')


def register():
    bpy.utils.register_class(WorkingSpaceMenu)

def unregister():
    bpy.utils.unregister_class(WorkingSpaceMenu)