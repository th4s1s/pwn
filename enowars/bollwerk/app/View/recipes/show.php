<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container">
        <div class="card">
            <h1 class="page-title title"><?= htmlspecialchars($recipe->title, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5) ?></h1>
            <div class="card-content">
                <p class="list__description"><?= htmlspecialchars($recipe->description, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5) ?></p>
                <div class="button-container">
                    <a class="primary-button" href="/recipes">all recipes</a>
                    <a class="primary-button" href="/recipes/<?= $recipe->id ?>/download">download as markdown</a>
                </div>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
