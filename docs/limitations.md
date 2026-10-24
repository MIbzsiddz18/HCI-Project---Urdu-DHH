# Limitations

This study provides an initial exploratory evaluation of an LLM-assisted touch interface for Pakistani Deaf and Hard of Hearing (DHH) Urdu speakers. While the findings are informative, several methodological and contextual limitations should be considered when interpreting the results.

---

## 1. Small sample size and limited statistical power

The study uses a small convenience sample of DHH participants, which limits the reliability and generalizability of the quantitative findings. With a limited number of participants, the analysis of System Usability Scale (SUS), Adjective Scale, Net Promoter Score (NPS), and latency differences is vulnerable to unstable estimates and reduced statistical power. Subgroup comparisons across communication preferences, hearing status, or device use are therefore difficult to justify with confidence.

This is especially relevant in a within-subjects design where repeated measures may increase sensitivity, but the number of participants remains modest. As a result, the findings should be interpreted as directional and exploratory rather than definitive.

### Mitigation / future work
- Recruit a larger and more diverse participant sample in future iterations.
- Use mixed-methods reporting that emphasizes effect sizes and qualitative depth alongside inferential statistics.
- Consider preregistered analyses or power estimates for subsequent studies with stronger statistical rigor.

---

## 2. Pilot-phase constraints and short timeline

This project was conducted in a short pilot phase with limited recruitment time, development time, and iterative refinement. Because of the compressed schedule, there was less opportunity for repeated prototyping, user testing, and post-study redesign before the main evaluation. In practice, this may have constrained the quality of both the interface and the study procedure.

A short timeline also affects the maturity of recruitment efforts, participant screening, and adaptation of the study materials for diverse access needs. As a result, the current implementation should be understood as a feasible early-stage prototype rather than a fully optimized deployment-ready system.

### Mitigation / future work
- Extend the study timeline to allow iterative design refinements after each pilot session.
- Run multiple rounds of usability testing before formal data collection.
- Increase the training and preparation period for facilitators and researchers to standardize the protocol.

---

## 3. Urdu translation and validation of SUS are not yet fully psychometrically validated

The study relies on a bilingual or translated version of the SUS and related subjective measures, but the Urdu adaptation has not yet been fully psychometrically validated in the Pakistani DHH context. This raises concerns about semantic equivalence, cultural appropriateness, and measurement invariance across participants with different literacy levels, language backgrounds, and communication preferences.

Although translated questionnaires can be useful for accessibility and user comprehension, they may not always preserve the same interpretive meaning as the original English instrument. This is particularly important for DHH users, whose language experience may include Urdu, English, Pakistan Sign Language (PSL), or mixed-language communication rather than a single dominant textual language.

### Mitigation / future work
- Conduct formal translation-backtranslation and cognitive interviewing with DHH Urdu speakers.
- Evaluate internal consistency and reliability for the adapted instrument.
- Compare translated and original-language responses where appropriate, and report measurement limitations transparently.

---

## 4. Wizard-of-Oz facilitator effects

The facilitated speech condition introduces a human intermediary who may influence participant perceptions, task execution, and latency outcomes. Because the facilitator is active rather than passive, the condition may reflect both the system design and the facilitator’s communication style, pacing, confidence, or conversational decisions. These effects may not be separable from the interface itself.

This is a common challenge in Wizard-of-Oz studies, but it is particularly salient in a DHH context where context-sensitive clarification, signing support, or interpretation can strongly shape user experience. The facilitated condition may therefore overstate or understate the usability of a fully automated system.

### Mitigation / future work
- Standardize facilitator scripts and response patterns across participants.
- Train facilitators to minimize variation in tone, pace, and wording.
- Compare performance across multiple facilitators or include facilitator-level logs in the analysis.

---

## 5. Lab setting versus real home environment

The study was conducted in a controlled lab or test setting rather than in participants’ actual homes. This creates a mismatch between the evaluation context and the real-life use of a smart-home interface. The testing environment may reduce friction, increase attention, and simplify task performance when compared with typical household routines, where distractions, interruptions, social factors, and home-specific needs can substantially affect usability.

