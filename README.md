# Relouderul

A Python-based hot-reloader utility that watches for file changes and automatically restarts services.

## Requirements

- Python 3.13+
- [uv](https://github.com/astral-sh/uv)

Install dependencies with uv:
```bash
uv sync
```

## Configuration

1. Create a `.env` file with:
   ```
   DIAGNOSTIC_PATH=/path/to/your/project
   ```

2. Edit `services.json` to configure your services:
   ```json
   {
     "service_name": {
       "name": "Service Display Name",
       "command": ["python", "main.py"],
       "watch_path": "src"
     }
   }
   ```

## Usage

```bash
python main.py --service <service_name>
```

The reloader will:
- Start the specified service
- Watch for changes in the configured watch path
- Automatically restart the service when `.py` files change

## Project Structure

- `main.py` - Main reloader implementation
- `services.json` - Service configuration
- `.env` - Environment variables