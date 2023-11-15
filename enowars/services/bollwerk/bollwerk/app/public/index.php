<?php

use Core\Kernel;

session_start();

define("BASE_PATH", realpath(__DIR__ . DIRECTORY_SEPARATOR . '..') . DIRECTORY_SEPARATOR);

require_once(BASE_PATH . 'Core' . DIRECTORY_SEPARATOR . 'helper.php');

require_once(resolvePath('Core/autoload.php', ['Core']));
require_once(resolvePath('Core/bootstrap.php', ['Core']));

(Kernel::make())->handle();
