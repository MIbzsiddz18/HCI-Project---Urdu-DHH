# Deaf and Hard of Hearing Access to Intelligent Personal Assistants

### Comparing Voice-Based Input with an LLM-Powered Touch Interface --- and Proposing an Urdu Replication for Pakistan

```{=html}
<p align="center">
```
`<strong>`{=html}An HCI project on accessible interaction, speech
recognition, and context-aware AI for Deaf and Hard of Hearing (DHH)
users.`</strong>`{=html}
```{=html}
</p>
```
```{=html}
<p align="center">
```
`<em>`{=html}Team: Muhammad Ibrahim · Faraz Ansari · Ashhal
Aamir`</em>`{=html}
```{=html}
</p>
```

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#overview)
-   [Why This Project Matters](#why-this-project-matters)
-   [Project Goals](#project-goals)
-   [Background and Research Basis](#background-and-research-basis)
-   [The Three Interaction
    Conditions](#the-three-interaction-conditions)
-   [Proposed LLM-Assisted Touch
    Interface](#proposed-llm-assisted-touch-interface)
-   [System Architecture](#system-architecture)
-   [Research Questions](#research-questions)
-   [Evaluation Framework](#evaluation-framework)
-   [Findings Reported by the Original
    Study](#findings-reported-by-the-original-study)
-   [Proposed Urdu Replication in
    Pakistan](#proposed-urdu-replication-in-pakistan)
-   [Proposed Methodology](#proposed-methodology)
-   [Accessibility, Privacy, and Responsible
    AI](#accessibility-privacy-and-responsible-ai)
-   [Project Status and Scope](#project-status-and-scope)
-   [Technology Overview](#technology-overview)
-   [Repository Structure](#repository-structure)
-   [Getting Started](#getting-started)
-   [Configuration](#configuration)
-   [Potential Future Work](#potential-future-work)
-   [Team](#team)
-   [Acknowledgements and Research
    Attribution](#acknowledgements-and-research-attribution)
-   [License](#license)

------------------------------------------------------------------------

## Overview

Intelligent personal assistants (IPAs), such as voice-controlled smart
assistants, can make everyday tasks easier---but voice-first interaction
can create barriers for people who are Deaf or Hard of Hearing.
Automatic speech recognition (ASR) may not reliably understand every
speaker, including people whose speech differs from the patterns on
which a recognition system was trained. Alternative touch interfaces can
help, but conventional menus may be rigid, lengthy, or unaware of the
user's context.

This project reviews research on DHH people's access to intelligent
personal assistants and examines an **LLM-powered touch interface** as
an alternative way to formulate commands. The interface concept uses a
language model to suggest contextually relevant actions, lets the user
refine and confirm a command, and then passes the confirmed command to a
voice assistant through text-to-speech (TTS).

The project also proposes extending the study to **Urdu-speaking DHH
people in Pakistan**. This proposed replication would adapt the task
language, model prompts, usability instruments, participant recruitment,
and interview process to a different language and cultural setting.

> **Scope note:** The presentation describes findings from an existing
> CHI 2026 study and a proposed Urdu replication. Findings attributed to
> the original study are not results from our own Pakistani participant
> study. The Urdu replication is presented as a proposed methodology,
> not as completed or validated research.

## Why This Project Matters

Accessible interaction is not achieved simply by adding a touchscreen to
a voice assistant. An effective system must consider the range of
communication preferences and abilities of DHH users, including people
who use spoken language, sign language, or a combination of
communication methods.

The project focuses on four challenges:

1.  **Speech recognition reliability:** Recognition errors can make
    voice assistants frustrating or unusable for some speakers.
2.  **Limited flexibility in touch interfaces:** Static menus may not
    reflect the task or the user's immediate context.
3.  **Interaction delay and uncertainty:** Re-speaking workflows and
    model-generated suggestions can introduce waiting time or
    uncertainty about what the system heard.
4.  **Language and cultural coverage:** Findings from English-speaking
    participants in the United States cannot automatically be
    generalized to Urdu-speaking DHH communities in Pakistan.

An LLM-assisted touch interface is worth investigating because it may
help users construct commands through visible, selectable choices
without requiring every command to be spoken directly by the user.

## Project Goals

The project has two connected goals.

### 1. Understand the existing research

-   Review the original study comparing natural deaf speech, facilitated
    speech, and LLM-assisted touch.
-   Understand the study's interaction design, measures, quantitative
    results, and participant feedback.
-   Identify design opportunities and limitations that matter for
    accessible intelligent assistants.

### 2. Propose a context-sensitive Urdu replication

-   Adapt command vocabulary and model prompts to Urdu and a Pakistani
    smart-home context.
-   Plan translation and validation of usability and satisfaction
    measures.
-   Propose recruitment through Pakistani DHH schools and associations.
-   Preserve a comparable three-condition, within-subjects design where
    feasible, so results can be discussed alongside the original study.
-   Include interviews in participants' preferred language or
    communication mode, subject to appropriate language support.

## Background and Research Basis

The presentation reviews the paper:

**"Deaf and Hard of Hearing Access to Intelligent Personal Assistants:
Comparing Voice-Based Input with an LLM-Powered Touch Interface."**

The presentation attributes the original work to DeVries, Okosi, Li,
Dunphy, Gezae, Conway, Glasser, Kushalnagar, and Vogler, with Gallaudet
University and collaborators. It identifies the work as a CHI 2026
study.

The original study compares three ways for DHH participants to interact
with a voice assistant. Its central motivation is that current voice
recognition and conventional touch interfaces can both create friction,
while a context-aware LLM might make touch-based command construction
more flexible.

This repository README summarizes the project framing and proposed
extension as described in the team's presentation. Please add the
paper's official publication URL, DOI, or BibTeX entry here once
verified against the final publication record.

## The Three Interaction Conditions

The original study used a mixed-methods, within-subjects design with 20
participants and three conditions.

  -----------------------------------------------------------------------
  Condition               How it works            What it helps
                                                  investigate
  ----------------------- ----------------------- -----------------------
  **Natural Deaf Speech** The participant speaks  How well the assistant
                          directly to the voice   recognizes the
                          assistant using their   participant's speech
                          own speech.             and how usable the
                                                  experience feels.

  **Facilitated English   A hidden researcher     How participants
  (Wizard-of-Oz)**        re-speaks the           experience a
                          participant's command   facilitated speech
                          clearly to the          pathway, including
                          assistant.              accuracy and the delay
                                                  or ambiguity introduced
                                                  by re-speaking.

  **LLM-Assisted Touch**  The participant selects Whether a flexible
                          context-aware options   touch interface can
                          on a tablet. The final  support command
                          command is confirmed    construction without
                          and read aloud to the   requiring the
                          assistant using TTS.    participant to speak
                                                  the full command
                                                  directly.
  -----------------------------------------------------------------------

A within-subjects design means that participants experience multiple
conditions, allowing their experiences to be compared across interaction
methods. The proposed Urdu replication would retain this overall
structure where feasible, while carefully documenting any necessary
localization changes.

## Proposed LLM-Assisted Touch Interface

The interface concept is designed to help users construct a complete
command through a series of manageable decisions rather than navigating
a large static menu or speaking a complete command.

### Interaction flow

1.  **Verb selection:** The language model suggests starter
    actions---for example, "Turn," "Set," or "Show"---using the
    available context and interaction history.
2.  **Task selection:** After the user selects an action, the model
    suggests task-specific options.
3.  **Detail clarification:** If important information is missing, the
    interface can ask a clarifying question and offer answer choices.
4.  **Review and confirmation:** The user sees the assembled command and
    confirms it before it is sent onward.
5.  **Speech output:** Text-to-speech reads the confirmed command to the
    voice assistant.

### Context maintained by the concept

The presentation describes three kinds of session context:

-   **Command history:** Previous commands that may help keep the
    interaction coherent.
-   **Running task list:** The tasks or actions currently being worked
    through.
-   **Smart-home environment:** A description of relevant devices, such
    as lights, plugs, and televisions.

### Interface characteristics in the presentation

-   A 3 × 3 button grid on each screen.
-   Eight proposed starter verbs at the first stage.
-   A clarification stage when more information is required.
-   An explicit command-confirmation stage before TTS.
-   Approximately 2 seconds for the Flask-to-GPT-4o round trip and
    approximately 8--10 seconds for total touch-command latency, as
    reported in the presentation's description of the original system.

These figures describe the system discussed in the presentation; they
are not performance guarantees for a new implementation or for the
proposed Urdu adaptation.

## System Architecture

The presentation describes the LLM-assisted touch system at a high level
as:

``` text
┌─────────────────────────┐
│      Tablet UI          │
│                         │
│ Select action, task,    │
│ details, and confirm    │
└────────────┬────────────┘
             │ User choices / context
             ▼
┌─────────────────────────┐
│      Flask Server       │
│                         │
│ Maintains session       │
│ context and coordinates │
│ the command workflow    │
└────────────┬────────────┘
             │ Prompt + context
             ▼
┌─────────────────────────┐
│        GPT-4o            │
│                         │
│ Suggests actions, tasks,│
│ and clarifying options  │
└────────────┬────────────┘
             │ Structured suggestions
             ▼
┌─────────────────────────┐
│   Tablet UI Review      │
│                         │
│ User confirms command   │
└────────────┬────────────┘
             │ Confirmed text
             ▼
┌─────────────────────────┐
│     Text-to-Speech      │
└────────────┬────────────┘
             ▼
┌─────────────────────────┐
│    Voice Assistant      │
│  (e.g., Alexa in the    │
│   original study)       │
└─────────────────────────┘
```

This diagram represents the architecture described in the presentation,
not a claim that this repository contains a deployable version of every
component. The precise API contract, state management, device
integration, authentication, and error-handling behavior should be
documented from the implementation if and when code is added.

## Research Questions

The original study, as summarized in the presentation, addresses:

-   **RQ1:** How do DHH voice users perceive the usability and
    usefulness of LLM-generated task suggestions compared with deaf
    speech input?
-   **RQ2:** How do satisfaction ratings compare between natural deaf
    speech and Wizard-of-Oz facilitated speech?

For the proposed Pakistani replication, the same broad questions can be
examined in an Urdu-language and local context. The team should
pre-register or otherwise document any changes to the questions before
collecting data, to make the comparison transparent.

## Evaluation Framework

The presentation identifies several quantitative measures and a
qualitative interview component.

  -----------------------------------------------------------------------
  Measure                             Purpose
  ----------------------------------- -----------------------------------
  **System Usability Scale (SUS)**    Standardized assessment of
                                      perceived system usability. The
                                      original study used English or an
                                      ASL translation.

  **Adjective Scale**                 A 1--7 holistic usability rating,
                                      as described in the presentation.

  **Net Promoter Score (NPS)**        A measure related to participants'
                                      likelihood of recommending the
                                      system.

  **Word Error Rate (WER)**           Recognition-error measure for the
                                      Natural Deaf Speech condition,
                                      using SCLite in the original study.

  **Semi-structured interviews**      Qualitative insight into
                                      participants' experience,
                                      preferences, frustrations, and
                                      technology adoption. The
                                      presentation reports interviews of
                                      approximately 15--30 minutes per
                                      participant.
  -----------------------------------------------------------------------

For a Pakistani Urdu replication, the proposed plan is to translate and
back-translate the relevant instruments and review them with appropriate
language and Pakistani Sign Language (PSL) expertise. Translation alone
does not establish that an instrument is psychometrically valid for a
new population; validation should be treated as a research task and
reported honestly.

### Analysis plan to consider

Subject to the final protocol and available expertise, a replication
could:

-   Compare usability and satisfaction scores across the three
    conditions.
-   Report descriptive statistics and uncertainty, not only averages.
-   Analyze WER for the natural-speech condition and examine its
    relationship with usability.
-   Analyze interview data thematically.
-   Document missing data, exclusions, changes to the protocol, and any
    differences from the original study.
-   Avoid treating a small sample as representative of all Pakistani DHH
    people.

The final statistical tests should be selected in advance based on the
study design, data characteristics, and research guidance.

## Findings Reported by the Original Study

The presentation reports the following findings from the original study
with 20 participants.

### Quantitative results

  -----------------------------------------------------------------------
  Result                               Value reported in the presentation
  ------------------------------ ----------------------------------------
  Mean SUS --- Natural Deaf                                          59.6
  Speech                         

  Mean SUS --- Facilitated                                           62.5
  English                        

  Mean SUS --- LLM Touch                                             63.5

  Difference in SUS between       No statistically significant difference
  conditions                                                     reported

  Correlation between WER and                     *r* = −0.51, *p* = .022
  SUS                            

  Participants with zero Alexa                                        50%
  recognition errors             

  Participants with WER of 100%                            2 participants
  -----------------------------------------------------------------------

The presentation also cites a SUS score of 71.6 from a prior ASL-input
study for comparison. This is contextual information from prior work,
not a fourth condition in the original three-condition experiment.

**Interpretation:** The presentation reports that usability scores did
not differ significantly across the three tested conditions. It also
reports a negative association between WER and SUS, suggesting that
worse speech recognition was associated with lower perceived usability
in this sample. These findings should not be interpreted as proof that
the methods are equivalent or that results will generalize to
Urdu-speaking users.

### Qualitative themes

The presentation groups participant feedback into three areas:

**Voice interaction** - Some participants were surprised that the
assistant understood their deaf-accented speech. - Facilitated speech
could be accurate, but the re-speaking delay sometimes caused
confusion. - Some participants were unsure whether the device had heard
them or the facilitator.

**Touch interaction** - Participants generally responded positively to
being able to see and select options. - Waiting for generated
suggestions and unpredictable option ordering caused frustration. -
Participants wanted a visible "type your own" option and shortcuts or
favorites.

**Technology adoption** - There was interest in hands-free interaction
for situations such as cooking, driving, or emergencies. - The
presentation reports interest in sign-language recognition for
intelligent assistants. - Participants expressed mixed comfort with AI
learning their habits and wanted control over data.

These themes motivate the proposed localization and provide design
considerations to investigate---not assumptions to impose on Pakistani
participants.

## Proposed Urdu Replication in Pakistan

### Why adapt the study?

The original study described in the presentation focused on
English-speaking DHH users in the United States. A replication in
Pakistan could examine how language, local smart-home context,
communication preferences, device access, and familiarity with voice
assistants affect the experience.

The presentation identifies several adaptation areas:

-   Urdu ASR and Urdu-accented deaf speech.
-   Translation and validation of SUS, the Adjective Scale, and NPS for
    the intended use.
-   Local task commands and LLM prompts.
-   TTS and wake-word handling for the selected Urdu-speaking
    smart-speaker setup.
-   Recruitment through Pakistani DHH schools or associations.
-   Interviews in Urdu or PSL, according to participant preference and
    available qualified support.

The project should not assume that all DHH participants use the same
language, literacy approach, speech style, or sign language. Recruitment
and study materials should make room for individual communication
preferences.

## Proposed Methodology

The following is the methodology proposed in the presentation.

### Phase 1 --- Translate and validate the instruments

1.  Translate the usability and satisfaction measures into Urdu.
2.  Back-translate and compare the versions for meaning.
3.  Seek review from people with appropriate Urdu-language, HCI,
    accessibility, and PSL expertise.
4.  Pilot the materials with appropriate consultation before the main
    study.
5.  Document translation decisions and any limitations in comparability
    with the original instruments.

### Phase 2 --- Localize the LLM touch prompts

1.  Adapt the original prompt workflow for Urdu task vocabulary.
2.  Use examples that reflect a locally appropriate smart-home
    environment.
3.  Check the quality and clarity of generated choices, clarification
    questions, and final commands.
4.  Test Urdu text rendering and the selected TTS/wake-word workflow.
5.  Keep the final command visible and require user confirmation before
    sending it to the voice assistant.

### Phase 3 --- Recruit Pakistani DHH participants

1.  Explore collaboration with DHH schools, associations, and community
    representatives.
2.  Define transparent inclusion criteria and recruitment procedures.
3.  Provide accessible study information and consent materials.
4.  Ask participants about their preferred communication method and
    accommodate it where feasible.
5.  Obtain the required institutional or ethics approval before
    recruitment or data collection.

### Phase 4 --- Run sessions and compare results

1.  Conduct the three interaction conditions using a documented and
    consistent protocol.
2.  Collect the planned usability, satisfaction, and speech-recognition
    measures.
3.  Conduct semi-structured interviews in Urdu or PSL, as appropriate
    and feasible.
4.  Analyze quantitative and qualitative data according to a documented
    plan.
5.  Compare findings with the original study while explicitly
    identifying methodological and contextual differences.

### Expected output of the proposed replication

The intended outcome is evidence about how these interaction approaches
work in a Pakistani Urdu-speaking DHH context, what changes are needed
for localization, and which accessibility needs should guide future
design. The direction and magnitude of any results remain unknown until
the study is conducted.

## Accessibility, Privacy, and Responsible AI

An LLM-assisted interface can introduce new barriers as well as
opportunities. Accessibility and user control should be treated as
design requirements throughout the project.

-   **User confirmation:** Show the complete command and allow the user
    to correct it before execution.
-   **Visible alternatives:** Consider a way to type a custom command
    rather than forcing users to choose from generated options.
-   **Predictability:** Keep button placement and interaction patterns
    consistent where possible.
-   **Latency feedback:** Clearly indicate when the system is generating
    suggestions and provide useful feedback if it is slow or fails.
-   **Error recovery:** Allow users to go back, revise details, cancel,
    or retry without restarting the entire interaction.
-   **Language accessibility:** Test Urdu script rendering,
    right-to-left layout, wording, and speech output with intended
    users.
-   **Communication choice:** Do not assume that speech, Urdu text, or
    PSL alone will suit every participant.
-   **Data minimization:** Avoid collecting or retaining voice
    recordings, transcripts, or interaction history unless necessary and
    appropriately consented to.
-   **Transparency:** Explain what context is sent to the language
    model, how it is used, and what data is retained.
-   **Safety:** Require confirmation for commands that could have
    meaningful consequences, and provide a clear cancel path.
-   **Research ethics:** Use informed consent, protect participant
    identities, and store research data securely under the approved
    protocol.

These are recommended considerations for the project and future
implementation; they should not be read as verified features of the
original system.

## Project Status and Scope

Based on the team's presentation, this project currently documents a
review of an existing study and a proposed Urdu replication methodology.

  -----------------------------------------------------------------------
  Component                           Status described by the
                                      presentation
  ----------------------------------- -----------------------------------
  Review of the original CHI 2026     Presented
  study                               

  Summary of the original             Presented
  three-condition design and findings 

  Conceptual description of the       Presented
  LLM-assisted touch workflow         

  Proposed Urdu localization and      Proposed
  replication methodology             

  Urdu instrument translation and     Not reported as completed
  validation                          

  Recruitment and data collection in  Not reported as completed
  Pakistan                            

  Results from a Pakistani            Not available in the presentation
  replication                         
  -----------------------------------------------------------------------

Update this table as the project develops. Only mark implementation,
validation, recruitment, or evaluation as completed when the team has
evidence to support that status.

## Technology Overview

The presentation names or describes the following technologies and
components in the original system or proposed workflow:

  -----------------------------------------------------------------------
  Technology / component              Role
  ----------------------------------- -----------------------------------
  **GPT-4o**                          Generates context-aware action
                                      suggestions, task options, and
                                      clarification choices in the
                                      described interface.

  **Flask**                           Server component in the
                                      architecture described by the
                                      presentation.

  **Tablet user interface**           Presents selectable choices and the
                                      final command for review.

  **Text-to-speech (TTS)**            Reads the confirmed command aloud
                                      to the voice assistant.

  **Voice assistant (Alexa in the     Receives the spoken command in the
  original study)**                   original experimental setup.

  **SCLite**                          Used for Word Error Rate analysis
                                      in the original study, as reported
                                      in the presentation.
  -----------------------------------------------------------------------

This is a technology overview of the described research system, not a
verified list of dependencies for this GitHub repository. The
repository's actual framework versions, package dependencies, API setup,
and hardware requirements should be added once the implementation is
available.

## Repository Structure

The team's presentation does not specify a source-code repository
structure. Replace this section with the actual tree when code is
available. For example, a future implementation might separate the user
interface, server, prompt/configuration files, study materials, and
documentation:

``` text
project-root/
├── README.md
├── docs/                 # Study protocol and design documentation
├── frontend/             # Tablet or web interface, if implemented
├── backend/              # Server and model integration, if implemented
├── prompts/              # Localized prompts, if appropriate
├── study-materials/      # Approved participant-facing materials
└── tests/                # Automated tests, if implemented
```

The tree above is **illustrative only**. It is not a statement about
files that already exist in this repository. Do not create or describe
folders as implemented until they are present.

## Getting Started

The presentation does not provide installation instructions or identify
the current repository's runnable implementation. Consequently, exact
setup commands cannot yet be stated reliably.

When the implementation is ready, add the following details:

1.  **Prerequisites:** Supported operating system, runtime versions,
    package manager, and any required device or smart-speaker setup.
2.  **Installation:** Exact dependency installation commands for the
    actual frontend and backend.
3.  **Configuration:** Required environment variables and how to
    configure them safely.
4.  **Run instructions:** Commands to start each service and access the
    interface.
5.  **Testing:** Commands for automated tests and any manual
    device-integration checks.
6.  **Troubleshooting:** Common setup, network, model API, TTS, and
    device-connection errors.

Never commit API keys, participant information, recordings, transcripts,
or other secrets to the repository.

## Configuration

If a future implementation integrates with a hosted LLM or external
voice service, use environment variables or an appropriate
secret-management mechanism. A future `.env.example` may document
variable names without containing real credentials.

Possible configuration categories---**not confirmed environment-variable
names**---include:

-   LLM provider credentials and model selection.
-   Server host and port.
-   Session and context configuration.
-   TTS provider or output settings.
-   Voice-assistant integration settings.
-   Logging and data-retention options.

Document the actual variable names and defaults from the code before
asking contributors to configure them. Use mock responses or a test mode
where possible so that interface development does not always require
live API calls.

## Potential Future Work

Possible next steps for the team include:

1.  Implement or document a reproducible version of the described
    tablet-to-server workflow.
2.  Make the interface usable with keyboard navigation, screen readers
    where appropriate, clear focus indicators, and accessible text
    sizing.
3.  Add stable button ordering, a custom-text path, favorites, and a
    clear back/cancel workflow.
4.  Evaluate Urdu generation quality, right-to-left layout, and TTS
    behavior with qualified language and accessibility reviewers.
5.  Conduct a pilot to identify confusing tasks, translation issues,
    latency problems, and consent-material gaps.
6.  Complete the required ethics review and study preparation before
    recruiting participants.
7.  Publish a transparent evaluation protocol and report limitations
    alongside any results.
8.  Investigate additional language and communication modes only with
    input from the communities concerned.

## Team

This project is prepared by:

-   **Muhammad Ibrahim**
-   **Faraz Ansari**
-   **Ashhal Aamir**

The presentation does not assign individual responsibilities, so no role
allocation is implied here. Add affiliations, contribution statements,
and contact details only after the team has agreed on the information to
publish.

## Acknowledgements and Research Attribution

This project is based on a review of the CHI 2026 paper titled *"Deaf
and Hard of Hearing Access to Intelligent Personal Assistants: Comparing
Voice-Based Input with an LLM-Powered Touch Interface,"* attributed in
the team's presentation to DeVries, Okosi, Li, Dunphy, Gezae, Conway,
Glasser, Kushalnagar, Vogler, and collaborators.

Please verify and add the official paper URL, full bibliographic
details, and any related materials from the publisher or authors before
publication. Cite the original authors whenever reproducing or
discussing their study design, results, or interface concept.

## License

No license is specified in the team's presentation. Add a license only
after deciding what the repository will distribute and confirming that
the team has the rights to release that material. If the repository
includes third-party code, research instruments, prompts, images, or
study materials, check their respective terms before redistributing
them.

------------------------------------------------------------------------

```{=html}
<p align="center">
```
`<em>`{=html}Accessible technology should offer people meaningful
choice, predictable interaction, and control over how they
communicate.`</em>`{=html}
```{=html}
</p>
```
