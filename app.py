import json

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session security (replace with a secure key)
# next_id = 1  # Initialize next_id with an appropriate value




# create a function to load existing blog data from the json file

def loads_blogs():
    """
        Loads the existing blog posts from a JSON file and returns them as a list.

        Returns:
        List[dict]: A list of blog posts where each post is represented as a dictionary.
        """
    try:
        with open('blog.json', 'r') as file_obj:
            blogs = json.load(file_obj)
    except (FileNotFoundError, json.JSONDecodeError):
        blogs = []

    return blogs


# create a function to save blog data  to the json file
def save_blogs(blogs):
    """
        Saves the provided list of blog posts to a JSON file.

        Args:
        blogs (List[dict]): A list of blog posts to be saved.

        Returns:
        None
        """
    with open('blog.json', 'w') as file_obj:
        json.dump(blogs, file_obj, indent=2)

# Function to get next available id
def get_next_id(blogs):
    """
     Get the next available ID for a new blog entry.

    Args:
        blogs (list of dict): A list of existing blog entries.

    Returns:
        int: The next available ID, which is one greater than the highest ID in the existing entries.
        If no existing entries are found, it returns 1.

    """
    if not blogs:
        return 1
    return  max(blog['id'] for blog in blogs) + 1


# adding new blogs to the json file
@app.route('/add', methods=['GET', 'POST'])
def add_blog():
    """
        Handles adding a new blog post. Accepts GET and POST methods.

        For GET:
        Displays a form to input a new blog post.

        For POST:
        Accepts form data to create a new blog post and saves it.

        Returns:
        GET: Rendered HTML form for adding a new blog post.
        POST: Redirects to the index page after adding the new post.
        """

    global next_id  # access the global variable
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']

        try:
            # load existing blog_data
            blogs = loads_blogs()
            next_id = get_next_id(blogs)

            # creating new blog
            new_blog = {'id': next_id, 'author': author, 'title': title, 'content': content}

            # append the new blog  to the list of the blogs
            blogs.append(new_blog)

            # Save the updated blog data to the JSON file
            save_blogs(blogs)

            # Flash a success message
            flash('New blog post added successfully', 'success')

            # After processing, you may redirect to a different page
            return redirect('/')

        except Exception as e:
            # Flash an error message
            flash(f'Error adding the new blog post: {str(e)}', 'error')

    return render_template('add.html')


# @app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
# def delete(post_id):
#     if request.method == 'POST':
#         blog_posts = loads_blogs()
#         print(blog_posts)
#         blog_posts = [post for post in blog_posts if post['id'] != post_id]
#         return redirect(url_for('index'))
#     else:
#         # Handle GET requests (display confirmation or deletion form)
#         return render_template('add.html', post_id=post_id)

@app.route('/delete/<int:post_id>', methods=['GET', 'POST'])
def delete(post_id):
    if request.method == 'POST':
        #load existing  blog data
        blogs = loads_blogs()

        # find the blog post with the given id and remove it from the list
        updated_blogs = [blog for blog in blogs if blog['id'] != post_id]
        save_blogs(updated_blogs)

        return redirect(url_for(index))
    # Handle get request to display the  delete confirmation page
    post =  next((blog for blog in loads_blogs() if blog['id'] == post_id), None)
    if post:
        return render_template('delete_confirmation.html', post=post)
    else:
        return 'Blog post not found', 404






@app.route('/')
def index():
    """
        Renders the index page to display a list of existing blog posts.

        Returns:
        Rendered HTML page with a list of blog posts.
        """

    # add code here to fetch the  posts from a file
    posts = loads_blogs()
    print(posts)
    return render_template('index.html', posts=posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
