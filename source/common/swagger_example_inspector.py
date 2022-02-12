from drf_yasg import openapi
from drf_yasg.inspectors import SerializerInspector
from drf_yasg.inspectors import SwaggerAutoSchema as _SAS
from drf_yasg.utils import swagger_settings


class ExampleInspector(SerializerInspector):
    def process_result(self, result, method_name, obj, **kwargs):
        has_examples = hasattr(obj, "Meta") and hasattr(obj.Meta, "examples")
        if isinstance(result, openapi.Schema.OR_REF) and has_examples:
            schema = openapi.resolve_ref(result, self.components)
            if "properties" in schema:
                properties = schema["properties"]
                for name in properties.keys():
                    if name in obj.Meta.examples:
                        properties[name]["example"] = obj.Meta.examples[name]

        return result


class SwaggerAutoSchema(_SAS):

    field_inspectors = [
        ExampleInspector,
    ] + swagger_settings.DEFAULT_FIELD_INSPECTORS
