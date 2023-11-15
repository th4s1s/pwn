<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="page-container">
    <div class="card">
        <h1 class="page-title title">Dependency Injection</h1>
        <div class="card-content">
            When crating object oriented applications at some point you run into the issue that the classes need
            instances of each other.
            <br/>
            Classes may depend on each other and some classes are used in many places.
            <br/>
            Bollwerk provides you with Dependency Injection.
            <br/>
            You can simply put the class you want to use into the Constructor of your class and it will automatically be
            passed into the class.
            <br/>
            All dependencies of your dependency will be resolved by bollwerk.
            <br/>
            Another benefit is, that the classes used via Dependency Injection are singletons so the much less overhead
            in your application.
            <br/>
            Dependency Injection also works inside methods of your controller!
            <br/>
            For example if you create a Service that depends on the Database class, you can simply put the Database
            class into the Constructor of the Service, and add the Service as Parameter to your Controller method.
            <br/>
            You can than just interact with the Service, without worrying if the dependencies of the Service will
            change.

            <div class="button-container">
                <a class="primary-button" href="/documentation/5">Back</a>
                <a class="primary-button" href="/documentation/7">Next</a>
            </div>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
