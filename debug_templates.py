import os

def check_templates():
    base_dir = os.path.dirname(__file__)
    templates_dir = os.path.join(base_dir, 'templates')
    
    print("🔍 Checking template structure...")
    print(f"Templates directory: {templates_dir}")
    print(f"Exists: {os.path.exists(templates_dir)}")
    
    if not os.path.exists(templates_dir):
        print("❌ Templates directory doesn't exist!")
        return False
    
    # Check essential files
    files_to_check = [
        'auth/login.html',
        'auth/register.html',
        'layouts/auth.html',
        'dashboard/index.html'
    ]
    
    all_exist = True
    for file_path in files_to_check:
        full_path = os.path.join(templates_dir, file_path)
        exists = os.path.exists(full_path)
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}: {exists}")
        
        if not exists:
            all_exist = False
            
            # Create missing file
            if file_path == 'layouts/auth.html':
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                with open(full_path, 'w') as f:
                    f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Steam Analytics{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    {% block content %}{% endblock %}
</body>
</html>''')
                print(f"   ✅ Created {file_path}")
    
    return all_exist

if __name__ == '__main__':
    if check_templates():
        print("\n🎉 All templates exist! The app should work now.")
        print("\nTry running: python run.py")
    else:
        print("\n⚠️ Some templates are missing but we created the essential ones.")
        print("Try running: python run.py")