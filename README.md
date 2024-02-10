<!-- TOC start (generated with https://github.com/derlin/bitdowntoc) -->

- [ModelViewSet](#modelviewset)
- [Seguridad](#seguridad)
   * [Login](#login)
   * [Users](#users)
      + [Campos disponibles:](#campos-disponibles)
      + [Ejemplo:](#ejemplo)
   * [Groups](#groups)
- [Pedidos](#pedidos)
   * [Clientes](#clientes)
      + [Request](#request)
      + [Search](#search)
   * [Platos](#platos)
      + [Search](#search-1)
      + [Filter](#filter)
   * [Mesas](#mesas)
      + [Filter](#filter-1)
      + [obtener_pedido](#obtener_pedido)
      + [liberar_mesa](#liberar_mesa)
      + [ocupar_mesa](#ocupar_mesa)
   * [Pedidos](#pedidos-1)
      + [Comportamiento](#comportamiento)
      + [Ejemplo:](#ejemplo-1)
      + [Response](#response)
      + [Search](#search-2)
      + [Filter](#filter-2)
      + [pagar_pedido](#pagar_pedido)
   * [DetallePedido](#detallepedido)
      + [Filter](#filter-3)

<!-- TOC end -->

## ModelViewSet
La gran mayoría de Modelos están implementados con el ModelViewSet, el cual genera por defecto los métodos y las rutas, son los siguientes (siempre usar slash al final):
- Listar: GET '/pedidos/clientes/' (se pueden incluir búsquedas: '/pedidos/clientes/?search=Juan' o filtros: '/pedidos/pedidos/?pagado=true')
- Obtener elemento: GET '/pedidos/clientes/1/'
- Crear elemento: POST '/pedidos/clientes/'
- Actualizar elemento: PUT '/pedidos/clientes/1/'
- Actualizar elemento (solo campos específicos): PATCH '/pedidos/clientes/1/'
- Eliminar elemento: DELETE '/pedidos/clientes/1/'

Los campos requeridos y no requeridos se detallarán a continuación, además se pueden consultar en el serializer, ejemplo:
class MesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mesa
        fields = ['id', 'nombre', 'enUso', 'horaUltimoUso']
        read_only_fields = ['enUso', 'horaUltimoUso']        # No van en el request, pero estarán presentes en el response

La UI muestra ejemplos de la mayoría de métodos (al menos GET y POST), filtros y búsquedas. También se puede usar el método OPTIONS para obtener los campos.  
Todos los métodos requieren autenticación (menos el login), esta se puede hacer mediante Token o Session en el caso de la UI.

Existen cuatro módulos:
- Seguridad
- Pedidos
- Compras
- Caja

## Seguridad

### Login

- **Endpoint:** `POST /api-token-auth`

- **Body:**
  ```json
  {
    "username": "<username>",
    "password": "<password>"
  }
  ```

- **Respuesta:**
  - Devuelve el token de autenticación:
    ```json
    {
      "token": "<Token>"
    }
    ```

- **Uso del Token:**
  - Se agrega como Header a los request:
    ```
    Authorization: Token <Token>
    ```

### Users
Modelo de los usuarios (también se usa para permisos).

**ModelViewSet en '/users/'**

#### Campos disponibles:

```json
{
  "username": {
    "type": "string",
    "required": true,
    "read_only": false,
    "label": "Username",
    "help_text": "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
    "max_length": 150
  },
  "email": {
    "type": "email",
    "required": false,
    "read_only": false,
    "label": "Email address",
    "max_length": 254
  },
  "groups": {
    "type": "array",
    "required": false,
    "read_only": false,
    "label": "Groups",
    "help_text": "The groups this user belongs to. A user will get all permissions granted to each of their groups."
  },
  "password": {
    "type": "string",
    "required": true,
    "read_only": false,
    "label": "Password",
    "max_length": 128
  }
}
```

#### Ejemplo

```json
{
  "username": "usuarioTest",
  "email": "test@hotmail.com",
  "groups": [
    1
  ],
  "password": "sdamjvadsn8734"
}
```

### Groups
Modelo de los groups, cada uno tiene varios permisos.

**ModelViewSet en '/groups/'**

## Pedidos

### Clientes
Modelo de los clientes.

**ModelViewSet en '/pedidos/clientes/'**

#### Request
```json
{
    "nombre": {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Nombre",
        "max_length": 80
    },
    "direccion": {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Direccion",
        "max_length": 50
    },
    "email": {
        "type": "email",
        "required": false,
        "read_only": false,
        "label": "Email",
        "max_length": 254
    },
    "telefono": {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Telefono",
        "max_length": 15
    },
    "tipoCliente": {
        "type": "choice",
        "required": true,
        "read_only": false,
        "label": "TipoCliente",
        "choices": [
            {
                "value": "Natural",
                "display_name": "Natural"
            },
            {
                "value": "Jurídico",
                "display_name": "Jurídico"
            }
        ]
    },
    "tipoDocumento": {
        "type": "choice",
        "required": true,
        "read_only": false,
        "label": "TipoDocumento",
        "choices": [
            {
                "value": "DNI",
                "display_name": "DNI"
            },
            {
                "value": "RUC",
                "display_name": "RUC"
            },
            {
                "value": "Carné de Extranjería",
                "display_name": "Carné de Extranjería"
            }
        ]
    },
    "nroDocumento": {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "NroDocumento",
        "max_length": 11
    }
}
```

#### Search
Se puede buscar por:
- 'nombre' ('?search=Juan')

### Platos
Modelo de los platos (no contiene insumos).

**ModelViewSet en '/pedidos/platos/'**

```json
{
    "nombre": {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Nombre",
        "max_length": 40
    },
    "categoria": {
        "type": "choice",
        "required": false,
        "read_only": false,
        "label": "Categoria",
        "choices": [
            {
                "value": "Plato",
                "display_name": "Plato"
            },
            {
                "value": "Bebida",
                "display_name": "Bebida"
            },
            {
                "value": "Acompañamiento",
                "display_name": "Acompañamiento"
            },
            {
                "value": "Otros",
                "display_name": "Otros"
            }
        ]
    },
    "precio": {
        "type": "decimal",
        "required": true,
        "read_only": false,
        "label": "Precio"
    }
}
```
#### Search
Se puede buscar por
- 'nombre' ('?search=Arroz')

#### Filter
Se puede filtrar por:
- 'categoria' ('?categoria=Plato')

### Mesas
Modelo de las mesas.

**ModelViewSet en '/pedidos/mesas/'**

```json
{
    "nombre": {
        "type": "string",
        "required": true,
        "read_only": false,
        "label": "Nombre",
        "max_length": 10
    }
}
```
#### Filter
Se puede filtrar por:
- 'enUso' ('?enUso=true')

#### obtener_pedido
Se usa para obtener el pedido que tiene la mesa (solo si está en uso, caso contrario devuelve 404)
- Request:
```
GET '/pedidos/mesas/1/obtener_pedido/'
```
- Response (lo mismo que hacer GET '/pedidos/pedidos/1/')

#### liberar_mesa
Se usa para liberar la mesa (no importa el estado actual, si no existe devuelve 404)
- Request:
```
GET '/pedidos/mesas/1/liberar_mesa/'
```
- Response (lo mismo que hacer GET '/pedidos/mesas/1/')

#### ocupar_mesa
Se usa para ocupar la mesa (no importa el estado actual, si no existe devuelve 404)
- Request:
```
GET '/pedidos/mesas/1/ocupar_mesa/'
```
- Response (lo mismo que hacer GET '/pedidos/mesas/1/')

### Pedidos
Modelo de los pedidos.

**ModelViewSet en '/pedidos/pedidos/'**
#### Comportamiento
- Cuando se guarda un pedido, la mesa se ocupa automáticamente.
- Cuando se elimina o paga un pedido, la mesa se libera automáticamente.
- Pagar un pedido genera un ComprobantePago.

```json
{
    "cliente": {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Cliente"
    },
    "mesa": {
        "type": "field",
        "required": false,
        "read_only": false,
        "label": "Mesa"
    },
    "detalles": {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Detalles",
        "child": {
            "type": "nested object",
            "required": true,
            "read_only": false,
            "children": {
                "plato": {
                    "type": "field",
                    "required": true,
                    "read_only": false,
                    "label": "Plato"
                },
                "cantidad": {
                    "type": "integer",
                    "required": true,
                    "read_only": false,
                    "label": "Cantidad",
                    "min_value": -2147483648,
                    "max_value": 2147483647
                },
                "indicaciones": {
                    "type": "string",
                    "required": false,
                    "read_only": false,
                    "label": "Indicaciones",
                    "max_length": 50
                }
            }
        }
    }
}
```

#### Ejemplo
```json
{
  "cliente": 1,
  "mesa": 1,
  "detalles": [
    {
      "plato": 1,
      "cantidad": 2,
      "indicaciones": "Sin ají"
    },
    {
      "plato": 2,
      "cantidad": 1,
      "indicaciones": "Extra pato"
    },
    {
      "plato": 3,
      "cantidad": 3,
      "indicaciones": "Bien cocido"
    }
  ]
}
```
#### Response

```json
{
    "id": 12,
    "usuarioRegistra": 1,
    "Fecha": "2024-02-09T20:14:35.399540Z",
    "cliente": 1,
    "mesa": 1,
    "pagado": true,
    "detalles": [
        {
            "id": 11,
            "plato": 1,
            "cantidad": 2,
            "indicaciones": "Sin ají",
            "precio": "12.00",
            "pedido": 12
        },
        {
            "id": 12,
            "plato": 2,
            "cantidad": 1,
            "indicaciones": "Extra pato",
            "precio": "15.00",
            "pedido": 12
        },
        {
            "id": 13,
            "plato": 3,
            "cantidad": 3,
            "indicaciones": "Bien cocido",
            "precio": "18.00",
            "pedido": 12
        }
    ]
}
```

#### Search
Se puede buscar por:
- 'nombre del cliente' ('?search=Juan')
- 'Fecha' ('?search=2024-02-09')

#### Filter
Se puede filtrar por:
- 'pagado' ('?pagado=true')
- 'usuarioRegistra' ('?usuarioRegistra=1')

#### pagar_pedido
Se usa para pagar el pedido y generar un ComprobantePago (si no existe el pedido devuelve 404).
- Requiere tener una caja abierta (AperturaCaja).
- Cambia el estado a 'pagado=True' y libera la mesa.
- Request:
```
POST '/pedidos/pedidos/1/pagar_pedido/'
{
    "apertura": {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Apertura"
    },
    "tipoPago": {
        "type": "choice",
        "required": true,
        "read_only": false,
        "label": "TipoPago",
        "choices": [
            {
                "value": "Efectivo",
                "display_name": "Efectivo"
            },
            {
                "value": "Tarjeta al contado",
                "display_name": "Tarjeta al contado"
            },
            {
                "value": "Tarjeta en cuotas",
                "display_name": "Tarjeta en cuotas"
            }
        ]
    },
    "tipoComprobante": {
        "type": "choice",
        "required": true,
        "read_only": false,
        "label": "TipoComprobante",
        "choices": [
            {
                "value": "Boleta",
                "display_name": "Boleta"
            },
            {
                "value": "Factura",
                "display_name": "Factura"
            }
        ]
    }
}
```
- Response (lo mismo que hacer GET '/caja/comprobantePago/1/')

### DetallePedido
Modelo del detalle de los pedidos.
- Se crean con el pedido, pero no hay problema en hacer todas las operaciones con detalles en específico.

**ModelViewSet en '/pedidos/detallepedidos/'**

```json
{
    "plato": {
        "type": "field",
        "required": true,
        "read_only": false,
        "label": "Plato"
    },
    "cantidad": {
        "type": "integer",
        "required": true,
        "read_only": false,
        "label": "Cantidad",
        "min_value": -2147483648,
        "max_value": 2147483647
    },
    "indicaciones": {
        "type": "string",
        "required": false,
        "read_only": false,
        "label": "Indicaciones",
        "max_length": 50
    }
}
```

#### Filter
Se puede filtrar por:
- 'pedido' ('/?pedido=1')