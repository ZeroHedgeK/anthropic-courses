# Fix Plan for custom_llm_eval.py Type Errors

## Problem Analysis

### Issues Identified

The code has **10 Pylance type errors** and **2 cSpell warnings**:

#### Type Errors (Lines 125 & 130)

- **Root Cause**: Accessing `.text` attribute on `response.content[0]` without type checking
- **Impact**: Pylance detects that `response.content[0]` could be any of these block types:
  - `TextBlock` ✅ (has `.text` attribute)
  - `ThinkingBlock` ❌ (no `.text` attribute)
  - `RedactedThinkingBlock` ❌ (no `.text` attribute)
  - `ToolUseBlock` ❌ (no `.text` attribute)
  - `ServerToolUseBlock` ❌ (no `.text` attribute)
  - `WebSearchToolResultBlock` ❌ (no `.text` attribute)

#### Spelling Warnings

- Line 23: "overexplain" - Valid technical term in context
- Line 66: "backpropagation" - Standard ML/AI terminology

## Solution Architecture

### 1. Type Safety Implementation

```python
from anthropic.types import TextBlock

# Current problematic code (lines 125, 130):
evaluation = json.loads(response.content[0].text)
return avg_score, response.content[0].text

# Fixed approach with type checking:
content_block = response.content[0]
if isinstance(content_block, TextBlock):
    evaluation = json.loads(content_block.text)
    # ... rest of the logic
else:
    raise TypeError(f"Expected TextBlock, got {type(content_block).__name__}")
```

### 2. Error Handling Strategy

**Defensive Programming Approach:**

- Check block type before accessing `.text`
- Provide clear error messages if unexpected block type is encountered
- Handle edge cases gracefully

**Expected Behavior:**
Given the API call configuration:

- Using `stop_sequences=["</json>"]`
- Prefilling with `{"role": "assistant", "content": "<json>"}`
- We expect a `TextBlock` containing JSON

**Fallback Strategy:**
If a non-TextBlock is returned (edge case), raise an informative error rather than failing silently.

### 3. Code Quality Improvements

**cSpell Suppression:**
Add inline comments to suppress false-positive spell warnings:

```python
# cspell:ignore overexplain backpropagation
```

## Implementation Steps

1. ✅ **Review Code Structure**

   - Identified both locations where `.text` is accessed (lines 125, 130)
   - Confirmed they both access `response.content[0].text`

2. **Add Type Import**

   - Import `TextBlock` from `anthropic.types`
   - This provides proper type hints for isinstance checks

3. **Implement Type Checking**

   - Extract `response.content[0]` to a variable
   - Use `isinstance(content_block, TextBlock)` to verify type
   - Access `.text` only after type verification

4. **Add Error Handling**

   - Raise `TypeError` with descriptive message if block is not TextBlock
   - This helps debugging if API behavior changes

5. **Suppress Spelling Warnings**

   - Add cSpell ignore directive near affected lines
   - Preserves legitimate technical terminology

6. **Validation**
   - Ensure all Pylance errors are resolved
   - Verify code still functions correctly
   - Check that error messages are informative

## Technical Considerations

### Why This Issue Occurs

The Anthropic Python SDK uses a union type for message content blocks to support various response types (text, tool calls, thinking blocks, etc.). Pylance's static type checker correctly identifies that without runtime type checking, accessing `.text` could fail.

### Why This Solution Works

1. **Type Narrowing**: `isinstance()` check narrows the type from `Union[TextBlock, ThinkingBlock, ...]` to just `TextBlock`
2. **Runtime Safety**: Prevents AttributeError if API returns unexpected block type
3. **Type Checker Satisfaction**: Pylance can verify `.text` exists after isinstance check
4. **Maintainability**: Clear, explicit type checking improves code readability

### Alternative Approaches (Not Recommended)

❌ **Type Casting**: `cast(TextBlock, response.content[0])` - Bypasses runtime check
❌ **Type Ignore**: `# type: ignore` - Hides the issue without fixing it
❌ **Attribute Access**: `getattr(response.content[0], 'text', None)` - Less explicit

## Expected Outcome

After implementation:

- ✅ All 10 Pylance type errors resolved
- ✅ 2 cSpell warnings suppressed appropriately
- ✅ Code is more robust with proper error handling
- ✅ Better developer experience with clear type checking

## Testing Strategy

1. **Positive Case**: Normal execution with TextBlock response
2. **Type Checking**: Verify isinstance check works correctly
3. **Error Message**: If edge case occurs, error message is informative

## Files to Modify

- [`custom_llm_eval.py`](./custom_llm_eval.py) - Main implementation file

## References

- [Anthropic Python SDK Documentation](https://github.com/anthropics/anthropic-sdk-python)
- [Python isinstance() Documentation](https://docs.python.org/3/library/functions.html#isinstance)
- [Type Narrowing in Python](https://peps.python.org/pep-0647/)
