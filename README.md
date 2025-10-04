# Expense Tracker MCP Server

A Model Context Protocol (MCP) server for tracking personal expenses, built with FastMCP. This server allows you to manage your expenses directly through Claude Desktop, making expense tracking conversational and intuitive.

## Features

- ✅ Add, update, and delete expenses
- ✅ Categorize expenses with subcategories
- ✅ Search and filter expenses by date range, category, or notes
- ✅ Generate expense summaries and reports
- ✅ Export expenses to CSV format
- ✅ Bulk operations for expense management
- ✅ SQLite database for reliable data storage

## Getting Started with Claude Desktop

### Prerequisites

- Claude Desktop application installed on your computer
- Python 3.8 or higher
- Git (for cloning the repository)

### Step 1: Install the MCP Server

1. **Clone this repository:**
   ```bash
   git clone https://github.com/sagar0023/Expense-Tracker-Mcp-Server.git
   cd Expense-Tracker-Mcp-Server
   ```

2. **Install dependencies:**
   ```bash
   pip install fastmcp
   ```

### Step 2: Configure Claude Desktop

1. **Open Claude Desktop** on your computer

2. **Access MCP Settings:**
   - Click on your profile/settings (usually in the top-right corner)
   - Look for "MCP Servers" or "Model Context Protocol" settings

3. **Add the Expense Tracker Server:**
   - Click "Add Server" or similar button
   - Configure the server with these details:
     - **Name:** `Expense Tracker`
     - **Command:** `python`
     - **Arguments:** `["/full/path/to/your/main.py"]`
       - Replace `/full/path/to/your/` with the actual path to where you cloned this repository
       - Example: `["C:\\Users\\YourName\\Expense-Tracker-Mcp-Server\\main.py"]` (Windows)
       - Example: `["/Users/YourName/Expense-Tracker-Mcp-Server/main.py"]` (Mac/Linux)

4. **Save and Restart:**
   - Save the configuration
   - Restart Claude Desktop

### Step 3: Verify Installation

1. **Start a new conversation** in Claude Desktop

2. **Test the connection** by asking Claude:
   ```
   Can you show me the available expense tracking tools?
   ```

3. **Claude should respond** with a list of available expense tracking functions like:
   - `add_expense` - Add a new expense
   - `list_expenses` - View expenses in a date range
   - `summarize` - Get expense summaries by category
   - And more...

## How to Use

### Adding Expenses

Ask Claude to add expenses naturally:
```
Add an expense: $25.50 for groceries on 2024-10-04, category "Food", note "Weekly shopping"
```

### Viewing Expenses

Ask Claude to show your expenses:
```
Show me all expenses from October 1st to October 31st, 2024
```

### Getting Summaries

Ask for spending summaries:
```
Summarize my expenses by category for this month
```

### Searching Expenses

Search through your expenses:
```
Find all expenses with "coffee" in the notes
```

### Exporting Data

Export your data:
```
Export all my expenses from January to December 2024 as CSV
```

## Available Categories

The server comes with predefined categories in `categories.json`:
- Food & Dining
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Healthcare
- Travel
- Education
- And more...

You can customize these categories by editing the `categories.json` file.

## Data Storage

- Expenses are stored in a local SQLite database (`expenses.db`)
- Your data stays completely private on your computer
- The database is automatically created when you first run the server

## Troubleshooting

### Server Not Connecting

1. **Check the file path** in your Claude Desktop MCP configuration
2. **Ensure Python is installed** and accessible from command line
3. **Verify FastMCP is installed:** `pip show fastmcp`
4. **Check file permissions** - make sure `main.py` is executable

### Database Issues

- The database file (`expenses.db`) is created automatically
- If you encounter database errors, try deleting `expenses.db` - it will be recreated
- Check that you have write permissions in the project directory

### General Issues

1. **Restart Claude Desktop** after making configuration changes
2. **Check the logs** in Claude Desktop for error messages
3. **Test the server independently:**
   ```bash
   python main.py
   ```

## Example Conversations

Here are some example ways to interact with your expense tracker through Claude:

**Adding expenses:**
- "Add a $15 lunch expense for today in the Food category"
- "I spent $120 on gas yesterday, add it to Transportation"

**Viewing data:**
- "What did I spend on groceries this week?"
- "Show me all my entertainment expenses from last month"

**Analysis:**
- "How much did I spend in total this month?"
- "What's my biggest expense category this year?"
- "Compare my spending between August and September"

## Contributing

Feel free to fork this repository and submit pull requests for improvements!

## License

This project is open source. Feel free to use and modify as needed.

---

**Need help?** Open an issue on GitHub or ask Claude directly when using the expense tracker!