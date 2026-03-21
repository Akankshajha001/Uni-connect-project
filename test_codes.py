from database.lost_found_db import lost_found_items

print("=== Checking Verification Codes in Database ===\n")
for item in lost_found_items:
    code = item.get('verification_code', 'MISSING')
    print(f"ID: #{item['id']} | Type: {item['type']} | Code: {code}")
    