import argparse
import subprocess
import sys

def is_rclone_configured():
    """Check if rclone has a configured remote for Google Drive."""
    try:
        result = subprocess.run(['rclone', 'listremotes'], capture_output=True, text=True, check=True)
        return 'gdrive:' in result.stdout
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def configure_rclone():
    """Guides the user to configure rclone."""
    print("rclone is not configured for Google Drive.")
    print("Please follow the steps to configure it.")
    try:
        subprocess.run(['rclone', 'config'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during rclone configuration: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("rclone command not found. Please install rclone.", file=sys.stderr)
        sys.exit(1)

def sync_one_way(local_path, remote_path):
    """Synchronizes files from local to remote."""
    print(f"Starting one-way sync from '{local_path}' to 'gdrive:{remote_path}'...")
    try:
        subprocess.run(['rclone', 'sync', local_path, f'gdrive:{remote_path}', '--progress'], check=True)
        print("One-way sync completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during one-way sync: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("rclone command not found. Please install rclone.", file=sys.stderr)

def sync_two_way(local_path, remote_path):
    """Synchronizes files between local and remote."""
    print(f"Starting two-way sync between '{local_path}' and 'gdrive:{remote_path}'...")
    try:
        subprocess.run(['rclone', 'bisync', local_path, f'gdrive:{remote_path}', '--progress'], check=True)
        print("Two-way sync completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error during two-way sync: {e}", file=sys.stderr)
    except FileNotFoundError:
        print("rclone command not found. Please install rclone.", file=sys.stderr)

def main():
    """Main function to handle command-line arguments."""
    parser = argparse.ArgumentParser(description="Synchronize files between a local directory and Google Drive using rclone.")
    parser.add_argument('sync_type', choices=['one-way', 'two-way'], help="The type of synchronization.")
    parser.add_argument('local_path', help="The local directory path.")
    parser.add_argument('remote_path', help="The remote Google Drive path (e.g., 'backup/folder').")

    args = parser.parse_args()

    if not is_rclone_configured():
        configure_rclone()
        if not is_rclone_configured():
            print("rclone configuration for Google Drive not completed. Exiting.", file=sys.stderr)
            sys.exit(1)

    if args.sync_type == 'one-way':
        sync_one_way(args.local_path, args.remote_path)
    elif args.sync_type == 'two-way':
        sync_two_way(args.local_path, args.remote_path)

if __name__ == "__main__":
    main()


