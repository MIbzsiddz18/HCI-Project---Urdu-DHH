# Implementation Plan
## Urdu DHH Intelligent Personal Assistant

**Project:** Deaf and Hard of Hearing Access to Intelligent Personal Assistants  
**Prototype:** Comparing voice-based input with an LLM-powered touch interface adapted for Urdu  
**Timeline:** 7 days  
**Branch:** `dev`

---

# Part 1 — System Architecture

## 1.1 Objective

Build a functional prototype that allows Deaf and Hard of Hearing (DHH) users to interact with an intelligent personal assistant through a visual, touch-based interface.

The user should be able to select an intended action, choose a task, answer clarification questions, review a proposed command, explicitly confirm it, and observe its simulated execution.

The initial implementation targets an Urdu-speaking context in Pakistan, with English support retained for development and testing.

**MVP priority:** Complete a reliable end-to-end workflow using mock devices before adding optional LLM functionality or attempting real device integrations.

## 1.2 Architecture Overview

```text
┌─────────────────────────────────────────┐
│          React + TypeScript             │
│                                         │
│ Touch UI | Task Selection | Review      │
│ Urdu/English | RTL/LTR | Status         │
└───────────────────┬─────────────────────┘
                    │
               HTTP / JSON
                    │
┌───────────────────▼─────────────────────┐
│             Flask REST API              │
│                                         │
│ Routes                                  │
│   ├── Session routes                    │
│   ├── Workflow routes                   │
│   └── Device routes                     │
│                                         │
│ Services                                │
│   ├── Session Service                   │
│   ├── Workflow Service                  │
│   ├── Command Service                   │
│   └── LLM Service (optional)            │
│                                         │
│ Adapter                                 │
│   └── Mock Assistant / Devices          │
└─────────────────────────────────────────┘
```

The frontend communicates only with the backend API. It must not call the LLM provider directly or execute device commands independently.

The backend owns session state, workflow transitions, command validation, confirmation enforcement, and simulated execution.

## 1.3 Technology Stack

| Component | Technology | Purpose |
|---|---|---|
| Frontend | React, TypeScript, Vite | Interactive touch interface |
| Backend | Python, Flask | REST API and workflow orchestration |
| API format | JSON over HTTP | Frontend/backend communication |
| LLM | Optional provider-compatible API | Generate suggestions and clarification questions |
| Device integration | Mock adapter | Simulate supported smart-home actions |
| Testing | pytest | Backend and API contract tests |
| Configuration | Environment variables | API keys and development settings |

Use the existing repository configuration where available. Do not introduce a second frontend or backend framework.

## 1.4 Repository Structure

```text
project-root/
├── frontend/
│   ├── package.json
│   ├── index.html
│   └── src/
│       ├── api/
│       │   └── client.ts
│       ├── components/
│       ├── pages/
│       ├── i18n/
│       │   └── labels.ts
│       ├── types/
│       │   └── api.ts
│       ├── App.tsx
│       └── main.tsx
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── routes/
│   │   ├── sessions.py
│   │   ├── workflow.py
│   │   └── devices.py
│   ├── services/
│   │   ├── session_service.py
│   │   ├── workflow_service.py
│   │   ├── command_service.py
│   │   └── llm_service.py
│   ├── adapters/
│   │   └── assistant_mock.py
│   └── tests/
│       └── test_api.py
├── docs/
│   ├── architecture.md
│   └── api-contract.md
├── .env.example
├── .gitignore
├── README.md
└── IMPLEMENTATION_PLAN.md
```

Keep modules focused on one responsibility. Add files only when needed rather than creating unnecessary abstractions.

## 1.5 Module Responsibilities

### Frontend

- `App.tsx`: Main application layout and language/direction setup.
- `pages/`: Main assistant workflow screen.
- `components/`: Reusable action cards, task options, clarification prompts, command review, and status indicators.
- `api/client.ts`: Centralized HTTP requests, error handling, and API base URL.
- `i18n/labels.ts`: English and Urdu interface labels.
- `types/api.ts`: Shared TypeScript interfaces for API requests and responses.

The interface must support large touch targets, clear visual feedback, keyboard-accessible controls, and Urdu right-to-left layout.

### Backend

- `app.py`: Create the Flask application, register routes, and expose the health endpoint.
- `routes/sessions.py`: Create, retrieve, and end sessions.
- `routes/workflow.py`: Handle action selection, task selection, clarification, command drafting, confirmation, and execution.
- `routes/devices.py`: Return the available mock devices and supported actions.
- `services/session_service.py`: Manage session state and lifecycle.
- `services/workflow_service.py`: Coordinate workflow stages and validate transitions.
- `services/command_service.py`: Validate, confirm, and execute allowed commands.
- `services/llm_service.py`: Optional LLM integration with deterministic fallback.
- `adapters/assistant_mock.py`: Supply mock devices and simulate assistant/device responses.
- `tests/test_api.py`: Verify API behavior, workflow progression, validation, and confirmation enforcement.

## 1.6 API Contract

