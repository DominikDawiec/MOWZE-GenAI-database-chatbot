[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mowze-chat.streamlit.app/)

# MOWZE GenAI Database Chatbot

> A HackYeah 2023 Streamlit prototype that turns a natural-language question into SQL, executes it and explains the returned rows.

![Status: Completed](https://img.shields.io/badge/status-completed-2ea44f)

## Overview

MOWZE demonstrates a conversational database workflow. Given model settings, a connection string and schema details stored in Streamlit session state, `main.py` asks an OpenAI chat model to generate SQL, shows that SQL in the sidebar, executes it through SQLAlchemy and requests a second natural-language answer based on the resulting dataframe.

## Project status

| Item | Details |
|---|---|
| Status | ✅ Completed |
| Origin | HackYeah 2023 |
| Last repository update | June 2025 |
| Last verified | Not recently verified |
| Live application | [Open in Streamlit](https://mowze-chat.streamlit.app/) |

## Key features

- Text-to-SQL prompt built from the question, schema and selected SQL dialect.
- Generated SQL displayed before or while it is executed.
- SQLAlchemy execution and tabular result rendering.
- Second model call that turns the dataframe output into a user-facing answer.
- Streamlit chat history, model details and a clear-history control.
- MySQL and PostgreSQL drivers declared in the project dependencies.

## Results

The repository contains the core code for an end-to-end question-to-SQL-to-answer prototype created for HackYeah 2023. No accuracy, safety or latency evaluation is included. The current `main.py` expects configuration values in session state, while no configuration screen or example configuration file was confirmed on the current branch, so local end-to-end operation remains unverified.

## Tech stack

| Technology | Purpose confirmed in the repository |
|---|---|
| Python | Application and prompt logic |
| Streamlit | Chat interface and session state |
| OpenAI Python client `0.28` | SQL generation and answer generation |
| SQLAlchemy | Database connections and SQL execution |
| Pandas | Query-result dataframe |
| PyMySQL | MySQL driver declared in `requirements.txt` |
| psycopg2-binary | PostgreSQL driver declared in `requirements.txt` |

## How it works

1. `main.py` reads database, schema and model values from `st.session_state`.
2. The user's question is combined with the supplied schema and SQL dialect.
3. `openai.ChatCompletion.create` returns SQL without an explanatory wrapper.
4. The SQL is shown in the sidebar and executed directly through SQLAlchemy.
5. Returned rows become a Pandas dataframe.
6. A second model request uses the question, SQL and dataframe text to formulate the chat answer.

## Repository structure

```text
.
├── main.py           # Chat interface, SQL generation, execution and answer generation
├── requirements.txt # Pinned runtime dependencies
└── README.md        # Project documentation
```

Only paths confirmed on the current default branch are shown. Setup pages referenced in comments and interface text were not confirmed through the current repository file API.

## Getting started

### Prerequisites

- Python 3
- An OpenAI API key
- A supported database and a connection string
- Schema details that can be supplied to the model

### Installation

```bash
git clone https://github.com/DominikDawiec/MOWZE-GenAI-database-chatbot.git
cd MOWZE-GenAI-database-chatbot

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run main.py
```

The current entry point expects values such as `connection_str`, `db_type`, `schema_details_json`, `selected_model`, `key` and generation parameters to already exist in Streamlit session state.

<!-- REVIEW: Restore or document the configuration flow and add a safe example file containing variable names but no credentials. -->

## Usage

Once the database and model session values are configured:

1. Enter a question in the Streamlit chat box.
2. Inspect the generated SQL in the sidebar.
3. Review the returned dataframe and conversational answer.
4. Clear the chat history when starting a new analysis.

Do not connect the current prototype to production or write-enabled data.

## Data and methodology

- **Inputs:** user question, database schema, SQL dialect, connection string and model settings.
- **Generation:** the first prompt instructs the model to use only supplied tables and columns and return SQL only.
- **Execution:** SQLAlchemy executes the returned statement inside a transaction without a validation layer.
- **Explanation:** a second prompt receives the question, generated SQL and `data.to_string()` output.
- **State:** chat messages and connection/model settings are maintained through Streamlit session state.

## Contact

Created by [Dominik Dawiec](https://www.linkedin.com/in/dominikdawiec/).
