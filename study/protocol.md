# Experimental Protocol: Usability Study of an LLM-Assisted Touch Interface for Pakistani Deaf and Hard of Hearing Urdu Speakers

## Study overview

This protocol describes a single-session usability study for a bilingual Urdu/English smart-home touch interface designed for Pakistani Deaf and Hard of Hearing (DHH) users. The aim is to observe how easily participants understand, navigate, and complete tasks using a simulated LLM-assisted assistant interface.

- Target session length: 35–40 minutes
- Participants: 5–8 Pakistani DHH adults who use Urdu and/or Pakistan Sign Language (PSL), with varying levels of prior technology experience
- Setting: Quiet room or lab; one researcher/facilitator; optional note-taker if available
- Materials: consent form, demographic survey, app, observation sheet, SUS questionnaire, interview guide, recording device (optional)

The session follows this flow: consent, pre-survey, 5-minute exploration, five structured tasks, SUS questionnaire, and a 5-minute semi-structured interview.

---

## Before the participant arrives

### Researcher preparation (5–10 minutes before session)

1. Confirm the testing room is quiet, well-lit, and free from distractions.
2. Set up the device with the study app running and test all interactions.
3. Prepare the participant packet:
   - consent form
   - demographic survey
   - SUS questionnaire
   - note-taking sheet or digital log
4. Check that the app is working and that the smart-home state is reset before each participant. Use the app's **Reset session and home** control between participants and confirm the data output directory is writable.
5. Confirm that the participant’s preferred communication mode is available (Urdu text, English text, sign support, or interpreter if needed).
6. If recording is used, confirm informed consent before starting audio/video capture.
7. Keep the session log ready for recording completion time, errors, help requests, and qualitative notes.
8. Assign a participant code (for example, P01). Do not enter the participant's name in the app.

---

## Session procedure

### 1. Arrival, greeting, and room setup
Estimated time: 2 minutes

1. Welcome the participant and thank them for attending.
2. Ask them to sit comfortably in front of the device.
3. Briefly explain that the study is about testing the usability of a smart-home touch interface, not their intelligence or ability.
4. Confirm the participant uses the preferred communication method for the session.
5. Ensure the participant can see the screen clearly and has enough space to interact without pressure.

Researcher script:
> “Thank you for participating. Today we are testing a touch-based smart-home app. We are interested in how easy or difficult it is to use, and your feedback will help improve the design. There are no right or wrong answers.”

---

### 2. Consent and confidentiality briefing
Estimated time: 4 minutes

1. Present the consent form in the participant’s preferred language and format.
2. Explain the purpose of the study in simple, clear language.
3. Clarify the following points:
   - participation is voluntary
   - they may stop at any time without penalty
   - they may skip any question they do not wish to answer
   - the session is being observed for research purposes
   - any data will be anonymized and kept confidential
4. Ask whether they have any questions before signing or agreeing.
5. If the participant agrees, obtain consent and note the time.

Important reminder:
- Do not pressure the participant to continue.
- If the participant is uncomfortable or unsure, pause and allow them time.
- If using recordings, explicitly confirm consent for recording before pressing record.

---

### 3. Pre-session demographic and background survey
Estimated time: 4 minutes

1. Enter the participant code and demographic answers in the app, confirm consent, and start the session. Also provide the demographic questionnaire and ask the participant to complete it.
2. Use the standard form from the project’s demographic survey to collect:
   - age
   - gender
   - hearing status
   - hearing device(s)
   - preferred communication languages
   - prior experience with voice assistants
   - accessibility needs
3. If needed, read the questions aloud, show them on screen, or provide written assistance in Urdu/English.
4. Note any accommodations required during the study.

Researcher prompt:
> “Please answer the questions as honestly as you can. You may skip any question you prefer not to answer.”

---

### 4. App introduction and accessibility check
Estimated time: 2 minutes

