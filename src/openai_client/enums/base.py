class EnumMeta(type):
    def __contains__(cls, value):
        for base_class in cls.mro():
            if value in vars(base_class).values():
                return True
            
        return False

    def __iter__(cls):
        attrs = set()
        for base_class in cls.mro():
            for attr_name, attr_value in vars(base_class).items():
                if isinstance(attr_value, str) and not attr_name.startswith('_'):
                    attrs.add(attr_value)

        return iter(attrs)
    
    @property
    def ALL(cls) -> list[str]:
        return list(cls)

class BaseStrEnum(metaclass=EnumMeta):
    pass
