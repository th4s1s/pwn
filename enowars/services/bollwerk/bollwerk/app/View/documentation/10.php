<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Service Container</h1>
        <div class="card-content">
            The service Container is a place where you can register Classes that need special configuration.
            <br/>
            These classes are then available via DI or the static resolve method.
            <br/>
            That might be useful if you need to resolve a dependency as a singleton inside a static context.

            <div class="button-container">
                <a class="primary-button" href="/documentation/9">Back</a>
                <a class="primary-button" href="/">Finish</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
