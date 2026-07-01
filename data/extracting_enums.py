import pandas as pd
from enum import Enum

# שם קובץ הפרקט של המסעדות
PARQUET_FILE = "CBF_item_features_1.parquet"

# השדות שאנחנו רוצים לחקור ולייצר עבורם Enum (כולל קטגוריות למסעדות ויוזרים)
fields_to_analyze = [
    'category', 'service_options', 'atmosphere', 
    'dining_options', 'crowd', 'offerings', 'accessibility'
]

print("Reading Parquet file and scanning all 40K+ restaurants...")
df = pd.read_parquet(PARQUET_FILE)

print("Extracting unique values and generating Python Enum classes...\n")

print("# ========================================================")
print("# AUTO-GENERATED ENUMS FOR YOUR MONGO PROJECT")
print("# ========================================================\n")
print("from enum import Enum\n")

for field in fields_to_analyze:
    if field in df.columns:
        unique_values = set()
        
        # מעבר על כל השורות, ניקוי ופיצול לפי פסיקים
        for row in df[field].dropna():
            if isinstance(row, str) and row.strip() != "":
                tags = [tag.strip() for tag in row.split(',')]
                unique_values.update(tags)
        
        # סינון ערכים ריקים או כותרות null מהרשימה
        clean_values = [v for v in unique_values if v and v.lower() != 'null']
        
        # יצירת שם מחלקה תקין (למשל ServiceOptions או Category)
        # שדה ה-category ישמש גם כבסיס ל-UserPreference של הקולד סטארט
        class_name = "".join([part.title() for part in field.split('_')])
        
        if field == 'category':
            print(f"class UserPreference(Enum):")
            print("    \"\"\" קטגוריות מובילות עבור העדפות קולד-סטארט של משתמשים \"\"\"")
        else:
            print(f"class {class_name}Option(Enum):")
            print(f"    \"\"\" אופציות ייחודיות עבור השדה {field} \"\"\"")
            
        if not clean_values:
            print("    NONE_FOUND = \"No options in data\"\n")
            continue
            
        for val in sorted(clean_values):
            # יצירת שם משתנה תקין (אותיות גדולות, ללא רווחים, מקפים או תווים מיוחדים)
            enum_key = val.upper().replace(' ', '_').replace('-', '_').replace("'", "").replace('&', 'AND').replace('/', '_')
            
            # אם שם המשתנה מתחיל במספר (למשל 24_hours), נוסיף לו קידומת חוקית כדי שהקוד לא יישבר
            if enum_key and enum_key[0].isdigit():
                enum_key = f"NUM_{enum_key}"
                
            print(f"    {enum_key} = \"{val}\"")
        print("\n")