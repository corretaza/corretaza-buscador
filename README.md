Corretaza (antigo nome para efeito de histórico: 'Seu Corretor' )
=========


SETUP (Instalação)
------------------
Temos 2 opções
- Usando Docker (Simples e rápido - Unico requisito é ter um máquina 64bits)
- Instalar os requisitos para funcionar um vitual env

Para maiores informações veja o arquivo docs/bootstrap_corretaza  


TAREFAS
--------
https://corretaza.kanbanize.com/ctrl_dashboard

Usamos um kanban simples:               
                                          Validado internamente
                                            /
                                           /      Validado pelo cliente
                                          /         /
   Backlog --> NEXT --> In Progress --> Q&A --> Approval --> DONE
      \           \
       \         Seleção do que será feito em cada Sprint
        \
        Todo request (interno/cliente) vira um item de backlog (que pode ou não ser quebrado em + tarefas)

   As tarefas são classificadas como:
	* New feature		--> Nova funcionalidade
	* Improvement     --> Melhoria de alguma funcionalidade existente
	* Bug             --> Correção de um bug
	* TechnicalDebt   --> Refatoração de código para deixá-lo melhor sem afetar seu funcionamento
