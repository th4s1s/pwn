<?php

namespace Attributes;

use Attribute;
use Http\Request;

#[Attribute]
readonly class Route
{
    public function __construct(
        public string $path,
        public string $method = Request::GET,
        public array $middlewares = [],
    ) {
    }
}