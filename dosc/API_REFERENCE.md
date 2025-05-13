```markdown
# Tonnel API Reference

## Authenticated Endpoints

### `GET /pageGifts`
- **Purpose**: Retrieve gift sale history
- **Parameters**:
  - `filter`: JSON string with query filters
  - `sort`: Sorting criteria
  - `page`: Pagination number
  - `limit`: Items per page

### `POST /giftFloor` 
- **Purpose**: Get current floor price
- **Required Fields**:
  - `gift_name`: Exact gift name
  - `asset`: Currency (TON)

### `POST /buyGift/{id}`
- **Security**: Requires WTF token
- **Fields**:
  - `price`: Exact purchase price
  - `timestamp`: Current UNIX time
  - `wtf`: Generated auth token
```