import json

from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for session security (replace with a secure key)

# next_id = 1  # Initialize next_id with an appropriate value



def loads_blogs():
    """
        Loads the existing blog posts from a JSON file and returns them as a list.

        Returns:
        List[dict]: A list of blog posts where each post is represented as a dictionary.
        """
    try:
        with open('blogs.json', 'r') as file_obj:
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
    with open('blogs.json', 'w') as file_obj:
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
    return max(blog['id'] for blog in blogs) + 1
# Function to fetch a blog post by id
def get_blog_post_id(post_id):
    for post in loads_blogs():
        if post['id'] == post_id:
            return post
    return None



# Function to update a blog post
# def update_blog_post(post_id, updated_data):
#     blogs = loads_blogs()
#     for post in blogs:
#         if post['id'] == post_id:
#             post.update(updated_data)
#
#     # Save the updated data back to the JSON file
#     with open('blogs.json', 'w') as json_file:
#         json.dump(blogs, json_file, indent=4)




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
        author = request.form['name']
        title = request.form['title']
        content = request.form['content']

        try:
            # load existing blog_data
            blogs = loads_blogs()
            next_id = get_next_id(blogs)

            # creating new blog
            new_blog = {'id': next_id, 'name': author, 'title': title, 'content': content}

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

        return redirect(url_for('index', deleted=True))

    if request.method == 'GET':
        # Handle get request to display the  delete confirmation page
        post = next((blog for blog in loads_blogs() if blog['id'] == post_id), None)
        if post:
            return render_template('delete_confirmation.html', post="GET")
        else:
            return 'Blog post not found', 404

list_of_blogs = loads_blogs()

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    post = get_blog_post_id(post_id)


    if post is None:
        return "Blog post not found", 404

    if request.method == 'POST':

        updated_name = request.form.get('name')
        updated_title = request.form.get('title')
        updated_content = request.form.get('content')

        # update the post
        for blog in list_of_blogs:
            if blog['id'] == post_id:
                blog['name'] = updated_name
                blog['title'] = updated_title
                blog['content'] = updated_content

        #Save the updated data back to the JSON file
        with open('blogs.json', 'w') as json_file:
            json.dump(list_of_blogs, json_file, indent=4)


        return redirect(url_for('index'))
    return render_template('blog_update.html', post='GET')

@app.route('/blog_update/<int:post_id>', methods=['GET'])
def blog_update(post_id):
    """
    Renders the blog update page with the details of the selected blog post.

    Args:
        post_id (int): The ID of the blog post to be updated.

    Returns:
        Rendered HTML page with the blog post details to populate the form.
    """
    post = get_blog_post_id(post_id)  # Fetch the details of the selected blog post
    if post is None:
        return "Blog post not found", 404  # Handle the case where the post is not found

    return render_template('blog_update.html', post=post)


@app.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    # Fetch the post from your data (e.g., JSON file)
    post = get_blog_post_id(post_id)

    if post is not None:
        if 'likes' not in post:
            post['likes'] = 0

        # Increment the 'likes' count for the post
        post['likes'] += 1

        for blog in list_of_blogs:
            if blog['id'] == post_id:
                blog['likes'] = post['likes']


        # Update the post in your data (e.g., save it back to the JSON file)

        # You can save the updated post back to the JSON file here
    with open('blogs.json', 'w') as json_file:
        json.dump(list_of_blogs, json_file, indent=4)


    # Redirect back to the index page
    return redirect(url_for('index'))



@app.route('/')
def index():
    """
        Renders the index page to display a list of existing blog posts.

        Returns:
        Rendered HTML page with a list of blog posts.
        """

    # add code here to fetch the  posts from a file
    posts = loads_blogs()
    # print(posts)
    return render_template('index.html', posts=posts)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
