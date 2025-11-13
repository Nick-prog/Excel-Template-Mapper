# Enhanced Column Details Widget - Feature Guide

## Overview

The **Selected Column Details** widget has been significantly improved to provide professional Excel-like capabilities for data transformation. The widget is now organized into intuitive tabs, each dedicated to a specific type of operation.

## Structure

The details widget is now divided into **5 main sections**:

### 1. **Basic Information** (Always Visible)
- **Target Column**: The output column name
- **Source Column**: The input column being mapped
- **Default Value**: Used when source data is empty or missing

### 2. **Type & Format Tab**
Set Excel-compatible data types and number formatting.

#### Data Type Options:
- **general** - Auto-detect (default)
- **text** - Forces text format
- **integer** - Whole numbers only
- **float** - Decimal numbers
- **date** - Date values
- **boolean** - True/False values

#### Format Templates:
- **None (Default)** - No special formatting
- **Number - 2 decimals** → `0.00`
- **Number - 4 decimals** → `0.0000`
- **Percentage** → `0%`
- **Currency ($)** → `$#,##0.00`
- **Currency (EUR €)** → `[$EUR -407] #,##0.00;[RED]-[$EUR -407] #,##0.00`
- **Date (MM/DD/YYYY)** → `mm/dd/yyyy`
- **Date (YYYY-MM-DD)** → `yyyy-mm-dd`
- **DateTime (MM/DD/YYYY HH:MM)** → `mm/dd/yyyy hh:mm`
- **Time (HH:MM:SS)** → `hh:mm:ss`
- **Phone (USA)** → `[<=9999999]###-####;(###) ###-####`
- **SSN (USA)** → `000-00-0000`

#### Custom Excel Format Codes:
- `0.00` - Two decimal places
- `#,##0` - Thousands separator
- `0%` - Percentage format
- `$#,##0.00` - Dollar currency
- `mm/dd/yyyy` - Date format
- `[<=9999999]###-####;(###) ###-####` - Phone numbers

### 3. **Find & Replace Tab**
Define multiple find/replace patterns for this column.

**Features:**
- Add multiple find/replace rules
- Each rule is applied sequentially
- Supports regex patterns for complex matching
- Delete individual rules

**Examples:**
| Find | Replace With | Purpose |
|------|--------------|---------|
| `old` | `new` | Simple text replacement |
| `^\\d{3}$` | `***` | Mask 3-digit patterns |
| `\\s+` | ` ` | Normalize whitespace |
| `NA` | `` (empty) | Remove placeholder values |

### 4. **Transforms Tab**
Apply built-in text and data transformations.

**Available Transforms:**
- **trim** - Remove leading/trailing whitespace
- **upper** - CONVERT TO UPPERCASE
- **lower** - convert to lowercase
- **title** - Convert To Title Case
- **to_string** - Convert to text format
- **to_int** - Convert to integer number
- **to_float** - Convert to decimal number
- **date_to_iso** - Convert to ISO format (YYYY-MM-DD)
- **digits_only** - Extract only numeric digits (0-9)

**Usage:**
Select multiple transforms in the order you want them applied. For example:
1. `trim` → Remove whitespace
2. `upper` → Convert to uppercase

### 5. **Advanced Tab**
Write custom logic for complex transformations using Python, Excel formulas, or regex patterns.

#### Format Types:

**Python Function**
Write Python code to transform data. Access values using:
- `source['ColumnName']` - Get value from source column
- `col['ColumnName']` - Get value from other target column
- Return the transformed value

**Example: Conditional Mapping**
```python
def format_column(col, source):
    """Map gender codes to full names."""
    mapping = {
        'M': 'Male',
        'F': 'Female',
        'U': 'Unknown'
    }
    return mapping.get(source['Gender'], 'Unknown')
```

**Excel Formula**
Use standard Excel formula syntax. The formula applies to each row.

**Example: Concatenation**
```
=CONCATENATE(A1, " - ", B1)
```

**Find & Replace Pattern**
Use regex for advanced text patterns.

**Example: Phone Number Formatting**
```
(\d{3})-(\d{3})-(\d{4}) -> ($1) $2-$3
```

#### Built-in Code Templates:

1. **Python: If/Else Logic**
   - Conditional transformations based on source values
   
