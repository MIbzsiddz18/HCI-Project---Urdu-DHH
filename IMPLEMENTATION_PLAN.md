# One-Week Modular Implementation Blueprint

## DHH Access to Intelligent Personal Assistants --- LLM Touch Interface + Urdu Prototype

**Team:** Muhammad Ibrahim, Faraz Ansari, Ashhal Aamir\
**Deadline:** 7 calendar days maximum\
**Primary objective:** Deliver a working, demonstrable prototype in
which a user selects a smart-home action through a touch interface, the
backend uses an LLM to help construct a command, the user confirms it,
and a mock assistant reports the result. Include a basic Urdu/RTL mode
if feasible.

> **Scope boundary:** The team's presentation describes an existing CHI
> 2026 study and proposes an Urdu replication. This plan covers a
> prototype inspired by the described workflow. It does not imply access
> to the original implementation, completion of a Pakistani participant
> study, or validation of Urdu research instruments.

------------------------------------------------------------------------

## 1. Delivery strategy

Use three workstreams that can be developed in parallel against a shared
contract:

1.  **Frontend and localization** --- tablet UI, workflow screens,
    Urdu/English labels, RTL layout.
2.  **Backend and AI orchestration** --- Flask API, session state, LLM
    adapter, validation, confirmation rules.
3.  **Mock smart-home integration, testing, and demo** --- device
    catalog, command execution simulator, API contract tests, end-to-end
    testing, README/demo.

The third workstream is deliberately implementation-oriented, not just
documentation. It owns the mock device adapter and integration tests so
the other two members can work against stable behavior immediately.

### Non-negotiable strategy

-   Agree on the API contract on Day 1 and do not casually rename routes
    or fields.
-   All members create stubs/mocks immediately; nobody waits for another
    component to be finished.
-   Start with a **mock assistant**. Real Alexa/smart-speaker
    integration is out of scope unless the mock flow is complete and
    integration feasibility is confirmed.
-   The backend owns session state and enforces confirmation.
-   The model proposes text/options; it must not execute device actions.
-   Keep one deployable local demo path. Avoid optional features until
    the core flow works.
-   Integrate every day, not only on Day 7.

------------------------------------------------------------------------

## 2. MVP acceptance criteria

The project is considered demo-ready when all of the following work:

-   User can start a session.
-   UI displays suggested actions in a touch-friendly grid.
-   Selecting an action leads to task choices.
-   The user can select task details or answer a clarification.
-   A complete command is shown before execution.
-   The user must explicitly confirm.
-   The backend rejects execution if the command was not confirmed.
-   A mock assistant returns a success/failure result for supported
    actions.
-   The UI displays the actual adapter result and supports cancel/retry.
-   LLM failure or missing credentials do not crash the demo;
    deterministic fallback options are available.
-   Basic Urdu RTL mode renders without broken alignment or navigation.
-   Setup instructions work on a clean developer environment.
-   No API keys or participant data are committed.

**Not required for the one-week MVP:** real Alexa device control, user
accounts, persistent database, production deployment, a polished
analytics dashboard, validated Urdu SUS/NPS instruments, or
human-subject data collection.

------------------------------------------------------------------------

## 3. Architecture decision

Use a small modular monolith for the backend. Do not split it into
microservices during a one-week project.

``` text
┌─────────────────────────────────────────────┐
│ Frontend: React + TypeScript (or existing UI)│
│ Action grid · task choices · review · status │
│ English/Urdu labels · RTL support            │
└──────────────────────┬──────────────────────┘
                       │ JSON over HTTP
┌──────────────────────▼──────────────────────┐
│ Flask API                                    │
│ routes → schemas/validation → services       │
│                                              │
│ SessionService ── WorkflowService            │
│                    │                         │
│             LLMService / fallback             │
│                    │                         │
│             CommandService                   │
│                    │                         │
│             AssistantAdapter                 │
└──────────────────────┬──────────────────────┘
                       │
            ┌──────────┴───────────┐
            ▼                      ▼
     LLM provider             Mock assistant
     (server-side key)       (in-memory devices)
```

### Suggested stack

Use the team's existing stack if one already exists. Otherwise:

-   Frontend: React + TypeScript + Vite.
-   Backend: Python 3.11+ + Flask.
-   Validation: Pydantic if already familiar; otherwise simple explicit
    validation functions.
-   AI: GPT-4o only if the team's API access supports it; otherwise use
    a currently available compatible model behind the same adapter.