1. Briefly explain the function of the app: a touch-based smart-home assistant that shows options in Urdu and English.
2. Explain that the participant will interact with the interface and complete tasks, not with real hardware.
3. Mention that the app is a simulation and that the researcher may observe but will not intervene unless necessary.
4. Clarify that the participant should think aloud if comfortable, but this is optional.
5. Ask the participant to begin when ready.

Example script:
> “This app is a simulated smart-home assistant. The goal is to complete a few example actions such as checking weather, setting a timer, changing a light, or showing a recipe. Please use the app as you normally would. There is no need to rush.”

---

### 5. Five-minute exploration phase
Estimated time: 5 minutes

1. Allow the participant to explore freely without any timed tasks. Start the logged session after exploration; the app then presents the five timed tasks in order.
2. Encourage them to click, read, and navigate the interface naturally.
3. Observe whether they understand the layout, wording, and next steps.
4. Do not give instructions on how to complete specific tasks during this phase.
5. If the participant asks a direct question unrelated to system function, answer minimally and neutrally.
6. Take notes on their first impressions, confusion points, and any accessibility barriers.

Researcher behavior:
- Keep interactions to a minimum.
- Avoid prompting with solution-specific hints.
- Record observations such as hesitation, repeated taps, confusion about labels, or uncertainty about the next screen.

---

### 6. Task 1: Check Lahore weather
Estimated time: 2 minutes

Task goal: Ask the system to check today’s weather in Lahore.

Instructions:
1. Read the task currently shown in the app: “Please complete the following task using the app: check today’s weather in Lahore.”
2. Allow the participant to navigate independently.
3. Observe whether they identify the correct action and whether the Urdu/English wording supports comprehension.
4. If the participant gets stuck, wait briefly before offering a neutral prompt such as: “Please use the app as you would normally.”
5. Record whether the task was completed successfully and whether the participant needed help.
6. Confirm the simulated command only after the participant chooses a suggestion. If the participant cannot complete the task, use **Could not complete** so the outcome and latency are recorded accurately.

Expected state/action: weather information for Lahore should appear in the interface.

---

### 7. Task 2: Set a 5-minute tea timer
Estimated time: 2 minutes

Task goal: Ask the system to set a 5-minute timer for tea.

Instructions:
1. Say: “Please set a 5-minute timer for tea.”
2. Observe whether the participant understands the timer option and whether the wording is intuitive.
3. Record any ambiguity in the language or button choices.
4. Note whether the participant attempts to use a different command structure or misinterprets the task.

Expected state/action: the timer is set to 5 minutes.

---

### 8. Task 3: Change the light to blue
Estimated time: 2 minutes

Task goal: Set the smart-home light color to blue.

Instructions:
1. Say: “Please change the light to blue.”
2. Watch whether the participant chooses the correct action flow and understands the visual state changes.
3. Note whether the participant reads the label correctly or looks for the light control in the wrong place.
4. Record whether task completion is quick, delayed, or unsuccessful.

Expected state/action: light turns on and appears blue.

---

### 9. Task 4: Show a biryani recipe
Estimated time: 2 minutes

Task goal: Ask the app to display a biryani recipe.

Instructions:
1. Say: “Please show a biryani recipe.”
2. Observe whether the participant recognizes the recipe function and whether the app language matches the task meaning.
3. Record any hesitation in finding the recipe option or confusion over wording.
4. Note reaction to the content and how easy it is to navigate to the correct option.

Expected state/action: the recipe panel or content appears in the app.

---

### 10. Task 5: Set a Fajr reminder
Estimated time: 2 minutes

Task goal: Set a reminder for Fajr prayer.

Instructions:
1. Say: “Please set a reminder for Fajr.”
2. Observe whether the participant understands the reminder function and whether cultural context affects their ability to complete it.
3. Record how they interpret the label and whether they use the app’s suggestions naturally.
4. Note whether there is any confusion between reminder, timer, and calendar-related actions.