All endpoints use the `/api/v1` prefix except `/health`.

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Check backend availability |
| GET | `/api/v1/devices` | List available mock devices |
| POST | `/api/v1/sessions` | Create a session |
| GET | `/api/v1/sessions/{session_id}` | Retrieve session state |
| POST | `/api/v1/sessions/{session_id}/actions` | Select an intended action |
| POST | `/api/v1/sessions/{session_id}/tasks` | Select a task |
| POST | `/api/v1/sessions/{session_id}/clarifications` | Submit clarification |
| POST | `/api/v1/sessions/{session_id}/command-draft` | Generate a command proposal |
| POST | `/api/v1/sessions/{session_id}/confirm` | Confirm the proposed command |
| POST | `/api/v1/sessions/{session_id}/execute` | Execute a confirmed command |
| POST | `/api/v1/sessions/{session_id}/cancel` | Cancel the current workflow |
| DELETE | `/api/v1/sessions/{session_id}` | End a session |

Request and response schemas must be documented in `docs/api-contract.md` before parallel implementation begins.

### Contract conventions

- JSON fields use `snake_case`.
- Session IDs are generated by the backend.
- The backend is the source of truth for workflow state.
- Every error response should contain a stable error code and a readable message.
- Invalid workflow transitions must return an appropriate 4xx response.
- An execution result must clearly identify simulated execution using `"simulated": true`.

### Session stages

```text
action_selection
      ↓
task_selection
      ↓
clarification (if required)
      ↓
review
      ↓
ready_to_execute
      ↓
executing
      ↓
completed
```

Cancellation and errors must be handled explicitly. A session must not skip required workflow stages.

### Command schema

```json
{
  "device_id": "living_room_light",
  "action": "turn_on",
  "parameters": {}
}
```

The backend must validate device IDs, supported actions, parameters, and the current session stage.

**Critical safety rule:** Drafting a command must never execute it. Execution is permitted only after explicit confirmation of the current command. Reject unconfirmed execution with HTTP `409` and error code `COMMAND_NOT_CONFIRMED`.

If a command changes after confirmation, its confirmation must be invalidated.

## 1.7 LLM and Mock Device Strategy

The application must work without an API key.

Implement deterministic suggestions and clarification rules first. The LLM service may later replace or improve suggestion generation without changing the API contract.

The LLM may:

- Suggest likely user intentions.
- Generate task options.
- Ask clarification questions.
- Help interpret supported natural-language requests.

The LLM must not execute commands directly, bypass validation, or mark commands as confirmed.

The mock adapter should initially support a small, predictable set of devices and actions, such as turning a light on or off and setting a thermostat temperature. Unsupported actions must return a controlled error.

No real smart-home device integration is required for the MVP.

## 1.8 Urdu and Accessibility Requirements

- Provide Urdu and English interface labels.
- Switch document direction between RTL for Urdu and LTR for English.
- Use appropriate Urdu text rendering and alignment.
- Present tasks and actions as clear selectable visual controls.
- Make clarification questions understandable and easy to answer.
- Show the proposed command before execution.
- Provide visible success, failure, loading, and cancellation states.
- Do not depend on sound alone to communicate important information.
- Keep text-to-speech or voice output optional; it is not a prerequisite for the touch-interface MVP.

---

# Part 2 — Team Responsibilities

Each member owns implementation deliverables, not just documentation. All members must use the agreed API contract and integrate through the shared `dev` branch.

## 2.1 Muhammad Ibrahim — Backend and Workflow

**Primary ownership:** Backend orchestration, session lifecycle, and command safety.

Deliverables:

1. Implement the Flask application and route registration.
2. Implement session creation, retrieval, and lifecycle management.
3. Implement workflow transitions and request validation.
4. Implement command drafting, confirmation, cancellation, and execution enforcement.
5. Add the optional LLM service behind a stable interface.
6. Ensure the deterministic fallback works without credentials.
7. Review backend tests and resolve integration defects.

**Definition of done:** The backend supports the documented workflow, rejects invalid transitions, and cannot execute an unconfirmed command.

## 2.2 Faraz Ansari — Frontend and Urdu Interface

**Primary ownership:** Touch interface, API integration, and bilingual presentation.

Deliverables:

1. Implement the main assistant screen.
2. Build reusable action, task, clarification, review, and status components.
3. Connect the interface to the backend through `client.ts`.
4. Define and use TypeScript API interfaces.
5. Implement Urdu/English switching and RTL/LTR layout.
6. Display backend validation errors and workflow state clearly.
7. Test the full interface against the deterministic backend.

**Definition of done:** A user can complete the workflow through the touch interface, review the proposed command, explicitly confirm it, and see the result.

## 2.3 Ashhal Aamir — Mock Adapter, Testing, and Integration

**Primary ownership:** Predictable device simulation, independent verification, and demo readiness.

Deliverables:

1. Implement the mock device catalog and supported action definitions.
2. Implement the mock assistant/device adapter.
3. Create API and workflow tests, including negative cases.
4. Test invalid device/action combinations and unconfirmed execution.
5. Verify frontend/backend integration using the agreed contract.
6. Prepare reproducible setup instructions and a short demo script.
7. Run clean-start and end-to-end checks and report defects.

