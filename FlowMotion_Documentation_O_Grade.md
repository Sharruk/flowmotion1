# FlowMotion: Intelligent Habit & Routine Management System
## ICS1405 – Software Engineering Principles and Practices
### Sri Sivasubramaniya Nadar College of Engineering (SSN)

---

## EXPERIMENT 1: PROBLEM IDENTIFICATION, REQUIREMENTS ANALYSIS, SYSTEM ARCHITECTURE & IMPLEMENTATION

### 1. Problem Identification
Modern productivity workflows are increasingly centralized around desktop environments, yet most habit-tracking solutions remain mobile-first. This creates a significant gap for Linux desktop users (developers, students, and engineers) who experience:
*   **Context Switching Costs:** Frequent switching to mobile devices to track habits leads to a loss of deep work focus.
*   **Notification Fatigue:** Browser-based notifications are often suppressed or ignored within cluttered tab environments.
*   **Low Emotional Resonance:** Robotic, repetitive feedback in existing apps fails to maintain long-term user engagement.

**FlowMotion** is positioned as a **desktop-native solution** for Linux, integrating habit tracking directly into the OS kernel via native notification systems and background daemons.

### 2. Objectives
*   **O1:** Develop a centralized Linux-native dashboard for unified habit and routine management.
*   **O2:** Implement a high-precision background scheduling system using APScheduler with 1-minute granularity.
*   **O3:** Integrate Google Gemini AI to generate context-aware, emotionally resonant feedback based on real-time performance.
*   **O4:** Achieve seamless OS-level integration using `notify-send` for non-intrusive, high-visibility reminders.
*   **O5:** Provide data-driven analytics using Chart.js to visualize habit consistency and streak growth.

### 3. Requirements Analysis

#### 3.1 Functional Requirements
| ID | Requirement | Priority | Module |
| :--- | :--- | :--- | :--- |
| FR1 | Secure User Authentication and Session Persistence. | High | Authentication |
| FR2 | Support for Binary (Yes/No) and Quantitative Habits. | High | Habit Management |
| FR3 | Automated Multi-Tier Background Notifications. | High | Notification Engine |
| FR4 | AI-Powered Emotional Feedback Generation. | Medium | AI Feedback Engine |
| FR5 | Real-time Streak and Performance Analytics. | Medium | Analytics Module |

#### 3.2 Non-Functional Requirements
*   **Performance:** Background daemon must execute checks in <100ms to avoid system lag.
*   **Reliability:** Use of atomic database transactions (SQLite) to prevent data corruption during power loss.
*   **Usability:** 100% compliance with Linux Desktop notification standards.
*   **Maintainability:** Modular MVT architecture for rapid feature scaling.

### 4. System Architecture
The system utilizes the **Django Model-View-Template (MVT)** architecture, chosen for its strong separation of concerns:
*   **Model Layer:** Defines structured schemas for habits, responses, and streaks.
*   **View Layer:** Orchestrates business logic, AI integration, and notification triggers.
*   **Background Layer:** An independent APScheduler process running parallel to the web server, ensuring persistent monitoring without blocking the UI.
*   **OS Layer:** Direct execution of Linux system calls for native desktop integration.

### 5. Technology Stack Justification
| Technology | Choice | Engineering Justification |
| :--- | :--- | :--- |
| **Backend** | Python / Django | Rapid development, robust ORM, and excellent subprocess management for OS interaction. |
| **Database** | SQLite3 | Zero-configuration, file-based persistence ideal for local Linux workstations. |
| **AI** | Gemini 1.5 Flash | Low-latency natural language generation for real-time emotional feedback. |
| **Scheduling** | APScheduler | Persistent job store support and precise interval-based execution. |
| **Notifications** | notify-send | Native Linux utility ensuring zero dependency on browser-based push services. |

---

## EXPERIMENT 2: SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

### 1. Product Perspective
FlowMotion is an intelligent desktop assistant designed to operate as a standalone system on Linux workstations. Unlike web-based trackers, it leverages OS-level hooks to ensure user accountability through persistent, intrusive-yet-elegant reminders.

