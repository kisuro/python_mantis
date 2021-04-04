def test_signup_new_account(app):
    username = "user1"
    password = "test"
    app.james.ensure_user_exists(username, password)
