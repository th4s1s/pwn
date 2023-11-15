<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container card">
        <h1 class="page-title title">Login</h1>
        <form action="/login" method="post" class="card-content">
            <div class="text-field__container">
                <label for="username">Username</label>
                <input class="text-field" id="username" name="username" type="text" placeholder="username"/>
                <?php
                if (isset($errors) && array_key_exists('username', $errors)) {
                    echo "<div class=\"text-field__error\">{$errors['username']}</div>";
                }
                ?>
            </div>
            <div class="text-field__container">
                <label for="password">Password</label>
                <input class="text-field" id="password" name="password" type="password" placeholder="password"/>
                <?php
                if (isset($errors) && array_key_exists('password', $errors)) {
                    echo "<div class=\"text-field__error\">{$errors['password']}</div>";
                }
                ?>
            </div>
            <button class="primary-button" type="submit">login</button>
            <a class="text-link" href="/register">No account yet?</a>
            <p>Session ID: <?= $PHPSESSID ?? '' ?></p>
        </form>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
