# reddit-saved-manager

Python project to explore working with databases and API calls. Intended end-game functionality is to retrieve a full list of a user's saved posts and allow for easy retrieval, modification, and searching of the saved posts. Ideally will be able to mass remove "[deleted]" or "[removed]" posts, filter saved posts by subreddit, sort results by standard reddit options (popularity, controversial, etc) and search for keywords within or without any aforementioned filters.

<ol>
    <li><s>Build database</s> - <b>Database.py</b>
        <ul>
            <li><s>Determine initial database requirements</s></li>
            <li><s>Create database</s></li>
            <li><s>Remove hard-coded DB path and implement config file</s></li>
        </ul>
    </li><br>
    <li><s>Grab a single listing of saved files</s> - decided to use PRAW instead of directly calling reddit API - <b>RedditHandler.py</b>
        <ul>
            <li><s>Store reddit API key somewhere (config file?)</s> - <em>using auth with username, password, client ID, and client secret</em>
                <ul><li><s>Auth data stored in config file with handling for 2FA</s></li></ul></li>
            <li><s>Create a method that sends a single GET request to the API and stores the response in a variable</s> - <b>RedditHandler.retrieve_saved()</b></li>
            <li><s>Return the variable storing the response data</s></li>
        </ul>
    </li><br>
    <li><s>Parse the list of saved files</s> - <b>utilities.py</b>
        <ul>
            <li><s>Create a method that takes in a response from (edit: RedditHandler.retrieve_saved())</s></li>
            <li><s>Process the items from and build database accordingly</s> - <b>utilities.parse_posts()</b>
                <ul>
                    <li><s>Possible create two subfunctions, one for parsing links and one for comments as the entries likely contain differently formatted data</s>
                        <ul>
                            <li><b>parse_comment()</b>, <b>parse_comments()</b></li>
                            <li><b>parse_submission()</b>, <b>parse_submissions()</b></li>
                        </ul>
                    </li>
                </ul>
            </li>
            <li><s>Return "after" value from JSON response to be used as a starting point for next iteration</s> - <em>not needed with PRAW?</em></li>
        </ul><br>
    <li><s>Populate the database</s> - <b>Database.py</b>
        <ul>
            <li><s>Create methods to write the saved comments and posts to the database</s>
                <ul>
                    <li><b>Datatbase.insert_comments()</b> - <em>takes a list of SavedComment objects and writes them all as a batch</em></li>
                    <li><b>Database.insert_submissions()</b> - <em>batch processes the writing of SavedSubmissions</em></li>
                </ul>
            </li>
        </ul>
    </li><br>
    <li><s>Create a crude user interface</s> - <b>menu.py</b>
        <ul>
            <li><s>Interface only needs two options to begin with (1- Update Saved List, 2- Exit)</s></li>
            <li><s>Implement the menu options by making use of methods created in steps 2 and 3</s> - <b>menu.parse_menu_option()</b></li>
            <li><s>Display the menu and loop it</s></li>
        </ul>
    </li><br>
    <li>Manipulate the database
        <ul>
            <li>Create a view table that joins comments and submissions, sorted by created_time
                <ul>
                    <li>Determine needed columns and how to handle flagging each as comment or submission</li>
                </ul>
            </li>
            <li>Create new menu options that display information from the database. For example:
                <ul>
                    <li>Display first 25 items</li>
                    <li>Display all links / display all comments</li>
                    <li>Show list of subreddits in database</li>
                    <li>Show database items by user-specified subreddit</li>
                </ul>
            </li>
        </ul>
    </li><br>
    <li>Implement basic error handling - <b>CustomExceptions.py</b>
        <ul>
            <li><b>UserCancelledException</b> - <em>Raised if the user enters "no" when prompted to confirm an operation</em></li>
            <li><b>InvalidMenuOptionException</b> <em>Raised if an out-of-bounds menu option gets past main.py and is caught by menu.py</em></li>
            <li>Possible needs?
                <ul>
                    <li>praw authentication fails?</li>
                    <li>praw returns nothing / Null / None</li>
                    <li>User requests data from an empty database</li>
                    <li>User tries to write nothing to the database</li>
                </ul>
            </li>
        </ul>
    </li><br>
    <li>Expand functionality
        <ul>
            <li>Add a new API call - create a method that allows the user to delete a saved post</li>
            <li>Update Menu Option 1 so that it will continue querying the API until it reaches the last Listing</li>
            <li>Allow for mass deletion of saved comments if the text only consists of <em>[saved]</em> or <em>[removed]</em></li>
            <li>Update first two functions to account for updating the database instead of just the initial build
                <ul>
                    <li>What if the API call returns data that already exists in the database?</li>
                    <li>What if the API call <strong>doesn't</strong> return data that <strong>does</strong> exist in the database?</li>
                </ul>
            </li>
            <li>Create new menu options as needed for new functionality</li>
            <li>Add error handling to any new code as needed</li>
        </ul>
    </li><br>
    <li>Create simple GUI
        <ul><li>???</li></ul>
    </li>
    <li>Introduce multithreading
        <ul>
            <li>When doing a full retrieve on all saved posts, the API is limited to 60 calls per minute and 100 items per call. This data can be transformed and written to the database while praw handles the rate limiting</li>
            <li>Deletions are handled one at a time - multithreading operations could allow app to still be functional while processing bulk deletes</li>
            </ul>
    </li>
</ol>