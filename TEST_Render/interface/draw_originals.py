import gpu


def draw_original_curves(self, context):
        layout = self.layout
        scene = context.scene
        view = scene.view_settings
        layout.use_property_split = False
        layout.use_property_decorate = False  # No animation.
        layout.enabled = view.use_curve_mapping
        layout.template_curve_mapping(view, "curve_mapping", type='COLOR', levels=True)


def draw_original_display(self, context):
    col = self.layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    col.enabled = context.scene.view_settings.view_transform == 'Standard' and gpu.capabilities.hdr_support_get()
    col.prop(context.scene.view_settings, 'use_hdr_view')


def draw_original_white_balance(self, context):
    col = self.layout.column()
    col.use_property_split = True
    col.use_property_decorate = False
    col.active = context.scene.view_settings.use_white_balance
    col.prop(context.scene.view_settings, 'white_balance_temperature')
    col.prop(context.scene.view_settings, 'white_balance_tint')


def draw_original_working_space(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False  # No animation.

        scene = context.scene
        blend_colorspace = context.blend_data.colorspace

        flow = layout.grid_flow(row_major=True, columns=0, even_columns=False, even_rows=False, align=True)

        col = flow.column()

        split = col.split(factor=0.4)
        row = split.row()
        row.label(text="File")
        row.alignment = 'RIGHT'
        split.operator_menu_enum("wm.set_working_color_space", "working_space", text=blend_colorspace.working_space)

        col.prop(scene.sequencer_colorspace_settings, "name", text="Sequencer")
     