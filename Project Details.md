# FinVue: Personal Expense Evaluator & Financial Analytics System

## 1. Project Title
**FinVue: Personal Expense Evaluator & Financial Analytics System**

---

## 2. Problem Statement
In today's digital economy, individuals manage multiple cash flows across various banking apps, digital wallets, and physical cash. This fragmentation often leads to passive overspending, an inability to meet personal savings goals, and a general lack of financial awareness. 

Manual tracking methods, such as notebooks or spreadsheet software, are tedious, prone to human error, and require constant manual upkeep. Furthermore, static spreadsheets fail to provide real-time, actionable insights; they cannot automatically classify spending habits, track budget exhaustion rates, or provide instant visual feedback on financial health. Without a centralized, automated application to evaluate expenses, users struggle to identify wasteful spending, leading to long-term financial insecurity and stress.

---

## 3. Project Objectives
* **Automate Capital Tracking:** Develop a user-friendly system to efficiently log, modify, and monitor daily multi-currency income and expenses.
* **Proactive Budget Discipline:** Implement a threshold engine allowing users to set strict spending limits on specific operational categories with automated visual warnings when limits are approached.
* **Descriptive Financial Analytics:** Build an interactive analytical dashboard using data visualization tools to display categorical spending distribution and chronological cash-flow trends.
* **Data Security and Persistence:** Establish a secure relational database architecture with user authentication to ensure complete data isolation, privacy, and continuous storage.
* **Structured Data Export:** Provide a utility to compile and export filtered financial records into standardized CSV and PDF formats for tax management or independent review.

---

## 4. Module List

### 4.1 User Management Module
Governs account creation, access control, and user configuration.
* **Authentication Subsystem:** Handles secure user registration, encrypted login verification, and secure logout cycles.
* **Profile Configuration:** Manages user metadata, password modification protocols, and global settings like preferred currency symbols ($, €, ₹).

### 4.2 Transaction Management Module
The core operational ledger responsible for processing and storing all cash flows.
* **Income Logger:** Captures financial inflows with fields for amount, source category (e.g., Salary, Freelance), date, and notes.
* **Expense Logger:** Tracks financial outflows against specific categories (e.g., Food, Rent, Utilities) with mandatory positive-value validation.
* **Audit Trail Ledger:** Provides an itemized history table with advanced capabilities for sorting, filtering by date/category, and keyword searching.

### 4.3 Budget & Goal Management Module
The boundary layer that evaluates active spending against pre-defined rules.
* **Threshold Configuration:** Allows users to allocate maximum spending caps to specific expense categories for a designated monthly cycle.
* **Velocity Tracker:** Dynamically computes active budget consumption, outputting real-time percentage indicators (e.g., "80% of Food budget spent").

### 4.4 Analytics & Reporting Module
The business intelligence layer that transforms raw rows of data into visual insights.
* **Categorical Visualizer:** Aggregates transaction data to render proportional distribution charts (e.g., Pie charts).
* **Chronological Trend Engine:** Maps temporal data to illustrate net monthly cash flow variations (Income vs. Expense) via bar or line graphs.
* **Document Compiler:** Generates clean, downloadable CSV or PDF file exports based on user-selected date ranges.

---

## 5. Table List (Database Schema Blueprint)

The system utilizes a relational database management system (RDBMS) design consisting of five core tables to manage entities, relationships, and transactional records cleanly.

### 5.1 `tbl_users`
**Purpose:** Stores unique user profiles, authentication parameters, and global localization UI configurations.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `user_id` | INT | PRIMARY KEY, AUTO_INCREMENT | System-generated unique identity token for each user. |
| `username` | VARCHAR(50) | NOT NULL, UNIQUE | Custom alphanumeric screen name for the user profile. |
| `email` | VARCHAR(100) | NOT NULL, UNIQUE | Verified email address used as the unique login username. |
| `password_hash`| VARCHAR(255) | NOT NULL | Salted cryptographic hash of the account login password. |
| `currency_code`| VARCHAR(3) | DEFAULT 'USD', NOT NULL | Standardized 3-letter currency code for financial display. |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | System timestamp capturing original user onboarding date. |

