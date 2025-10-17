import bpy
from ..utilities.settings import Settings
from .update_RR import update_all


def update_layer_name(self, context):
    # Called when the layer name property on the Pre node is changed
    # Currently nothing else needs to be done
    pass


def update_active_layer(self, context):
    # Called when the layer is switched via the UI
    # Currently nothing else needs to be done
    pass


def update_layer_factor(self, context, RR_group=None, layer_index=None):
    if bpy.app.version >= (4, 5, 0):
        RR = Settings(context, RR_group, layer_index)
        RR.layer_pre.inputs['Factor'].default_value = RR.props_pre.layer_factor
        RR.layer_post.inputs['Factor'].default_value = RR.props_pre.layer_factor
    else:
        update_all(self, context, RR_group, layer_index)