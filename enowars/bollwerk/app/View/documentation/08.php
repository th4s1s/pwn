<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Storing Data</h1>
        <div class="card-content">
            <p>
                To store Data you can simply call the static <span class="code">create()</span> method of the model you
                want to create. It will take an array as argument with the desired data to store. For example:
            </p>
            <p class="code-block">
                Recipe::create([
                'userId' => 2,
                'title' => 'Recipe title',
                'description' => 'Recipe description',
                ])
            </p>
            <p>
                This will create a recipe for the user with the id <span class="code">2</span> with the title <span
                        class="code">Recipe title</span> and the description <span
                        class="code">Recipe description</span>. The changes will be persisted in the database
                automatically.
            </p>
            <p>
                To update an Entity just call the static <span class="code">update()</span> method. It will take the id
                of the entity to update and an array with all the fields to update as arguments. For example
            </p>
            <p class="code-block">
                Recipe::update(
                1,
                ['description' => 'Updated description']
                )
            </p>
            <p>
                This will update the description of recipe with the id <span class="code">1</span> to <span
                        class="code">Updated description</span>. The changes will be persisted in the database
                automatically.
            </p>

            <div class="button-container">
                <a class="primary-button" href="/documentation/7">Back</a>
                <a class="primary-button" href="/documentation/9">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