### 5.2 `tbl_categories`
**Purpose:** A lookup dictionary mapping categories to their directional financial flow types.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `category_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Unique internal key for classification lookups. |
| `name` | VARCHAR(50) | NOT NULL, UNIQUE | Plain text classification name (e.g., "Salary", "Utilities"). |
| `flow_type` | ENUM | ('Income', 'Expense') NOT NULL | Restricts category classification strictly to input or output. |

### 5.3 `tbl_transactions`
**Purpose:** The ledger holding the historic sequence of all logged cash inflows and outflows.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `transaction_id`| INT | PRIMARY KEY, AUTO_INCREMENT | Unique sequential tracking identifier for each entry. |
| `user_id` | INT | FOREIGN KEY references `tbl_users` | Traces the transactional entry back to its specific owner. |
| `category_id` | INT | FOREIGN KEY references `tbl_categories` | Groups the entry under a designated ledger classification. |
| `amount` | DECIMAL(12,2)| NOT NULL | Numerical asset value of the record (strictly non-negative). |
| `description` | TEXT | NULLABLE | Optional open-ended user documentation on the item. |
| `actual_date` | DATE | NOT NULL | User-specified calendar day the payment occurred. |
| `logged_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Automatic background timestamp when database row inserts. |

### 5.4 `tbl_budgets`
**Purpose:** Tracks spending constraint boundaries defined by users for fixed temporal tracking cycles.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `budget_id` | INT | PRIMARY KEY, AUTO_INCREMENT | System token identifying the active budget rule. |
| `user_id` | INT | FOREIGN KEY references `tbl_users` | Identifies which user account the constraint checks. |
| `category_id` | INT | FOREIGN KEY references `tbl_categories` | Targets the specific outflow group being locked down. |
| `limit_amount` | DECIMAL(12,2)| NOT NULL | Absolute maximum capital threshold for the period. |
| `start_date` | DATE | NOT NULL | Calendar validation window start date. |
| `end_date` | DATE | NOT NULL | Calendar validation window cutoff date. |

### 5.5 `tbl_audit_logs`
**Purpose:** Background security table logging administrative activity for session auditing.

| Column Name | Data Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `log_id` | INT | PRIMARY KEY, AUTO_INCREMENT | Sequential record item key. |
| `user_id` | INT | FOREIGN KEY references `tbl_users` | Traces the session operator triggering the system change. |
| `action_performed`| VARCHAR(100)| NOT NULL | System event descriptor (e.g., "LOGIN", "DELETE_TX"). |
| `event_time` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Absolute server time execution stamp. |

---

## 6. Expected Outcome

Upon successful execution, the **Personal Expense Evaluator** will yield the following operational outcomes:

* **Centralized Financial Visibility:** Users gain immediate clarity via a unified landing dashboard displaying real-time metrics for total revenue, total expense expenditures, and calculated net disposable savings balance.
* **Mitigated Overspending through Notifications:** The platform will visually flag budget overruns instantly. The user-interface dynamically switches color schemes (e.g., shifting status gauges from green to red) when category expenditures breach 80% and 100% threshold limits.
* **Data-driven Insight Derivation:** Raw transaction grids translate effortlessly into interactive charts, allowing users to accurately deduce high-burn spend categories (e.g., exactly what percentage goes to entertainment vs savings) within a billing cycle.
* **Frictionless Compliance Exporting:** Users can download curated ledger histories on-demand into formatted `.csv` sheets or formal `.pdf` data files, reducing preparation time for individual tax compliance assessments or strategic multi-year tracking.
* **Cross-Session Structural Persistence:** Relational query mapping guarantees absolute data isolation, ensuring multi-user profiles can interact concurrently while reliably protecting underlying data states securely across subsequent system sessions.
