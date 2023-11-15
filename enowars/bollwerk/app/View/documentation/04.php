<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Creating a Model</h1>
        <div class="card-content">
            Bollwerk has builtin support for SQLite databases.
            <br/>
            Just add the path to your SQLite file in the kernel.php and you are ready to go.
            <br/>
            <br/>
            To create a Model you just have to follow these steps:
            <p>
            1. Create a table that corresponds to your model in your sqlite database
            </p>
            <p>
                2. Then create a php Class that extends the <span class="code">AbstractModel</span>
            </p>
            All columns in the table will be automatically mapped to the properties of the models.
            Even the names of the columns will get be converted to camelCase.
            You only need to keep the model properties in sync with the table definitions.

            <div class="button-container">
                <a class="primary-button" href="/documentation/3">Back</a>
                <a class="primary-button" href="/documentation/5">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