-   Tests: pytest for backend; frontend test tooling only if already
    configured. Prioritize API smoke tests over adding a new test
    framework late.
-   State: in-memory sessions for the demo.
-   Device execution: mock adapter with a small fixed device catalog.
-   Run locally with two terminals. Docker is optional, not a blocker.

**Avoid a database, authentication system, queue, vector database, RAG,
and multi-agent design.** None is necessary for the minimum interaction
loop.

------------------------------------------------------------------------

## 4. Three-way ownership

### Workstream A --- Frontend and localization

**Owner: Faraz Ansari**

**Owns:** `frontend/`, frontend interaction states, styling, language
labels, RTL behavior.

Tasks: 1. Create the main page and session start action. 2. Build
reusable `OptionGrid`, `ProgressIndicator`, `CommandReview`,
`ExecutionStatus`, and `ErrorNotice` components. 3. Implement the
stages: action → task → clarification (optional) → review → execution
result. 4. Connect to the agreed API contract. 5. Add English/Urdu label
dictionaries and a language toggle. 6. Set `dir="rtl"` for Urdu and
check button order, alignment, punctuation, and mixed-script command
text. 7. Add loading, timeout, retry, back, and cancel states. 8.
Provide a frontend mock mode or fixture responses on Day 1 so UI work
continues before backend integration. 9. Deliver a repeatable demo
sequence and note any UI limitations.

**Must not own:** LLM API calls, secrets, command authorization, device
execution logic, or session truth.

**Definition of done:** A user can complete the UI flow using the API or
fixtures; the final command is clearly displayed; confirmation and
result states are visible; Urdu RTL does not break the core screen.

### Workstream B --- Backend, workflow, and LLM

**Owner: Muhammad Ibrahim**

**Owns:** `backend/`, API contract, session state, LLM integration,
validation and confirmation enforcement.

Tasks: 1. Create Flask app and health route. 2. Implement session
creation and in-memory state. 3. Implement
action/task/clarification/draft routes with deterministic fallback data
first. 4. Add an `LLMProvider` adapter with one function per generation
stage. 5. Validate model output against expected schemas and reject
malformed options. 6. Implement command review and server-side
confirmation. 7. Ensure execution cannot proceed unless the session
contains a confirmed command. 8. Connect the command service to the
`AssistantAdapter` interface provided by Workstream C. 9. Add timeouts,
error responses, basic logs without secrets, and smoke tests. 10.
Provide `.env.example`, actual setup commands, and sample API calls.

**Must not own:** frontend layout, Urdu visual polish, or
device-specific code inside route handlers.

**Definition of done:** API works locally with fallback mode even
without an API key; model integration can be enabled via environment
configuration; invalid or unconfirmed commands are rejected.

### Workstream C --- Mock assistant, integration, QA, and demo

**Owner: Ashhal Aamir**

**Owns:** device/action catalog, mock execution adapter, API contract
test cases, integration test plan, demo script, project documentation.

Tasks: 1. Define the initial device catalog, for example
`living_room_light`, `bedroom_light`, `fan`, and `television`, with
supported capabilities. 2. Define allowed actions and parameters for
each device. 3. Implement `MockAssistantAdapter.execute(command)`
returning a stable result shape. 4. Write example user journeys and
expected command objects. 5. Create API smoke-test scripts or pytest
tests against the agreed contract. 6. Test success, unsupported device,
invalid action, missing confirmation, cancelled session, duplicate
execution, timeout/failure, and model fallback cases. 7. Review whether
the API contract is implemented consistently by frontend and backend. 8.
Prepare a 2--3 minute demo script, sample scenarios, and a
troubleshooting section. 9. Coordinate integration issues and maintain a
shared `INTEGRATION.md` checklist. 10. Confirm the README does not claim
the Urdu replication or participant study is complete.

**Must not own:** model prompt architecture or frontend implementation.
Provide interfaces and tests rather than building duplicate versions of
the other members' modules.

**Definition of done:** The mock adapter works independently, critical
API rules have tests, the end-to-end scenario is repeatable, and
documentation matches the actual build.

### Shared responsibilities

-   Every member pulls and runs the integrated branch daily.
-   Each owner reviews changes that cross their module boundary.
-   All members agree before changing shared API field names.
-   One person merges PRs, but no component is integrated for the first
    time on Day 7.
-   If the project already has a repository or stack, adapt this plan
    rather than creating a competing structure.

------------------------------------------------------------------------

## 5. Fixed API contract

