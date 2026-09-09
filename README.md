# 🛡️ Mini SOC Lab

> Laboratório defensivo de cibersegurança desenvolvido em Python para simular um pequeno fluxo de SOC: **geração de telemetria → coleta → detecção → triagem → investigação**.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Security](https://img.shields.io/badge/Security-Blue%20Team-0A66C2?style=for-the-badge&logo=shield&logoColor=white)](https://github.com/hotplug1n)
[![Flask](https://img.shields.io/badge/Flask-Web%20Dashboard-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)

## 📌 Sobre o projeto

O **Mini SOC Lab** é um ambiente local de segurança defensiva que transforma telemetria sintética de autenticação em eventos normalizados, detecções estruturadas e uma interface web inspirada em um SOC corporativo.

A proposta é demonstrar, de forma prática, conceitos de **Blue Team, SOC e engenharia de detecção**, sem depender de uma infraestrutura real de SIEM.

> **Importante:** todos os eventos usados pelo projeto são sintéticos e gerados exclusivamente para fins de laboratório.

## 🎯 Objetivos

- simular um fluxo básico de monitoramento de segurança;
- gerar eventos de autenticação variados e não estáticos;
- identificar padrões suspeitos por meio de regras de detecção;
- apresentar alertas em uma interface semelhante a um console de SOC;
- praticar análise, triagem e investigação de eventos;
- manter uma base simples para futuras integrações com SIEM e outras fontes de telemetria.

## 🧩 Arquitetura

```text
┌──────────────────────────┐
│ Telemetria sintética     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Simulador de eventos     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Eventos normalizados     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Motor de detecção        │
│ AUTH-001 / 002 / 003     │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ API Flask                │
└────────────┬─────────────┘
             │
             ▼
┌──────────────────────────┐
│ Dashboard Web do SOC     │
└──────────────────────────┘
```

## 🚨 Regras de detecção

| Regra | Severidade | Detecção |
|---|---|---|
| `AUTH-001` | HIGH | Cinco ou mais falhas de autenticação para a mesma origem e conta em até cinco minutos |
| `AUTH-002` | CRITICAL | Login bem-sucedido após uma sequência recente de falhas |
| `AUTH-003` | HIGH | Tentativas de autenticação malsucedidas contra contas administrativas |

Essas regras são propositalmente simples para facilitar o entendimento do processo de **detection engineering**. Em um ambiente real, seria necessário ajustar os limiares e adicionar contexto para reduzir falsos positivos.

## 🖥️ Dashboard do SOC

A interface web foi criada para representar uma console de monitoramento corporativa limpa e objetiva.

Ela apresenta:

- fluxo contínuo de eventos sintéticos;
- atividade de eventos em uma janela temporal;
- quantidade de eventos e detecções abertas;
- alertas críticos e falhas de autenticação;
- atividade por regra de detecção;
- fontes com maior volume de eventos;
- tabela de alertas recentes;
- tabela de eventos de autenticação normalizados;
- atualização automática sem recarregar a página;
- botão para reiniciar a simulação.

A interface consulta a API local a cada **3,5 segundos**, fazendo com que os indicadores e alertas mudem continuamente durante a execução.

## 🔄 Simulação de telemetria

O simulador gera uma combinação variável de:

- autenticações bem-sucedidas;
- falhas de autenticação;
- tentativas contra contas administrativas;
- rajadas de falhas repetidas;
- sequências de falhas seguidas por sucesso;
- múltiplas origens e contas.

A finalidade é evitar uma interface estática e aproximar o comportamento de um fluxo de eventos observado em um laboratório de SOC.

## 🧠 Conceitos praticados

- análise e parsing de logs;
- normalização de eventos;
- correlação baseada em janela de tempo;
- engenharia de detecção;
- classificação de severidade;
- triagem de alertas;
- investigação inicial de incidentes;
- automação com Python;
- geração de telemetria sintética;
- desenvolvimento de dashboard com Flask;
- testes unitários;
- metodologia defensiva de segurança.

## 📂 Estrutura do projeto

```text
mini-soc-lab/
├── README.md                  # documentação principal
├── app.py                     # aplicação Flask e API local
├── detector.py                # motor de detecção
├── simulator.py               # geração de telemetria sintética
├── requirements.txt           # dependências Python
│
├── data/
│   └── auth.log               # amostra de log sintético
│
├── templates/                 # páginas HTML/Jinja
│   ├── base.html
│   ├── dashboard.html
│   ├── alerts.html
│   └── events.html
│
├── static/                    # recursos do dashboard
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── app.js
│
├── tests/                     # testes automatizados
│   └── test_detector.py
│
└── docs/                      # documentação técnica
    ├── architecture.md
    ├── detection-rules.md
    └── investigation.md
```

A separação entre **código**, **interface**, **testes**, **dados sintéticos** e **documentação** mantém o projeto fácil de navegar e de evoluir.

## ⚙️ Requisitos

- Python **3.10+**
- `pip`

Não é necessário banco de dados ou serviço externo para executar o laboratório.

## ▶️ Executando o projeto

Clone o repositório e entre na pasta:

```bash
git clone https://github.com/hotplug1n/mini-soc-lab.git
cd mini-soc-lab
```

Instale as dependências:

```bash
python3 -m pip install -r requirements.txt
```

Inicie o dashboard:

```bash
python3 app.py
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

## 🧪 Detector via terminal

O motor de detecção também pode ser executado diretamente sobre o log sintético:

```bash
python3 detector.py data/auth.log
```

## ✅ Testes

Execute a suíte automatizada com:

```bash
python3 -m unittest discover -s tests -v
```

## 🔎 Fluxo de investigação

Quando uma detecção aparece, o analista pode seguir uma primeira triagem:

```text
Alerta
  ↓
Validar origem e conta
  ↓
Verificar janela temporal
  ↓
Correlacionar eventos próximos
  ↓
Avaliar sucesso após falhas
  ↓
Verificar se a conta é privilegiada
  ↓
Classificar o incidente
  ↓
Escalar ou encerrar com evidências
```

O playbook completo está em [`docs/investigation.md`](docs/investigation.md).

## 📚 Documentação

- [`docs/architecture.md`](docs/architecture.md) — arquitetura e fluxo de dados;
- [`docs/detection-rules.md`](docs/detection-rules.md) — regras e lógica das detecções;
- [`docs/investigation.md`](docs/investigation.md) — fluxo de triagem e investigação.

## 🛣️ Próximos passos

- suporte a Windows Event Log e Sysmon;
- exportação de alertas em JSON;
- regras compatíveis com Sigma;
- exemplos de SPL para Splunk;
- enriquecimento de IOCs;
- thresholds configuráveis;
- mapeamento MITRE ATT&CK;
- pipeline de testes em CI;
- reconhecimento e acompanhamento de casos;
- novas fontes de telemetria, como VPN, endpoint, web e DNS.

## 🔐 Escopo e ética

Este projeto é um **laboratório defensivo**. Utilize-o somente com dados próprios ou em ambientes para os quais você tenha autorização explícita.

Não adicione credenciais, segredos ou telemetria real ao repositório.

## 👤 Autor

**hotplug1n** — estudante de cibersegurança com foco em **Blue Team, SOC, redes, Linux e desenvolvimento seguro**.

[GitHub](https://github.com/hotplug1n) · [Studies](https://github.com/hotplug1n/studies) · [TryHackMe](https://tryhackme.com/p/.hotplug1n)
