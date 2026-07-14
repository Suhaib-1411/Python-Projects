import time
from datetime import datetime
from database import load_contacts, load_templates, log_message, view_logs
from automation import WhatsAppAutomation

def schedule_delay(target_time_str):
    """Parses delay until HH:MM time target"""
    try:
        target_time = datetime.strptime(target_time_str, "%H:%M").time()
        now = datetime.now()
        target_datetime = datetime.combine(now.date(), target_time)
        
        if target_datetime < now:
            print("[!] Target time is in the past. Scheduling for tomorrow.")
            from datetime import timedelta
            target_datetime += timedelta(days=1)
            
        delay_seconds = (target_datetime - now).total_seconds()
        print(f"[*] Sleeping for {round(delay_seconds/60, 2)} minutes until {target_time_str}...")
        time.sleep(delay_seconds)
    except ValueError:
        print("[✘] Invalid time format. Please use HH:MM.")

def run_menu():
    bot = None
    while True:
        print("\n" + "═"*15 + " WHATSAPP AUTOMATION " + "═"*15)
        print("1. Send Single Message")
        print("2. Send Bulk Messages (Using Contacts File)")
        print("3. Send Template Messages (Personalized Bulk)")
        print("4. Schedule Message")
        print("5. View Log History")
        print("6. Exit")
        print("═"*51)
        
        choice = input("Select an option (1-6): ").strip()
        
        if choice in ['1', '2', '3', '4']:
            if not bot:
                bot = WhatsAppAutomation()
                bot.open_whatsapp()

        if choice == '1':
            phone = input("Enter Phone Number (with country code, e.g., +123456789): ")
            msg = input("Enter Message Text: ")
            bot.send_message(phone, msg)

        elif choice == '2':
            contacts = load_contacts()
            msg = input("Enter Message Text for all contacts: ")
            print(f"[*] Starting bulk transmission to {len(contacts)} contacts...")
            for contact in contacts:
                bot.send_message(contact['phone'], msg)
                time.sleep(2)

        elif choice == '3':
            contacts = load_contacts()
            templates = load_templates()
            
            print("\nAvailable Templates:")
            for key, val in templates.items():
                print(f" - {key}: '{val}'")
            
            tmpl_name = input("\nEnter chosen template key: ").strip()
            if tmpl_name not in templates:
                print("[✘] Invalid Template Selection.")
                continue
                
            selected_tmpl = templates[tmpl_name]
            print(f"[*] Starting personalized templated campaign to {len(contacts)} users...")
            
            for contact in contacts:
                # Safely replace variables or default to empty values
                personalized_msg = selected_tmpl.format(
                    name=contact.get('name', 'Customer'),
                    course=contact.get('course', 'Selected Program')
                )
                bot.send_message(contact['phone'], personalized_msg)
                time.sleep(2)

        elif choice == '4':
            phone = input("Enter Phone Number: ")
            msg = input("Enter Message Text: ")
            time_str = input("Enter Scheduled Time (HH:MM / 24hr format, e.g., 15:30): ")
            schedule_delay(time_str)
            bot.send_message(phone, msg)

        elif choice == '5':
            view_logs()

        elif choice == '6':
            if bot:
                bot.close()
            print("\n[+] Exiting application. Goodbye!")
            break
        else:
            print("[✘] Invalid selection. Try again.")

if __name__ == "__main__":
    run_menu()