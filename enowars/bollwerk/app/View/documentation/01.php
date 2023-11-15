<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Creating a Controller</h1>
        <div class="card-content">
            The first step in a MVP-Framework is a Controller.
            <br/>
            A Controller consists of file with at least one Method that can be called.
            <br/>
            In general a Controller is a file that has at leas one method that can be called.
            For the best developer experience we advise you to create a class for each controller in a file.
            <br/>
            Bollwerk provides you an Attribute called Route that you can add to each function in your controller.
            Here you can pass a path and a method that will map to a Route in your Application.
            <br/>
            <p>For example <span class="code">#[Route(path: '/foo/bar')]</span> will map to <span class="code">/foo/bar</span> in your application.</p>
            <p>
            All Controller Classes inside the Controller directory will be automatically detected.
            If you need Controllers outside of that directory, you can simply register them via the <span class="code">kernel.php</span>
            </p>

            <div class="button-container">
                <a class="primary-button" href="/documentation">Back</a>
                <a class="primary-button" href="/documentation/2">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
