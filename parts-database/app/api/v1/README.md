# Universal Parts Database API v1

RESTful API for programmatic access to the parts database.

## Base URL

```
https://your-domain.com/api/v1
```

## Endpoints

### Parts

#### GET /api/v1/parts
List and search parts

**Query Parameters:**
- `category` - Filter by category (e.g., "fastener")
- `manufacturer` - Filter by manufacturer
- `thread` - Filter by thread ID (e.g., "M3x0.5")
- `search` - Full-text search across part_number, manufacturer, designation
- `limit` - Results per page (default: 50, max: 100)
- `offset` - Pagination offset (default: 0)

**Example:**
```bash
curl "https://your-domain.com/api/v1/parts?category=fastener&thread=M3x0.5&limit=10"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "part_id": "DIN-912-M3x12",
      "manufacturer": "DIN",
      "part_number": "912-M3x12",
      "category": "fastener",
      "thread_id": "M3x0.5",
      "length": 12,
      "material_grade": "A2-70"
    }
  ],
  "pagination": {
    "total": 150,
    "limit": 10,
    "offset": 0,
    "hasMore": true
  }
}
```

#### GET /api/v1/parts/:id
Get single part by ID

**Example:**
```bash
curl "https://your-domain.com/api/v1/parts/DIN-912-M3x12"
```

#### POST /api/v1/parts
Create new part

**Body:**
```json
{
  "manufacturer": "DIN",
  "part_number": "912-M3x12",
  "category": "fastener",
  "thread_id": "M3x0.5",
  "length": 12,
  "material_grade": "A2-70"
}
```

#### PUT /api/v1/parts/:id
Update part

#### DELETE /api/v1/parts/:id
Delete part

### Batch Operations

#### POST /api/v1/parts/batch
Bulk import parts (up to 1000 at once)

**Body:**
```json
{
  "parts": [
    {
      "manufacturer": "DIN",
      "part_number": "912-M3x12",
      "category": "fastener",
      "thread_id": "M3x0.5",
      "length": 12
    },
    {
      "manufacturer": "DIN",
      "part_number": "912-M4x16",
      "category": "fastener",
      "thread_id": "M4x0.7",
      "length": 16
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "imported": 2,
    "parts": [...]
  }
}
```

### Compatibility

#### POST /api/v1/compatibility
Check if screw fits hole

**Body:**
```json
{
  "screw_thread": "M3x0.5",
  "screw_length": 12,
  "hole_thread": "M3x0.5",
  "material_thickness": 8
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "compatible": true,
    "engagement_length": 8,
    "protrusion": 4,
    "engagement_ratio": 2.67,
    "warnings": [],
    "recommendations": ["Good engagement ratio: 2.7x diameter"]
  }
}
```

## Error Responses

All endpoints return errors in this format:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**HTTP Status Codes:**
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `404` - Not Found
- `500` - Server Error

## Rate Limiting

Currently no rate limiting. Production deployment should add rate limiting middleware.

## Authentication

Currently no authentication required for read operations. Write operations should add authentication in production.

## Examples

### JavaScript/TypeScript
```typescript
// Search parts
const response = await fetch('https://your-domain.com/api/v1/parts?search=M3')
const { data, pagination } = await response.json()

// Create part
await fetch('https://your-domain.com/api/v1/parts', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    manufacturer: 'DIN',
    part_number: '912-M3x12',
    category: 'fastener'
  })
})

// Check compatibility
const compat = await fetch('https://your-domain.com/api/v1/compatibility', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    screw_thread: 'M3x0.5',
    screw_length: 12,
    hole_thread: 'M3x0.5',
    material_thickness: 8
  })
})
const result = await compat.json()
console.log('Compatible:', result.data.compatible)
```

### Python
```python
import requests

# Search parts
response = requests.get('https://your-domain.com/api/v1/parts', params={
    'category': 'fastener',
    'thread': 'M3x0.5'
})
parts = response.json()['data']

# Create part
requests.post('https://your-domain.com/api/v1/parts', json={
    'manufacturer': 'DIN',
    'part_number': '912-M3x12',
    'category': 'fastener'
})

# Batch import
requests.post('https://your-domain.com/api/v1/parts/batch', json={
    'parts': [
        {'manufacturer': 'DIN', 'part_number': '912-M3x12', 'category': 'fastener'},
        {'manufacturer': 'DIN', 'part_number': '912-M4x16', 'category': 'fastener'}
    ]
})
```

### cURL
```bash
# Get parts
curl "https://your-domain.com/api/v1/parts?category=fastener"

# Create part
curl -X POST "https://your-domain.com/api/v1/parts" \
  -H "Content-Type: application/json" \
  -d '{"manufacturer":"DIN","part_number":"912-M3x12","category":"fastener"}'

# Check compatibility
curl -X POST "https://your-domain.com/api/v1/compatibility" \
  -H "Content-Type: application/json" \
  -d '{"screw_thread":"M3x0.5","screw_length":12,"hole_thread":"M3x0.5","material_thickness":8}'
```
