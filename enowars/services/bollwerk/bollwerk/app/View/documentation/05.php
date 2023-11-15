<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Route Model Binding</h1>
        <div class="card-content">
            In most application there will be the need to find Models based on the current url.
            <br/>
            Bollwerk provides Route Model Binding to you.
            <br/>
            So all you need to do is to create a Route in a controller.
            <p>
                The path has to contain a path parameter e.g. <span class="code">'/foo/{bar}'</span>.
            </p>
            <br/>
            You gain access to the value of a route parameter by just adding a parameter to your function with the name
            of the path parameter.
            <br/>
            If you have a CRUD application, your parameters will probably often relate to an entity.
            <p>
                For example you can see in the RecipeController that the <span class="code">show()</span> method
                corresponds to a recipe entity.
            </p>
            Because that is so common, bollwerk supports Route Model Binding.
            <br/>
            If your route parameter is the id of an Entity, just add the Entity to the parameters of the function and
            name the variable like the path parameter.
            <br/>
            You will automagically get a hydrated Entity, and if it is not found the 404 page will be served.

            <div class="button-container">
                <a class="primary-button" href="/documentation/4">Back</a>
                <a class="primary-button" href="/documentation/6">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
