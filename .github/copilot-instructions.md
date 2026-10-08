# CODEWEAVER — Copilot Instructions

## Project Identity

CODEWEAVER is a Human-Controlled AI Developer Assistant.

Current release:

**Alpha.1 — Project Understanding**

Current engineering phase:

**SPECIFICATION → ARCHITECTURE**

The human developer retains final authority over architecture, implementation, dependencies, tests, commits, releases, and consequential changes.

---

## Current Gate: Architecture Review

Do NOT implement CODEWEAVER yet.

Do NOT:

- write implementation code
- create application source files
- create scaffolding
- install dependencies
- modify project files outside explicitly requested documentation
- execute project commands that modify state
- create commits
- create releases
- introduce unnecessary frameworks
- introduce unnecessary abstractions

Your current responsibility is architecture review.

---

## Specification

The authoritative Alpha.1 specification is:

`docs/specifications/alpha-1-project-understanding.md`

Read and evaluate that specification before proposing implementation.

---

## Alpha.1 Mission

CODEWEAVER Alpha.1 establishes a deterministic, read-only foundation for understanding software projects.

It should determine what can be reliably established about a project while preserving the distinction between:

- OBSERVED
- INFERRED
- PROPOSED
- UNKNOWN

CODEWEAVER must never present an inference as though it were a direct observation.

---

## Evidence Requirements

Every finding must preserve provenance:

- state
- subject
- value
- source
- confidence
- reason

State and confidence are separate concepts.

State describes the type of knowledge.

Confidence describes the strength of supporting evidence.

UNKNOWN does not require a meaningful value.

Ambiguous findings must preserve multiple supported candidates rather than arbitrarily selecting one.

---

## Alpha.1 Capabilities

The initial implementation is intentionally limited to:

1. project file discovery
2. project structure detection
3. Python project detection
4. Node project detection
5. evidence collection
6. project context
7. CLI presentation

Future capabilities may include:

- metadata detection
- dependency detection
- entry-point detection
- file classification
- additional language detectors
- AI-assisted interpretation

Do not prematurely implement future capabilities.

---

## Architecture Principles

The initial architecture should remain small, explicit, deterministic, and testable.

Conceptual structure:

    CODEWEAVER
         │
        CLI
         │
    Project Analyzer
         │
    ┌────┴────┐
    │         │
File      Detectors
Discovery     │
        ┌─────┼─────┐
        │     │     │
    Structure Python Node
        │     │     │
        └─────┼─────┘
              │
           Evidence
              │
       Project Context
              │
             CLI

Responsibilities:

### CLI

Receives commands, selects the project, and presents results.

The CLI must not contain detector logic.

### Project Analyzer

Coordinates analysis, invokes detectors, collects findings, and constructs project context.

### File Discovery

Discovers project files and supplies the discovered file set to detectors.

### Detectors

Observe project evidence and produce Evidence findings.

Detectors must not modify the project.

### Evidence

Provides the common representation for project findings.

### Project Context

Provides structured understanding of the analyzed project.

---

## Detector Contract

Keep the detector contract simple.

Conceptually:

    Input:
        ProjectRoot
        ProjectFiles

    Output:
        Evidence[]

Detectors should:

- observe
- analyze
- report

Detectors should not:

- modify files
- install dependencies
- execute arbitrary shell commands
- invoke AI
- access remote services
- hide assumptions
- silently collapse ambiguity

Detector registration should be explicit for Alpha.1.

Do not introduce plugin discovery.

---

## Non-Goals

Alpha.1 does not:

- generate code
- edit code
- repair code
- refactor projects
- install dependencies
- execute arbitrary commands
- publish software
- modify production systems
- use AI
- use remote AI APIs
- use embeddings
- perform autonomous reasoning

---

## Architecture Review Task

Before implementation, evaluate the Alpha.1 specification and identify:

1. Missing architectural requirements
2. Contradictions
3. Unnecessary complexity
4. Risks
5. Component boundaries
6. Data-flow concerns
7. Testing implications
8. Decisions that should be made before implementation

Then propose 2–3 architectural approaches.

For each approach provide:

- component structure
- responsibilities
- data flow
- major tradeoffs
- testing implications
- complexity
- strengths
- weaknesses
- suitability for Alpha.1

Do not choose the architecture for the human developer.

Do not implement an architecture.

Do not generate source code.

The human developer will review the alternatives and explicitly select the architecture.

---

## Engineering Principle

CODEWEAVER follows:

    IDEA
      ↓
    SPECIFICATION
      ↓
    ARCHITECTURE
      ↓
    AI IMPLEMENTATION
      ↓
    HUMAN REVIEW
      ↓
    TEST
      ↓
    DOCUMENT
      ↓
    COMMIT
      ↓
    RELEASE
      ↓
    ITERATE

Never skip the architecture gate.

---

## Core Principle

> Understand before acting.

CODEWEAVER should first establish what it can reliably observe about a software project.

Only after that foundation is trustworthy should CODEWEAVER begin making plans, proposing changes, or assisting with implementation.

