<?php

namespace Middleware;

use Middleware\MiddlewareInterface;
use Exception\NotAuthenticatedException;
use Http\Request;

class Authenticated implements MiddlewareInterface
{
    public function hande(Request $request): void
    {
        if ($request->session->getUser() === null) {
            throw new NotAuthenticatedException();
        }
    }
}
