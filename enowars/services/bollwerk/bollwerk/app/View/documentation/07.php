<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Validating User Input</h1>
        <div class="card-content">
            To validate user input you can create a class that extends the AbstractRequest Class.
            Inside your Request you will have Access to all parameters provided to your application via GET parameter or
            inside the request body.

            <br/>
            You can overwrite two arrays.
            <br/>
            Messages is an associative area.
            <br/>
            Each key corresponds to a parameter provided by the user (via GET parameter or inside the request body).
            <br/>
            The values are the error messages you want to have access to when validating that parameter fails.
            <br/>
            Rules are also an associative array.
            <br/>
            The keys corresponds to the variable name and the value is a string with chained rules.
            <br/>
            The values are strings.
            <br/>
            Each string contains two parts: The data type to be validated (e.g. string) and rules, that can be chained.
            <p>
            The data type and the rules are separated via <span class="code">-></span>.
            </p>
            <p>
            Rules can be chained via <span class="code">|</span> and can receive arguments by adding it after <span
                    class="code">:</span>.
            </p>
            If you want to validate, that there is a parameter <span class="code">username</span> passed that is a
            string between 4 and 255 characters, you can add this to your rules array:
            <p class="code-block">'username' => 'string->required|min:4|max:12'</p>

            <div class="button-container">
                <a class="primary-button" href="/documentation/6">Back</a>
                <a class="primary-button" href="/documentation/8">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
