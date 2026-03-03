# TinyTroupe-Inspired UX Testing Patterns

> **Optional advanced patterns** that can enhance the base UX Sense Check agent.
> These are inspired by Microsoft Research's TinyTroupe framework for simulating
> realistic persona behavior. The base UX Sense Check agent works without them.
> Add these patterns when the project has complex UX that justifies the
> additional testing depth.

---

## Pattern 1: Action Quality Correction

When a persona takes an action during a UX walkthrough, evaluate the **quality**
of that action. Is it realistic? Is it consistent with the persona's profile?

If the action quality is low — the persona does something unrealistic or
inconsistent with their background — retry the action with a corrective prompt
that reinforces the persona's constraints.

**Why this matters:** Without quality correction, AI personas tend to drift
toward "competent user" behavior. A persona defined as "first-time user, no
technical background" might start clicking exactly the right buttons. Action
quality correction catches this drift and forces the persona to behave as a
real person with that profile would.

**Implementation:** After each simulated action, score it against the persona
profile. If the score falls below a threshold, regenerate the action with an
explicit reminder of the persona's limitations and background.

---

## Pattern 2: Cognitive State Evolution

Personas are not static. As they navigate through the application, track their
**cognitive state** across these dimensions:

- **Confusion level** (0–10) — How lost are they?
- **Frustration level** (0–10) — How annoyed are they?
- **Confidence level** (0–10) — How sure are they about what to do next?
- **Mental model accuracy** (0–10) — Does their understanding match reality?

A persona that starts confused but gradually gains clarity is fine — the UX is
teaching them. A persona whose confusion **increases** page by page is a UX
failure — the interface is making things worse.

**Implementation:** After each step in the walkthrough, update the cognitive
state scores. Flag any sequence where confusion or frustration trends upward
across three or more consecutive steps.

---

## Pattern 3: Memory Consolidation

After a testing session ends, the persona **reflects** on what they experienced.
This converts episodic memories (what happened) into semantic memories (what
they learned).

This produces insights like:
- "I learned that the dashboard shows my spending, but I still don't understand
  what 'P-score' means."
- "I figured out how to export data, but only because I accidentally found
  the button — it wasn't where I expected."

**Implementation:** After the walkthrough completes, prompt the persona to
summarize: (1) what they accomplished, (2) what they learned, (3) what they
still don't understand, and (4) what surprised them. These summaries often
surface UX issues that step-by-step logs miss.

---

## Pattern 4: Multi-Persona Convergence

When multiple personas independently reach the **same confusion point**, that
is a high-confidence UX finding. A single persona getting confused might be
persona-specific. Three different personas all getting confused at the same
screen is a design problem.

**Implementation:** Run the same walkthrough with 3+ personas. After all
sessions complete, cross-reference confusion spikes by screen/step. Any
confusion point that appears in 2+ persona sessions gets flagged as a
convergence finding with elevated priority.

---

## Pattern 5: Persona Consistency Validation

Periodically check whether the persona is behaving consistently with their
defined profile. A "non-technical user" who starts using API terminology has
**broken character**. A "busy executive" who patiently reads every tooltip
is not behaving realistically.

**Implementation:** Every N steps, validate the persona's recent actions and
language against their profile. Flag inconsistencies. If the persona has
drifted, either correct it (Pattern 1) or note that the UX may be implicitly
requiring expertise that the persona shouldn't have.

---

## When to Use These Patterns

- **Skip them** for simple UX with straightforward flows (forms, CRUD screens)
- **Use Patterns 1 + 5** when persona fidelity matters (accessibility testing,
  domain-specific tools)
- **Use Patterns 2 + 4** when you need to find the worst UX pain points fast
- **Use Pattern 3** when you want qualitative insights, not just pass/fail
- **Use all five** for complex multi-step workflows where user comprehension
  is critical (onboarding flows, financial tools, medical interfaces)
