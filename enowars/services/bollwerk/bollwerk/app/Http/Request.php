<?php

namespace Http;

use Http\Session;
use Exception\NotAuthenticatedException;
use Model\User;

readonly class Request
{
    public const GET = 'GET';
    public const POST = 'POST';

    public function __construct(
        public string $requestUri,
        public string $requestMethod,
        public Session $session,
        public array $queryParameters,
        public array $body,
        public array $cookie,
    ) {
    }

    public static function create(): Request
    {
        return new self(
            requestUri: $_SERVER['REQUEST_URI'],
            requestMethod: $_SERVER['REQUEST_METHOD'],
            session: Session::create(),
            queryParameters: $_GET,
            body: $_POST,
            cookie: $_COOKIE,
        );
    }

    public function getCurrentUserId(): int
    {
        $id = $this->session->getUser()?->id;

        if ($id === null) {
            throw new NotAuthenticatedException();
        }

        return $id;
    }
}
