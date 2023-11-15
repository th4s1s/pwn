<?php

use Core\App;
use Core\ServiceContainer;
use Database\Database;
use Http\Request;

$container = new ServiceContainer();

$container->bind(Database::class, fn() => new Database('/var/www/html/Database/db.sqlite'));
$container->bind(Request::class, fn() => Request::create());

App::setContainer($container);