2. **Python: Text Operations**
   - String manipulation: concatenate, extract, transform
   
3. **Python: Number Operations**
   - Arithmetic, rounding, conversions
   
4. **Python: String Replacement**
   - Regex-based text replacements
   
5. **Python: Date Parsing**
   - Parse and reformat date values
   
6. **Python: Conditional Mapping**
   - Map source values to categories
   
7. **Python: Null/Empty Handling**
   - Handle missing or blank values
   
8. **Excel: Basic Formula**
   - Simple conditional Excel formulas
   
9. **Excel: Concatenation**
   - Combine multiple columns
   
10. **Excel: VLOOKUP**
    - Lookup values in tables
    
11. **Regex: Phone Number**
    - Format phone numbers with regex
    
12. **Regex: Email Extraction**
    - Extract email addresses from text

## Advanced Python Examples

### String Operations
```python
def format_column(col, source):
    """Clean and normalize text."""
    value = source['Name'].strip()  # Remove whitespace
    return value.title() if value else 'Unknown'
```

### Number Calculations
```python
def format_column(col, source):
    """Calculate with fallback."""
    try:
        amount = float(source['Amount'])
        return round(amount * 1.1, 2)  # Add 10% and round
    except (ValueError, TypeError):
        return 0
```

### Date Formatting
```python
from datetime import datetime
def format_column(col, source):
    """Convert date format."""
    try:
        date_obj = datetime.strptime(source['Date'], '%m/%d/%Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return ''
```

### Complex Conditional Logic
```python
def format_column(col, source):
    """Multi-level decision logic."""
    age = float(source['Age'])
    if age < 18:
        return 'Minor'
    elif age < 65:
        return 'Adult'
    else:
        return 'Senior'
```

## Advanced Regex Examples

### Phone Number: Format `123456789` → `(123) 456-7890`
```
(\d{3})(\d{3})(\d{4}) -> ($1) $2-$3
```

### SSN: Format `123456789` → `123-45-6789`
```
(\d{3})(\d{2})(\d{4}) -> $1-$2-$3
```

### Extract Domain from Email
```
(.+)@([^.]+\.[^.]+) -> $2
```

### Remove All Non-Numeric Characters
```
[^\d] ->
```

## Workflow Example

Transforming customer data with all features:

1. **Type & Format**: Set to `text`
2. **Find & Replace**: 
   - Find: `customer_` Replace: `` (empty)
   - Find: `  ` Replace: ` `
3. **Transforms**: Apply `trim` then `title`
4. **Advanced**: Add Python logic for special cases

```python
def format_column(col, source):
    """Format customer names."""
    if source['Status'] == 'VIP':
        return source['Name'].upper() + ' (VIP)'
    return source['Name'].title()
```

## Tips & Best Practices

1. **Order Matters**: Find/Replace patterns and Transforms apply in sequence
2. **Type First**: Set data type before formatting (text operations before number formatting)
3. **Test Complex Logic**: Use "Validate Syntax" button for Python/Regex code
4. **Use Templates**: Start with a template and modify rather than writing from scratch
5. **Reference Other Columns**: In Python, access other columns with `col['ColumnName']`
6. **Handle Empty Values**: Always consider what happens when source is empty
7. **Regex Testing**: Test regex patterns thoroughly, especially with special characters

## Troubleshooting

**Syntax errors in Python code:**
- Click "Validate Syntax" to check for issues
- Ensure proper indentation
- Check that column names are spelled correctly

**Format not applying:**
- Verify the data type matches the format code
- Number formats require numeric data
- Date formats require proper date values

**Find/Replace not working:**
- Check regex syntax if using patterns
- Remember that patterns are case-sensitive
- Ensure find pattern actually exists in data

**Empty results:**
- Check default value is set
- Verify source column has data
- Test Python code with sample data

## Integration with Excel

All format codes, data types, and transformations are designed to work seamlessly with Excel:
- Format codes use standard Excel syntax
- Data types map to Excel cell types
- Results export directly to `.xlsx` with proper formatting applied

For more information about Excel format codes, see the [Microsoft Excel support documentation](https://support.microsoft.com/en-us/office/number-format-codes-5026bbd6-04bc-48cd-bf33-80f18b4671f7).