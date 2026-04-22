from openai import OpenAI
import pandas as pd
import time
import os


# =========================
# IA CLIENT
# =========================

class AIClient:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://api.groq.com/openai/v1",
            api_key=os.getenv("GROQ_API_KEY")  # 🔐 nunca deixar key no código
        )

    def chat(self, message: str) -> str:
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": message}]
        )
        return response.choices[0].message.content


# =========================
# HOSPITAL SYSTEM
# =========================

class Hospital:
    def __init__(self, manager: str):
        self.manager = manager
        self.patients = []
        self.running = True

        self.print_header("Hospital System v2.1")
        self.main_menu()




    def print_header(self, text: str):
        print("=" * 50)
        print(f"{text.center(50)}")
        print("=" * 50)




    def main_menu(self):
        options = {
            1: "Register Patients",
            2: "View Patients (WIP)",
            3: "Exit"
        }

        while self.running:
            print("\n--- MENU ---")
            for key, value in options.items():
                print(f"{key}: {value}")

            choice = self.get_choice(options.keys())

            if choice == 1:
                self.register_patients()
            elif choice == 2:
                print("Feature in progress...")
            elif choice == 3:
                print("Exiting system...")
                self.running = False



    def get_choice(self, valid_choices):
        while True:
            try:
                choice = int(input("\nSelect an option: ").strip())
                if choice in valid_choices:
                    return choice
                print("Invalid option. Try again.")
            except ValueError:
                print("Please enter a valid number.")



    def register_patients(self):
        time.sleep(0.5)

        try:
            total = int(input("\nHow many patients to register? ").strip())
        except ValueError:
            print("Invalid number.")
            return

        for i in range(total):
            self.print_header(f"PATIENT {i + 1}")

            patient = {
                "patient_id": len(self.patients) + 1,
                "full_name": input("Full name: ").strip(),
                "age": input("Age: ").strip(),
                "gender": input("Gender (M/F): ").strip().upper(),
                "blood_type": input("Blood type: ").strip().upper(),
                "diagnosis": input("Diagnosis: ").strip(),
                "doctor": input("Doctor: ").strip(),
                "department": input("Department: ").strip(),
                "room_number": input("Room number: ").strip(),
                "status": input("Status: ").strip().capitalize()
            }

            self.patients.append(patient)

        self.save_to_csv()

        again = input("\nAdd more patients? (y/n): ").strip().lower()
        if again == "y":
            self.register_patients()

    def save_to_csv(self):
        if not self.patients:
            return

        df = pd.DataFrame(self.patients)

        df.to_csv(
            "hospital_records.csv",
            sep=";",                # 🇧🇷 Excel friendly
            index=False,
            encoding="utf-8-sig"    # evita bug de acento
        )

        print("\n✔ Data saved to hospital_records.csv")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    hospital = Hospital("Bernardo")