Prefix all routes with `/api/v1`. JSON is the default request/response
format. The backend owns the session state.

### 5.1 Endpoints

  ------------------------------------------------------------------------------------------------
  Method                  Endpoint                                         Purpose
  ----------------------- ------------------------------------------------ -----------------------
  `GET`                   `/health`                                        Service health and mode

  `GET`                   `/api/v1/devices`                                Return mock
                                                                           environment/device
                                                                           catalog

  `POST`                  `/api/v1/sessions`                               Create session

  `GET`                   `/api/v1/sessions/{session_id}`                  Read current session
                                                                           state

  `POST`                  `/api/v1/sessions/{session_id}/actions`          Generate action options

  `POST`                  `/api/v1/sessions/{session_id}/tasks`            Generate task options
                                                                           for selected action

  `POST`                  `/api/v1/sessions/{session_id}/clarifications`   Submit answer or
                                                                           request clarification
                                                                           options

  `POST`                  `/api/v1/sessions/{session_id}/command-draft`    Build a complete
                                                                           command draft

  `POST`                  `/api/v1/sessions/{session_id}/confirm`          Confirm the current
                                                                           draft

  `POST`                  `/api/v1/sessions/{session_id}/execute`          Execute the confirmed
                                                                           command through the
                                                                           adapter

  `POST`                  `/api/v1/sessions/{session_id}/cancel`           Cancel the active
                                                                           workflow

  `DELETE`                `/api/v1/sessions/{session_id}`                  End session and clear
                                                                           in-memory context
  ------------------------------------------------------------------------------------------------

Do not add separate endpoints for every tiny UI action. The list above
is enough for the MVP.

### 5.2 Common conventions

-   JSON field names use `snake_case`.
-   Every response includes `ok: true` on success.
-   Errors use `ok: false` and a stable error object.
-   Session IDs are opaque strings generated by the backend.
-   Use HTTP status codes meaningfully: `400` invalid input, `404`
    unknown session/resource, `409` invalid workflow state or
    unconfirmed command, `502` upstream LLM failure when no fallback is
    possible, `500` unexpected server error.
-   Do not return stack traces or provider secrets to the frontend.
-   The frontend should not invent a session state if the server rejects
    a transition.

### 5.3 Create a session

`POST /api/v1/sessions`

Request:

``` json
{
  "language": "en",
  "environment_id": "demo_home"
}
```

Response:

``` json
{
  "ok": true,
  "session": {
    "session_id": "generated-id",
    "language": "en",
    "stage": "action_selection",
    "environment_id": "demo_home"
  }
}
```

Supported `language` values for the first version: `en`, `ur`.

### 5.4 Generate action options

`POST /api/v1/sessions/{session_id}/actions`

Request:

``` json
{}
```

Response:

``` json
{
  "ok": true,
  "stage": "action_selection",
  "options": [
    {"id": "turn_on", "label": "Turn on", "value": "turn_on"},
    {"id": "turn_off", "label": "Turn off", "value": "turn_off"},
    {"id": "set_level", "label": "Set level", "value": "set_level"}
  ]
}
```

These options are examples. The backend may return up to eight action
choices plus navigation controls handled by the UI.

### 5.5 Generate task options

`POST /api/v1/sessions/{session_id}/tasks`

Request:

``` json
{
  "action": "turn_on"
}
```

Response:

``` json
{
  "ok": true,
  "stage": "task_selection",
  "options": [
    {"id": "living_room_light", "label": "Living room light", "value": "living_room_light"},
    {"id": "bedroom_light", "label": "Bedroom light", "value": "bedroom_light"}
  ]
}
```

The server validates that `action` is supported. Task options must
reference devices in the configured catalog.

### 5.6 Clarification

`POST /api/v1/sessions/{session_id}/clarifications`

Request to submit an answer:

``` json
{
  "question_id": "brightness",
  "answer": "70"
}
```

Response:

``` json
{
  "ok": true,
  "stage": "review",
  "message": "Details saved"
}
```

For MVP speed, clarification may be deterministic: ask for a missing
value only when the selected action requires it. Avoid an elaborate
multi-turn planner unless time permits.

### 5.7 Create command draft

`POST /api/v1/sessions/{session_id}/command-draft`

Request:

``` json
{}
```

Response:

``` json
{
  "ok": true,
  "stage": "review",
  "command": {
    "device_id": "living_room_light",
    "action": "turn_on",
    "parameters": {}
  },
  "display_text": "Turn on the living room light",
  "confirmed": false
}
```

