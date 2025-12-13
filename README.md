# CampusOps AI

> Problem Statement
Title

CampusOps AI: A Role-Aware, Explainable Generative AI System for Policy-Driven Campus Operations

The Problem

Higher-education campuses operate through a complex ecosystem of academic regulations, attendance rules, examination policies, placement eligibility criteria, and administrative circulars.
Although these policies exist in official documents, campuses face persistent operational challenges:

Information is scattered across PDFs, notices, emails, and messaging platforms

Policies are difficult to interpret, especially when decisions depend on multiple rules

Students and faculty repeatedly seek clarifications for the same policy-based questions

Administrators manually generate circulars that remain disconnected from decision systems

Existing campus systems primarily store documents, but they do not understand, reason over, or explain institutional rules.
At the same time, generic AI chatbots are unsafe for institutional use due to hallucinated or unverifiable responses.


Our Approach: CampusOps AI

CampusOps AI is a role-aware, policy-driven Generative AI system that combines Retrieval-Augmented Generation (RAG) with deterministic rule reasoning to deliver accurate, explainable campus decisions.

Rather than relying on general knowledge, CampusOps AI operates strictly on official institutional documents.

Core Intelligence Design

CampusOps AI:

Retrieves only relevant policy clauses using semantic search (RAG)

Applies deterministic rule logic (e.g., attendance thresholds, eligibility cutoffs)

Uses Generative AI only to explain decisions, not to infer or guess rules

Provides explicit citations to policy sections used in each response

This ensures all outputs are traceable, trustworthy, and institution-safe.

Role-Based Functionality
Student Role

Ask questions about attendance, examinations, eligibility, or academic rules

Receive clear decisions, structured reasoning, and actionable next steps

View exact policy citations to understand why a decision was made


Administrator Role

Upload and manage official policy documents

Semantically query institutional rules to validate decisions

Generate official circulars from text or voice input using Generative AI

Automatically index generated circulars into the CampusOps knowledge base, making them immediately available for future reasoning and queries

This creates a closed intelligence loop where administrative actions directly strengthen institutional memory.

## How It Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              CAMPUSOPS AI                                   │
└─────────────────────────────────────────────────────────────────────────────┘

     👨‍💼 ADMIN                                             👤 USER
        │                                                    │
        │ Uploads, updates                                   │ Asks question
        │ & manages data                                     │
        ▼                                                    ▼
┌───────────────┐                                   ┌───────────────┐
│  📄 Policy    │                                   │  "What is the │
│   Documents   │                                   │   minimum     │
│               │                                   │  attendance?" │
└───────┬───────┘                                   └───────┬───────┘
        │                                                   │
        ▼                                                   ▼
┌───────────────────────────────────────────────────────────────────────────┐
│                                                                           │
│                        🧠 AI PROCESSING ENGINE                            │
│                                                                           │
│   ┌─────────────┐      ┌─────────────┐      ┌─────────────┐              │
│   │  Understand │ ───► │   Search    │ ───► │  Generate   │              │
│   │   Content   │      │  Relevant   │      │   Answer    │              │
│   │             │      │   Sections  │      │             │              │
│   └─────────────┘      └─────────────┘      └─────────────┘              │
│                                                                           │
└───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                          ┌─────────────────┐
                          │  💬 Answer      │
                          │                 │
                          │ "The minimum    │
                          │  attendance is  │
                          │  75%..."        │
                          └─────────────────┘
```




## Architecture Overview

```
┌──────────────────────────────────────────────────────────────┐
│                      KNOWLEDGE BASE                          │
│                                                              │
│   📄 Attendance    📄 Placements    📄 Library    📄 Hostel  │
│      Policy           Policy          Rules       Guidelines │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                    AI UNDERSTANDING LAYER                    │
│                                                              │
│   Documents are converted into a format that AI can          │
│   search and understand semantically (not just keywords)     │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                     SMART SEARCH ENGINE                      │
│                                                              │
│   Finds the most relevant policy sections for any question   │
│   using meaning-based search (understands context)           │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           ▼
┌──────────────────────────────────────────────────────────────┐
│                   ANSWER GENERATION                          │
│                                                              │
│   AI reads the relevant policies and generates a clear,      │
│   accurate answer in natural language                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

---

## The Flow

### 1️⃣ Document Management (Admin)

```
Admin uploads/updates documents
        │
        ▼
Documents are split into smaller sections
        │
        ▼
Each section is converted to AI-readable format
        │
        ▼
Stored in the knowledge database
```

### 2️⃣ Question Answering (User)

```
User asks: "What CGPA do I need for placements?"
        │
        ▼
Question is understood by AI
        │
        ▼
Most relevant policy sections are retrieved
        │
        ▼
AI generates answer: "You need a minimum CGPA of 7.0
and no active backlogs to participate in placements."
```

---



## Future Scalability

### Role-Based Access Control (3 Roles)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         ROLE HIERARCHY                                      │
└─────────────────────────────────────────────────────────────────────────────┘

                              👨‍💼 ADMIN
                           ┌─────────────┐
                           │ Full Access │
                           │             │
                           │ • Manage    │
                           │   all data  │
                           │ • All roles │
                           │   control   │
                           └──────┬──────┘
                                  │
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             👨‍🏫 FACULTY                    🎓 STUDENT
          ┌─────────────┐               ┌─────────────┐
          │  Elevated   │               │   Basic     │
          │  Access     │               │   Access    │
          │             │               │             │
          │ • Query all │               │ • Query     │
          │   data      │               │   public    │
          │ • Access    │               │   data only │
          │   restricted│               │             │
          │   data      │               │             │
          └─────────────┘               └─────────────┘
```

### Data Restriction Model

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          KNOWLEDGE BASE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      🔓 PUBLIC DATA                                 │   │
│   │                                                                     │   │
│   │   • Attendance Policy          • Library Rules                     │   │
│   │   • Exam Guidelines            • Hostel Timings                    │   │
│   │   • General Campus Rules                                           │   │
│   │                                                                     │   │
│   │   Accessible by: Admin, Faculty, Student                           │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      🔒 RESTRICTED DATA                             │   │
│   │                                                                     │   │
│   │   • Placement Statistics       • Internal Memos                    │   │
│   │   • Faculty Guidelines         • Grading Criteria                  │   │
│   │   • Disciplinary Records       • Budget Information                │   │
│   │                                                                     │   │
│   │   Accessible by: Admin, Faculty                                    │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │                      🔐 ADMIN ONLY DATA                             │   │
│   │                                                                     │
│   │   • User Management Logs       • System Configuration              │   │
│   │   • Audit Trails               • Sensitive Records                 │   │
│   │                                                                     │   │
│   │   Accessible by: Admin                                             │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Future Query Flow with Access Control

```
User submits query with role token
        │
        ▼
┌───────────────────┐
│ Identify User Role│
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Filter Knowledge  │──► Only search data user has access to
│ Base by Role      │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Retrieve Relevant │
│ Chunks            │
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│ Generate Answer   │
└─────────┬─────────┘
          │
          ▼
    Return Response
```