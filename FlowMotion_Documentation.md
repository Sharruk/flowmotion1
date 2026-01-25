# FlowMotion: Intelligent Habit & Routine Management
## Lab Record - Sri Sivasubramaniya Nadar College of Engineering

---

### EXPERIMENT 1: Problem Identification, Requirements Analysis, System Design & Implementation

#### 1. Problem Identification
*   **Problem Statement:** Users on Linux desktop environments lack integrated, emotionally engaging habit trackers. Most existing solutions are mobile-based, causing a disconnect from the primary workstation.
*   **Motivation:** Increasing productivity by embedding habit tracking directly into the desktop workflow using native system notifications.
*   **Sub-problems:**
    1.  Fragmented notification delivery.
    2.  Lack of native desktop integration.
    3.  Low user engagement due to robotic feedback.

#### 2. Requirements Analysis
**Functional Requirements:**
| ID | Requirement |
| :--- | :--- |
| FR1 | Secure User Authentication (Login/Register). |
| FR2 | Support for Yes/No and Measurable habits. |
| FR3 | Automated background notifications via APScheduler. |
| FR4 | AI-powered emotional feedback based on habit completion. |

**Non-Functional Requirements:**
*   **Performance:** Background checks must run every 1 minute.
*   **Reliability:** The system must use a persistent SQLite database.
*   **Usability:** Native Linux notifications (notify-send) for minimal distraction.

#### 3. System Design
*   **Architecture:** Django Model-View-Template (MVT).
*   **Modules:**
    *   **Frontend:** HTML5, CSS3, Vanilla JS.
    *   **Backend:** Django 5.x, APScheduler.
    *   **AI:** Google Gemini API for natural language feedback.
    *   **System integration:** `notify-send` for Linux desktop alerts.

#### 4. Implementation
Developed using Python/Django. Implemented `notification_service.py` to handle `subprocess` calls to `notify-send`. Integrated Gemini AI in `ai_utils.py` to provide varied feedback.

---

### EXPERIMENT 2: Software Requirements Specification (SRS)

#### 1. Overall Description
*   **Product Perspective:** FlowMotion acts as a personal assistant integrated into the Ubuntu/Linux desktop environment.
*   **Operating Environment:** Linux (NixOS/Ubuntu), Python 3.11+, Django 5.x.

#### 2. Constraints
*   **Hardware:** Local workstation execution.
*   **Software:** Dependency on Linux `libnotify` for notifications.
*   **Business:** Academic prototype for SSN Software Engineering Lab.

#### 3. Traceability
Requirements are mapped to specific Django views (`habit_respond`) and services (`notification_service`).

---

### EXPERIMENT 3: Data Flow Diagrams (DFD)

#### 1. Level-0 DFD
**External Entities:** User, Linux Desktop System.
**Process:** FlowMotion Central Logic.
**Data Flows:** User provides completions; System provides notifications/feedback.

#### 2. Level-1 DFD
1.  **Auth Process:** Validates User Credentials.
2.  **Habit Logic:** Manages CRUD and Response tracking.
3.  **Scheduling Process:** Triggers timely reminders.
4.  **Feedback Engine:** Queries AI for emotional responses.

#### 3. DFD Validation
All data inputs (completions) result in corresponding outputs (updated streaks, notifications). Data stores (SQLite) ensure persistence.

---
**Conclusion:** The prototype successfully demonstrates the integration of Software Engineering principles (modularity, requirements traceability) into a functional Linux-centric application.