`display_text` is for review only. Execution must use the structured
`command` object, not parse arbitrary natural-language text.

### 5.8 Confirm

`POST /api/v1/sessions/{session_id}/confirm`

Request:

``` json
{
  "confirmed": true
}
```

Response:

``` json
{
  "ok": true,
  "stage": "ready_to_execute",
  "confirmed": true
}
```

Reject confirmation if no current draft exists. `confirmed: false`
should cancel or return to review rather than authorize execution.

### 5.9 Execute command

`POST /api/v1/sessions/{session_id}/execute`

Request:

``` json
{}
```

Response:

``` json
{
  "ok": true,
  "stage": "completed",
  "result": {
    "status": "success",
    "message": "Living room light turned on",
    "simulated": true
  }
}
```

Return `409` if the command is not confirmed. The mock adapter should
return `simulated: true` so nobody mistakes a simulation for real device
control.

### 5.10 Error response

``` json
{
  "ok": false,
  "error": {
    "code": "COMMAND_NOT_CONFIRMED",
    "message": "Confirm the command before execution."
  }
}
```

Suggested stable error codes: - `INVALID_REQUEST` -
`SESSION_NOT_FOUND` - `INVALID_STAGE` - `UNSUPPORTED_ACTION` -
`UNSUPPORTED_DEVICE` - `COMMAND_NOT_CONFIRMED` - `LLM_UNAVAILABLE` -
`LLM_INVALID_OUTPUT` - `EXECUTION_FAILED`

### 5.11 Contract freeze

On Day 1, the three owners should agree on: - Endpoint paths and HTTP
methods. - Request and response keys. - Session stages and allowed
transitions. - Device/action IDs. - Error shape. - The exact `command`
object.

After this, changes require a quick team agreement and simultaneous
updates to tests, backend, and frontend.

------------------------------------------------------------------------

## 6. Shared data model

Use one simple session object. In-memory storage is acceptable for a
local demo; sessions will be lost on restart.

``` python
session = {
    "session_id": "...",
    "language": "en",
    "environment_id": "demo_home",
    "stage": "action_selection",
    "selected_action": None,
    "selected_device_id": None,
    "parameters": {},
    "command_draft": None,
    "confirmed": False,
    "executed": False,
    "history": []
}
```

Use stable stage names:

-   `action_selection`
-   `task_selection`
-   `clarification`
-   `review`
-   `ready_to_execute`
-   `executing`
-   `completed`
-   `cancelled`
-   `error`

Keep the stage transitions in one backend workflow module, not scattered
through route handlers.

### Command object

``` json
{
  "device_id": "living_room_light",
  "action": "turn_on",
  "parameters": {}
}
```

For a brightness example:

``` json
{
  "device_id": "living_room_light",
  "action": "set_brightness",
  "parameters": {"level": 70}
}
```

The backend must validate device/action compatibility and parameter
ranges. The model cannot introduce arbitrary devices, actions, or
parameter names.

------------------------------------------------------------------------

## 7. Suggested repository layout

Adapt to the existing repository instead of restructuring needlessly.

``` text
project-root/
├── README.md
├── INTEGRATION.md
├── .env.example
├── .gitignore
├── frontend/
│   ├── src/
│   │   ├── api/client.ts
│   │   ├── components/
│   │   ├── pages/
│   │   ├── i18n/labels.ts
│   │   ├── types/api.ts
│   │   └── App.tsx
│   └── package.json
├── backend/
│   ├── app.py
│   ├── routes/
│   │   ├── health.py
│   │   ├── sessions.py
│   │   └── workflow.py
│   ├── schemas.py
│   ├── services/
│   │   ├── session_service.py
│   │   ├── workflow_service.py
│   │   ├── llm_service.py
│   │   └── command_service.py
│   ├── adapters/
│   │   └── assistant_mock.py
│   ├── config.py
│   ├── requirements.txt
│   └── tests/
└── docs/
    ├── architecture.md
    ├── api-contract.md
    └── demo-script.md
```

This is a proposal, not a claim about files that currently exist.

------------------------------------------------------------------------

## 8. Seven-day parallel schedule

### Day 1 --- Contract and independent stubs

**All members together, first 60--90 minutes** - Agree on the MVP and
the exact API contract above. - Confirm repo structure, ports, local
commands, stage names, and device catalog. - Create GitHub issues and a
shared integration branch. - Create `.env.example` and a no-secrets
`.gitignore`.

