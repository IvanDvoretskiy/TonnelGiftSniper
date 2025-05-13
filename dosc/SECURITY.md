```markdown
# Security Practices

## Data Handling
- AUTH_DATA should never be shared
- All requests use HTTPS
- Proxy credentials encrypted in transit

## Rate Limiting
- Built-in 1-second delay between requests
- Randomized delay variance (0.5-1.5s)
- Automatic retry with exponential backoff
```