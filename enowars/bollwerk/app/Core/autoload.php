<?php

spl_autoload_register(function ($class) {
    $class = str_replace('\\', DIRECTORY_SEPARATOR, $class);

    require BASE_PATH . $class . '.php';
});