Expected state/action: Fajr reminder is scheduled.

---

### 11. System Usability Scale (SUS) questionnaire
Estimated time: 4 minutes

1. Provide the SUS questionnaire in the participant’s preferred language format.
2. Ask the participant to rate each item on the 1–5 Likert scale.
3. If needed, read the items aloud or explain terms without suggesting how to answer.
4. Encourage the participant to answer based on their actual experience with the app.
5. Record the final SUS score and note any missing or unclear responses.
6. Enter the 10 item responses, adjective rating (1–7), and NPS response (0–10) in the app. Each entry is saved automatically.

Instructions for the researcher:
- Do not interpret the questions for them.
- Keep wording neutral.
- If a participant asks what an item means, rephrase briefly without leading them.

---

### 12. Semi-structured interview
Estimated time: 5 minutes

1. Conduct a short, conversational interview using the prepared interview guide.
2. Ask the five main questions below, allowing the participant time to answer:
   1. Which part of the app was easiest and which was most difficult?
   2. How clear and natural were the Urdu words and sentences?
   3. What did you think about the app remembering habits or preferences?
   4. Would you want a hands-free option such as voice or sign-based interaction?
   5. What one change would improve the app most?
3. Use optional probes only when necessary.
4. Encourage the participant to speak in their preferred language or communication mode.
5. Record responses in notes or, with permission, an audio recording.
6. Enter brief notes for each interview question in the app. Audio is not captured by the app and must be stored separately under the participant code.

Interview prompts:
- “Can you give an example?”
- “What made that difficult or easy?”
- “Is there anything else you would like to change?”

Important note:
- Keep the interview conversational and respectful.
- Do not correct or challenge participant comments.
- If the participant uses sign language, a sign interpreter or support person may be involved as needed.

---

### 13. Debriefing, thanks, and close-out
Estimated time: 2 minutes

1. Thank the participant for their time and feedback.
2. Briefly explain what the study was testing and how their feedback will be used.
3. Ask whether they would like a summary of the results once the study is complete.
4. Confirm that they have no additional questions.
5. End the session and log the final notes in the participant session file.
6. Select **Save and finish session** in the app, then confirm the session was saved before resetting for the next participant.

Example closing script:
> “Thank you for your time and honest feedback. Your responses will help us improve the app for Pakistani Deaf and Hard of Hearing users. We appreciate your contribution.”

---

## Researcher observation checklist

During the session, record the following:

- time to first successful interaction
- number of navigation errors
- number of times the participant asks for help
- number of incorrect taps or dead ends
- task completion success/failure
- whether the participant appears confused by Urdu wording or app flow
- preference for Urdu, English, or a mixed-language interface
- comments about privacy, accessibility, or assistive alternatives

These notes should be entered into the project’s session log template to support later analysis.

---

## Recommended researcher behavior

- Use calm, neutral language at all times.
- Speak slowly and clearly.
- Allow participants to proceed at their own pace.
- Avoid giving direct answers to task questions unless absolutely required for safety or to prevent abandonment.
- Treat the participant as the expert on their own experience.
- Offer accommodations when needed, including larger text, extra time, or a communication support person.

---

## Session summary

A full session should run approximately 35–40 minutes and include the following sequence:

1. Arrival and setup (2 min)
2. Consent briefing (4 min)
3. Demographic survey (4 min)
4. App introduction and accessibility check (2 min)
5. 5-minute exploration (5 min)
6. Task 1: weather (2 min)
7. Task 2: tea timer (2 min)
8. Task 3: blue light (2 min)
9. Task 4: biryani recipe (2 min)
10. Task 5: Fajr reminder (2 min)
11. SUS questionnaire (4 min)
12. Semi-structured interview (5 min)
13. Debrief and close-out (2 min)

This design keeps the participant workload manageable while gathering both usability metrics and meaningful qualitative feedback on language, accessibility, privacy, and future design directions.
