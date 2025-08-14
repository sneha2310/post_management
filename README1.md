pytest fixture are called everytime whenever the test functions are called.
Because of this after user create when I run the test login the fixture called and make the database empty as it calls the 
delete database then create one through the session fixture.
When I am defining the functions individually
So, we will fix it through the scope="module" as bydefault it is scope="function". But using module make the test functions
dependent on each other which leads to bad practice. Module means the file like fixture one time run for the user test, then 
one time for test_file, then next for the test_post.
