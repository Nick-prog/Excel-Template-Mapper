# Column Details Widget - Quick Reference Card

## 🎯 At a Glance

**New organized interface with 5 tabs for professional Excel-like data transformations**

```
┌─────────────────────────────────────────────────────┐
│ Selected Column Details                             │
├─────────────────────────────────────────────────────┤
│ Target: example_col | Source: source_col | Default: [__] │
├─────────────────────────────────────────────────────┤
│ [Type & Format] [Find & Replace] [Transforms] [Advanced]... │
├─────────────────────────────────────────────────────┤
│ Content area (varies by tab)                        │
├─────────────────────────────────────────────────────┤
│           [Apply to Selected Column]                │
└─────────────────────────────────────────────────────┘
```

## 📑 The 5 Tabs

### 1️⃣ Type & Format
**Set data type and Excel formatting**

Quick picks:
- 💵 Currency ($#,##0.00)
- 📅 Date (mm/dd/yyyy)
- ☎️ Phone ([<=9999999]###-####)
- 🔢 Percentage (0%)

### 2️⃣ Find & Replace  
**Pattern-based text replacement**

Example rules:
| Find | Replace | Effect |
|------|---------|--------|
| `old` | `new` | Simple replace |
| `^\\d{3}$` | `***` | Mask patterns |
| `\\s+` | ` ` | Normalize space |

### 3️⃣ Transforms
**Built-in operations**

Chain them:
1. `trim` (remove spaces)
2. `upper` (UPPERCASE)
3. `title` (Title Case)

Full list: trim, upper, lower, title, to_string, to_int, to_float, date_to_iso, digits_only

### 4️⃣ Advanced
**Custom logic**

Three modes:
- **Python** - Full Python functions
- **Excel** - Native Excel formulas
- **Regex** - Pattern matching

12 templates to choose from

### 5️⃣ Basic Info (Always Visible)
- Target Column name
- Source Column name
- Default Value (if empty)

## 🔧 Quick Recipes

### Recipe 1: Format as Currency
1. Go to **Type & Format** tab
2. Select preset: `Currency ($)`
3. Done! Format code `$#,##0.00` auto-filled
4. Click **Apply**

### Recipe 2: Clean Phone Numbers
1. **Find & Replace** tab
2. Add rule: Find `[^\d]`, Replace `` (empty)
3. **Transforms** tab: Add `trim`
4. **Type & Format**: Select `Phone (USA)`
5. Click **Apply**

### Recipe 3: Conditional Mapping
1. **Advanced** tab
2. Format Type: `Python Function`
3. Select template: `Conditional Mapping`
4. Modify mapping dictionary with your values
5. Click **Validate Syntax**
6. Click **Apply**

### Recipe 4: Multi-Step Transformation
1. **Find & Replace**: Clean up patterns
2. **Transforms**: Apply standard operations
3. **Type & Format**: Set data type
4. **Advanced**: Add custom logic
5. Click **Apply** (all applied in sequence)

## ✨ Common Use Cases

| Use Case | Tab(s) | How |
|----------|--------|-----|
| Format currency | Type & Format | Select preset |
| Standardize dates | Type & Format + Advanced | Preset + parse function |
| Clean messy data | Find & Replace + Transforms | Multiple rules + operations |
| Conditional logic | Advanced | Python if/else |
| Extract pattern | Advanced | Regex pattern |
| Multi-column logic | Advanced | Reference other columns |
| Remove duplicates | Find & Replace | Multiple patterns |
| Format phone | Type & Format + Transforms | Preset + digits_only |

## 🐍 Python Quick Reference

**Access data:**
```python
source['ColumnName']  # Input value
col['ColumnName']     # Other target column
```

**Template structure:**
```python
def format_column(col, source):
    # Your logic here
    return transformed_value
```

**Common patterns:**
```python
# If/else
if source['Gender'] == 'M': return 'Male'

# String operations
return source['Name'].upper().strip()

# Number operations
return round(float(source['Amount']), 2)

# Try/catch
try:
    return int(source['Value'])
except: 
    return 0
```

## 📊 Excel Format Codes

| Format | Code | Example |
|--------|------|---------|
| 2 decimals | `0.00` | 123.45 |
| 4 decimals | `0.0000` | 123.4500 |
| Thousands | `#,##0` | 1,234 |
| Currency | `$#,##0.00` | $1,234.50 |
| Percentage | `0%` | 45% |
| Date | `mm/dd/yyyy` | 12/25/2024 |
| Date ISO | `yyyy-mm-dd` | 2024-12-25 |
| Phone | `[<=9999999]###-####;(###) ###-####` | (123) 456-7890 |
| SSN | `000-00-0000` | 123-45-6789 |

## ⚡ Pro Tips

1. **Test Templates First** - Use templates as starting points, then modify
2. **Validate Before Applying** - Click "Validate Syntax" for Python/Regex
3. **Chain Operations** - Combine Find/Replace + Transforms + Advanced
4. **Use Defaults** - Always set default value for empty sources
5. **Reference Other Columns** - In Python, use `col['OtherColumn']`
6. **Handle Null Values** - In Python, check `if value:` before operations
7. **Preview in Advanced** - Python templates show exact structure
8. **Preset First** - Use format presets before custom codes
9. **Document Complex Logic** - Add docstrings to Python functions
10. **Test with Sample Data** - Mentally run through your transformation logic

## 🚀 Workflow Template

```
Column Setup Workflow:
  1. Select column in table
  2. Type & Format tab → Set type + format
  3. Find & Replace tab → Add cleanup rules (optional)
  4. Transforms tab → Add standard operations (optional)
  5. Advanced tab → Add custom logic (optional)
  6. Click [Apply to Selected Column]
  7. Repeat for next column
  8. Click Export to apply to all data
```

## ❌ Common Mistakes

| ❌ Wrong | ✅ Right | Issue |
|---------|--------|-------|
| Forget to click Apply | Click Apply button | Changes saved only when applied |
| Using $ in Find field | Use `\$` for literal $ | Special chars need escaping |
| Python syntax `if x =` | Python syntax `if x ==` | Wrong operators cause errors |
| Format code with spaces | Format code no spaces | Extra spaces break Excel |
| Accessing non-existent column | Check available columns | KeyError in Python |
| No default value | Set a default | Empty results on missing data |

## 📖 Full Documentation

- **[COLUMN_DETAILS_GUIDE.md](COLUMN_DETAILS_GUIDE.md)** - Complete manual with 25+ examples
- **[COLUMN_DETAILS_VISUAL_GUIDE.md](COLUMN_DETAILS_VISUAL_GUIDE.md)** - UI layouts and workflows
- **[FEATURE_DELIVERY_SUMMARY.md](FEATURE_DELIVERY_SUMMARY.md)** - What's new and metrics

---

**In a nutshell:** 
💼 Professional Excel formatting + 🔧 Find & Replace + 🎛️ Built-in transforms + 🐍 Custom Python/Regex = Powerful data transformation in 5 organized tabs