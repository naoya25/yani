// This is a simple project and doesn't require complex JavaScript functionality.
// However, we can add some basic form validation to the login and input forms.

document.addEventListener('DOMContentLoaded', function() {
    // Get the login form
    var loginForm = document.querySelector('.login-container form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            var username = loginForm.querySelector('input[name="username"]');
            var password = loginForm.querySelector('input[name="password"]');
            if (!username.value || !password.value) {
                e.preventDefault();
                alert('ユーザー名とパスワードを入力してください');
            }
        });
    }

    // Get the input form
    var inputForm = document.querySelector('form[method="POST"]');
    if (inputForm) {
        inputForm.addEventListener('submit', function(e) {
            var count = inputForm.querySelector('input[name="count"]');
            if (!count.value || isNaN(count.value) || count.value < 0) {
                e.preventDefault();
                alert('タバコの本数を正しく入力してください');
            }
        });
    }
});
