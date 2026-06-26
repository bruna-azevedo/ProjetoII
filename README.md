# 🩰 Dance Academy

> Sistema Web para gerenciamento de reservas de salas de ballet, desenvolvido como Projeto Integrador da disciplina **Projeto de Desenvolvimento II** do curso de **Análise e Desenvolvimento de Sistemas**.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![HTML5](https://img.shields.io/badge/HTML5-Frontend-orange)
![CSS3](https://img.shields.io/badge/CSS3-Style-blue)
![JavaScript](https://img.shields.io/badge/JavaScript-Interatividade-yellow)
![Status](https://img.shields.io/badge/Status-Concluído-success)

---

# 📑 Sumário

* Contexto
* Problema
* Objetivos
* Benchmarking
* Tecnologias
* Funcionalidades
* Arquitetura
* Diagrama ER
* Project Model Canvas
* Estrutura do Projeto
* Como Executar
* Trabalhos Futuros
* Desenvolvedora

---

# 📖 Contexto

O Dance Academy surgiu a partir da necessidade de informatizar o processo de reserva de salas de uma escola de ballet.

Anteriormente, os agendamentos eram realizados manualmente, ocasionando conflitos de horários, reservas duplicadas, dificuldade de organização e perda de tempo na administração.

O sistema foi desenvolvido para centralizar todas essas atividades em uma única plataforma web, tornando o processo mais seguro, organizado e eficiente.

---

# 🚨 Problema

Antes da implantação do sistema, a instituição enfrentava problemas como:

* reservas duplicadas;
* conflitos entre professores;
* controle manual das salas;
* dificuldade para localizar reservas;
* ausência de notificações automáticas;
* necessidade de alterar reservas manualmente.

Esses fatores comprometiam a organização da escola e dificultavam a gestão administrativa.

---

# 🎯 Objetivos

## Objetivo Geral

Desenvolver uma aplicação web para gerenciamento de reservas de salas de ballet, proporcionando maior organização, praticidade e redução de conflitos de agendamento.

## Objetivos Específicos

* cadastrar professores;
* cadastrar salas;
* reservar salas;
* impedir conflitos de horários;
* calcular automaticamente o horário final da reserva;
* visualizar reservas existentes;
* editar reservas;
* excluir reservas;
* enviar notificações por e-mail;
* restringir funções administrativas apenas ao administrador.

---

# 📊 Benchmarking

Foi realizado um benchmarking com plataformas de agendamento utilizadas no mercado, como:

* Reservio
* SimplyBook.me
* SuperSaaS
* Calendly

A análise permitiu identificar funcionalidades consolidadas em sistemas profissionais, como controle de disponibilidade, bloqueio de conflitos e gerenciamento de reservas.

O principal diferencial do Dance Academy é sua personalização para o contexto de uma escola de ballet, atendendo diretamente às necessidades da instituição.

---

# 🛠 Tecnologias Utilizadas

| Camada         | Tecnologia |
| -------------- | ---------- |
| Front-end      | HTML5      |
| Estilização    | CSS3       |
| Interatividade | JavaScript |
| Templates      | Jinja2     |
| Back-end       | Python     |
| Framework      | Flask      |
| Banco de Dados | SQLite     |
| Versionamento  | Git        |
| Repositório    | GitHub     |

---

# 🚀 Funcionalidades

## Dashboard

* painel inicial;
* mural de notícias;
* eventos;
* estatísticas da academia;
* destaque da aluna do mês.

## Professores

* cadastro;
* gerenciamento.

## Salas

* cadastro;
* capacidade.

## Reservas

* criação de reservas;
* cálculo automático do horário final;
* duração personalizada (30 min, 40 min, 1 hora, etc.);
* observações;
* listagem completa;
* edição;
* exclusão.

## Segurança

* login administrativo;
* proteção das funções administrativas;
* somente administradores podem alterar ou excluir reservas.

## Validações

* bloqueio de conflitos de horário;
* verificação de disponibilidade das salas;
* validação dos formulários.

## Notificações

Envio automático de e-mails para:

* confirmação da reserva;
* alteração da reserva;
* cancelamento.

Os e-mails são enviados em formato HTML.

## JavaScript

O sistema utiliza JavaScript para melhorar a experiência do usuário, realizando:

* cálculo em tempo real do horário final da reserva;
* atualização dinâmica das informações exibidas durante o preenchimento do formulário.

---

# 🏗 Arquitetura

O sistema segue uma arquitetura Cliente-Servidor.

Professor/Admin

↓

Interface Web

HTML + CSS + JavaScript

↓

Flask

Regras de Negócio

↓

SQLite

Banco de Dados

---

# 🗄 Diagrama ER

O banco de dados foi modelado utilizando o modelo Entidade-Relacionamento.

Entidades principais:

* Professores
* Salas
* Reservas

Relacionamentos:

* um professor pode possuir diversas reservas;
* uma sala pode possuir diversas reservas;
* cada reserva pertence a um único professor e a uma única sala.

---

# 📋 Project Model Canvas

Durante o planejamento do projeto foi elaborado um Project Model Canvas contendo:

* justificativa;
* objetivos SMART;
* benefícios;
* stakeholders;
* requisitos;
* restrições;
* riscos;
* premissas;
* entregas;
* equipe;
* custos.

<img width="1536" height="1024" alt="PMC" src="https://github.com/user-attachments/assets/5da829f5-4279-40ca-bbe4-9db5d4cc0296" />


  🎯 Justificativa

A academia realizava o agendamento das salas manualmente, ocasionando conflitos de horários, retrabalho e dificuldade no controle das reservas. O projeto foi desenvolvido para informatizar esse processo, tornando-o mais organizado e eficiente.

🎯 Objetivo SMART

Desenvolver um sistema web para gerenciamento de reservas de salas de ballet até o final do semestre letivo, permitindo cadastro de professores, salas e reservas, reduzindo conflitos de horários e facilitando a administração da academia.

👥 Benefícios
Para a academia
Organização das reservas
Eliminação de conflitos de horários
Centralização das informações
Melhor aproveitamento das salas
Para os professores
Reserva rápida e intuitiva
Visualização das reservas realizadas
Notificações sobre alterações
Para a administração
Cadastro simplificado
Controle das salas
Facilidade na gestão das informações

📦 Produto

Sistema web para reserva de salas contendo:

Dashboard
Cadastro de professores
Cadastro de salas
Reserva de salas
Consulta de reservas
Edição de reservas
Exclusão de reservas
Painel administrativo
Mural de notícias
Controle de conflitos de horários
Envio de e-mail ao editar reservas

✅ Requisitos
Funcionais
Cadastro de professores
Cadastro de salas
Cadastro de reservas
Editar reservas
Excluir reservas
Listar reservas
Impedir reserva duplicada
Dashboard
Login administrativo
Envio de e-mails
Não Funcionais
Interface responsiva
Facilidade de uso
Banco SQLite
Desenvolvimento em Flask
Tempo de resposta adequado
Organização e padronização do código

👥 Stakeholders
Administração da academia
Professores
Alunos (indiretamente)
Desenvolvedora
Professor orientador

⚠️ Riscos
Perda de dados
Erros no banco SQLite
Falhas no envio de e-mail
Conflitos de reservas não tratados
Pouco tempo para desenvolvimento
Alterações de requisitos durante o projeto

📅 Premissas
Professores utilizarão corretamente o sistema.
Todas as salas estarão cadastradas.
O servidor Flask estará disponível.
O banco SQLite permanecerá íntegro.
Os usuários terão acesso à internet.

🚧 Restrições
Desenvolvimento dentro do prazo da disciplina.
Utilização de Flask e SQLite.
Recursos financeiros limitados.

💰 Custos
Software
Python (gratuito)
Flask (gratuito)
SQLite (gratuito)
VS Code (gratuito)
GitHub (gratuito)
Infraestrutura
Computador
Internet
Hospedagem

Custo estimado: baixo (praticamente zero durante o desenvolvimento).

📅 Entregas
Levantamento de requisitos
Protótipo da interface
Banco de dados
Desenvolvimento Front-end
Desenvolvimento Back-end
Integração
Testes
Documentação
Apresentação final

👨‍💻 Equipe
Desenvolvedora Front-end e Back-end
Scrum Master
Product Owner
Professor orientador

🛠 Tecnologias
HTML5
CSS3
Python
Flask
SQLite
Jinja2
JavaScript
Git/GitHub


---

# 📁 Estrutura do Projeto

```text
DanceAcademy/
│
├── static/
│   ├── css
│   ├── imagens
│   └── javascript
│
├── templates/
│
├── app.py
├── banco.db
└── README.md
```

---

# ▶ Como Executar

```bash
pip install flask
```

```bash
python app.py
```

Após iniciar o servidor, acesse:

```
http://127.0.0.1:5000
```

---

# 🔮 Trabalhos Futuros

* aumento de clientes;
* autenticação individual para professores;
* calendário mensal das reservas;
* filtros por professor e sala;
* exportação em PDF;
* integração com Google Calendar;
* hospedagem em nuvem;
* notificações por WhatsApp.

---

# 👩‍💻 Desenvolvedora

**Bruna Azevedo**

Projeto desenvolvido para a disciplina **Projeto de Desenvolvimento II** do curso de **Análise e Desenvolvimento de Sistemas**.

---

⭐ Projeto acadêmico desenvolvido com foco na organização de reservas de salas para instituição de ensino de ballet.
