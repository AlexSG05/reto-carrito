# Cliente del servicio Catálogo (equipo vecino) · Reto de integración
# Contrato del vecino: catalogo.proto · Qué hace y con qué datos probar: servicios/catalogo/README.md
# Antes de correrlo, el servidor del vecino debe estar corriendo (README.md, paso 5).
import grpc

import catalogo_pb2
import catalogo_pb2_grpc

canal = grpc.insecure_channel("localhost:50051")
stub = catalogo_pb2_grpc.CatalogoStub(canal)

print("=== Parte 1 · ObtenerProducto con un dato válido ===")
try:
    # 1. Se usa el campo 'clave' como lo define catalogo.proto
    peticion_valida = catalogo_pb2.ProductoRequest(clave="P001")
    respuesta = stub.ObtenerProducto(peticion_valida)
    
    print("Producto encontrado:")
    print(respuesta)
except grpc.RpcError as e:
    print(f"Error inesperado en Parte 1 [{e.code()}]: {e.details()}")

print("\n=== Parte 2 · ObtenerProducto con un dato que provoca error ===")
try:
    # 2. Clave inexistente para probar captura de error
    peticion_invalida = catalogo_pb2.ProductoRequest(clave="CLAVE_INEXISTENTE_999")
    respuesta = stub.ObtenerProducto(peticion_invalida)
    print(f"Respuesta inesperada (debió fallar): {respuesta}")
except grpc.RpcError as e:
    # Imprime código y detalles del error sin que el programa truene
    print(f"Código de error capturado: {e.code()}")
    print(f"Detalles: {e.details()}")
print("\n=== Parte 3 · ListarCategoria (streaming) ===")
try:
    # Cambiamos "electronica" por "computo"
    peticion_categoria = catalogo_pb2.CategoriaRequest(categoria="computo")
    
    stream_productos = stub.ListarCategoria(peticion_categoria)
    
    print("Recibiendo productos en streaming:")
    for producto in stream_productos:
        print(f"  -> {producto}")
except grpc.RpcError as e:
    print(f"Error en streaming [{e.code()}]: {e.details()}")