from rest_framework import viewsets, filters
from .models import CustomUser, Part, CarModel, PartCarModel
from .serializers import PartListSerializer, PartDetailSerializer, CarModelSerializer, PartCarModelSerializer
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsAdminOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from rest_framework import status
from django.core.files.storage import default_storage
from .tasks import process_csv

class RegisterUserView(generics.CreateAPIView):
    '''
    API para Registro de Usuário

    ### Descrição
    - Esta API permite o registro de novos usuários.
    - **Permissões**:
        - Qualquer usuário.

    ### Endpoints
    - `POST /register/` - Registrar um novo usuário.

    ### Parâmetros (POST)
    | Nome     | Tipo   | Obrigatório | Descrição               | Exemplo         |
    |----------|--------|-------------|-------------------------|-----------------|
    | username | string | Sim         | Nome de usuário.        | "joao"          |
    | email    | string | Sim         | E-mail do usuário.      | "joao@email.com"|
    | password | string | Sim         | Senha do usuário.       | "12345678"      |
    | role     | string | Sim         | Papel do usuário.       | "user"          |

    - **Tipos de Usuário**:
        - `user`: Usuário comum com permissões limitadas.
        - `admin`: Administrador com permissões completas.

    ### Respostas
    - **201 (Created)**: Usuário criado com sucesso.
        ```json
        {
            "id": 1,
            "email": "joao@email.com",
            "username": "joao",
            "role": "user"
        }
        ```
    - **400 (Bad Request)**: Erro de validação dos dados.
        ```json
        {
            "error": "O campo 'username' é obrigatório."
        }
        ``` 
    '''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class UserManagementViewSet(viewsets.ModelViewSet):
    '''
    API para Gerenciamento de Usuários

    ### Descrição
    - Esta API permite o gerenciamento de usuários.
    - **Permissões**:
        - Visualização: Apenas administradores.
        - Edição: Apenas administradores.

    ### Endpoints
    - `GET /users/` - Listar todos os usuários.
    - `POST /users/` - Criar um novo usuário.
    - `GET /users/{id}/` - Detalhar um usuário.
    - `PUT /users/{id}/` - Atualizar um usuário.
    - `DELETE /users/{id}/` - Deletar um usuário.

    ### Parâmetros (POST/PUT)
    | Nome     | Tipo   | Obrigatório | Descrição               | Exemplo         |
    |----------|--------|-------------|-------------------------|-----------------|
    | username | string | Sim         | Nome de usuário.        | "joao"          |
    | email    | string | Sim         | E-mail do usuário.      | "joao@email.com"|
    | password | string | Sim         | Senha do usuário.       | "12345678"      |
    | role     | string | Sim         | Papel do usuário.       | "user"          |

    - **Tipos de Usuário**:
        - `user`: Usuário comum com permissões limitadas.
        - `admin`: Administrador com permissões completas.

    ### Respostas
    - **200 (OK)**: Retorna os dados do usuário.
        ```json
        {
            "id": 1,
            "email": "joao@email.com",
            "username": "joao",
            "role": "user"
        }
        ```
    - **400 (Bad Request)**: Erro de validação dos dados.
        ```json
        {
            "error": "O campo 'username' é obrigatório."
        }
        ```
    - **401 (Unauthorized)**: Usuário não autenticado.
    - **403 (Forbidden)**: Usuário não tem permissão para editar.
    - **404 (Not Found)**: Usuário não encontrado.
    '''
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