**Faraz** - Create UI skeleton and API client with mocked responses. -
Implement the action grid and stage navigation.

**Muhammad** - Create Flask app, `/health`, session creation, in-memory
session store. - Implement route stubs with the agreed response shapes.

**Ashhal** - Implement mock assistant adapter and device catalog. -
Create API smoke-test collection and `INTEGRATION.md`.

**End-of-day gate:** each component starts independently; API shapes
match; no member is blocked by another.

### Day 2 --- Complete the deterministic end-to-end flow

**Faraz** - Connect session creation, action options, task options,
draft review, and result screen to the API client or fixtures. - Add
loading/error/back/cancel states.

**Muhammad** - Implement deterministic action/task generation and
workflow transitions. - Implement command draft and confirmation
enforcement.

**Ashhal** - Implement mock execution and success/failure results. -
Test unsupported actions, missing session, invalid stage, and
unconfirmed execution.

**End-of-day gate:** a complete command can be constructed and executed
in mock mode without an LLM.

### Day 3 --- LLM integration and contract tests

**Faraz** - Connect the live API and remove any duplicate frontend
business logic. - Ensure UI follows backend-returned stage and errors.

**Muhammad** - Implement LLM adapter, prompt templates, schema
validation, timeout, and fallback behavior. - Keep deterministic
fallback enabled by default when credentials are absent.

**Ashhal** - Run contract tests against the real backend. - Add
regression cases for invalid model output, repeated execute requests,
and session isolation.

**End-of-day gate:** the LLM can improve suggestions, but the demo still
works if the provider fails.

### Day 4 --- Urdu/RTL and interaction completion

**Faraz** - Add Urdu labels, language switch, RTL layout, and
mixed-script checks.

**Muhammad** - Localize prompt instructions and labels returned by the
backend. - Ensure model language output does not change IDs or command
schema.

**Ashhal** - Test Urdu API responses and rendered UI; report text,
device, or TTS limitations. - Verify the README distinguishes proposed
research from completed implementation.

**End-of-day gate:** the core workflow works in English and a basic Urdu
UI mode.

### Day 5 --- Integration hardening

**Faraz** - Fix layout, keyboard/touch interaction, navigation, and
error display.

**Muhammad** - Fix state bugs, validation, server-side confirmation,
configuration, and exception handling.

**Ashhal** - Run regression checklist; test timeouts, cancellation,
duplicate execution, and mock adapter failures. - Measure model response
and total interaction latency.

**End-of-day gate:** no known blocker in the core demo; all critical
safety/state tests pass.

### Day 6 --- Freeze and rehearse

**All members** - Feature freeze. Only bug fixes and essential
documentation changes. - Clone into a clean directory or machine and
follow setup instructions. - Run the demo sequence several times with
and without an API key. - Verify no secrets, personal data, or raw
participant data are committed.

**End-of-day gate:** another teammate can start the system and reproduce
the demo using the README.

### Day 7 --- Final delivery

-   Fix only release-blocking bugs.
-   Tag a release or commit hash.
-   Record a short backup demo video if useful.
-   Finalize architecture, API, limitations, and future-work
    documentation.
-   Demonstrate the same preselected scenario reliably.

Do not begin real-device integration on Day 7 unless it already works
and does not risk the core demo.

------------------------------------------------------------------------

## 9. Integration rules

1.  **Single contract owner:** Muhammad maintains
    `docs/api-contract.md`; all three can propose changes, but update
    the document before changing code.
2.  **Mock first:** frontend fixtures and backend fallback responses
    must match the same schema.
3.  **Small PRs:** one issue per focused PR where practical.
4.  **Daily integration:** merge and test the integrated branch every
    day.
5.  **No silent API changes:** a field or route rename requires updates
    to frontend types, backend schemas, and contract tests.
6.  **Separate provider code:** only `llm_service.py` should know the
    LLM SDK specifics.
7.  **Separate device code:** routes call `command_service`, which calls
    an adapter; routes do not operate devices directly.
8.  **Secrets stay server-side:** only the backend reads the model API
    key.
9.  **No false success:** display execution success only when the
    adapter returns success.
10. **Keep a fallback:** deterministic options and mock execution must
    remain available for the demo.

### Daily 15-minute sync

Each member reports: - What is working now? - What is blocking
integration? - Which contract or file will change today? - What is the
end-of-day acceptance test?

------------------------------------------------------------------------

## 10. Demo scenario

