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

**FlowMotion** is positioned as a **desktop-native solution** for Linux, leveraging OS-level user-space notification services and background daemons.

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
*   **Security:** User data is isolated per account using Django’s authentication framework, session middleware, and access-controlled views.
*   **Scalability:** While optimized for single-user local execution, the architecture supports future migration to multi-user environments.

### 4. System Architecture
As illustrated in the system architecture diagram, the system utilizes the **Django Model-View-Template (MVT)** architecture, chosen for its strong separation of concerns:
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
*   **Assumptions:** All data entities are linked to a unique User ID to maintain isolation.
*   `YesNoHabit` / `MeasurableHabit` (Specialized): Quantitative or binary-specific fields.
*   `HabitResponse`: Links specific completions to dates, enabling historic analytics.

### 4. Validation & Consistency (DFD Balancing)
DFD balancing is maintained by ensuring that all data stores (Habit DB) accessed in Level-1 are consistent with the high-level data flows in Level-0. Data integrity is enforced through Django's ORM validation layer, preventing orphan responses or invalid streak increments.

---

## IMPLEMENTATION & TESTING

### 1. Implementation Highlights
*   **Asynchronous Scheduling:** APScheduler runs in the `ready()` method of `habits/apps.py`, ensuring it starts with the server.
*   **OS Integration:** Subprocess calls to `notify-send --action` allow for clickable notifications that redirect back to the app.
*   **Responsible AI Integration:** The AI feedback engine utilizes deterministic prompt structures with explicit output length constraints to ensure consistency. Basic hallucination control is implemented via constrained prompts that restrict responses to purely emotional feedback related to the specific habit.

### 2. Testing & Validation
| Test Case | Method | Expected Outcome | Result |
| :--- | :--- | :--- | :--- |
| Notification Delay | Manual | Trigger within 10s of scheduled time. | PASS |
| Streak Calculation | Unit Test | Increment correctly on daily completion. | PASS |
| AI Sanity Check | Manual | Feedback must be unique and non-robotic. | PASS |
| DB Persistence | Stress Test | Data remains consistent after server restart. | PASS |

### 3. Qualitative Observations
Continuous testing of the system has yielded positive qualitative outcomes:
*   **Improved Consistency:** Users reported higher adherence rates due to the tiered notification system.
*   **Reduced Missed Reminders:** The 10-minute repetition logic successfully captured attention during busy workflows.
*   **Emotional Engagement:** The AI-generated feedback provided a sense of achievement, making the habit-tracking process less monotonous.

---

## CONCLUSION
FlowMotion successfully demonstrates the application of high-level Software Engineering principles—specifically **separation of concerns, requirement traceability, and modular design**. By integrating a background scheduling daemon with a modern AI layer, the system transcends traditional habit trackers, offering a robust, Linux-native solution for productivity. The successful application and validation of these principles ensured that the system remains maintainable and reliable.

This project provided deep insights into the lifecycle of a software product, from initial problem identification to final validation. The learning outcomes include mastery of background orchestration and responsible AI implementation within a local desktop ecosystem, reflecting a mature approach to academic software development.

---

## FUTURE SCOPE AND EXTENSIONS

1. **Mobile Platform Expansion**
   - The current system is Linux-desktop–first; future extensions may incorporate Android/iOS clients using shared backend APIs to provide a multi-platform experience.

2. **Cross-Device Synchronization**
   - Future versions may incorporate an optional cloud-based synchronization layer with a privacy-first design emphasis to keep habit data consistent across multiple workstations.

3. **Advanced AI Personalization**
   - The architecture allows for more emotion-adaptive feedback and potential habit difficulty auto-adjustment based on long-term user behavior patterns.

4. **System-Level Enhancements**
   - Future development may include deeper GNOME/KDE integration through tray-based widgets or more advanced background service management.

5. **Scalability & Deployment**
   - The system is designed to allow migration from SQLite to PostgreSQL for multi-user support, alongside optional Docker-based deployment for easier environment replication.

---
**Learning Outcomes:**
*   Mastery of Django MVT and background task orchestration.
*   Understanding of OS-level user-space notification services in Linux.
*   Practical application of responsible AI techniques in enhancing user experience through emotional feedback.
