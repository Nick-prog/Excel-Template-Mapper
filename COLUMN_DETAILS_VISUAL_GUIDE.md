# Column Details Widget - Visual Structure

## UI Layout

```
┌─────────────────────────────────────────────────────────┐
│            Selected Column Details                       │
├─────────────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Basic Information                                   │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │ Target Column:        [example_column]              │ │
│ │ Source Column:        [source_column]               │ │
│ │ Default Value:        [______________________]       │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ [Type & Format] [Find & Replace] [Transforms]...   │ │
│ ├─────────────────────────────────────────────────────┤ │
│ │                                                     │ │
│ │ Type & Format TAB:                                  │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ Data Type: [General ▼]                         │ │ │
│ │ │                                                 │ │ │
│ │ │ Format Template:                                │ │ │
│ │ │   [None (Default) ▼]  [Insert Template]        │ │ │
│ │ │                                                 │ │ │
│ │ │ Custom Excel Format Code:                       │ │ │
│ │ │   [Format code (e.g., #,##0.00) ________]      │ │ │
│ │ │                                                 │ │ │
│ │ │ Examples: 0.00, $#,##0.00, mm/dd/yyyy...      │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                     │ │
│ │ Find & Replace TAB:                                 │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ Find          │ Replace With      │ Remove      │ │ │
│ │ ├───────────────┼───────────────────┼─────────────┤ │ │
│ │ │ old           │ new               │ [Delete]    │ │ │
│ │ │ NA            │ (empty)           │ [Delete]    │ │ │
│ │ │ ---           │ _                 │ [Delete]    │ │ │
│ │ ├───────────────┴───────────────────┴─────────────┤ │ │
│ │ │ [Add Rule]                                      │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                     │ │
│ │ Transforms TAB:                                     │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ Selected: [trim] [upper] [title]                │ │ │
│ │ │ [Add Transform ▼]                               │ │ │
│ │ │                                                 │ │ │
│ │ │ Available: trim, upper, lower, title,           │ │ │
│ │ │            to_string, to_int, to_float,         │ │ │
│ │ │            date_to_iso, digits_only             │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                     │ │
│ │ Advanced TAB:                                       │ │
│ │ ┌─────────────────────────────────────────────────┐ │ │
│ │ │ Format Type: [Python Function ▼]                │ │ │
│ │ │                                                 │ │ │
│ │ │ Code Templates:                                 │ │ │
│ │ │   [Python: If/Else Logic ▼]  [Insert Template] │ │ │
│ │ │                                                 │ │ │
│ │ │ ┌─────────────────────────────────────────────┐ │ │
│ │ │ │ def format_column(col, source):             │ │ │
│ │ │ │     if source['Column'] == 'Value':         │ │ │
│ │ │ │         return 'MappedValue'                 │ │ │
│ │ │ │     else:                                   │ │ │
│ │ │ │         return source['Column']             │ │ │
│ │ │ └─────────────────────────────────────────────┘ │ │
│ │ │                                                 │ │
│ │ │ [Validate Syntax]                               │ │ │
│ │ │                                                 │ │ │
│ │ │ Tips: Access source with source['Name']         │ │ │
│ │ │       Access target with col['Name']            │ │ │
│ │ │       Return the transformed value              │ │ │
│ │ └─────────────────────────────────────────────────┘ │ │
│ │                                                     │ │
│ └─────────────────────────────────────────────────────┘ │
│                                                         │
│ ┌─────────────────────────────────────────────────────┐ │
│ │           [Apply to Selected Column]                │ │
│ └─────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Tab Navigation

```
┌────────────────┬──────────────────┬────────────┬──────────┬──────────┐
│ Type & Format  │ Find & Replace   │ Transforms │ Advanced │ (scroll) │
└────────────────┴──────────────────┴────────────┴──────────┴──────────┘
         │                │              │            │
         └────────────────┴──────────────┴────────────┘
              Organized by operation type
