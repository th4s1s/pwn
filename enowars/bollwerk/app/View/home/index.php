<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div class="landing-page-container card">
    <h1 class="page-title title">Welcome to <strong>cheffy</strong>, a demo application for <strong>bollwerk</strong>
    </h1>
    <div class="card-content">
        <div>
            Welcome to 1997 and the world of PHP, the web development language that has taken the internet by storm. As
            PHP continues to evolve, we are proud to introduce Bollwerk - the first-ever PHP framework that puts
            security and structure at the forefront of your web applications.
            <br/>
            <br/>
            Bollwerk is a cutting-edge solution that will revolutionize the way you build web applications. With our
            framework, you'll be able to write more secure, maintainable, and scalable code, while improving your
            overall development workflow.
            <br/>
            <br/>
            <strong>Bollwerk</strong> is built with security in mind. We understand that the internet can be a dangerous
            place, and that's
            why we've implemented the latest security measures to ensure your web applications are protected from common
            vulnerabilities. You can rest easy knowing your data and your users are safe.
            <br/>
            <br/>
            But that's not all. Bollwerk also follows the industry-standard Model-View-Controller (MVC) pattern,
            providing a
            clear separation of concerns that will make your code easier to understand and maintain. With Bollwerk,
            you'll
            be able to focus on building your application's functionality without getting bogged down in the
            complexities of
            managing your codebase.
            <br/>
            <br/>
            Bollwerk is designed to make your life easier. It's lightweight, easy to install, and comes with everything
            you
            need to get started. Whether you're building a simple blog or a complex web application, Bollwerk will help
            you
            get the job done faster and more efficiently.
            <br/>
            <br/>
            So why wait? Join the revolution and start building secure, structured web applications with Bollwerk today.
            <br/>
            <br/>
            <h2><strong>bollwerk</strong> is the first and last ever framework you will need.</h2>
        </div>
        <div class="button-container">
            <?= $user ? '<a class="primary-button" href="/recipes">my recipes</a>' : '<a class="primary-button" href="/login">explore cheffy</a>' ?>
            <a class="primary-button" href="/documentation">read the docs</a>
            <a class="primary-button" href="/support">get support</a>
        </div>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
