<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container grid">
    <div class="card">
        <h1 class="page-title title">Create Recipe</h1>
        <form action="/recipes" method="post" class="card-content">
            <div class="text-field__container">
                <label for="title">Title</label>
                <input class="text-field" id="title" name="title" type="text" placeholder="Title"/>
                <?php
                if (isset($errors) && array_key_exists('title', $errors)) {
                    echo "<div class=\"text-field__error\">{$errors['title']}</div>";
                }
                ?>
            </div>
            <div class="text-field__container">
                <label for="description">Description</label>
                <textarea class="text-field" id="description" name="description" placeholder="Description"
                          rows="10"></textarea>
                <?php
                if (isset($errors) && array_key_exists('description', $errors)) {
                    echo "<div class=\"text-field__error\">{$errors['description']}</div>";
                }
                ?>
            </div>
            <button class="primary-button" type="submit">save</button>
        </form>
    </div>
    <div class="card">
        <h1 class="title">Tip</h1>
        <div class="card-content">
            <p>
                Did you know you can use Markdown in the recipe description?
                <br/>
                <br/>
                Markdown allows you to format text with headings, bold and italic text, lists, and much more. It's a
                great way to make your recipe descriptions more visually appealing and organized. To get started with
                Markdown, simply use some basic syntax, such as adding ## for headings or * for bullet points.
                <br/>
                <br/>
                Happy recipe creating!
            </p>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
