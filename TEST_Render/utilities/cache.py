import bpy
import gc
from functools import lru_cache, wraps, _lru_cache_wrapper
from datetime import datetime, timedelta


cached_functions = []


def get_context(args):
    context_list=[x for x in args if isinstance(x, bpy.context.__class__)]
    return context_list[0] if context_list else bpy.context


def RR_cache(seconds: float = 1.0, maxsize: int = None, animated = False):

    # Uncomment to see if caching in general is the issue
    # def test_wrapper(func):
    #     @wraps(func)
    #     def wrap(*args, **kwargs):
    #         return func(*args, **kwargs)
    #     return wrap
    # return test_wrapper

    def wrapper_cache(func):
        func = lru_cache(maxsize=maxsize)(func)
        cached_functions.append(func)
        func.lifetime = timedelta(seconds=seconds)
        func.expiration = datetime.now() + func.lifetime
        func.frame = 0
        func.scene = None

        @wraps(func)
        def wrapped_func(*args, **kwargs):
            context = get_context(args)
            if(
                # True or # Uncomment True to see if a problem is stale cache related
                not context.scene.render_raw_scene.use_cache or
                ('use_cache' in kwargs and kwargs['use_cache'] == False) or
                datetime.now() >= func.expiration or
                (context and context.scene != func.scene) or
                (animated and func.frame != context.scene.frame_current)
            ):
                func.cache_clear()
                func.expiration = datetime.now() + func.lifetime
                func.scene = context.scene
                if animated:
                    func.frame = context.scene.frame_current
            return func(*args, **kwargs)

        return wrapped_func

    return wrapper_cache


def cacheless(func):
    """
    Useful for making sure top level, non-drawing functions don't use cached data
    """
    def wrapped(*args, **kwargs):
        context = get_context(args)
        RR_SCENE = context.scene.render_raw_scene
        was_enabled = RR_SCENE.use_cache

        # print('DISABLING CACHE')
        RR_SCENE.use_cache = False
        result = func(*args, **kwargs)
        RR_SCENE.use_cache = was_enabled
        # print(f'CHANGING CACHE: {was_enabled}')

        return result

    return wrapped


def clear_cache():
    # From https://stackoverflow.com/questions/40273767/clear-all-lru-cache-in-python
    for func in cached_functions:
        func.cache_clear()