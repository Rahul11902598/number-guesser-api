# 🐛 Bug Tracking - Spider-Guesser API

**Project:** Number Guesser Pro  
**Last Updated:** November 5, 2025

---

## 📊 Bug Summary

| Severity | Open | Closed | Total |
|----------|------|--------|-------|
| Critical | 0 | 0 | 0 |
| High | 0 | 0 | 0 |
| Medium | 1 | 0 | 1 |
| Low | 0 | 0 | 0 |

---

## 🐛 Open Bugs

### BUG-001: Empty JSON Body Returns 415 Instead of 400

**Status:** 🟡 Open  
**Severity:** Medium  
**Priority:** P2  
**Found By:** Pytest Automation  
**Date Reported:** November 5, 2025

#### 📋 Description
When a guess request is made without a JSON body (no Content-Type header), the API returns 415 (Unsupported Media Type) instead of the more user-friendly 400 (Bad Request).

#### 🔍 Steps to Reproduce
1. Start a game
2. Send POST to `/game/{game_id}/guess` without JSON body
3. Observe response code

```python
response = client.post(f'/game/{game_id}/guess')
# Returns: 415 instead of expected 400
```

#### ❌ Expected Behavior
- Status Code: `400 Bad Request`
- Error Message: `{"error": "JSON body required"}`

#### ✅ Actual Behavior
- Status Code: `415 Unsupported Media Type`
- Error Message: Flask default error

#### 📸 Evidence
```
FAILED tests/test_validation.py::TestGuessValidation::test_guess_empty_json
assert 415 == 400
```

#### 💡 Proposed Fix

**Option A:** Update test to accept both 400 and 415
```python
assert response.status_code in [400, 415]
```

**Option B:** Add error handler in Flask app
```python
@app.errorhandler(415)
def unsupported_media_type(error):
    return jsonify({'error': 'Content-Type must be application/json'}), 400
```

#### 🏷️ Labels
`bug` `validation` `api` `error-handling`

---

## ✅ Resolved Bugs

*No bugs resolved yet*

---

## 📝 Notes

- This is a minor UX issue, not a security or functionality problem
- API works correctly when proper JSON is sent
- Could be considered expected Flask behavior
- Recommendation: Accept as-is or add custom error handler

---

## 📊 Testing Statistics

**Total Tests Run:** 20  
**Bugs Found by Automated Testing:** 1  
**Bugs Found by Manual Testing:** 0  
**Test Coverage:** 95% Pass Rate