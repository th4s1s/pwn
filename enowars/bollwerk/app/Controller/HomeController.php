<?php

namespace Controller;

use Attributes\Route;
use Http\Response;
use Http\View;

readonly class HomeController
{
    #[Route(path: '/', middlewares: [])]
    public static function get(): Response
    {
        return View::render('home/index');
    }
}