class PartViewSet(viewsets.ModelViewSet):
    '''
    API para Gerenciamento de Peças

    ### Descrição
    - Esta API permite o gerenciamento de peças de carro.
    - **Permissões**:
        - Visualização: Qualquer usuário autenticado.
        - Edição: Apenas administradores.

    ### Endpoints
    - `GET /parts/` - Listar todas as peças.
    - `POST /parts/` - Criar uma nova peça.
    - `GET /parts/{id}/` - Detalhar uma peça.
    - `PUT /parts/{id}/` - Atualizar uma peça.
    - `DELETE /parts/{id}/` - Deletar uma peça.

    ### Parâmetros (POST/PUT)
    | Nome        | Tipo   | Obrigatório | Descrição               | Exemplo         |
    |-------------|--------|-------------|-------------------------|-----------------|
    | part_number | string | Sim         | Número da peça.         | "ABC123"        |
    | name        | string | Sim         | Nome da peça.           | "Parafuso"      |
    | details     | string | Não         | Detalhes da peça.       | "Parafuso 10mm" |
    | price       | float  | Sim         | Preço da peça.          | 15.99           |
    | quantity    | int    | Sim         | Quantidade em estoque.  | 100             |

    ### Respostas
    - **200 (OK)**: Retorna os dados da peça.
        ```json
        {
            "id": 1,
            "part_number": "ABC123",
            "name": "Parafuso",
            "details": "Parafuso 10mm",
            "price": 15.99,
            "quantity": 100
        }
        ```
    - **400 (Bad Request)**: Erro de validação dos dados.
        ```json
        {
            "error": "O campo 'part_number' é obrigatório."
        }
        ```
    - **401 (Unauthorized)**: Usuário não autenticado.
    - **403 (Forbidden)**: Usuário não tem permissão para editar.
    - **404 (Not Found)**: Peça não encontrada.

    ### Filtros
    - `part_number`: Filtrar por número da peça.
    - `name`: Filtrar por nome.
    - `price`: Filtrar por preço.

    ### Ordenação
    - `price`: Ordenar por preço.
    - `name`: Ordenar por nome.

    ### Busca
    - `name`: Buscar por nome.
    - `details`: Buscar por detalhes.
    '''
    queryset = Part.objects.all()
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'retrieve':  # GET by ID (detalhe)
            return PartDetailSerializer
        return PartListSerializer  # GET (listar todas as peças)

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['part_number', 'name', 'price']
    search_fields = ['name', 'details']
    ordering_fields = ['price', 'name']

class CarModelViewSet(viewsets.ModelViewSet):
    '''
    API para Gerenciamento de Modelos de Carro

    ### Descrição
    - Esta API permite o gerenciamento de modelos de carro.
    - **Permissões**:
        - Visualização: Qualquer usuário autenticado.
        - Edição: Apenas administradores.

    ### Endpoints
    - `GET /car-models/` - Listar todos os modelos de carro.
    - `POST /car-models/` - Criar um novo modelo de carro.
    - `GET /car-models/{id}/` - Detalhar um modelo de carro.
    - `PUT /car-models/{id}/` - Atualizar um modelo de carro.
    - `DELETE /car-models/{id}/` - Deletar um modelo de carro.

    ### Parâmetros (POST/PUT)
    | Nome        | Tipo   | Obrigatório | Descrição               | Exemplo         |
    |-------------|--------|-------------|-------------------------|-----------------|
    | name        | string | Sim         | Nome do modelo.         | "Gol"           |
    | manufacturer| string | Sim         | Fabricante do modelo.   | "Volkswagen"    |
    | year        | int    | Sim         | Ano de fabricação.      | 2020            |

    ### Respostas
    - **200 (OK)**: Retorna os dados do modelo de carro.
        ```json
        {
            "id": 1,
            "name": "Gol",
            "manufacturer": "Volkswagen",
            "year": 2020
        }
        ```
    - **400 (Bad Request)**: Erro de validação dos dados.
        ```json
        {
            "error": "O campo 'name' é obrigatório."
        }
        ```
    - **401 (Unauthorized)**: Usuário não autenticado.
    - **403 (Forbidden)**: Usuário não tem permissão para editar.
    - **404 (Not Found)**: Modelo de carro não encontrado.

    ### Filtros
    - `name`: Filtrar por nome.
    - `manufacturer`: Filtrar por fabricante.
    - `year`: Filtrar por ano de fabricação.

    ### Ordenação
    - `name`: Ordenar por nome.
    - `manufacturer`: Ordenar por fabricante.
    - `year`: Ordenar por ano de fabricação.

    ### Busca
    - `name`: Buscar por nome.
    - `manufacturer`: Buscar por fabricante.
    '''
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['name', 'manufacturer', 'year']
    search_fields = ['name', 'manufacturer']
    ordering_fields = ['name', 'manufacturer', 'year']

