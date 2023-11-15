<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Middlewares</h1>
        <div class="card-content">
            You will probably have some functionality that has to be checke in multiple controller method.
            <br/>
            For example if you have a login there will be some routes that should only be accessible to logged in users.
            <br/>
            To achieve this, bollwerk has support for middlewares
            <br/>
            Just create a class that implements the MiddlewareInterface.
            <p>
                You will implement a method called <span class="code">handle()</span> that will receive the Request as
                an argument
            </p>
            You can than do whatever you nee inside the method (e.g. checking if the user is logged in).
            <br/>
            After implementing the method, just add the class to the middlewares argument in the Route-Attribute:
            <p class="code-block">#[Route(path: '/recipes', middlewares: [Authenticated::class])]</p>

            <div class="button-container">
                <a class="primary-button" href="/documentation/8">Back</a>
                <a class="primary-button" href="/documentation/10">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
