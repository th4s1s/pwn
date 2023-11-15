<?php require(resolvePath('View/partials/head.php')) ?>

<?php require(resolvePath('View/partials/navigation.php')) ?>

<div>
    <div class="page-container grid">
        <div class="card">
            <p class="title">Attention: Please note that we currently receive many requests</p>
            <div class="card-content">
                <p>
                    You can see the status of all submitted complaints here:
                </p>
                <div class="button-container">
                    <a class="primary-button" href="/support-disclaimer">status</a>
                </div>
            </div>
        </div>
        <div class="card">
            <h1 class="page-title title">Need Support?</h1>
            <div class="card-content">
                <p>
                    Thank you for choosing bollwerk! We're sorry to hear that you're experiencing difficulties with our
                    framework. Our team is here to help you resolve any issues or answer any questions you may have.
                    <br/>
                    <br/>
                    To contact us for support, please provide us a short description of your issue. We'll get back to
                    you as soon as possible with a solution or a request for additional information.
                    <br/>
                    <br/>
                    Thank you again for using Bollwerk, and we look forward to helping you resolve your issue!
                </p>
                <form action="/support" method="post">
                    <div class="text-field__container">
                        <label for="description">Description</label>
                        <textarea class="text-field" id="description" name="description" placeholder="Description"
                                  rows="10"></textarea>
                        <?php
                        if (isset($errors) && array_key_exists('description', $errors)) {
                            echo "<div class=\"text-field__error\">{$errors['description']}</div>";
                        }
                        ?>
                        <button class="primary-button" type="submit">submit</button>
                    </div>
                </form>
            </div>
        </div>
        <ul class="list">
            <?php
            foreach ($complaints as $index => $complaint) {
                $description = htmlspecialchars($complaint->description, ENT_QUOTES | ENT_SUBSTITUTE | ENT_HTML5);
                echo <<<DESCRIPTION
                <a href="/support/$complaint->token" class="list__card card">
                    <li class="list__container list__card card">
                        <p class="list__title">$index</p>
                        <p class="list__description card-content">$description</p>
                    </li>
                </a>
                DESCRIPTION;
            }
            ?>
        </ul>
    </div>
</div>

<?php require(resolvePath('View/partials/footer.php')) ?>