In addition, a simulated smart-home interface may not fully capture the practical realities of domestic routines, accessibility barriers, or device placement in real homes. Therefore, lab-based findings may not fully reflect performance or acceptance in everyday contexts.

### Mitigation / future work
- Conduct in-home or semi-naturalistic field testing with real household routines.
- Evaluate the interface in different room configurations and contexts of use.
- Include contextual observations and household-level task scenarios in future studies.

---

## 6. LLM latency and GPT-4o variability

The study depends on a language model to generate or facilitate suggestions in real time. LLM response latency can vary due to network conditions, model load, prompt structure, and system-level stochasticity. This introduces uncertainty in task completion time and may influence user perception of responsiveness, especially in a touch-based interactive setting.

Furthermore, the quality of model output may vary across prompts, languages, or conversation context. In a multilingual or cross-modal study involving Urdu, English, and DHH communication preferences, variability in output quality can affect both usability and user trust. This limits the reproducibility of the findings and complicates comparisons across participants or sessions.

### Mitigation / future work
- Log model latency, token usage, and response quality for each interaction.
- Use a consistent model version and document any changes over time.
- Compare latency and quality across stable prompt templates and multiple runs to estimate variability.

---

## 7. Diversity within the DHH participant group

The DHH population is highly diverse, and this study may not fully capture that heterogeneity. Participants may differ in age, literacy, language background, communication preference, prior exposure to technology, hearing device use, and familiarity with digital interfaces. Some may prefer Urdu written text, others may prefer English, PSL, or mixed communication strategies. Others may use sign language as a primary mode of communication, while still others may rely on written communication or lipreading support.

Because of this variability, a single interface design may not suit all participants equally. What feels intuitive to one participant may be confusing or inaccessible to another. This limitation matters particularly for a study that aims to support a broad range of Pakistani DHH users.

### Mitigation / future work
- Stratify recruitment by hearing status, device use, and communication preference.
- Offer multiple modes of access and instruction with participant-specific accommodations.
- Explore adaptive or customizable interfaces that support different language and accessibility profiles.

---

## 8. Generalizability beyond Pakistan and beyond this task set

The study focuses on Pakistani DHH Urdu speakers and a small set of smart-home tasks relevant to the local context, such as weather, timers, lighting, recipes, and prayer reminders. While this contextualization is valuable for cultural relevance, it limits generalizability to other countries, other Deaf communities, and other application domains.

The findings may not transfer to users in different social, linguistic, or technological settings. Similarly, the smart-home task set may not represent broader assistive technology needs, such as healthcare reminders, education, transportation, or workplace support. Thus, the results should not be treated as universal claims about DHH interaction design or LLM accessibility more generally.

### Mitigation / future work
- Replicate the study across additional regions and linguistic communities.
- Test the interface in a broader range of assistive and everyday scenarios.
- Compare findings with other culturally grounded task domains beyond the smart-home context.

---

## 9. Potential bias in thematic coding by a single coder

The interview analysis may be vulnerable to coder bias because thematic coding was conducted by a single coder or by a small number of coders without independent validation. Even when qualitative analysis is systematic, interpretation can be influenced by the coder’s prior assumptions, familiarity with the project, or expectations about the interface.

This limitation affects the reliability of the emergent themes and may reduce transparency about alternative interpretations. Qualitative findings are valuable, but they should be treated as contextually grounded and potentially shaped by interpretive bias.

### Mitigation / future work
- Use double coding or inter-rater reliability checks for the main themes.
- Maintain a coding framework and memo trail to increase transparency.
- Conduct reflexive analysis to document assumptions and researcher positionality.

---

## Overall assessment

This study offers a promising exploratory evaluation of an LLM-assisted touch interface for Pakistani DHH Urdu speakers, but the findings should be interpreted in light of the methodological and contextual limitations described above. The work is best viewed as an early pilot that identifies design opportunities, accessibility concerns, and directions for future refinement rather than a final, generalizable conclusion about LLM-based assistive systems for DHH users.
