# Sistema-prof

Aplicação Sistema-prof

    reporta algum discente
        visualizar reportes
        
Instruções para execução

    $ git clone https://github.com/Williais/Sistema-prof.git
    $ cd Sistema-prof
    # cria ambiente virtual do python
    $ virtualenv --python=`which pyhton3` env
    # para ativar o ambiente virtual
    $ . env/bin/activate
    # instala essas bibliotecas no ambiente virtal ativado
    $ pip install -r requirements.txt 
    
Configurar as variáveis de ambiente para execução do flask:

    $ export FLASK_APP=app.py
    $ export FLASK_DEBUG=1
    
Agora vamos adicionar valores ao banco de dados, ativa o python em modo interativo, com o flask ativado.

    $ flask shell

Depois, insere os seguintes valores:
    
    $ from app import db, Classe, Comentario
    $ db.drop_all()
    $ db.create_all()
    $ Classe.inserir_classes()
    $ exit()

E executar a aplicação

    $ flask run -p 8080

Navegação:

    Na primeira pagina (rota "/" ou Botão "Inicio") mostra as turmas e series que foram cadastradas.
    Na segunda pagina (rota "/comentar" ou Botão "Reportar") é onde o docente pode fazer o reporte escolhendo a turma, digitando o nome do discente, seu nome, sua diciplina e o comentario.
    Na terceira pagina (rota "/listar" ou Botão "Comentários") é onde os docentes podem observar os comentarios dos seus colegas. Tambem poderá observar qual aluno está dando mais trabalho para os outros docentes. 
    
    
    
Equipe

    José William Padilha de Lima da Silva
