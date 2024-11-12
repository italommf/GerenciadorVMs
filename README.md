# GerenciadorVMs

Este projeto está ainda em desenvolvimento e tem como objetivo principal agilizar a abertura e gerenciamento das máquinas virtuais cadastradas no sistema, fornecendo uma 
fácil visualização e controle sobre o que está aberto ou não.

## Como utilizar o projeto?

1. Clone o repositório.
   
    - git clone https://github.com/italommf/GerenciadorVMs.git
    - caso tenha o arquivo do banco de dados ja pronto, cole na pasta *backend*, pasta esta que abriga o arquivo *manage.py*.
    - o projeto necessita de um .env na pasta *backend* com as seguintes chaves:
    
      TELEGRAM_TOKEN = Sua chave de api aqui.  
      TELEGRAM_CHAT_ID = Seu chat id aqui.

2. Crie o banco de dados e o super usuário.
  
    Projeto clonado, *.env* e *.db.sqlite3* na pasta *backend*? Hora de executar a aplicação.
  
    No terminal execute:

    - Caso não tenha o arquivo do banco ja pronto
      - python manage.py makemigrations - Caso haja alguma migração a ser feita
      - python manage.py migrate - Para realizar as migrações
      - python manage.py createsuperuser - Para criar o super usuário do seu sistema
        - Insira as credenciais desejadas
       
3. Execute a aplicação.
   
    - Caso ja tenha o arquivo do banco baixado e ja na pasta correta ou mesmo tenha realizado o passo a passo para a criação do banco
      - python manage.py runserver

    Caso apareça algo parecido com isso aqui, parabéns, seu projeto está rodando e pronto para ser utilizado.

    ```
    Watching for file changes with StatReloader
    Performing system checks...
    
    System check identified no issues (0 silenced).
    October 31, 2024 - 02:39:40
    Django version 5.1.1, using settings 'gerenciador_de_projetos.settings'
    Starting development server at http://127.0.0.1:8000/
    Quit the server with CTRL-BREAK.
    ```
      
## Funcionalidades

O projeto consiste em uma *API* ainda em desenvolvimento, porém funcional. Não existe front end pronto para a aplicação, logo a utilizacão é toda feita atravéz do navegador ou algum gerenciador de APIs como Postman.

### *Endpoints* e funcionalidades

http://localhost:8000/ - Endereço principal do projeto.  
http://localhost:8000/admin/ - Painel de administrador da aplicação.  

http://localhost:8000/api/  - Hub com todos as funções atuais deste projeto.  
  - api/adicionar_vm/  
    - Para cadastrar uma nova Máquina Virtual, um JSON deve ser mandado com os seguintes dados:
    
      ```
      {
        'endereco_computador': String - Dado obrigatório
        'nome_de_usuario': String - Dado obrigatório,
        'senha': String - Dado obrigatório,
        'favoritada': Boll - Dado opcional - Default = False
        'resolucao': String - Dado opcional, - Defult = None
        'usar_todos_os_monitores': Boll - Dado opcional - Default = False,
        'area_de_transferencia': Boll - Dado opcional - Default = True,
        'area_de_trabalho': Int - Dado obrigatório - Default = 1
      }
      ```
  - api/adicionar_rpa/
    - Ainda sem funcionalidade  
      
  - api/listar_vms_cadastradas/
    - Retorna um json mostrando todas as Máquinas Virtuais cadastradas no sistema
      
  - api/listar_todas_as_robotizacoes/
    - Ainda sem funcionalidade
      
  - api/listar_robotizacoes_vms/<int:id_da_vm>/
     - Retorna a lista de todas as Robotizações cadastradas nas Máquinas Virtuais - Ainda sem funcionalidade
       
  - api/abrir_vm/<int:vm_id>/
    - Retorna a abertura da máquina virtual correspondente ao ID informado em ```<int:vm_id>```, ao final da abertura, um json com as informações da abertura é exibido no navegador. 
       
  - api/listar_vms_abertas/
    - Retorna um JSON com todas as Máquinas Virtuais abertas no sistema. Este JSON é atualizado em tempo real e exibe as principais informações de cada Máquina Virtual aberta naquele momento.
      
  - api/abrir_todas_as_vms/
    - Retorna a abertura de todas as Máquinas Virtuais com o processo de abertura sendo uma a uma. As áreas de trabalho correspondentes a cada máquina virtual são criadas de acordo com a necessidade durante a abertura das mesmas.  
        
  - api/abrir_vms_favoritadas/
    - Retorna a abertura de todas as Máquinas Virtuais que possuem o campo ```favoritada == True```. Ou seja, abre todas as Máquinas Virtuais marcadas como favorito no painel do Django Admin
    