class PartCarModelViewSet(viewsets.ModelViewSet):
    queryset = PartCarModel.objects.all()
    serializer_class = PartCarModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
    serializer_class = PartCarModelSerializer

    @action(detail=False, methods=['post'], url_path='associate')
    def associate_parts_to_car_models(self, request):
        '''
        Associar Peças a Modelos de Carro

        ### Descrição
        - Este endpoint permite associar múltiplas peças a múltiplos modelos de carro.

        ### Parâmetros (Body)
        | Nome          | Tipo   | Obrigatório | Descrição                | Exemplo         |
        |---------------|--------|-------------|--------------------------|-----------------|
        | part_ids      | int[]  | Sim         | IDs das peças.           | [3, 4]          |
        | car_model_ids | int[]  | Sim         | IDs dos modelos de carro.| [2]             |

        ### Respostas
        - **201 (Created)**: Associações criadas com sucesso.
            ```json
            [
                {
                    "id": 3,
                    "part": {
                        "name": "Correia dentada",
                        "details": "Correia reforçada para motores de alto desempenho.",
                        "price": "80.90",
                        "quantity": 20
                    },
                    "car_model": {
                        "id": 2,
                        "name": "Civic",
                        "manufacturer": "Honda",
                        "year": 2022
                    }
                }
            ]
            ```
        - **400 (Bad Request)**: Dados inválidos ou ausentes.
            ```json
            {
                "error": "part_ids e car_model_ids são obrigatórios."
            }
            ```
        - **404 (Not Found)**: Peça ou modelo de carro não encontrado.
            ```json
            {
                "error": "Essa peça não existe."
            }
            ```
        '''
        part_ids = request.data.get('part_ids', [])
        car_model_ids = request.data.get('car_model_ids', [])

        if not part_ids or not car_model_ids:
            return Response({"error": "part_ids e car_model_ids são obrigatórios."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            parts = Part.objects.filter(id__in=part_ids)
            car_models = CarModel.objects.filter(id__in=car_model_ids)

            if len(parts) != len(part_ids):
                return Response({"error": "Essa peça não existe."}, status=status.HTTP_404_NOT_FOUND)
            elif len(car_models) != len(car_model_ids):
                return Response({"error": "Esse modelo de carro não existe"}, status=status.HTTP_404_NOT_FOUND)

            associations = []
            for part in parts:
                for car_model in car_models:
                    association, created = PartCarModel.objects.get_or_create(part=part, car_model=car_model)
                    if created:
                        associations.append(association)

            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='parts-by-car-model')
    def get_parts_by_car_model(self, request):
        '''
        Listar Peças por Modelo de Carro

        ### Descrição
        - Retorna todas as peças associadas a um modelo de carro específico.

        ### Parâmetros (Query)
        | Nome          | Tipo   | Obrigatório | Descrição               | Exemplo         |
        |---------------|--------|-------------|-------------------------|-----------------|
        | car_model_id  | int    | Sim         | ID do modelo de carro.  | 2               |
        **Exemplo de query**
        - `/part-carmodel/parts-by-car-model/?car_model_id=2`

        ### Respostas
        - **200 (OK)**: Lista de peças associadas ao modelo de carro.
            ```json
            [
                {
                "id": 3,
                "part": {
                    "name": "Correia dentada",
                    "details": "Correia reforçada para motores de alto desempenho.",
                    "price": "80.90",
                    "quantity": 20
                }
            ]
            ```
        - **400 (Bad Request)**: `car_model_id` não fornecido.
            ```json
            {
                "error": "car_model_id é obrigatório"
            }
            ```
        - **404 (Not Found)**: Modelo de carro não encontrado.
            ```json
            {
                "error": "Nenhuma peça associada a este modelo de carro"
            }
            ```
        '''
        car_model_id = request.query_params.get('car_model_id')

        if not car_model_id:
            return Response({"error": "car_model_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            car_model_exists_in_association = PartCarModel.objects.filter(car_model_id=car_model_id).exists()
            if not car_model_exists_in_association:
                return Response({"error": "Nenhuma peça associada a este modelo de carro"}, status=status.HTTP_404_NOT_FOUND)

            associations = PartCarModel.objects.filter(car_model_id=car_model_id)
            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='car-models-by-part')
    def get_car_models_by_part(self, request):
        '''
        Listar Modelos de Carro por Peça

        ###Descrição
        - Retorna todos os modelos de carro associados a uma peça específica.

        ### Parâmetros (Query)
        | Nome          | Tipo   | Obrigatório | Descrição               | Exemplo         |
        |---------------|--------|-------------|-------------------------|-----------------|
        | part_id       | int    | Sim         | ID da peça.             | 3               |
        **Exemplo de query**
        - `/part-carmodel/car-models-by-part/?part_id=3`

        ### Respostas
        - **200 (OK)**: Lista de modelos de carro associados à peça.
            ```json
            [
                {
                    "id": 4,
                    "part": {
                        "name": "Filtro de água premium",
                        "details": "Filtro de óleo compatível com motores 1.6 a 2.0.",
                        "price": "25.50",
                        "quantity": 100
                    },
                    "car_model": {
                        "id": 2,
                        "name": "Civic",
                        "manufacturer": "Honda",
                        "year": 2022
                    }
                }
            ]
            ```
        - **400 (Bad Request)**: `part_id` não fornecido.
            ```json
            {
                "error": "part_id é obrigatório"
            }
            ```
        - **404 (Not Found)**: Peça não encontrada.
            ```json
            {
                "error": "Nenhum modelo de carro associado a esta peça"
            }
        '''
        part_id = request.query_params.get('part_id')

        if not part_id:
            return Response({"error": "part_id é obrigatório"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            part_exists_in_association = PartCarModel.objects.filter(part_id=part_id).exists()
            if not part_exists_in_association:
                return Response({"error": "Nenhum modelo de carro associado a esta peça"}, status=status.HTTP_404_NOT_FOUND)

            associations = PartCarModel.objects.filter(part_id=part_id)
            serializer = self.get_serializer(associations, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class CSVUploadView(APIView):
    '''
    API para Upload de Arquivo CSV para cadastro de peças

    ### Descrição
    - Esta API permite o envio de um arquivo CSV para cadastro de peças.
    - **Permissões**:
        - Apenas administradores.
        
    ### Endpoints
    - `POST /upload-csv/` - Enviar um arquivo CSV.

    ### Parâmetros (POST)
    | Nome | Tipo | Obrigatório | Descrição   | Exemplo     |
    |------|------|-------------|-------------|-------------|
    | file | file | Sim         | Arquivo CSV | "peças.csv" |

    ### O CSV deverá seguir o seguinte formato:
    | part_number | name          | details           | price | quantity |
    |-------------|---------------|-------------------|-------|----------|

    ### Tipos de Dados
    | Nome        | Tipo   | Obrigatório | Descrição               | Exemplo         |
    |-------------|--------|-------------|-------------------------|-----------------|
    | part_number | string | Sim         | Número da peça.         | "ABC123"        |
    | name        | string | Sim         | Nome da peça.           | "Parafuso"      |
    | details     | string | Não         | Detalhes da peça.       | "Parafuso 10mm" |
    | price       | float  | Sim         | Preço da peça.          | 15.99           |
    | quantity    | int    | Sim         | Quantidade em estoque.  | 100             |

    ### Respostas
    - **202 (Accepted)**: Arquivo enviado e processamento iniciado.
        ```json
        {
            "message": "Arquivo enviado e processamento iniciado"
        }
        ```
    - **400 (Bad Request)**: Arquivo não fornecido.
        ```json
        {
            "error": "Arquivo não fornecido"
        }
        ```

    ### Observações
    - O processamento do arquivo é feito de forma assíncrona via Celery.
    '''
    parser_classes = [MultiPartParser]
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        """
        Recebe um arquivo CSV e inicia o processamento assíncrono via Celery.
        """
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "Arquivo não fornecido"}, status=status.HTTP_400_BAD_REQUEST)

        file_path = default_storage.save(f"uploads/{file.name}", file)
        with default_storage.open(file_path, 'rb') as f:
            file_data = f.read()
            process_csv.delay(file_data)

        return Response({"message": "Arquivo enviado e processamento iniciado"}, status=status.HTTP_202_ACCEPTED)