Use one predictable scenario:

**"Turn on the living room light."**

1.  Start session in English.
2.  Select "Turn on."
3.  Select "Living room light."
4.  Review the command.
5.  Confirm.
6.  Mock assistant returns success.
7.  Show the same basic workflow in Urdu.
8.  Optionally demonstrate a missing-detail clarification or a failed
    LLM request falling back safely.

The demo should visibly label mock execution as simulated. If a model
API key is unavailable or network access fails, switch to deterministic
fallback mode instead of improvising during the presentation.

------------------------------------------------------------------------

## 11. Environment and configuration

Use backend environment variables; do not hardcode credentials.

Example `.env.example`:

``` dotenv
FLASK_ENV=development
PORT=5000
LLM_API_KEY=
LLM_MODEL=
LLM_ENABLED=false
FRONTEND_ORIGIN=http://localhost:5173
```

These are proposed names. Match them to the implementation. Keep
`LLM_ENABLED=false` or a fallback mode available so the app starts
without credentials.

Local development target: - Frontend: `http://localhost:5173` - Backend:
`http://localhost:5000` - Health check:
`GET http://localhost:5000/health`

Use a development CORS configuration restricted to the frontend origin.
Do not expose the backend to the public internet merely to make local
integration work.

------------------------------------------------------------------------

## 12. Test checklist

### Critical tests --- must pass

-   [ ] Health endpoint responds.
-   [ ] Session can be created and retrieved.
-   [ ] Action and task options match the contract.
-   [ ] Invalid action/device is rejected.
-   [ ] Draft displays a structured command and `confirmed: false`.
-   [ ] Execution before confirmation returns
    `409 COMMAND_NOT_CONFIRMED`.
-   [ ] Execution after confirmation returns an explicit mock result.
-   [ ] LLM unavailable or malformed output triggers fallback/error
    recovery.
-   [ ] Cancelled session cannot execute a command.
-   [ ] One session's context does not leak into another session.
-   [ ] UI displays failure rather than falsely showing success.
-   [ ] Urdu RTL mode renders the main workflow.
-   [ ] Clean setup works using documented commands.

### Nice-to-have if time remains

-   [ ] Keyboard-only navigation.
-   [ ] Persisted session history.
-   [ ] Real TTS playback.
-   [ ] Real smart-speaker integration.
-   [ ] More elaborate model-generated clarification.
-   [ ] Formal user study.

------------------------------------------------------------------------

## 13. Risks and cuts

  -----------------------------------------------------------------------
  Risk                                Immediate response
  ----------------------------------- -----------------------------------
  LLM API key or quota unavailable    Use deterministic fallback and mock
                                      execution

  Frontend/backend integration drifts Freeze API contract and run smoke
                                      tests daily

  Urdu TTS is unsupported             Deliver Urdu text/RTL UI; document
                                      TTS limitation

  Real assistant integration is       Keep mock adapter; do not block
  blocked                             delivery

  Too many features for seven days    Cut persistence, login, deployment,
                                      and optional screens

  Model generates invalid or unsafe   Validate structured output and
  commands                            allow-listed device/action pairs

  Last-day merge breaks the demo      Freeze features on Day 6 and keep a
                                      known-good commit
  -----------------------------------------------------------------------

### Explicitly out of scope for this week

-   Full production deployment and monitoring.
-   Multi-user authentication and role management.
-   Database-backed persistence.
-   Real device control unless trivial and verified.
-   Collecting participant data without required approval.
-   Claiming Urdu SUS/NPS/Adjective Scale validation without the
    appropriate process.
-   Claiming that the Pakistani replication has results before
    conducting it.

------------------------------------------------------------------------

## 14. Final definition of done

At the deadline, the team should be able to show, from a clean start:

1.  The app launches using documented commands.
2.  The user completes the action/task/review flow.
3.  The LLM provides suggestions when enabled; fallback works when it is
    not.
4.  The command is visible and requires explicit confirmation.
5.  The mock adapter executes only allowed, confirmed commands.
6.  The result is accurately reported.
7.  The basic Urdu/RTL UI is demonstrable.
8.  Critical API and workflow tests pass.
9.  The repository documents setup, architecture, API contract,
    limitations, and the proposed---not completed---research work.

**Priority order:** deterministic end-to-end workflow → API contract
stability → LLM suggestions → confirmation and error handling → Urdu/RTL
→ optional TTS/device integration. This order maximizes the chance of a
complete demo within one week.