```

## Data Flow

```
Source Data
    │
    ├─→ [Basic Info] → Set Target Column, Source Column, Default Value
    │
    ├─→ [Find & Replace] → Apply multiple find/replace patterns
    │       (Pattern 1: old → new)
    │       (Pattern 2: NA → empty)
    │
    ├─→ [Transforms] → Apply built-in operations
    │       (1. trim) → (2. upper) → (3. title)
    │
    ├─→ [Type & Format] → Apply data type and formatting
    │       Set to: Currency → Format: $#,##0.00
    │
    ├─→ [Advanced] → Custom Python/Excel/Regex logic
    │       if col['Status'] == 'VIP': return value.upper()
    │
    └─→ Excel Output
         (Properly formatted and transformed)
```

## Feature Comparison

### Type & Format Tab
```
Before:                          After:
┌──────────────────┐            ┌──────────────────┐
│ Type: [general]  │            │ Type: [General] │
│ Format: [______] │            │                  │
└──────────────────┘            │ Format Template: │
                                │ [None         ▼]│
                                │ [Currency     ▼]│ ← Preset
                                │ [Date         ▼]│   templates
                                │ ...              │
                                │                  │
                                │ Custom Code:     │
                                │ [$#,##0.00___] ← Direct input
                                │                  │
                                │ Examples shown ← Help text
                                └──────────────────┘
```

### Find & Replace Tab
```
Before: N/A (Not available)

After:
┌─────────────────────────────────────────┐
│ Find        │ Replace With  │ Remove   │
├─────────────┼───────────────┼──────────┤
│ pattern     │ replacement   │ [Delete] │
├─────────────┼───────────────┼──────────┤
│             │               │ [Delete] │
├─────────────┼───────────────┼──────────┤
│ [Add Rule]                             │
└─────────────────────────────────────────┘
```

### Advanced Tab
```
Before:                          After:
┌────────────────────┐          ┌──────────────────────┐
│ Format Type: N/A   │          │ Format Type:         │
│                    │          │ [Python      ▼]      │
│ Limited snippets   │          │ [Excel       ▼]      │
│ (4 options)        │          │ [Regex       ▼]      │
│                    │          │                      │
│ [Code editor]      │          │ Code Templates:      │
│                    │          │ [12 templates ▼] ← Many more!
│ [Validate]         │          │                      │
│                    │          │ [Code editor]        │
│                    │          │                      │
│                    │          │ [Validate Syntax] ← Smart validation
│                    │          │                      │
│                    │          │ Tips & examples ← Better guidance
│                    │          │                      │
│                    │          │ Format-aware validation
│                    │          │ (Python/Excel/Regex)
│                    │          │                      │
└────────────────────┘          └──────────────────────┘
```

## Workflow Example: Transform Phone Numbers

```
Step 1: Type & Format
  Data Type: Text
  Format Template: Phone (USA) → 000-00-0000

Step 2: Find & Replace
  Rule 1: Find [^\d] → Replace "" (removes non-digits)
  Rule 2: Find (\d{3})(\d{3})(\d{4}) → Replace ($1) $2-$3

Step 3: Transforms
  Apply: digits_only → trim

Step 4: Advanced
  Format Type: Excel Formula
  Code: =TEXT(VALUE(A1),"[<=9999999]###-####;(###) ###-####")

Result: 1234567890 → (123) 456-7890 ✓
```

## Color & Visual Hierarchy

```
┌─────────────────────────────────────────┐
│ ▲ Section Header (Bold)                 │  
├─────────────────────────────────────────┤
│ Label: [Input/Selector]                 │
│ Label: [Input/Selector]                 │
│                                         │
│ [Tab 1] [Tab 2] [Tab 3] [Tab 4] [Tab 5] │  ← Tab navigation
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │ Tab Content Area                    │ │
│ │ (Specific to selected tab)          │ │
│ └─────────────────────────────────────┘ │
│                                         │
│ ┌─────────────────────────────────────┐ │
│ │   [Apply to Selected Column] ▶      │ │  ← Primary action
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Keyboard Shortcuts (Potential Future Additions)

```
Tab Editor:
  Tab       → Indent (4 spaces)
  Enter     → New line with auto-indent
  Ctrl+K    → Validate (quick check)

Find & Replace Table:
  Insert   → Add new row
  Delete   → Remove selected row
  Ctrl+V   → Paste patterns

Format Presets:
  Alt+1    → None
  Alt+2    → Currency
  Alt+3    → Date
  (etc.)
```

---

This visual structure makes it clear that every feature is discoverable, organized, and serves a specific purpose in the data transformation pipeline.