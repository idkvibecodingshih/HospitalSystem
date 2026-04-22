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
            api_key=os.getenv("GROQ_API_KEY")
        )

    def analyze_patient(self, patient: dict) -> dict:
        prompt = f"""
Analyze this hospital patient:

Name: {patient['full_name']}
Age: {patient['age']}
Diagnosis: {patient['diagnosis']}
Department: {patient['department']}

Return:
- short_summary (1 sentence)
- severity (low, medium, high)
- recommendation (short)

Respond in JSON format.
"""

        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            temperature=0,
            messages=[{"role": "user", "content": prompt}]
        )

        content = response.choices[0].message.content

        # fallback simples (caso IA não retorne JSON perfeito)
        return {
            "ai_summary": content,
            "ai_severity": "unknown",
            "ai_recommendation": "N/A"
        }


# =========================
# HOSPITAL SYSTEM
# =========================

class Hospital:
    def __init__(self, manager: str):
        self.manager = manager
        self.patients = []
        self.ai = AIClient()
        self.running = True

        self.print_header("Hospital System v2.2 (AI Enhanced)")
        self.main_menu()

    def print_header(self, text: str):
        print("=" * 50)
        print(text.center(50))
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
                print("Invalid option.")
            except ValueError:
                print("Enter a valid number.")

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

            print("\n[AI] Analyzing patient...")
            ai_data = self.ai.analyze_patient(patient)

            # junta IA com dados
            patient.update(ai_data)

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
            sep=";",
            index=False,
            encoding="utf-8-sig"
        )

        print("\n✔ Data saved with AI insights")


# =========================
# ENTRY POINT
# =========================

if __name__ == "__main__":
    Hospital("Bernardo")
