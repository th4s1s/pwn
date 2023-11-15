<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container grid">
        <div class="card">
            <h1 class="page-title title">Need Support?</h1>
            <div class="card-content">
                <p>
                    At Bollwerk, we strive to provide the best possible support to all of our users. However, due to a
                    high volume of support requests, our response times may be longer than usual.
                    <br/>
                    <br/>
                    Please know that we are working diligently to address every complaint in a timely manner, and we
                    appreciate your patience and understanding during this busy period.
                    <br/>
                    <br/>
                    Rest assured that we are committed to providing you with the support you need to get the most out of
                    our framework, and we will do our best to resolve your issue as quickly as possible.
                    <br/>
                    <br/>
                    Thank you for your understanding, and we apologize for any inconvenience this may cause.
                    You can see the current status and position of your complaint below.
                </p>
            </div>
        </div>
        <ul class="list">
            <?php
            foreach ($complaints as $index => $complaint) {
                $submittedAt = new DateTime("@$complaint->submittedAt");
                $submittedAt->setTimeZone(new DateTimeZone('Europe/Berlin'));
                $submittedAt = $submittedAt->format('Y-m-d H:i:s');
                $username = $complaint->getUser()->username;
                echo <<<DESCRIPTION
                <li class="list__container list__card card">
                    <p class="list__description title">$index: $username</p>
                    <div class="list__description card-content">
                        <p>Submitted: $submittedAt</p>
                        <p>Status: Not yet resolved</p>
                    </div>
                </li>
                DESCRIPTION;
            }
            ?>
        </ul>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
