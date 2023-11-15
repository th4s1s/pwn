<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container grid">
        <div class="card">
            <h1 class="page-title title">My Recipes</h1>
            <div class="card-content">
                <form class="search-from" action="/recipes" method="get">
                    <label class="search-from__label" for="title">Search</label>
                    <input class="text-field" id="title" name="title" type="text" placeholder="Title"
                           value="<?= $title ?? '' ?>"/>
                    <button class="primary-button" type="submit">search</button>
                    <?php
                    if (isset($errors) && array_key_exists('title', $errors)) {
                        echo "<div class=\"text-field__error\">{$errors['title']}</div>";
                    }
                    ?>
                </form>
            </div>
        </div>
        <ul class="list">
            <?php
            foreach ($recipes as $recipe) {
                $title = htmlspecialchars($recipe->title, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5);
                $description = htmlspecialchars($recipe->description, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5);
                echo <<<RECIPE
            <a href="/recipes/$recipe->id" class="list__card card">
                <li class="list__container">
                    <p class="list__title">$title</p>
                    <p class="list__description card-content">$description</p>
                </li>
            </a>
        RECIPE;
            }
            ?>
        </ul>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
