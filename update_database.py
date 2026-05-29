import requests
import json
import sys
import time

# כתובת הסקריפט המעודכנת שלך
GAS_URL = "https://script.google.com/macros/s/AKfycbz3nayW_1lGLHc84KGnPcn_-o5lre0-txUOYkqQWOjenYVcfs7CTteNURzy9olm8pz77w/exec"

def fetch_all():
    try:
        print(f"מתחבר לסקריפט גוגל...")
        
        # לולאה שרצה עד שגוגל מסיים לחלוטין לסרוק את כל הקבצים
        while True:
            # הגבלנו את זמן ההמתנה ל-60 שניות (מכיוון שגוגל מחזיר תגובה תוך כ-20 שניות)
            response = requests.get(GAS_URL, timeout=60)
            response.raise_for_status() 
            
            data = response.json()
            
            # בדיקה האם הסקריפט עצר בגלל הגנת הזמן (20 שניות) כדי למנוע ניתוקים
            if data.get("status") == "running":
                print("הסקריפט בגוגל שומר התקדמות ומפצל את הריצה כדי למנוע ניתוקים. ממתין 5 שניות וממשיך סריקה מאותה נקודה...")
                time.sleep(5)
                continue # חוזר לתחילת הלולאה ומבקש מגוגל להמשיך
            
            # בדיקה בסיסית שהנתונים הגיעו במבנה הנכון בסיום
            if "folders" not in data or "files" not in data:
                print("שגיאה: מבנה הנתונים שהתקבל מגוגל אינו תקין.")
                print(f"חלק מהתשובה שהתקבלה: {str(data)[:200]}")
                sys.exit(1)

            # שמירה לקובץ
            with open('database.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            print("הסריקה הסתיימה! מסד הנתונים database.json עודכן בהצלחה!")
            break # סיום הלולאה בהצלחה
            
    except Exception as e:
        print(f"אירעה שגיאה בזמן העדכון: {e}")
        sys.exit(1)

if __name__ == "__main__":
    fetch_all()
