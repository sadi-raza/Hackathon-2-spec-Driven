---
name: error-graceful-handler
description: Handles all errors in chatbot flow with graceful responses
---

You manage failures gracefully throughout the chatbot flow.

## Core Principle

**Log internals, show friendly messages.** Users never see stack traces or technical details.

## Error Categories

### 1. Resource Errors (4xx)

| Error | Internal Code | User Message (EN) | User Message (UR) |
|-------|---------------|-------------------|-------------------|
| Task not found | `TASK_NOT_FOUND` | Sorry, that task doesn't exist. | معذرت، یہ ٹاسک موجود نہیں۔ |
| Conversation not found | `CONV_NOT_FOUND` | Conversation not found. Starting fresh. | بات چیت نہیں ملی۔ نئی شروع کرتے ہیں۔ |
| Not authorized | `UNAUTHORIZED` | Please log in again to continue. | جاری رکھنے کے لیے دوبارہ لاگ ان کریں۔ |
| Forbidden | `FORBIDDEN` | You don't have access to this task. | آپ کو اس ٹاسک تک رسائی نہیں۔ |

### 2. Validation Errors (400)

| Error | Internal Code | User Message (EN) | User Message (UR) |
|-------|---------------|-------------------|-------------------|
| Missing title | `MISSING_TITLE` | Please provide a task title. | براہ کرم ٹاسک کا عنوان دیں۔ |
| Invalid task ID | `INVALID_ID` | Please provide a valid task ID. | براہ کرم درست ٹاسک آئی ڈی دیں۔ |
| Empty input | `EMPTY_INPUT` | I didn't catch that. What would you like to do? | سمجھ نہیں آیا۔ آپ کیا کرنا چاہتے ہیں؟ |
| Invalid status | `INVALID_STATUS` | Status must be 'pending' or 'completed'. | حیثیت 'زیر التواء' یا 'مکمل' ہونی چاہیے۔ |

### 3. System Errors (5xx)

| Error | Internal Code | User Message (EN) | User Message (UR) |
|-------|---------------|-------------------|-------------------|
| Database error | `DB_ERROR` | Temporary issue – please try again. | عارضی مسئلہ – دوبارہ کوشش کریں۔ |
| Network error | `NETWORK_ERROR` | Connection issue – please try again. | کنکشن مسئلہ – دوبارہ کوشش کریں۔ |
| Timeout | `TIMEOUT` | Request timed out – please try again. | درخواست ٹائم آؤٹ – دوبارہ کوشش کریں۔ |
| Unknown error | `UNKNOWN` | Something went wrong. Please try again. | کچھ غلط ہو گیا۔ دوبارہ کوشش کریں۔ |

### 4. Agent/Tool Errors

| Error | Internal Code | User Message (EN) | User Message (UR) |
|-------|---------------|-------------------|-------------------|
| Tool not found | `TOOL_NOT_FOUND` | I can't do that action right now. | میں یہ عمل ابھی نہیں کر سکتا۔ |
| Tool failed | `TOOL_FAILED` | Action failed – please try again. | عمل ناکام – دوبارہ کوشش کریں۔ |
| Intent unclear | `UNKNOWN_INTENT` | I didn't understand. Try: add, list, complete, or delete task. | سمجھ نہیں آیا۔ کوشش کریں: ٹاسک شامل، فہرست، مکمل، یا حذف۔ |

## Error Handler Function

```python
def handle_error(
    error: Exception | dict,
    is_urdu: bool = False,
    context: dict = None
) -> dict:
    """
    Handle any error and return user-friendly response.

    Returns:
        {
            "success": False,
            "message": "User-friendly message",
            "retry": True/False,
            "suggestion": "Try this instead..."
        }
    """

    # 1. Log full error internally
    log_error(error, context)

    # 2. Map to error code
    code = map_to_error_code(error)

    # 3. Get user message
    message = get_user_message(code, is_urdu)

    # 4. Determine if retryable
    retry = is_retryable(code)

    # 5. Get suggestion
    suggestion = get_suggestion(code, is_urdu)

    return {
        "success": False,
        "message": message,
        "retry": retry,
        "suggestion": suggestion
    }
```

## Retry Logic

### Retryable Errors
- `DB_ERROR` - Retry after 1s
- `NETWORK_ERROR` - Retry after 2s
- `TIMEOUT` - Retry after 3s

### Non-Retryable Errors
- `TASK_NOT_FOUND` - User must correct input
- `UNAUTHORIZED` - User must re-authenticate
- `INVALID_ID` - User must correct input
- `FORBIDDEN` - Access denied permanently

## Suggestions by Error

| Error Code | Suggestion (EN) | Suggestion (UR) |
|------------|-----------------|-----------------|
| `TASK_NOT_FOUND` | Try listing your tasks first. | پہلے اپنے ٹاسک دیکھیں۔ |
| `INVALID_ID` | Use a number like: complete task 5 | نمبر استعمال کریں: ٹاسک 5 مکمل کرو |
| `EMPTY_INPUT` | Try: "add task buy milk" | کوشش کریں: "ٹاسک شامل کرو دودھ خریدو" |
| `UNKNOWN_INTENT` | Say: add, list, complete, or delete | کہیں: شامل، فہرست، مکمل، یا حذف |
| `UNAUTHORIZED` | Click here to log in again. | دوبارہ لاگ ان کریں۔ |

## Logging Format

```python
def log_error(error: Exception, context: dict):
    """Log error with full details for debugging."""
    log.error({
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "message": str(error),
        "stack_trace": traceback.format_exc(),
        "context": {
            "user_id": context.get("user_id"),
            "conversation_id": context.get("conversation_id"),
            "intent": context.get("intent"),
            "input": context.get("raw_input")
        }
    })
```

## Response Format

```json
{
  "success": false,
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Sorry, that task doesn't exist.",
    "retry": false,
    "suggestion": "Try listing your tasks first."
  },
  "language": "en"
}
```

## Integration Points

- **natural-language-parser**: Provides `is_urdu` flag
- **mcp-tool-craft**: Catches tool execution errors
- **conversation-state-manager**: Stores error responses in history
- **confirmation-responder**: Formats final error message
