from fastmcp import FastMCP
import os
import sqlite3
import csv
import io

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")
CATEGORIES_PATH = os.path.join(os.path.dirname(__file__), "categories.json")

mcp = FastMCP("ExpenseTracker")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""
            CREATE TABLE IF NOT EXISTS expenses(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT '',
                note TEXT DEFAULT ''
            )
        """)

init_db()

@mcp.tool()
def add_expense(date, amount, category, subcategory="", note=""):
    '''Add a new expense entry to the database.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            "INSERT INTO expenses(date, amount, category, subcategory, note) VALUES (?,?,?,?,?)",
            (date, amount, category, subcategory, note)
        )
        return {"status": "ok", "id": cur.lastrowid}
    
@mcp.tool()
def list_expenses(start_date, end_date):
    '''List expense entries within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date DESC, id DESC
            """,
            (start_date, end_date)
        )
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def summarize(start_date, end_date, category=None):
    '''Summarize expenses by category within an inclusive date range.'''
    with sqlite3.connect(DB_PATH) as c:
        query = (
            """
            SELECT category, SUM(amount) AS total_amount
            FROM expenses
            WHERE date BETWEEN ? AND ?
            """
        )
        params = [start_date, end_date]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " GROUP BY category ORDER BY category ASC"

        cur = c.execute(query, params)
        cols = [d[0] for d in cur.description]
        return [dict(zip(cols, r)) for r in cur.fetchall()]

@mcp.tool()
def get_expense_by_id(expense_id: int):
    '''Get a specific expense by its ID.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE id = ?
            """,
            (expense_id,)
        )
        cols = [d[0] for d in cur.description]
        row = cur.fetchone()
        if row:
            return dict(zip(cols, row))
        else:
            return {"status": "error", "message": f"Expense with id {expense_id} not found"}

@mcp.tool()
def delete_expense(expense_id: int):
    '''Delete a specific expense by its ID.'''
    with sqlite3.connect(DB_PATH) as c:
        # Check if expense exists
        cur = c.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Expense with id {expense_id} not found"}
        
        c.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        c.commit()
        return {"status": "ok", "message": f"Expense {expense_id} deleted successfully"}

@mcp.tool()
def update_expense(expense_id: int, date=None, amount=None, category=None, subcategory=None, note=None):
    '''Update an existing expense. Only provided fields will be updated.'''
    with sqlite3.connect(DB_PATH) as c:
        # Check if expense exists
        cur = c.execute("SELECT id FROM expenses WHERE id = ?", (expense_id,))
        if not cur.fetchone():
            return {"status": "error", "message": f"Expense with id {expense_id} not found"}
        
        # Build dynamic update query
        updates = []
        params = []
        
        if date is not None:
            updates.append("date = ?")
            params.append(date)
        if amount is not None:
            updates.append("amount = ?")
            params.append(amount)
        if category is not None:
            updates.append("category = ?")
            params.append(category)
        if subcategory is not None:
            updates.append("subcategory = ?")
            params.append(subcategory)
        if note is not None:
            updates.append("note = ?")
            params.append(note)
        
        if not updates:
            return {"status": "error", "message": "No fields to update"}
        
        params.append(expense_id)
        query = f"UPDATE expenses SET {', '.join(updates)} WHERE id = ?"
        
        c.execute(query, params)
        c.commit()
        return {"status": "ok", "message": f"Expense {expense_id} updated successfully"}

@mcp.tool()
def search_expenses(search_term: str, search_in="note"):
    '''Search expenses by note, category, or subcategory. Returns all matching expenses.'''
    with sqlite3.connect(DB_PATH) as c:
        if search_in == "note":
            query = """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE note LIKE ?
                ORDER BY date DESC, id DESC
            """
        elif search_in == "category":
            query = """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE category LIKE ?
                ORDER BY date DESC, id DESC
            """
        elif search_in == "subcategory":
            query = """
                SELECT id, date, amount, category, subcategory, note
                FROM expenses
                WHERE subcategory LIKE ?
                ORDER BY date DESC, id DESC
            """
        else:
            return {"status": "error", "message": "search_in must be 'note', 'category', or 'subcategory'"}
        
        cur = c.execute(query, (f"%{search_term}%",))
        cols = [d[0] for d in cur.description]
        results = [dict(zip(cols, r)) for r in cur.fetchall()]
        return {"status": "ok", "count": len(results), "expenses": results}

@mcp.tool()
def delete_all_expenses(start_date=None, end_date=None, category=None, confirm=False):
    '''Delete multiple expenses. Use filters to narrow down deletion. REQUIRES confirm=True to execute.'''
    if not confirm:
        return {
            "status": "error", 
            "message": "This is a destructive operation. Set confirm=True to proceed."
        }
    
    with sqlite3.connect(DB_PATH) as c:
        query = "DELETE FROM expenses WHERE 1=1"
        params = []
        
        if start_date and end_date:
            query += " AND date BETWEEN ? AND ?"
            params.extend([start_date, end_date])
        if category:
            query += " AND category = ?"
            params.append(category)
        
        # If no filters, delete everything
        cur = c.execute(query, params)
        deleted_count = cur.rowcount
        c.commit()
        
        return {
            "status": "ok", 
            "message": f"Deleted {deleted_count} expense(s)",
            "count": deleted_count
        }

@mcp.tool()
def delete_expenses_by_category(category: str, confirm=False):
    '''Delete all expenses in a specific category. REQUIRES confirm=True to execute.'''
    if not confirm:
        return {
            "status": "error",
            "message": "This is a destructive operation. Set confirm=True to proceed."
        }
    
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute("DELETE FROM expenses WHERE category = ?", (category,))
        deleted_count = cur.rowcount
        c.commit()
        
        return {
            "status": "ok",
            "message": f"Deleted {deleted_count} expense(s) from category '{category}'",
            "count": deleted_count
        }

@mcp.tool()
def get_total_expenses(start_date, end_date, category=None):
    '''Get the total amount of expenses for a date range, optionally filtered by category.'''
    with sqlite3.connect(DB_PATH) as c:
        query = "SELECT SUM(amount) as total FROM expenses WHERE date BETWEEN ? AND ?"
        params = [start_date, end_date]
        
        if category:
            query += " AND category = ?"
            params.append(category)
        
        cur = c.execute(query, params)
        result = cur.fetchone()
        total = result[0] if result[0] is not None else 0.0
        
        return {
            "status": "ok",
            "total": total,
            "start_date": start_date,
            "end_date": end_date,
            "category": category if category else "all"
        }

@mcp.tool()
def export_expenses_csv(start_date, end_date):
    '''Export expenses to CSV format for a given date range. Returns CSV as a string.'''
    with sqlite3.connect(DB_PATH) as c:
        cur = c.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            WHERE date BETWEEN ? AND ?
            ORDER BY date ASC, id ASC
            """,
            (start_date, end_date)
        )
        
        # Create CSV in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow([d[0] for d in cur.description])
        
        # Write rows
        rows = cur.fetchall()
        writer.writerows(rows)
        
        csv_content = output.getvalue()
        output.close()
        
        return {
            "status": "ok",
            "csv": csv_content,
            "row_count": len(rows)
        }

@mcp.tool()
def get_categories():
    """Get the list of valid expense categories"""
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

@mcp.resource("expense://categories", mime_type="application/json")
def categories():
    # Read fresh each time so you can edit the file without restarting
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    mcp.run()
