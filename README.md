# 🩰 Dance Academy

> Projeto desenvolvido a partir de uma necessidade real observada em uma escola de ballet, onde os agendamentos de salas eram realizados manualmente, ocasionando conflitos de horários, reservas duplicadas e dificuldades de gerenciamento.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Flask](https://img.shields.io/badge/Flask-Web_App-black)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-orange)

---

## 📑 Sumário

* [Contexto](#-contexto)
* [Ideação](#-ideação)
* [Objetivos](#-objetivos)
* [Stack](#-stack)
* [Solução](#-solução)
* [Arquitetura](#-arquitetura)

---

## 📖 Contexto

A Dance Academy é uma escola de ballet que realizava o gerenciamento de reservas de salas de forma manual.

Os professores dependiam de anotações e comunicação direta para verificar a disponibilidade dos espaços, o que frequentemente gerava conflitos de horários, reservas duplicadas e dificuldades no controle das salas disponíveis.

Com o crescimento da demanda, surgiu a necessidade de desenvolver uma solução digital capaz de centralizar e automatizar esse processo.

---

## 💡 Ideação

O projeto surgiu a partir da observação de problemas reais enfrentados diariamente na escola de ballet.

Durante o levantamento de requisitos foram identificadas as seguintes dificuldades:

* Conflitos de horários entre professores;
* Falta de visualização da disponibilidade das salas;
* Processo totalmente manual;
* Dificuldade para localizar reservas existentes;
* Possibilidade de erros humanos;
* Falta de histórico organizado dos agendamentos.

A partir desses problemas foi idealizada uma aplicação web capaz de centralizar e automatizar todo o processo de reservas.

---

## 🎯 Objetivos

### Objetivo Geral

Desenvolver um sistema web para gerenciamento de reservas de salas, proporcionando maior organização e reduzindo conflitos de agendamento.

### Objetivos Específicos

* Permitir cadastro de professores;
* Permitir cadastro de salas;
* Realizar reservas de salas;
* Impedir reservas conflitantes;
* Disponibilizar um painel administrativo;
* Gerenciar reservas existentes;
* Enviar notificações por e-mail aos professores;
* Centralizar as informações em um único ambiente.

---

## 🛠 Stack

| Camada         | Tecnologia |
| -------------- | ---------- |
| Front-end      | HTML5      |
| Estilização    | CSS3       |
| Templates      | Jinja2     |
| Back-end       | Python     |
| Framework      | Flask      |
| Banco de Dados | SQLite     |
| Versionamento  | Git        |
| Repositório    | GitHub     |

---

## 🚀 Solução

A solução desenvolvida consiste em uma aplicação web para gerenciamento de reservas de salas da academia.

O sistema permite que professores realizem reservas informando sala, data e horário desejados.

### Funcionalidades

* Dashboard inicial;
* Cadastro de professores;
* Cadastro de salas;
* Reserva de salas;
* Validação automática de conflitos;
* Painel administrativo;
* Visualização de reservas;
* Alteração de reservas;
* Exclusão de reservas;
* Notificações por e-mail;
* Controle centralizado das informações.

A implementação da solução reduz significativamente problemas causados por processos manuais e proporciona maior controle para a administração da instituição.

---

## 🏗 Arquitetura

O sistema utiliza uma arquitetura baseada no modelo Cliente-Servidor.

```text
┌─────────────────────┐
│ Professor / Admin   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Interface Web       │
│ HTML + CSS          │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Flask (Back-end)    │
│ Regras de Negócio   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ SQLite              │
│ Banco de Dados      │
└─────────────────────┘
```

### Camada de Apresentação

Responsável pela interação com o usuário.

* HTML
* CSS
* Templates Jinja2

### Camada de Aplicação

Responsável pelas regras de negócio.

* Flask
* Controle de reservas
* Validação de conflitos
* Notificações por e-mail

### Camada de Dados

Responsável pelo armazenamento das informações.

* SQLite
* Professores
* Salas
* Reservas

---

## 📈 Resultados Esperados

* Redução de conflitos de agendamento;
* Maior organização administrativa;
* Melhor experiência para professores;
* Centralização das informações;
* Automatização de processos manuais;
* Maior confiabilidade nos registros de reservas.

---

## 👩‍💻 Desenvolvido por

**Bruna Azevedo**

Projeto desenvolvido para a disciplina de **Projeto de Desenvolvimento II** do curso de **Análise e Desenvolvimento de Sistemas**.
