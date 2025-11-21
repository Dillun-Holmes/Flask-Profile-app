# Render Start Command Configuration

## Current Start Command

```
gunicorn run:app --workers 1 --worker-class sync --max-requests 1000 --max-requests-jitter 50 --timeout 30
```

## What Each Part Does

### `gunicorn run:app`
- **gunicorn** - Production WSGI HTTP Server (required for Render)
- **run:app** - Runs the Flask app from `run.py` module

### Performance Flags

- **`--workers 1`**
  - Single worker process (optimal for free tier with 0.5GB RAM)
  - More workers = higher memory usage
  - Paid tiers can use `--workers 2-4`

- **`--worker-class sync`**
  - Synchronous worker (standard for Flask)
  - Best for I/O-bound applications like web servers
  - Alternative: `gevent` for high concurrency (requires `gevent` package)

- **`--max-requests 1000`**
  - Recycles worker after 1000 requests
  - Prevents memory leaks over time
  - Prevents stale database connections

- **`--max-requests-jitter 50`**
  - Randomizes max-requests by ±50 requests
  - Prevents all workers from recycling simultaneously
  - Ensures high availability during restarts

- **`--timeout 30`**
  - Kills worker if no response after 30 seconds
  - Prevents hanging requests from blocking app
  - Set based on longest expected response time

## For Different Scenarios

### Free Tier (Current)
```
gunicorn run:app --workers 1 --worker-class sync --max-requests 1000 --timeout 30
```
✅ Use this (already configured)

### Production (Paid Tier)
```
gunicorn run:app --workers 4 --worker-class sync --max-requests 1000 --timeout 60 --access-logfile - --error-logfile -
```

### High Concurrency (Paid Tier with gevent)
First, add to `requirements.txt`:
```
gevent>=22.0
gevent-websocket>=0.10.1
```

Then use:
```
gunicorn run:app --workers 1 --worker-class gevent --worker-connections 1000 --timeout 30
```

### Development (Local)
Use Flask development server instead:
```
python run.py
```

## Why Gunicorn?

1. **Production-Ready** - Handles concurrent requests properly
2. **Auto-Reloading** - Can reload on code changes (with `--reload` flag)
3. **Multiple Workers** - Scale up request handling
4. **Stable** - Industry standard for Python web apps
5. **Compatible** - Works with all WSGI frameworks (Flask, Django, etc.)

## Render Automatically Uses

- `render.yaml` for start command (checked first)
- `Procfile` as fallback (if no render.yaml)
- Environment variables configured in dashboard

## Troubleshooting

### "Worker timeout" errors
→ Increase `--timeout` value (current: 30s)
→ Check if request processing is slow

### High memory usage
→ Reduce `--workers` (try `--workers 1`)
→ Check for memory leaks in code

### Requests not responding
→ Check `max-requests` - may be too low
→ Verify database connections pool

### App restarts frequently
→ Increase `--max-requests` value
→ Check logs for crash reasons

## Monitoring

In Render Dashboard:
1. Go to **Logs** tab
2. Look for gunicorn startup messages
3. Monitor for timeout errors or restarts
4. Check CPU and memory usage

## Manual Override in Render Dashboard

If needed, override the start command in Render:
1. Go to **Settings**
2. Find **Start Command**
3. Paste your custom command
4. Click **Save**
5. Service redeploys automatically

---

**Current Status:** ✅ Optimized for free tier  
**Next Step:** Deploy to Render to activate
