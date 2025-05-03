import subprocess

def run_command(command):
    """Run a shell command and print its output."""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=True)
    return result.returncode == 0

def main():
    print("Truncating food_trucks table...")
    truncate_cmd = 'docker compose exec db psql -U foodtruck -d foodtruck -c "TRUNCATE TABLE food_trucks CASCADE;"'
    if not run_command(truncate_cmd):
        print("Error truncating table")
        return
    
    print("Table truncated successfully!")

if __name__ == "__main__":
    main()

