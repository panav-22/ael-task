# 🏭 Amba Enterprises Limited — ERP System Design & Strategy Challenge

## 📋 Stage 2 Submission — ERP System Design & Strategy

A complete ERP system design, strategy document, and working Streamlit prototype for Amba Enterprises Limited — a ₹337 Cr BSE-listed transformer lamination manufacturer.

---

## 🎥 Prototype Demo

https://github.com/panav-22/ael-task/raw/main/demo.mov

---

## 📦 Deliverables

| # | Deliverable | Description |
|---|------------|-------------|
| 1 | **🔍 Company Research & Pain Points** | Top 3 pain points identified from AEL's Excel management report |
| 2 | **⚖️ Build vs. Buy Strategy** | Recommends BUILD (custom Python/Streamlit) with 3-year TCO comparison |
| 3 | **🏗️ System Architecture** | Streamlit + FastAPI + PostgreSQL stack with system diagrams |
| 4 | **📊 Data Modeling** | Full SQL DDL schema — 10 tables, FKs, constraints, 15+ indexes |
| 5 | **🎯 Implementation Flow** | Sales Order creation workflow, REST API specs, class diagrams |
| 6 | **💻 Streamlit Prototype** | Working app with Inventory Dashboard + Order Form + SQL generation |

> All written deliverables (1–5) are in [`AEL_ERP_Design_Document.md`](./AEL_ERP_Design_Document.md)

---

## 🚀 Run the Prototype Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Launch the app
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🖥️ Prototype Features

### Tab 1 — Inventory Dashboard
- Loads product data from the Excel management report
- Metric cards: Total Products, In Stock, Low Stock, Out of Stock
- Interactive inventory table with status indicators
- Raw material usage summary

### Tab 2 — New Sales Order
- Customer and Product dropdowns (from Excel data)
- Order Qty, Rate, Date, and Remarks fields
- **Validation**: all mandatory fields checked, qty/rate > 0
- **Output**: generates valid SQL `INSERT` statements for `orders`, `order_items`, and `inventory_log` tables

### Tab 3 — Reports Overview
- Customer Profitability with collection rate analysis
- Order Balance with fulfillment percentage
- Production & Despatch logs
- Outstanding invoices & Collection reports

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | Streamlit |
| Backend API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Automation | Power Automate / n8n |
| AI/ML | Python (scikit-learn, Prophet) |

---

## 📁 File Structure

```
├── app.py                                    # Streamlit prototype
├── requirements.txt                          # Python dependencies
├── AEL_ERP_Design_Document.md                # All written deliverables (1-5)
├── Management Report - Intern Challenge.xlsx # Source Excel data
├── demo.mov                                  # Prototype demo recording
└── README.md                                 # This file
```

---

## 👤 Author

**Panav Jogi**  
Stage 2 — ERP System Design & Strategy Challenge
