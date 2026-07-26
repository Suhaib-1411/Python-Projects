from typing import List, Optional, Dict, Any
from database import get_connection

def create_post(title: str, content: str, category: str, author_id: int) -> bool:
    """Creates a new blog post entry."""
    if not title.strip() or not content.strip() or not category.strip():
        print("\nError: Title, content, and category cannot be blank.")
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO posts (title, content, category, author_id)
            VALUES (?, ?, ?, ?);
        """, (title.strip(), content.strip(), category.strip(), author_id))
        conn.commit()
        print("\nSuccess: Blog post published successfully.")
        return True

def get_all_posts() -> List[Dict[str, Any]]:
    """Fetches all posts ordered by creation date descending."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.title, p.content, p.category, p.created_at, u.username as author
            FROM posts p
            JOIN users u ON p.author_id = u.id
            ORDER BY p.created_at DESC;
        """)
        return [dict(row) for row in cursor.fetchall()]

def get_post_by_id(post_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves details for a single post by ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT p.id, p.title, p.content, p.category, p.created_at, p.author_id, u.username as author
            FROM posts p
            JOIN users u ON p.author_id = u.id
            WHERE p.id = ?;
        """, (post_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

def update_post(post_id: int, title: str, content: str, category: str, user_id: int) -> bool:
    """Updates an existing post if the logged-in user is the author."""
    post = get_post_by_id(post_id)
    if not post:
        print(f"\nError: Post ID {post_id} not found.")
        return False

    if post["author_id"] != user_id:
        print("\nPermission Error: You can only edit your own posts.")
        return False

    if not title.strip() or not content.strip() or not category.strip():
        print("\nError: Updated fields cannot be empty.")
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE posts
            SET title = ?, content = ?, category = ?
            WHERE id = ?;
        """, (title.strip(), content.strip(), category.strip(), post_id))
        conn.commit()
        print("\nSuccess: Post updated successfully.")
        return True

def delete_post(post_id: int, user_id: int) -> bool:
    """Deletes a post if the logged-in user is the author."""
    post = get_post_by_id(post_id)
    if not post:
        print(f"\nError: Post ID {post_id} not found.")
        return False

    if post["author_id"] != user_id:
        print("\nPermission Error: You can only delete your own posts.")
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM posts WHERE id = ?;", (post_id,))
        conn.commit()
        print("\nSuccess: Post deleted successfully.")
        return True

def add_comment(post_id: int, author_id: int, content: str) -> bool:
    """Attaches a comment to a specific blog post."""
    post = get_post_by_id(post_id)
    if not post:
        print(f"\nError: Target Post ID {post_id} does not exist.")
        return False

    if not content.strip():
        print("\nError: Comment content cannot be empty.")
        return False

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO comments (post_id, author_id, content)
            VALUES (?, ?, ?);
        """, (post_id, author_id, content.strip()))
        conn.commit()
        print("\nSuccess: Comment added successfully.")
        return True

def get_comments_for_post(post_id: int) -> List[Dict[str, Any]]:
    """Retrieves all comments for a post."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.id, c.content, c.created_at, u.username as author
            FROM comments c
            JOIN users u ON c.author_id = u.id
            WHERE c.post_id = ?
            ORDER BY c.created_at ASC;
        """, (post_id,))
        return [dict(row) for row in cursor.fetchall()]