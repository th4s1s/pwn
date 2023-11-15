<?php

namespace Controller;

use Attributes\Route;
use Exception\NotFoundException;
use Http\Request;
use Http\Response;
use Http\View;

readonly class DocumentationController
{
    #[Route(path: '/documentation')]
    public static function index(Request $request): Response
    {
        return View::render('documentation/index');
    }

    #[Route(path: '/documentation/{step}')]
    public static function show(Request $request, int $step): Response
    {
        if ($step < 0 || $step > 10) {
            throw new NotFoundException();
        }

        $step = sprintf('%02d', $step);

        return View::render("documentation/$step");
    }
}