### 2. Operating Environment
*   **OS:** Ubuntu 22.04+, NixOS, or any Linux distro with `libnotify`.
*   **Runtime:** Python 3.11+.
*   **Framework:** Django 5.x.
*   **Client:** Any modern web browser (for local dashboard access).

### 3. Design Constraints
*   **Linux Dependency:** Notification logic is strictly coupled with `notify-send`.
*   **Local Execution:** Designed for single-user local deployment to ensure maximum data privacy.
*   **Resource Constraints:** Optimized for low CPU/RAM overhead to run continuously in the background.

### 4. Assumptions and Dependencies
*   **Assumption:** The local Linux notification server (e.g., Dunst, Mako) is active.
*   **Dependency:** Consistent internet access is required only for the AI feedback module (Gemini API).

### 5. Requirements Traceability Matrix
| Req ID | Django Module | View/Service | Implementation Status |
| :--- | :--- | :--- | :--- |
| FR1 | `users/` | `login_view`, `register_view` | Finalized |
| FR2 | `habits/` | `habit_create`, `habit_detail` | Finalized |
| FR3 | `habits/` | `notification_service.py` | Finalized |
| FR4 | `habits/` | `ai_utils.get_emotional_feedback` | Finalized |
| FR5 | `habits/` | `dashboard`, `history` | Finalized |

---

## EXPERIMENT 3: SYSTEM DESIGN & DATA FLOW DIAGRAMS

### 1. Level-0 DFD (Context Diagram)
The system receives User inputs (Habit Definitions, Completion Status) and interacts with the Linux OS to deliver Notifications. It acts as a black box that transforms routine data into persistent behavioral cues.

### 2. Level-1 DFD
1.  **Auth Process:** Manages user identity and session tokens.
2.  **Habit Logic:** Handles the lifecycle of habits and quantitative tracking.
3.  **Scheduling Engine:** A time-aware process that monitors deadlines and triggers alerts.
4.  **AI Feedback Loop:** Processes completion data into natural language feedback.
5.  **Analytics Process:** Aggregates history into visual charts.

### 3. Data Storage Design
The database utilizes **Model Inheritance**:
*   `Habit` (Base Model): Common fields like name, time, and user.
*   `YesNoHabit` / `MeasurableHabit` (Specialized): Quantitative or binary-specific fields.
*   `HabitResponse`: Links specific completions to dates, enabling historic analytics.

### 4. Validation & Consistency (DFD Balancing)
DFD balancing is maintained by ensuring that all data stores (Habit DB) accessed in Level-1 are consistent with the high-level data flows in Level-0. Data integrity is enforced through Django's ORM validation layer, preventing orphan responses or invalid streak increments.

---

## IMPLEMENTATION & TESTING

### 1. Implementation Highlights
*   **Asynchronous Scheduling:** APScheduler runs in the `ready()` method of `habits/apps.py`, ensuring it starts with the server.
*   **OS Integration:** Subprocess calls to `notify-send --action` allow for clickable notifications that redirect back to the app.
*   **AI Prompt Engineering:** Specialized prompts ensure feedback is under 15 words with exactly one relevant emoji for high readability.

### 2. Testing & Validation
| Test Case | Method | Expected Outcome | Result |
| :--- | :--- | :--- | :--- |
| Notification Delay | Manual | Trigger within 10s of scheduled time. | PASS |
| Streak Calculation | Unit Test | Increment correctly on daily completion. | PASS |
| AI Sanity Check | Manual | Feedback must be unique and non-robotic. | PASS |
| DB Persistence | Stress Test | Data remains consistent after server restart. | PASS |

---

## CONCLUSION
FlowMotion successfully demonstrates the application of high-level Software Engineering principles—specifically **separation of concerns, requirement traceability, and modular design**. By integrating a background scheduling daemon with a modern AI layer, the system transcends traditional habit trackers, offering a robust, Linux-native solution for productivity. The use of the MVT pattern ensured that the system remains maintainable and scalable for future enterprise-level enhancements.

---
**Learning Outcomes:**
*   Mastery of Django MVT and background task orchestration.
*   Understanding of OS-level system integration in Linux.
*   Practical application of LLMs in enhancing user experience through emotional feedback.
