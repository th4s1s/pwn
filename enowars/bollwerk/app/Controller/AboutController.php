<?php

namespace Controller;

use Attributes\Route;
use Http\Response;
use Http\View;

readonly class AboutController
{
    #[Route(path: '/about', middlewares: [])]
    public static function get(): Response
    {
        return View::render('about/index');
    }
}
