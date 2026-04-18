# Phase 2 — Workflow Outputs (Controlled External Validation)

This file is the official log for Phase 2 workflow execution outputs.

## Why this file exists
- Keep evidence organized for the rubric requirement.
- Avoid heavy runtime inside the interactive IDE thread.
- Enable incremental commits with clear checkpoints.

## Controlled execution command (external terminal)
```powershell
cd "notebooks\COURSE_2\17_AI-Powered Agentic Workflow for Project Management\starter\phase_2"
python -u .\agentic_workflow.py
```

## Execution record template

### Run metadata
- Date/Time:
- Environment:
- Python version:
- API provider endpoint:
- Command executed:

### Action Planning output
- Number of generated steps:
- Steps list:

### Routing output
- Step 1 -> selected agent:
- Step 2 -> selected agent:
- Step 3 -> selected agent:

### Evaluation output
- Product Manager evaluation summary:
- Program Manager evaluation summary:
- Development Engineer evaluation summary:

### Final workflow output
- Last completed step output:

### Incidents and mitigation
- Timeout observed? (yes/no)
- Credential error? (yes/no)
- Unexpected stop/hang? (yes/no)
- Mitigation applied:

### Notes for next iteration
- Improvement opportunities:
- Follow-up actions:

## Execution record — 2026-04-13 (completed)

### Run metadata
- Date/Time: 2026-04-13
- Environment: local venv + Vocareum OpenAI endpoint
- Python version: project interpreter in `.venv`
- API provider endpoint: `https://openai.vocareum.com/v1`

### Run A (baseline workflow script)
- Command executed:
  - `python -u .\agentic_workflow.py`
- Action Planning output:
  - Number of generated steps: 1
  - Steps list: generic step focused on development tasks
- Routing output:
  - Step 1 -> selected agent: Development Engineer
- Evaluation output:
  - Development Engineer evaluation summary: first response rejected, second response accepted (2 interactions)
- Final workflow output:
  - Structured development tasks (`Task ID`, `Task Title`, `Related User Story`, `Description`, `Acceptance Criteria`, `Estimated Effort`, `Dependencies`)

### Run B (controlled prompt for full phase coverage)
- Command executed:
  - `python -u -c "import agentic_workflow as aw; aw.run_workflow('For the Email Router product spec, generate EXACTLY 3 workflow steps only: 1) create user stories, 2) define product features grouped from those stories, 3) define engineering tasks with dependencies. Return concise steps only.')"`
- Action Planning output:
  - Number of generated steps: 3
  - Steps list:
    - `1) Create user stories from the Email Router product spec.`
    - `2) Define product features by grouping related user stories.`
    - `3) Define engineering tasks with dependencies for each user story.`
- Routing output:
  - Step 1 -> selected agent: Program Manager
  - Step 2 -> selected agent: Program Manager
  - Step 3 -> selected agent: Development Engineer
- Evaluation output:
  - Product Manager evaluation summary: not triggered in this run
  - Program Manager evaluation summary: accepted after refinement in step 1 and step 2
  - Development Engineer evaluation summary: accepted after refinement in step 3
- Final workflow output:
  - Structured engineering task list (with `Task ID`, `Acceptance Criteria`, and dependencies)

### Incidents and mitigation
- Timeout observed? yes (in a broader run with excessive step expansion)
- Credential error? no
- Unexpected stop/hang? no persistent hang (only timeout interruption in one long run)
- Mitigation applied:
  - Used constrained prompt (`EXACTLY 3` steps) to keep runtime bounded and reproducible.
  - Re-ran workflow with controlled command and collected successful evidence.

### Notes for next iteration
- Improvement opportunities:
  - Tune route descriptions/prompts to increase deterministic selection of Product Manager for user-story steps.
  - Optionally add a post-processing consolidation stage to merge outputs into one final project-plan artifact.
- Follow-up actions:
  - Include this output file and `ETAPA_ATUAL.md` in final submission commit.