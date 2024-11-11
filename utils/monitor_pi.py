import psutil
import discord
import datetime

def monitor_stats():
    # CPU Temperature
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            cpu_temp = float(f.read()) / 1000
        cpu_temp = f"CPU Temperature: {cpu_temp:.1f}°C"
    except FileNotFoundError:
        cpu_temp = "CPU Temperature not available."

    cpu_freq = psutil.cpu_freq()

    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())

    # CPU Usage
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory Usage
    memory = psutil.virtual_memory()

    # Disk Usage
    disk = psutil.disk_usage('/')

    file = discord.File('images/bot_logo.png', filename='bot_logo.png')

    embed=discord.Embed(title="Bot Stats", color=0x1f9551, timestamp=datetime.datetime.now(datetime.timezone.utc))
    embed.set_thumbnail(url='attachment://bot_logo.png')
    embed.add_field(name="CPU Temperature", value=cpu_temp, inline=False)
    embed.add_field(name="CPU Frequency", value=f"{cpu_freq.current:.2f} MHz (Min: {cpu_freq.min:.2f} MHz, Max: {cpu_freq.max:.2f} MHz)", inline=False)
    embed.add_field(name="System Uptime", value=uptime, inline=False)
    embed.add_field(name="CPU Usage", value=f"{cpu_usage}%", inline=False)
    embed.add_field(name="Memory Usage", value=f"{memory.percent}% ({memory.used / (1024**2):.1f} MB used of {memory.total / (1024**2):.1f} MB)", inline=False)
    embed.add_field(name="Disk Usage", value=f"{disk.percent}% ({disk.used / (1024**3):.2f} GB used of {disk.total / (1024**3):.2f} GB)", inline=False)
    
    return file, embed