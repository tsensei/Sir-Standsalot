# Docker Deployment

Deploy the bot using Docker or Docker Compose.

## Quick Start

```bash
# 1. Configure
cp .env.example .env
nano .env  # Add your Discord token and channel IDs

# 2. Run
docker-compose up -d

# 3. View logs
docker-compose logs -f
```

## Docker Compose (Recommended)

### Basic Usage

```bash
# Start bot
docker-compose up -d

# View logs
docker-compose logs -f
docker-compose logs --tail 100

# Restart bot
docker-compose restart

# Stop bot
docker-compose down

# Update and restart
docker-compose pull
docker-compose up -d
```

### Configuration

The `docker-compose.yml` file:
- Reads environment from `.env` file
- Mounts `./data` directory for persistence
- Auto-restarts on failure
- Includes health checks

## Using Docker Directly

### Pull from Docker Hub

```bash
docker pull <username>/discord-standup-bot:latest
```

### Run Container

```bash
docker run -d \
  --name discord-standup-bot \
  --restart unless-stopped \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  <username>/discord-standup-bot:latest
```

### Basic Commands

```bash
# View logs
docker logs -f discord-standup-bot

# Restart
docker restart discord-standup-bot

# Stop
docker stop discord-standup-bot

# Remove
docker rm discord-standup-bot

# Update
docker pull <username>/discord-standup-bot:latest
docker stop discord-standup-bot
docker rm discord-standup-bot
# Then run again with docker run command above
```

## Building Locally

```bash
# Build
docker build -t discord-standup-bot .

# Run
docker run -d \
  --name discord-standup-bot \
  --env-file .env \
  -v $(pwd)/data:/app/data \
  discord-standup-bot
```

## Data Persistence

Attendance records are saved in `./data/` directory:

```bash
# View records
ls -la data/
cat data/attendance_2025_10.json

# Backup
tar -czf backup.tar.gz data/

# Restore
tar -xzf backup.tar.gz
```

The volume mount ensures data persists across container restarts.

## CI/CD with GitHub Actions

### Setup

1. **Create Docker Hub Access Token**
   - Docker Hub → Settings → Security
   - Generate new token with Read & Write permissions

2. **Add GitHub Secrets**
   - Repository → Settings → Secrets → Actions
   - Add `DOCKERHUB_USERNAME` (your Docker Hub username)
   - Add `DOCKERHUB_TOKEN` (the token from step 1)

### Automatic Builds

The bot includes GitHub Actions workflow that builds on:
- Push to `main` branch → tagged as `latest`
- Push tags like `v1.0.0` → tagged as `1.0.0`, `1.0`, `1`, `latest`

### Create Release

```bash
git tag v1.0.0
git push origin v1.0.0
```

This automatically builds and pushes to Docker Hub.

## Cloud Deployment

### Railway

```bash
railway login
railway init
railway up
```

Add environment variables in Railway dashboard.

### Render

1. New Web Service
2. Connect GitHub repository
3. Environment: Docker
4. Add environment variables from `.env.example`

### DigitalOcean

```bash
# SSH to droplet
ssh root@your-droplet-ip

# Install Docker and Docker Compose
curl -fsSL https://get.docker.com | sh
apt install docker-compose

# Clone and run
git clone <repo>
cd discord_attendance_bot
cp .env.example .env
nano .env
docker-compose up -d
```

### AWS ECS/Fargate

1. Push image to ECR or use Docker Hub
2. Create task definition with environment variables
3. Create service
4. Attach EFS volume for `/app/data`

## Monitoring

### Health Check

```bash
# Status
docker ps | grep standup-bot

# Health details
docker inspect discord-standup-bot | grep -A 10 Health

# Resource usage
docker stats discord-standup-bot
```

### Logs

```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail 100

# Since 1 hour ago
docker-compose logs --since 1h

# Specific timeframe
docker-compose logs --since 2025-10-08T10:00:00
```

## Troubleshooting

### Container keeps restarting

Check logs:
```bash
docker-compose logs --tail 50
```

Common causes:
- Invalid Discord token
- Missing required environment variables
- Bot doesn't have channel permissions

### Can't connect to Discord

- Verify `DISCORD_TOKEN` is correct
- Check network connectivity
- Ensure Discord API isn't rate-limiting

### Permission denied errors

```bash
# Fix data directory permissions
sudo chown -R $(id -u):$(id -g) data/
```

### Port conflicts

Bot doesn't expose any ports by default, so this shouldn't occur.
If customizing, check for conflicts:
```bash
docker ps
```

### Out of memory

Increase container memory limit in `docker-compose.yml`:
```yaml
deploy:
  resources:
    limits:
      memory: 512M  # Increase from 256M
```

## Security

### Best Practices

1. **Never commit `.env`** - Already in `.gitignore`
2. **Use Docker secrets** for production
3. **Keep images updated**
4. **Scan for vulnerabilities:**
   ```bash
   docker scan discord-standup-bot
   ```

### Using Docker Secrets

For production, use Docker secrets instead of `.env`:

```yaml
# docker-compose.yml
services:
  standup-bot:
    secrets:
      - discord_token
    environment:
      DISCORD_TOKEN_FILE: /run/secrets/discord_token

secrets:
  discord_token:
    file: ./secrets/discord_token.txt
```

## Resource Limits

Default limits in `docker-compose.yml`:
- **CPU:** 0.25-0.5 cores
- **Memory:** 128-256 MB

Adjust based on team size:

```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 512M
    reservations:
      cpus: '0.5'
      memory: 256M
```

## Multi-Platform Builds

The GitHub Actions workflow builds for:
- `linux/amd64` (x86_64)
- `linux/arm64` (ARM, Apple Silicon, Raspberry Pi)

Works on most hardware without changes.
