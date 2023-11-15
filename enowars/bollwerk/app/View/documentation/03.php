<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Passing Information to a View</h1>
        <div class="card-content">
            The render function of the view class accepts an array as a second argument.
            <br/>
            Create a associative array, and you will have access to variables with the name of the key and the values of
            the value
            <p>
                For example you can create an <span class="code">array ['foo' => 'bar']</span> and you will have access
                to a variable <span class="code">$foo</span> with the value <span class="code">'bar'</span> in your view.
            </p>
            <br/>
            There are also global variables that are injected in every view.
            <br/>
            That are the current user and the session id.

            <div class="button-container">
                <a class="primary-button" href="/documentation/2">Back</a>
                <a class="primary-button" href="/documentation/4">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
