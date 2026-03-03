"""
AEL ERP Prototype — Streamlit Application
Amba Enterprises Limited — ERP System Design & Strategy Challenge

Features:
1. Inventory List — loaded from the sample Excel management report
2. New Order Form — with validation and SQL INSERT statement generation
"""

import streamlit as st
import pandas as pd
from datetime import date, datetime
from decimal import Decimal

# ──────────────────────────────────────────────
# Page Configuration
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="AEL ERP Prototype",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ──────────────────────────────────────────────
# Custom CSS for Premium Styling
# ──────────────────────────────────────────────
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #1a1a3e 50%, #24243e 100%);
    }

    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2rem;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-header p {
        color: rgba(255,255,255,0.85);
        margin: 0.3rem 0 0 0;
        font-size: 1rem;
    }

    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-label {
        color: rgba(255,255,255,0.6);
        font-size: 0.85rem;
        margin-top: 0.3rem;
    }

    /* Status badges */
    .status-in-stock {
        background: rgba(0, 200, 83, 0.15);
        color: #00c853;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-low-stock {
        background: rgba(255, 171, 0, 0.15);
        color: #ffab00;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-out-of-stock {
        background: rgba(255, 82, 82, 0.15);
        color: #ff5252;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    /* SQL output box */
    .sql-box {
        background: rgba(30, 30, 50, 0.9);
        border: 1px solid rgba(102, 126, 234, 0.4);
        border-radius: 12px;
        padding: 1.5rem;
        font-family: 'Fira Code', 'Courier New', monospace;
        color: #a8e6cf;
        font-size: 0.9rem;
        line-height: 1.6;
        overflow-x: auto;
        white-space: pre-wrap;
        word-wrap: break-word;
    }

    /* Success message */
    .success-box {
        background: linear-gradient(135deg, rgba(0,200,83,0.1), rgba(0,200,83,0.05));
        border: 1px solid rgba(0,200,83,0.3);
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 10px 24px;
        font-weight: 600;
    }

    /* Form styling */
    .stSelectbox, .stNumberInput, .stDateInput {
        margin-bottom: 0.5rem;
    }

    /* Divider */
    .section-divider {
        border: none;
        border-top: 1px solid rgba(255,255,255,0.1);
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
# Data Loading Functions
# ──────────────────────────────────────────────
@st.cache_data
def load_excel_data():
    """Load all sheets from the Management Report Excel file."""
    excel_file = "Management Report - Intern Challenge.xlsx"

    try:
        # Load all relevant sheets
        sales_orders = pd.read_excel(excel_file, sheet_name="Sales Order (Sample)")
        order_balance = pd.read_excel(excel_file, sheet_name="Order Balance Report (Sample)")
        production = pd.read_excel(excel_file, sheet_name="Production Report (Sample)")
        despatches = pd.read_excel(excel_file, sheet_name="Despatches Report (Sample)")
        customers = pd.read_excel(excel_file, sheet_name="Customer Profitability Summary ")
        raw_materials = pd.read_excel(excel_file, sheet_name="Raw Material Used (Sample)")
        outstanding = pd.read_excel(excel_file, sheet_name="Outstanding Report (as of 31-Ju")
        collections = pd.read_excel(excel_file, sheet_name="Customer Collection Report (Sam")

        return {
            "sales_orders": sales_orders,
            "order_balance": order_balance,
            "production": production,
            "despatches": despatches,
            "customers": customers,
            "raw_materials": raw_materials,
            "outstanding": outstanding,
            "collections": collections
        }
    except FileNotFoundError:
        st.error(f"❌ Excel file '{excel_file}' not found. Please ensure it's in the same directory as this app.")
        return None


def build_inventory_data(data):
    """
    Build a consolidated inventory view by combining:
    - Products from Sales Orders (what's been ordered)
    - Production data (what's been produced)
    - Despatch data (what's been shipped)
    - Order Balance (ordered vs dispatched vs pending)
    """
    # Get unique products from various sheets
    products_from_orders = data["sales_orders"][["Item Description", "Rate ($)"]].drop_duplicates(subset="Item Description")
    products_from_production = data["production"][["Product Name", "Qty Produced"]].copy()
    products_from_despatches = data["despatches"][["Item Description", "Despatch Qty"]].copy()

    # Aggregate production by product
    prod_agg = products_from_production.groupby("Product Name")["Qty Produced"].sum().reset_index()
    prod_agg.columns = ["Product", "Total Produced"]

    # Aggregate despatches by product
    desp_agg = products_from_despatches.groupby("Item Description")["Despatch Qty"].sum().reset_index()
    desp_agg.columns = ["Product", "Total Dispatched"]

    # Aggregate order quantities from order balance
    order_bal = data["order_balance"][["Item Description", "Order Qty", "Dispatched Qty", "Balance Qty"]].copy()
    order_bal.columns = ["Product", "Total Ordered", "Dispatched (Orders)", "Pending Qty"]
    order_agg = order_bal.groupby("Product").agg({
        "Total Ordered": "sum",
        "Dispatched (Orders)": "sum",
        "Pending Qty": "sum"
    }).reset_index()

    # Get rates
    rates = products_from_orders.copy()
    rates.columns = ["Product", "Rate (₹)"]

    # Merge all data
    all_products = set(prod_agg["Product"].tolist() +
                       desp_agg["Product"].tolist() +
                       order_agg["Product"].tolist() +
                       rates["Product"].tolist())

    inventory_rows = []
    for product in sorted(all_products):
        produced = prod_agg[prod_agg["Product"] == product]["Total Produced"].sum()
        dispatched = desp_agg[desp_agg["Product"] == product]["Total Dispatched"].sum()
        ordered = order_agg[order_agg["Product"] == product]["Total Ordered"].sum()
        pending = order_agg[order_agg["Product"] == product]["Pending Qty"].sum()

        rate_match = rates[rates["Product"] == product]["Rate (₹)"]
        rate = rate_match.values[0] if len(rate_match) > 0 else 0

        # Calculate current stock = produced - dispatched
        current_stock = produced - dispatched

        # Determine status
        if current_stock <= 0:
            status = "🔴 Out of Stock"
        elif current_stock < (ordered * 0.3):
            status = "🟡 Low Stock"
        else:
            status = "🟢 In Stock"

        inventory_rows.append({
            "Product": product,
            "Rate (₹)": f"₹{rate:,.2f}",
            "Total Produced": int(produced),
            "Total Dispatched": int(dispatched),
            "Current Stock": int(current_stock),
            "Total Ordered": int(ordered),
            "Pending Orders": int(pending),
            "Status": status
        })

    return pd.DataFrame(inventory_rows)


def get_customer_list(data):
    """Get unique customer names from the Excel data."""
    return data["customers"]["Customer Name"].tolist()


def get_product_list(data):
    """Get unique product descriptions from Sales Orders."""
    return data["sales_orders"]["Item Description"].unique().tolist()


def get_product_rate(data, product_name):
    """Get the rate for a given product."""
    match = data["sales_orders"][data["sales_orders"]["Item Description"] == product_name]["Rate ($)"]
    if len(match) > 0:
        return float(match.values[0])
    return 0.0


def get_next_order_no(data):
    """Generate the next sequential order number."""
    existing = data["sales_orders"]["Order No"].tolist()
    max_num = 0
    for order_no in existing:
        try:
            num = int(str(order_no).replace("SO-", ""))
            max_num = max(max_num, num)
        except ValueError:
            pass
    return f"SO-{max_num + 1}"


def generate_sql_insert(order_data):
    """Generate SQL INSERT statements for the order."""
    # INSERT for orders table
    order_sql = f"""-- ═══════════════════════════════════════════
-- SQL INSERT Statements for New Sales Order
-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
-- ═══════════════════════════════════════════

-- Step 1: Insert into ORDERS table
INSERT INTO orders (order_no, customer_id, order_date, status, total_amount, remarks, created_at)
VALUES (
    '{order_data['order_no']}',
    (SELECT customer_id FROM customers WHERE customer_name = '{order_data['customer_name']}'),
    '{order_data['order_date']}',
    'Pending',
    {order_data['total_amount']:.2f},
    '{order_data.get('remarks', '')}',
    CURRENT_TIMESTAMP
);

-- Step 2: Insert into ORDER_ITEMS table
INSERT INTO order_items (order_id, product_id, order_qty, rate, dispatched_qty)
VALUES (
    (SELECT order_id FROM orders WHERE order_no = '{order_data['order_no']}'),
    (SELECT product_id FROM products WHERE product_name || ' - ' || specification = '{order_data['product_name']}'),
    {order_data['order_qty']},
    {order_data['rate']:.2f},
    0
);

-- Step 3: Insert into INVENTORY_LOG (stock reservation)
INSERT INTO inventory_log (product_id, movement_type, quantity, reference_type, reference_id, remarks, created_at)
VALUES (
    (SELECT product_id FROM products WHERE product_name || ' - ' || specification = '{order_data['product_name']}'),
    'RESERVED',
    -{order_data['order_qty']},
    'ORDER',
    (SELECT order_id FROM orders WHERE order_no = '{order_data['order_no']}'),
    'Stock reserved for order {order_data['order_no']}',
    CURRENT_TIMESTAMP
);

-- Step 4: Update product stock level
UPDATE products
SET current_stock = current_stock - {order_data['order_qty']}
WHERE product_name || ' - ' || specification = '{order_data['product_name']}';"""

    return order_sql


# ──────────────────────────────────────────────
# Main Application
# ──────────────────────────────────────────────
def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏭 Amba Enterprises Limited — ERP Prototype</h1>
        <p>Transformer Lamination Manufacturing | Inventory & Order Management System</p>
    </div>
    """, unsafe_allow_html=True)

    # Load Data
    data = load_excel_data()
    if data is None:
        return

    # ────────────────────────────────────────
    # Tabs
    # ────────────────────────────────────────
    tab1, tab2, tab3 = st.tabs(["📦 Inventory Dashboard", "📝 New Sales Order", "📊 Reports Overview"])

    # ══════════════════════════════════════════
    # TAB 1: INVENTORY DASHBOARD
    # ══════════════════════════════════════════
    with tab1:
        st.markdown("### 📦 Inventory Overview")
        st.markdown("*Real-time stock levels derived from production and dispatch data*")

        # Build inventory data
        inventory_df = build_inventory_data(data)

        # Summary Metrics
        col1, col2, col3, col4 = st.columns(4)

        total_products = len(inventory_df)
        in_stock = len(inventory_df[inventory_df["Status"].str.contains("In Stock")])
        low_stock = len(inventory_df[inventory_df["Status"].str.contains("Low")])
        out_of_stock = len(inventory_df[inventory_df["Status"].str.contains("Out")])

        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_products}</div>
                <div class="metric-label">Total Products</div>
            </div>""", unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{in_stock}</div>
                <div class="metric-label">In Stock ✅</div>
            </div>""", unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{low_stock}</div>
                <div class="metric-label">Low Stock ⚠️</div>
            </div>""", unsafe_allow_html=True)

        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{out_of_stock}</div>
                <div class="metric-label">Out of Stock 🔴</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

        # Inventory Table
        st.markdown("#### 📋 Product Inventory List")

        # Filter options
        filter_col1, filter_col2 = st.columns([1, 3])
        with filter_col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "🟢 In Stock", "🟡 Low Stock", "🔴 Out of Stock"],
                key="inv_status_filter"
            )

        filtered_df = inventory_df.copy()
        if status_filter != "All":
            filtered_df = filtered_df[filtered_df["Status"] == status_filter]

        # Display the dataframe
        st.dataframe(
            filtered_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Product": st.column_config.TextColumn("Product", width="large"),
                "Rate (₹)": st.column_config.TextColumn("Rate", width="small"),
                "Total Produced": st.column_config.NumberColumn("Produced", format="%d"),
                "Total Dispatched": st.column_config.NumberColumn("Dispatched", format="%d"),
                "Current Stock": st.column_config.NumberColumn("Current Stock", format="%d"),
                "Total Ordered": st.column_config.NumberColumn("Ordered", format="%d"),
                "Pending Orders": st.column_config.NumberColumn("Pending", format="%d"),
                "Status": st.column_config.TextColumn("Status", width="medium"),
            }
        )

        # Additional: Raw Material Stock
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
        st.markdown("#### 🧱 Raw Material Usage Summary")
        raw_mat_df = data["raw_materials"].copy()
        raw_mat_df.columns = ["Issue Date", "Raw Material", "Qty Issued (kg)", "Issued to Machine"]
        raw_mat_df["Issue Date"] = pd.to_datetime(raw_mat_df["Issue Date"]).dt.strftime("%Y-%m-%d")
        st.dataframe(raw_mat_df, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # TAB 2: NEW SALES ORDER FORM
    # ══════════════════════════════════════════
    with tab2:
        st.markdown("### 📝 Create New Sales Order")
        st.markdown("*Fill in the order details below. Upon submission, the system will validate your input and generate the SQL INSERT statements.*")

        # Get next order number
        next_order_no = get_next_order_no(data)

        st.markdown(f"""
        <div class="metric-card" style="max-width: 200px; margin-bottom: 1.5rem;">
            <div class="metric-label">Order Number</div>
            <div class="metric-value" style="font-size: 1.5rem;">{next_order_no}</div>
        </div>
        """, unsafe_allow_html=True)

        # Order Form
        with st.form("order_form", clear_on_submit=False):
            st.markdown("#### Order Details")

            col1, col2 = st.columns(2)

            with col1:
                customer_name = st.selectbox(
                    "Customer Name *",
                    options=["-- Select Customer --"] + get_customer_list(data),
                    key="customer_select"
                )

                order_date = st.date_input(
                    "Order Date *",
                    value=date.today(),
                    key="order_date_input"
                )

            with col2:
                product_name = st.selectbox(
                    "Product *",
                    options=["-- Select Product --"] + get_product_list(data),
                    key="product_select"
                )

                # Show rate for selected product
                if product_name != "-- Select Product --":
                    default_rate = get_product_rate(data, product_name)
                    st.info(f"📌 Standard Rate: ₹{default_rate:,.2f}")
                else:
                    default_rate = 0.0

            col3, col4 = st.columns(2)

            with col3:
                order_qty = st.number_input(
                    "Order Quantity *",
                    min_value=0,
                    max_value=1000000,
                    value=0,
                    step=100,
                    key="order_qty_input"
                )

            with col4:
                rate = st.number_input(
                    "Rate per Unit (₹) *",
                    min_value=0.0,
                    max_value=100000.0,
                    value=default_rate,
                    step=0.5,
                    format="%.2f",
                    key="rate_input"
                )

            remarks = st.text_area(
                "Remarks (Optional)",
                placeholder="Enter any special instructions or notes...",
                key="remarks_input"
            )

            # Calculated Total
            total_amount = order_qty * rate
            if total_amount > 0:
                st.markdown(f"**💰 Order Total: ₹{total_amount:,.2f}**")

            st.markdown("---")
            submitted = st.form_submit_button(
                "✅ Submit Order & Generate SQL",
                use_container_width=True,
                type="primary"
            )

        # ── Form Validation & SQL Generation ──
        if submitted:
            errors = []

            # Validate mandatory fields
            if customer_name == "-- Select Customer --":
                errors.append("⚠️ **Customer Name** is required.")

            if product_name == "-- Select Product --":
                errors.append("⚠️ **Product** is required.")

            if order_qty <= 0:
                errors.append("⚠️ **Order Quantity** must be greater than 0.")

            if rate <= 0:
                errors.append("⚠️ **Rate** must be greater than 0.")

            if errors:
                st.markdown("### ❌ Validation Errors")
                for error in errors:
                    st.error(error)
            else:
                # All validations passed — generate SQL
                order_data = {
                    "order_no": next_order_no,
                    "customer_name": customer_name,
                    "product_name": product_name,
                    "order_date": order_date.strftime("%Y-%m-%d"),
                    "order_qty": order_qty,
                    "rate": rate,
                    "total_amount": total_amount,
                    "remarks": remarks.replace("'", "''") if remarks else ""
                }

                # Success message
                st.markdown(f"""
                <div class="success-box">
                    <h4 style="color: #00c853; margin: 0;">✅ Order Validated Successfully!</h4>
                    <p style="color: rgba(255,255,255,0.7); margin: 0.5rem 0 0 0;">
                        <strong>{next_order_no}</strong> | {customer_name} | {product_name} |
                        Qty: {order_qty:,} | Rate: ₹{rate:,.2f} | Total: ₹{total_amount:,.2f}
                    </p>
                </div>
                """, unsafe_allow_html=True)

                # Generate and display SQL
                sql_statements = generate_sql_insert(order_data)

                st.markdown("### 🗄️ Generated SQL INSERT Statements")
                st.markdown("*These are the SQL statements that would be executed against the proposed PostgreSQL database:*")

                st.markdown(f'<div class="sql-box">{sql_statements}</div>', unsafe_allow_html=True)

                # Also show in a copyable code block
                with st.expander("📋 Click to copy SQL (plain text)", expanded=False):
                    st.code(sql_statements, language="sql")

                # Order Summary Table
                st.markdown("### 📋 Order Summary")
                summary_df = pd.DataFrame([{
                    "Field": "Order No",
                    "Value": next_order_no
                }, {
                    "Field": "Customer",
                    "Value": customer_name
                }, {
                    "Field": "Product",
                    "Value": product_name
                }, {
                    "Field": "Order Date",
                    "Value": order_date.strftime("%Y-%m-%d")
                }, {
                    "Field": "Quantity",
                    "Value": f"{order_qty:,}"
                }, {
                    "Field": "Rate",
                    "Value": f"₹{rate:,.2f}"
                }, {
                    "Field": "Total Amount",
                    "Value": f"₹{total_amount:,.2f}"
                }, {
                    "Field": "Status",
                    "Value": "Pending"
                }])
                st.dataframe(summary_df, use_container_width=True, hide_index=True)

    # ══════════════════════════════════════════
    # TAB 3: REPORTS OVERVIEW
    # ══════════════════════════════════════════
    with tab3:
        st.markdown("### 📊 Management Reports Overview")
        st.markdown("*Data loaded from the Management Report Excel file*")

        report_tab1, report_tab2, report_tab3, report_tab4 = st.tabs([
            "💰 Customer Profitability",
            "📦 Order Balance",
            "🏭 Production Log",
            "💳 Outstanding & Collections"
        ])

        with report_tab1:
            st.markdown("#### Customer Profitability Summary")
            cust_df = data["customers"].copy()
            cust_df["Collection Rate (%)"] = (
                cust_df["Total Collected ($)"] / cust_df["Total Order Value ($)"] * 100
            ).round(1)
            st.dataframe(cust_df, use_container_width=True, hide_index=True)

            # Bar chart
            st.markdown("#### Revenue vs. Collections")
            chart_data = cust_df[["Customer Name", "Total Order Value ($)", "Total Collected ($)"]].set_index("Customer Name")
            st.bar_chart(chart_data)

        with report_tab2:
            st.markdown("#### Order Balance Report")
            ob_df = data["order_balance"].copy()
            ob_df["Fulfillment %"] = (ob_df["Dispatched Qty"] / ob_df["Order Qty"] * 100).round(1)
            st.dataframe(ob_df, use_container_width=True, hide_index=True)

        with report_tab3:
            st.markdown("#### Production Report")
            prod_df = data["production"].copy()
            prod_df["Prod. Date"] = pd.to_datetime(prod_df["Prod. Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(prod_df, use_container_width=True, hide_index=True)

            st.markdown("#### Despatches Report")
            desp_df = data["despatches"].copy()
            desp_df["Despatch Date"] = pd.to_datetime(desp_df["Despatch Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(desp_df, use_container_width=True, hide_index=True)

        with report_tab4:
            st.markdown("#### Outstanding Report (as of 31-Jul)")
            out_df = data["outstanding"].copy()
            out_df["Invoice Date"] = pd.to_datetime(out_df["Invoice Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(out_df, use_container_width=True, hide_index=True)

            st.markdown("#### Customer Collection Report")
            coll_df = data["collections"].copy()
            coll_df["Collection Date"] = pd.to_datetime(coll_df["Collection Date"]).dt.strftime("%Y-%m-%d")
            st.dataframe(coll_df, use_container_width=True, hide_index=True)

    # ────────────────────────────────────────
    # Footer
    # ────────────────────────────────────────
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; color: rgba(255,255,255,0.4); font-size: 0.8rem; padding: 1rem 0;">
        🏭 AEL ERP Prototype | Built with Streamlit | Amba Enterprises Limited — Stage 2 Challenge
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