**Definition of done:** The prototype can be started from documented instructions, its simulated actions behave consistently, and its critical workflow and safety rules are covered by tests.

## 2.4 Collaboration Rules

- Agree on `docs/api-contract.md` before developing dependent features in parallel.
- Keep changes within each member's owned modules where possible.
- Communicate any API schema change before implementing it.
- Use feature branches for independent work and merge through pull requests into `dev`.
- Avoid committing `.env` files containing secrets.
- Every merged feature must be runnable and include relevant tests.
- Integrate small changes frequently instead of merging all work at the end.

---

# Part 3 — Seven-Day Implementation Schedule

## Day 1 — Foundation and Contract

**Goal:** Everyone can develop against the same architecture.

- Muhammad: Initialize Flask, health endpoint, and basic route registration.
- Faraz: Verify frontend setup and create the application shell.
- Ashhal: Implement the initial mock device catalog and agree on test scenarios.
- All: Finalize API request/response schemas, session stages, and error conventions.

**Milestone:** Frontend and backend start independently; API contract is agreed upon.

## Day 2 — Deterministic End-to-End Workflow

- Muhammad: Implement sessions and workflow transitions.
- Faraz: Implement action/task selection and connect the initial API calls.
- Ashhal: Implement mock execution and test the main workflow.

**Milestone:** A user can select a task, generate a deterministic command, confirm it, and simulate execution.

## Day 3 — Clarification and Safety

- Muhammad: Implement clarification handling, command validation, and confirmation enforcement.
- Faraz: Add clarification UI, command review, and cancellation states.
- Ashhal: Add positive and negative API tests.

**Milestone:** Required clarification works, invalid commands are rejected, and unconfirmed execution is impossible through the API.

## Day 4 — Urdu and Optional LLM Integration

- Muhammad: Add the optional LLM provider behind the existing service interface.
- Faraz: Implement Urdu labels, language switching, and RTL layout.
- Ashhal: Test deterministic fallback behavior, mock responses, and representative Urdu workflows.

**Milestone:** The core workflow works in both languages, whether or not an LLM API key is configured.

## Day 5 — Integration and Error Handling

- Muhammad: Resolve backend defects and stabilize error responses.
- Faraz: Handle loading, network errors, invalid responses, and completed states.
- Ashhal: Run integrated tests and verify session isolation and command safety.

**Milestone:** No known critical defect in the main workflow.

## Day 6 — Feature Freeze and Rehearsal

- All: Freeze new features.
- Muhammad: Verify backend setup and confirmation enforcement.
- Faraz: Test the interface at presentation/demo size and verify RTL behavior.
- Ashhal: Verify clean setup, run the full test suite, and prepare demo steps.

**Milestone:** The prototype runs from documented setup instructions without relying on developer-specific configuration.

## Day 7 — Final Verification and Presentation

- Run the full workflow from a clean start.
- Verify the no-API-key fallback.
- Demonstrate Urdu/English interface behavior.
- Verify command review, explicit confirmation, simulated execution, and cancellation.
- Fix only critical defects and prepare the final demonstration.

**Milestone:** A stable, reproducible prototype ready for evaluation.

---

# Part 4 — Acceptance Criteria

The MVP is complete when all the following conditions are satisfied:

- [ ] Frontend and backend start using documented commands.
- [ ] The backend health endpoint responds successfully.
- [ ] A session can be created and retrieved.
- [ ] A user can select an action and task.
- [ ] Clarification is supported when needed.
- [ ] A proposed command is displayed before execution.
- [ ] The user must explicitly confirm the current command.
- [ ] Unconfirmed and invalid commands are rejected by the backend.
- [ ] Successful mock execution is reported as simulated.
- [ ] Cancellation and error states are handled.
- [ ] Urdu RTL and English LTR layouts work.
- [ ] The prototype runs without LLM credentials.
- [ ] Tests cover the core workflow and critical negative cases.
- [ ] Setup instructions and a repeatable demo script are available.

# Part 5 — Scope and Priorities

## Must have

- Working React/Flask integration.
- Session and workflow management.
- Touch-based task selection.
- Clarification and command review.
- Explicit confirmation and simulated execution.
- Urdu/English support.
- Deterministic fallback and essential tests.

## Should have

- Optional LLM-generated task suggestions.
- Improved Urdu phrasing and error messages.
- Stronger test coverage and polished demo flow.

## Out of scope for the first week

- Real smart-home device control.
- Real Alexa integration.
- User accounts and production authentication.
- Persistent database storage.
- Production deployment and scalability.
- Claims that the Urdu replication study has already been conducted.

These features can be considered after the core prototype is stable.

---

# Part 6 — Development Principles

1. **Contract first:** Define interfaces before parallel implementation.
2. **Mock first:** Make the complete workflow work without external services.
3. **Safety first:** Enforce confirmation and command validation on the backend.
4. **Modular design:** Keep routes, workflow logic, command validation, and adapters separate.
5. **Accessible by design:** Treat Urdu/RTL and visual feedback as core requirements.
6. **Test continuously:** Validate each integration milestone instead of waiting until Day 7.
7. **Freeze early:** Reserve the final two days for stabilization, setup verification, and demonstration.
