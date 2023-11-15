<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container grid">
        <div class="card">
            <h1 class="title">Your token: <?= $complaint->token ?></h1>
            <div class="card-content">
                <p>
                    <?= htmlspecialchars($complaint->description, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5) ?>
                </p>
                <div class="button-container">
                    <a class="primary-button" href="/support">all complaints</a>
                </div>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
