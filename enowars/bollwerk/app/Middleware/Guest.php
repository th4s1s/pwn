<?php

namespace Middleware;

use Middleware\MiddlewareInterface;
use Http\Request;
use Http\Response;

class Guest implements MiddlewareInterface
{
    public function hande(Request $request): void
    {
        if ($request->session->getUser() !== null) {
            Response::redirect('/');
        }
    }
}
