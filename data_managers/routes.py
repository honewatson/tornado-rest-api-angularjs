__author__ = 'honhon'


dynamic_classes_cache = {}

def get_unique_handler_class_name(model, base_handler):
    model_name = model.__name__
    base_name = base_handler.__name__
    class_name = model_name + base_name
    index = dynamic_classes_cache.setdefault(class_name, 1)
    unique_class_name = class_name + str(index)
    index += 1
    dynamic_classes_cache[class_name] = index
    return unique_class_name


def rest_handler(model, data_manager, base_handler, handler=None, **kwargs):
    attrs = {}
    attrs.update(kwargs)
    attrs['model'] = model
    attrs['data_manager'] = data_manager
    attrs['motor'] = motor

    unique_class_name = get_unique_handler_class_name(model, base_handler)

    if handler:
        rest_handler = type(unique_class_name, (handler, base_handler), attrs)
    else:
        rest_handler = type(unique_class_name, (base_handler,), attrs)
    return rest_handler


def rest_routes(model, data_manager, base_handler, handler=None, **kwargs):
    prefix = kwargs.get('prefix', model.__name__.lower())
    handler = rest_handler(model, data_manager, base_handler, handler=handler, **kwargs)
    return [
        (r'/%s/?' % prefix, handler),
        (r'/%s/new/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/(edit|delete|)/?' % prefix, handler),
    ]