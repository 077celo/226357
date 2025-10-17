import bpy


def toggle_handlers(is_enabled, fn, handlers):
    fn_name = str(fn).split(' ')[1]
    for handler_list in handlers:
        has_handler = False
        for handler_name in [str(x) for x in handler_list]:
            if fn_name in handler_name:
                has_handler = True
        if is_enabled and not has_handler:
            handler_list.append(fn)
        elif not is_enabled and has_handler:
            handler_list.remove(fn)