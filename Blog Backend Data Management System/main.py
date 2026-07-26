import sys
import database
import auth
import blog

current_user = None

def print_menu():
    print("\n--- BLOG BACKEND MANAGEMENT SYSTEM ---")
    if current_user:
        print(f"Logged in as: {current_user['username']}")
        print("1. Create Blog Post")
        print("2. View All Posts")
        print("3. View Detailed Post & Comments")
        print("4. Edit Blog Post")
        print("5. Delete Blog Post")
        print("6. Add Comment to Post")
        print("7. Logout")
        print("8. Exit")
    else:
        print("Status: Guest")
        print("1. View All Posts")
        print("2. View Detailed Post & Comments")
        print("3. Login")
        print("4. Register Account")
        print("5. Exit")

def handle_login():
    global current_user
    print("\n--- ACCOUNT LOGIN ---")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    user = auth.login_user(username, password)
    if user:
        current_user = user
        print(f"\nWelcome back, {current_user['username']}!")

def handle_registration():
    print("\n--- REGISTER NEW USER ---")
    username = input("Enter Username: ").strip()
    email = input("Enter Email Address: ").strip()
    password = input("Enter Password: ").strip()
    user_id = auth.register_user(username, password, email)
    if user_id:
        print("\nRegistration successful! Please log in with your credentials.")

def handle_view_all():
    posts = blog.get_all_posts()
    if not posts:
        print("\nInformation: No blog posts available.")
        return

    print("\n" + "="*60)
    print(" ALL BLOG POSTS")
    print("="*60)
    print(f"{'ID':<5} | {'Title':<25} | {'Category':<12} | {'Author':<12}")
    print("-" * 60)
    for p in posts:
        print(f"{p['id']:<5} | {p['title'][:24]:<25} | {p['category'][:11]:<12} | {p['author'][:11]:<12}")
    print("="*60)

def handle_view_detailed():
    try:
        post_id = int(input("\nEnter Post ID to view details: "))
    except ValueError:
        print("\nError: Invalid post ID format. Expected an integer.")
        return

    post = blog.get_post_by_id(post_id)
    if not post:
        print(f"\nError: Post ID {post_id} not found.")
        return

    print("\n" + "="*60)
    print(f" TITLE: {post['title']}")
    print("="*60)
    print(f" Author   : {post['author']}")
    print(f" Category : {post['category']}")
    print(f" Date     : {post['created_at']}")
    print("-" * 60)
    print(f" Content:\n{post['content']}")
    print("="*60)

    comments = blog.get_comments_for_post(post_id)
    print("\n--- COMMENTS ---")
    if not comments:
        print(" No comments on this post yet.")
    else:
        for c in comments:
            print(f"[{c['created_at']}] {c['author']}: {c['content']}")

def handle_create_post():
    if not current_user:
        print("\nError: You must be logged in to create a post.")
        return

    print("\n--- CREATE BLOG POST ---")
    title = input("Enter Title: ").strip()
    category = input("Enter Category: ").strip()
    content = input("Enter Content: ").strip()

    blog.create_post(title, content, category, current_user["id"])

def handle_edit_post():
    if not current_user:
        print("\nError: You must be logged in to edit posts.")
        return

    try:
        post_id = int(input("\nEnter Post ID to edit: "))
    except ValueError:
        print("\nError: Invalid post ID format.")
        return

    post = blog.get_post_by_id(post_id)
    if not post:
        print(f"\nError: Post ID {post_id} not found.")
        return

    if post["author_id"] != current_user["id"]:
        print("\nPermission Error: You can only edit posts authored by you.")
        return

    print(f"\nEditing Post #{post_id} (Leave blank to retain current values)")
    new_title = input(f"New Title [{post['title']}]: ").strip() or post['title']
    new_category = input(f"New Category [{post['category']}]: ").strip() or post['category']
    new_content = input(f"New Content [{post['content']}]: ").strip() or post['content']

    blog.update_post(post_id, new_title, new_content, new_category, current_user["id"])

def handle_delete_post():
    if not current_user:
        print("\nError: You must be logged in to delete posts.")
        return

    try:
        post_id = int(input("\nEnter Post ID to delete: "))
    except ValueError:
        print("\nError: Invalid post ID format.")
        return

    confirm = input(f"Are you sure you want to delete post #{post_id}? (y/n): ").strip().lower()
    if confirm == 'y':
        blog.delete_post(post_id, current_user["id"])

def handle_add_comment():
    if not current_user:
        print("\nError: You must be logged in to add comments.")
        return

    try:
        post_id = int(input("\nEnter Target Post ID: "))
    except ValueError:
        print("\nError: Invalid post ID format.")
        return

    content = input("Enter Comment Message: ").strip()
    blog.add_comment(post_id, current_user["id"], content)

def run_app():
    global current_user
    database.init_db()
    database.seed_sample_data()

    while True:
        print_menu()
        choice = input("\nSelect option: ").strip()

        if current_user:
            if choice == "1":
                handle_create_post()
            elif choice == "2":
                handle_view_all()
            elif choice == "3":
                handle_view_detailed()
            elif choice == "4":
                handle_edit_post()
            elif choice == "5":
                handle_delete_post()
            elif choice == "6":
                handle_add_comment()
            elif choice == "7":
                current_user = None
                print("\nSuccess: Logged out successfully.")
            elif choice == "8":
                print("\nExiting system.")
                sys.exit()
            else:
                print("\nInvalid choice. Try again.")
        else:
            if choice == "1":
                handle_view_all()
            elif choice == "2":
                handle_view_detailed()
            elif choice == "3":
                handle_login()
            elif choice == "4":
                handle_registration()
            elif choice == "5":
                print("\nExiting system.")
                sys.exit()
            else:
                print("\nInvalid choice. Try again.")

if __name__ == "__main__":
    run_app()