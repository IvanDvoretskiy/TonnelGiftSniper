```markdown
# Common Issues

## Authentication Errors
- Symptom: 403 Forbidden responses
- Solutions:
  1. Verify AUTH_DATA is current
  2. Check SECRET_KEY matches Tonnel's current version

## Purchase Failures
- Symptom: Transactions failing after 3 attempts
- Action: Check:
  - Available balance
  - Price hasn't changed
  - Item still available
```