# reddit-saved-manager

Python project to explore working with databases and API calls. Intended end-game functionality is to retrieve a full list of a user's saved posts and allow for easy retrieval, modification, and searching of the saved posts. Ideally will be able to mass remove "[deleted]" or "[removed]" posts, filter saved posts by subreddit, sort results by standard reddit options (popularity, controversial, etc) and search for keywords within or without any aforementioned filters.

<ol>
    <li>Build database
        <ul>
            <li><s>Explore reddit API and determine initial database requirements</s></li>
            <li><s>Create Python code to create database</s></li>
            <li><s>Remove hard-coded DB path and implement config file</s></li>
        </ul>
    </li><br>
    <li>Grab a single listing of saved files
        <ul>
            <li><s>Store reddit API key somewhere (config file?)</s>
                <ul><li><s>Auth data stored in config file with handling for 2FA</s></li></ul></li>
            <li><s>Create a method <em>(name: updateSavedFromWeb ?)</em> that sends a single GET request to the API and stores the response in a variable</s></li>
            <li><s>Return the variable storing the response data</s></li>
        </ul>
    </li><br>
    <li>Parse the list of saved files
        <ul>
            <li>Create a method <em>(name: parseSavedListing ?)</em> that takes in a JSON response from <em>updateSavedFromWeb</em></li>
            <li>Process the items from the JSON response and build database accordingly
                <ul>
                    <li>Possible create two subfunctions, one for parsing links and one for comments as the entries likely contain differently formatted data</li>
                </ul>
            </li>
            <li>Return "after" value from JSON response to be used as a starting point for next iteration</li>
        </ul><br>
    <li>Create a crude user interface
        <ul>
            <li>Interface only needs two options to begin with (1- Update Saved List, 2- Exit)</li>
            <li>Implement the menu options by making use of methods created in steps 2 and 3
                <ul><li>No recursion to begin with, just process a single Listing response</li></ul>
            </li>
        </ul>
    </li><br>
    <li>Manipulate the database
        <ul>
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
    <li>Implement basic error handling
        <ul>
            <li>For example:
                <ul>
                    <li>What if the API call returns nothing?</li>
                    <li>What if <em>parseSavedListing</em> receives a null value?</li>
                    <li>For any menu items created in #5, what if the database is empty?</li>
                    <li>What if the user enters an invalid value?</li>
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
</ol>