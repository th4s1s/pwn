<?php

namespace Middleware;

use Http\Request;

interface MiddlewareInterface
{
    public function hande(Request $request): void;
}