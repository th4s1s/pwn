<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Creating a View</h1>
        <div class="card-content">
            To create a view that can be returned by your controller, create a php file in the View directory.
            <br/>
            You should put all the markup for your response in a view.
            <br/>
            bollwerk provides a Class called View with a method render.
            <br/>
            You can call this method and return the result in your controller.

            <div class="button-container">
                <a class="primary-button" href="/documentation/1">Back</a>
                <a class="primary-button" href="/documentation/3">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
