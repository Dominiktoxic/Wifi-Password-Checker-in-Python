import subprocess
import qrcode

def get_wifi_password(profile_name):
    try:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', profile_name, 'key=clear']).decode('utf-8').split('\n')
        results = [b.split(":")[1][1:-1] for b in results if "Key Content" in b]
        if results:
            return results[0]
        else:
            return "Password not found for this profile."
    except subprocess.CalledProcessError:
        return "Profile not found or error occurred."

if __name__ == "__main__":
    command = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8').split('\n')
    profiles = [i.split(":")[1][1:-1] for i in command if "All User Profile" in i]

    print("Available Wi-Fi profiles:")
    for i, profile in enumerate(profiles, 1):
        password = get_wifi_password(profile)
        print(f"{i}. {profile} - Password: {password}")

    try:
        selection = int(input("Enter the number of the profile you want to create a QrCode for: ")) - 1
        selected_profile = profiles[selection]

        password = get_wifi_password(selected_profile)
        img = qrcode.make(password)
        img.save(f"{selected_profile}.png")
    except (IndexError, ValueError):
        print("Invalid selection.")