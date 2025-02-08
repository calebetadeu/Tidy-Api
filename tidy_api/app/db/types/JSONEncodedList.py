import json
from sqlalchemy.types import TypeDecorator, Text

class JSONEncodedList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Garante que estamos convertendo uma lista para JSON
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            try:
                # Tenta carregar o JSON e garante que seja uma lista
                result = json.loads(value)
                if not isinstance(result, list):
                    # Se não for lista, converte para lista ou lança erro
                    return [result]
                return result
            except json.JSONDecodeError:
                # Se ocorrer erro na conversão, pode tratar ou lançar exceção
                return []
        return value
